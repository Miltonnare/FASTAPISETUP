from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  
from typing import Optional
import pathlib

app=FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_file = pathlib.Path("templates/index.html")
    return html_file.read_text()

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