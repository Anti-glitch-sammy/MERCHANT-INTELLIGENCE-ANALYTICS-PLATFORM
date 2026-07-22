from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health/db")
def check_db(db: Session = Depends(get_db)):
    return {"status": "connected"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xlsx', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx and .csv files are allowed.")
    
    # Here you can add logic to save the file or process it as needed
    # For demonstration, we'll just return the filename
    return {"filename": file.filename}