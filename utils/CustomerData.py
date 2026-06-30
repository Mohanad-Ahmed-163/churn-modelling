from pydantic import BaseModel,Field
from typing import Literal
class CustomerData(BaseModel):

  CreditScore: int=Field(..., description="The credit score of the customer")
  Geography: Literal["France", "Spain", "Germany"]=Field(..., description="The country of the customer")
  Gender: Literal["Male","Female"]=Field(..., description="The gender of the customer")
  Age: int=Field(..., description="The age of the customer", ge=18, le=100)
  Tenure: int=Field(..., description="The number of years the customer has been with the bank", ge=0, le=10)
  Balance: float=Field(..., description="The balance of the customer's account", ge=0)
  NumOfProducts: int=Field(..., description="The number of products the customer has with the bank", ge=1, le=4)
  HasCrCard: Literal[0,1]=Field(..., description="Whether the customer has a credit card (1) or not (0)")
  IsActiveMember: Literal[0,1]=Field(..., description="Whether the customer is an active member (1) or not (0)")
  EstimatedSalary: float=Field(..., description="The estimated salary of the customer", ge=0)
