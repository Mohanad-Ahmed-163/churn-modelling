from .CustomerData import CustomerData
import pandas as pd
def predict_new(data:CustomerData,preprocessor,model):
    df=pd.DataFrame([data.model_dump()])
    # Preprocess the input data
    x_processed = preprocessor.transform(df)     
    # Make predictions
    y_pred = model.predict(x_processed)
    y_prob =model.predict_proba(x_processed)
    
    return{
        "churn prediction":bool(y_pred[0]),
        " churn probability":float(y_prob[0][1])

    }

