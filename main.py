from fastapi import FastAPI ,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from config import session ,engine
import dbmodels
from sqlalchemy.orm import Session

app=FastAPI()
origins = [
    "http://localhost:3000",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
dbmodels.Base.metadata.create_all(bind=engine)



@app.get("/")
def greet():
    return "This is my first console"




Products=[
    Product(id=1,name="laptop",desc="Asus TUF gaming laptop",price=40000,quantity=1),
    Product(id=2,name="mobile",desc="nord 5",price=30000,quantity=1),
    Product(id=3,name="mobile",desc="nord 5",price=30000,quantity=1),
    Product(id=4,name="keyboard",desc="Redragon K552 Kumara Mechanical Gaming Keyboard",price=2279,quantity=1),
    Product(id=5,name="mouse",desc="Logitech G304 Lightspeed Wireless Gaming Mouse",price=2795,quantity=1),
    Product(id=6,name="earbuds",desc="OnePlus Nord Buds 3 Pro with 49dB ANC",price=2649,quantity=1),
    Product(id=7,name="smartwatch",desc="Redmi Watch 5 Lite with 1.96 inch AMOLED",price=3499,quantity=1),
    Product(id=8,name="controller",desc="Cosmic Byte ARES Wireless Controller with Magnetic Triggers",price=3500,quantity=1),
]

#fetching db here 
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


# initializig the Products on static array to the db 
def init_db():
    db=session()
    
    count=db.query(dbmodels.Product).count()
    if count==0:
        for product in Products:
            db.add(dbmodels.Product(**product.model_dump()))
    db.commit()

init_db()

# get all routes
@app.get("/products/")
def get_all(db:Session = Depends(get_db)):
    db_products = db.query(dbmodels.Product).all()
    return db_products


@app.get('/products/{id}')
def getProductByid(id:int,db:Session = Depends(get_db)):
    db_products = db.query(dbmodels.Product).filter(dbmodels.Product.id == id).first() 
    if db_products.id ==id:
           return db_products
    return "Product not found"

# @app.post('/products/')
# def add_product(product:Product,db:Session = Depends(get_db)):
#     db.add(dbmodels.Product(**product.model_dump()))
#     db.commit()
#     return product


@app.post("/products/")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = dbmodels.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put('/products/{id}')
def update_product(id:int ,product:Product,db:Session = Depends(get_db)):
    db_products = db.query(dbmodels.Product).filter(dbmodels.Product.id == id).first()
    if(db_products):
        db_products.name=product.name
        db_products.desc=product.desc
        db_products.price=product.price
        db_products.quantity=product.quantity
        db.commit()

        return "Product Updated Succesfully"

    return "Product not found"

@app.delete('/products/{id}')
def delete_product(id:int,db:Session =Depends(get_db)):
        db_products= db.query(dbmodels.Product).filter(dbmodels.Product.id==id).first()
        if db_products:
            db.delete(db_products)
            db.commit()
            return "Product deleted succesfully"
        return "Product Not found"