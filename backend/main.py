from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from services import (
    get_kpis,
    get_segments,
    get_forecast,
    get_recommendations,
    get_clv,
    get_segment_summary,
    get_segment_analytics,
    get_forecast_summary,
    get_products
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Retail BI Platform API"}

@app.get("/kpis")
def kpis():
    return get_kpis()

@app.get("/segments")
def segments():
    return get_segments()

@app.get("/forecast")
def forecast():
    return get_forecast()

@app.get("/recommendations/{product}")
def recommendations(product: str):
    return get_recommendations(product)

@app.get("/clv/{customer_id}")
def clv(customer_id: int):

    result = get_clv(customer_id)

    return result

@app.get("/segment-summary")
def segment_summary():
    return get_segment_summary()

@app.get("/segment-analytics")
def segment_analytics():
    return get_segment_analytics()

@app.get("/forecast-summary")
def forecast_summary():
    return get_forecast_summary()

@app.get("/products")
def products():
    return get_products()