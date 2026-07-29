from pydantic import BaseModel
from typing import Optional


class TotalOrdersResponse(BaseModel):
    total_orders: int

class CompletedOrdersResponse(BaseModel):
    completed_orders: int

class CancelledOrdersResponse(BaseModel):
    cancelled_orders: int

class GrossSalesResponse(BaseModel):
    gross_sales: float

class NetSalesResponse(BaseModel):
    net_sales: float

class TotalRevenueResponse(BaseModel):
    total_revenue: float

class AverageOrderValueResponse(BaseModel):
    average_order_value: float

class ConversionRateResponse(BaseModel):
    total_orders: int
    completed_orders: int
    conversion_rate_percent: float

class MonthlyGrowthRateResponse(BaseModel):
    current_month: Optional[str] = None
    previous_month: Optional[str] = None
    current_revenue: Optional[float] = None
    previous_revenue: Optional[float] = None
    monthly_growth_rate_percent: Optional[float] = None
    message: Optional[str] = None

class WeeklyTrend(BaseModel):
    week: str
    revenue: float

class WeeklySalesTrendsResponse(BaseModel):
    items: list[WeeklyTrend]
    total: int
    skip: int
    limit: int

class MerchantRanking(BaseModel):
    merchant_id: int
    name: Optional[str]
    order_count: int
    revenue: float

class TopMerchantsResponse(BaseModel):
    items: list[MerchantRanking]
    total: int
    skip: int
    limit: int

class ProductRanking(BaseModel):
    item_id: int
    name: Optional[str]
    units_sold: int
    revenue: float

class TopProductsResponse(BaseModel):
    items: list[ProductRanking]
    total: int
    skip: int
    limit: int

class PeriodRevenue(BaseModel):
    start: str
    end: str
    revenue: float

class RevenueComparisonResponse(BaseModel):
    period1: PeriodRevenue
    period2: PeriodRevenue
    difference: float
    percent_change: Optional[float]

