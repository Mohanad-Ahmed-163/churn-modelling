from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from utils.inference import predict_new
from utils.CustomerData import CustomerData
from utils.config import (
    APP_NAME,
    VERSION,
    SECRET_KEY,
    preprocessor,
    forest_tuned,
    xgboost_tuned
)

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Endpoint
@app.get("/", tags=["General"])
async def home():
    return {
        "Welcome": f"Welcome to {APP_NAME} API v{VERSION}"
    }

api_key_header= APIKeyHeader(name='X_API_Key')
async def verify_api_key(api_key:str=Depends(api_key_header)):
    if api_key != SECRET_KEY:
        raise HTTPException(status_code=403,detail="you are not authorized to use this API")
    return api_key
# Random Forest Prediction
@app.post("/predict/forest", tags=["Models"])
async def predict_forest(data: CustomerData,api_key:str=Depends(verify_api_key)) ->dict:
    try:
        result = predict_new(
            data=data,
            preprocessor=preprocessor,
            model=forest_tuned
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    #  XGBOOST Prediction
@app.post("/predict/xgboost",tags=["Models"])
async def predict_xgb(data:CustomerData,api_key:str=Depends(verify_api_key))->dict:
     try:
        result = predict_new(
            data=data,
            preprocessor=preprocessor,
            model=xgboost_tuned
        )
        return result
     
     except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )