from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import pandas as pd
from io import BytesIO
import json 
from models import Orders, Products, Suppliers, Bales, RawImports
import re
from collections import defaultdict
from datetime import date
from schemas import (
    TotalOrdersResponse, CompletedOrdersResponse, CancelledOrdersResponse,
    GrossSalesResponse, NetSalesResponse, TotalRevenueResponse, AverageOrderValueResponse,
    ConversionRateResponse, MonthlyGrowthRateResponse,
    WeeklySalesTrendsResponse, TopMerchantsResponse, TopProductsResponse, RevenueComparisonResponse
)

def parse_price(value) -> float:
    if value is None:
        return 0.0
    cleaned = re.sub(r'[^\d.\-]', '', str(value))
    try:
        return float(cleaned) if cleaned else 0.0
    except ValueError:
        return 0.0

def find_matching_table(df_columns: set[str]):
    best_name, best_model, best_score = None, None, 0.0
    for name, model in KNOWN_TABLES.items():
        table_columns = {c.name for c in model.__table__.columns}
        score = len(df_columns & table_columns) / len(df_columns)
        if score > best_score:
            best_name, best_model, best_score = name, model, score
    return (best_name, best_model) if best_score >= 0.8 else (None, None)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

KNOWN_TABLES = {
    "orders": Orders,
    "products": Products,
    "suppliers": Suppliers,
    "bales": Bales,
}

app = FastAPI()

@app.get("/health/db")
def check_db(db: Session = Depends(get_db)):
    return {"status": "connected"}


@app.post("/uploadfile/" )
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xlsx', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx and .csv files are allowed.")

    contents = await file.read()
    df = pd.read_csv(BytesIO(contents)) if file.filename.endswith('.csv') else pd.read_excel(BytesIO(contents))
    df.columns = df.columns.str.strip()
    df = df.where(pd.notnull(df), None)

    table_name, model = find_matching_table(set(df.columns))

    if model:
        matching_cols = [c.name for c in model.__table__.columns if c.name in df.columns]
        records = df[matching_cols].to_dict(orient="records")

        inserted, failed = 0, []
        for i, record in enumerate(records):
            try:
                db.add(model(**record))
                db.commit()
                inserted += 1
            except Exception as e:
                db.rollback()
                failed.append({"row": i, "error": str(e)})

        return {
            "status": "inserted",
            "table": table_name,
            "inserted": inserted,
            "failed_count": len(failed),
            "failed": failed[:20],  # cap it so one garbage file doesn't return a wall of text
        }

    records = [{"source_filename": file.filename, "row_data": json.dumps(row)} for row in df.to_dict(orient="records")]
    db.bulk_insert_mappings(RawImports, records)
    db.commit()
    return {"status": "staged", "table": "raw_imports", "rows": len(records)}


# 1.	total revenue

@app.get("/orders/total_revenue", response_model=TotalRevenueResponse)
def get_total_revenue(db: Session = Depends(get_db)):
    orders = db.query(Orders.price).filter(Orders.status == 'completed').all()
    total = sum(parse_price(o.price) for o in orders)
    return {"total_revenue": round(total, 2)}


# 2.	gross sales

@app.get("/orders/gross_sales", response_model=GrossSalesResponse)
def get_gross_sales(db: Session = Depends(get_db)):
    orders = db.query(Orders.price).all()
    total = sum(parse_price(o.price) for o in orders)
    return {"gross_sales": round(total, 2)}


# 3.	net sales

@app.get("/orders/net_sales", response_model=NetSalesResponse)
def get_net_sales(db: Session = Depends(get_db)):
    orders = db.query(Orders.price).filter(Orders.status != 'cancelled').all()
    total = sum(parse_price(o.price) for o in orders)
    return {"net_sales": round(total, 2)}


# 4.	total orders

@app.get("/orders/total_orders", response_model=TotalOrdersResponse)
def get_total_orders(db: Session = Depends(get_db)):
    return {"total_orders": db.query(Orders).count()}


# 5.	completed orders

@app.get("/orders/completed_orders", response_model=CompletedOrdersResponse)
def get_completed_orders(db: Session = Depends(get_db)):
    return {"completed_orders": db.query(Orders).filter(Orders.status == 'completed').count()}


# 6.	cancelled orders

@app.get("/orders/cancelled_orders", response_model=CancelledOrdersResponse)
def get_cancelled_orders(db: Session = Depends(get_db)):
    return {"cancelled_orders": db.query(Orders).filter(Orders.status == 'cancelled').count()}


# 7.	average order value

@app.get("/orders/average_order_value", response_model=AverageOrderValueResponse)
def get_average_order_value(db: Session = Depends(get_db)):
    orders = db.query(Orders.price).filter(Orders.status != 'cancelled').all()
    if not orders:
        return {"average_order_value": 0}
    total = sum(parse_price(o.price) for o in orders)
    return {"average_order_value": round(total / len(orders), 2)}

 
# 10.	top-performing merchants

@app.get("/orders/top_merchants", response_model=TopMerchantsResponse)
def get_top_merchants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Orders.merchant_id, Orders.price).filter(
        Orders.status == 'completed', Orders.merchant_id.isnot(None)
    ).all()

    totals = defaultdict(lambda: {"order_count": 0, "revenue": 0.0})
    for o in orders:
        totals[o.merchant_id]["order_count"] += 1
        totals[o.merchant_id]["revenue"] += parse_price(o.price)

    ranked = sorted(totals.items(), key=lambda x: x[1]["revenue"], reverse=True)
    page = ranked[skip:skip + limit]
    ids = [mid for mid, _ in page]
    names = {s.id: s.name for s in db.query(Suppliers.id, Suppliers.name).filter(Suppliers.id.in_(ids)).all()}

    return {
        "items": [
            {"merchant_id": mid, "name": names.get(mid), "order_count": st["order_count"], "revenue": round(st["revenue"], 2)}
            for mid, st in page
        ],
        "total": len(ranked), "skip": skip, "limit": limit,
    }


# 11.	top-selling products

@app.get("/orders/top_products", response_model=TopProductsResponse)
def get_top_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Orders.item_id, Orders.quantity, Orders.price).filter(
        Orders.status == 'completed', Orders.item_id.isnot(None)
    ).all()

    totals = defaultdict(lambda: {"units_sold": 0, "revenue": 0.0})
    for o in orders:
        totals[o.item_id]["units_sold"] += (o.quantity or 1)
        totals[o.item_id]["revenue"] += parse_price(o.price)

    ranked = sorted(totals.items(), key=lambda x: x[1]["revenue"], reverse=True)
    page = ranked[skip:skip + limit]
    ids = [pid for pid, _ in page]
    names = {p.id: p.name for p in db.query(Products.id, Products.name).filter(Products.id.in_(ids)).all()}

    return {
        "items": [
            {"item_id": pid, "name": names.get(pid), "units_sold": st["units_sold"], "revenue": round(st["revenue"], 2)}
            for pid, st in page
        ],
        "total": len(ranked), "skip": skip, "limit": limit,
    }


# 12.	monthly growth rate

@app.get("/orders/monthly_growth_rate", response_model=MonthlyGrowthRateResponse)
def get_monthly_growth_rate(db: Session = Depends(get_db)):
    orders = db.query(Orders.created_at, Orders.price).filter(Orders.status == 'completed').all()

    monthly = defaultdict(float)
    for o in orders:
        monthly[o.created_at.strftime('%Y-%m')] += parse_price(o.price)

    months = sorted(monthly.keys())
    if len(months) < 2:
        return {"monthly_growth_rate_percent": None, "message": "Not enough months of data yet"}

    current, previous = monthly[months[-1]], monthly[months[-2]]
    rate = ((current - previous) / previous * 100) if previous else None

    return {
        "current_month": months[-1], "previous_month": months[-2],
        "current_revenue": round(current, 2), "previous_revenue": round(previous, 2),
        "monthly_growth_rate_percent": round(rate, 2) if rate is not None else None
    }


# 13.	weekly sales trends

@app.get("/orders/top_products", response_model=TopProductsResponse)
def get_top_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Orders.item_id, Orders.quantity, Orders.price).filter(
        Orders.status == 'completed', Orders.item_id.isnot(None)
    ).all()

    totals = defaultdict(lambda: {"units_sold": 0, "revenue": 0.0})
    for o in orders:
        totals[o.item_id]["units_sold"] += (o.quantity or 1)
        totals[o.item_id]["revenue"] += parse_price(o.price)

    ranked = sorted(totals.items(), key=lambda x: x[1]["revenue"], reverse=True)
    page = ranked[skip:skip + limit]
    ids = [pid for pid, _ in page]
    names = {p.id: p.name for p in db.query(Products.id, Products.name).filter(Products.id.in_(ids)).all()}

    return {
        "items": [
            {"item_id": pid, "name": names.get(pid), "units_sold": st["units_sold"], "revenue": round(st["revenue"], 2)}
            for pid, st in page
        ],
        "total": len(ranked), "skip": skip, "limit": limit,
    }


# 14.	order conversion rates

@app.get("/orders/conversion_rate", response_model=ConversionRateResponse)
def get_conversion_rate(db: Session = Depends(get_db)):
    total = db.query(Orders).count()
    completed = db.query(Orders).filter(Orders.status == 'completed').count()
    if total == 0:
        return {"total_orders": 0, "completed_orders": 0, "conversion_rate_percent": 0}
    return {"total_orders": total, "completed_orders": completed,
            "conversion_rate_percent": round(completed / total * 100, 2)}


# 15.	revenue comparisons across different periods.

@app.get("/orders/revenue_comparison", response_model=RevenueComparisonResponse)
def get_revenue_comparison(
    period1_start: date = Query(...), period1_end: date = Query(...),
    period2_start: date = Query(...), period2_end: date = Query(...),
    db: Session = Depends(get_db)
):
    def revenue_between(start, end):
        rows = db.query(Orders.price).filter(
            Orders.status == 'completed', Orders.created_at >= start, Orders.created_at < end
        ).all()
        return sum(parse_price(o.price) for o in rows)

    r1, r2 = revenue_between(period1_start, period1_end), revenue_between(period2_start, period2_end)
    diff = r2 - r1
    return {
        "period1": {"start": str(period1_start), "end": str(period1_end), "revenue": round(r1, 2)},
        "period2": {"start": str(period2_start), "end": str(period2_end), "revenue": round(r2, 2)},
        "difference": round(diff, 2),
        "percent_change": round(diff / r1 * 100, 2) if r1 else None
    }