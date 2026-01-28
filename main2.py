from fastapi import FastAPI
from pydantic import BaseModel  
from typing import Optional

app=FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price:float
    quantity:int=1
    tax: Optional[float] = 0.0
    
@app.post("/items/" )
async def create_item(item: Item):
   subtotal=item.price * item.quantity
   total_tax=item.tax*item.quantity
   total_price= subtotal + total_tax
   
   return{
       "name":item.name,
       "quantity":item.quantity,
       "unit Price":item.price,
       "tax per item":item.tax,
       "subtotal":subtotal,
       "total tax":total_tax,
       "total price":total_price
   }