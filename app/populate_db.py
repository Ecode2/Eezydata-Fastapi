from app.db.models.ebills import Prices
from app.db.session import session_scope
from app.schemas.bills import PricesPublic


electricity = [
    {
    "bill_type": "electric",
    "brand": "eko-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },{
    "bill_type": "electric",
    "brand": "abuja-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },{
    "bill_type": "electric",
    "brand": "ibadan-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },{
    "bill_type": "electric",
    "brand": "ikeja-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },{
    "bill_type": "electric",
    "brand": "jos-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },{
    "bill_type": "electric",
    "brand": "kaduna-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },{
    "bill_type": "electric",
    "brand": "kano-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },{
    "bill_type": "electric",
    "brand": "portharcout-electric",
    "name": "Price per KiloWatt",
    "code": "prepaid",
    "price": "500"
    },
]

airetime = [
    {
    "bill_type": "airtime",
    "brand": "mtn",
    "name": "Price for 100 naira",
    "code": "mtn",
    "price": "100"
    },{
    "bill_type": "airtime",
    "brand": "glo",
    "name": "Price for 100 naira",
    "code": "glo",
    "price": "100"
    },{
    "bill_type": "airtime",
    "brand": "airtel",
    "name": "Price for 100 naira",
    "code": "airtel",
    "price": "100"
    },{
    "bill_type": "airtime",
    "brand": "etisalat",
    "name": "Price for 100 naira",
    "code": "etisalat",
    "price": "100"
    },
]

data = [
    {
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 500MB – 30 Days",
    "code": "500",
    "price": "130"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 1GB – 30 Days",
    "code": "M1024",
    "price": "260"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 2GB – 30 Days",
    "code": "M2024",
    "price": "520"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 3GB – 30 Days",
    "code": "3000",
    "price": "780"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 3GB – 30 Days",
    "code": "5000",
    "price": "780"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 10GB – 30 Days",
    "code": "10000",
    "price": "780"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 6GB – 7 Days",
    "code": "mtn-20hrs-1500",
    "price": "780"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 30GB – 30 Days",
    "code": "mtn-30gb-8000",
    "price": "780"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 40GB – 30 Days",
    "code": "mtn-40gb-10000",
    "price": "780"
    },{
    "bill_type": "data",
    "brand": "mtn",
    "name": "MTN Data 75GB – 30 Days",
    "code": "mtn-75gb-15000",
    "price": "780"
    },
]

user = [

]

add_to_db = [ electricity, airetime, data]

# Create the database connector
def AddPrices():

    for item in add_to_db:

        for subItem in item:

            data = PricesPublic(**subItem)

            with session_scope() as session:
                price_exists = session.query(Prices).filter_by(bill_type = data.bill_type, brand= data.brand, code= data.code).scalar()
                if price_exists:
                    continue
                newPrice = Prices.add_price(bill_type=data.bill_type, 
                                        brand=data.brand,
                                        name=data.name, 
                                        code=data.code,
                                        price=data.price)
                session.add(newPrice)
                session.commit()

if __name__=="__main__":
    AddPrices()
