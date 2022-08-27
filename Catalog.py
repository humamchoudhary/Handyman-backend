from math import prod
from typing import List
from unicodedata import name
from tinydb.operations import delete,subtract
from tinydb import TinyDB, Query
import uuid

from pprint import pprint as print


class Product:
    def __init__(self,name,amount,price,image_loc,tags) -> None:
        self.name = name
        self.amount = amount
        self.price = price
        uuid_str = uuid.uuid1().urn
        self.id = uuid_str[9:]
        self.tags = tags
        self.image = image_loc
        
        # with open(image_loc, "rb") as img_file:
        #     self.image = base64.b64encode(img_file.read())

"""
Create a class of a card widget and set the key as the uuid,add all the returned cards in a list
"""
    
class Catalog:
    User = Query()
    DB = TinyDB('catalog.json')
    DB.default_table_name = "Products"
    def Add(self,product):
        prod = {}
        prod['id'] = product.id
        prod["name"] = product.name 
        prod["price"] = product.price 
        prod["amount"] = product.amount 
        prod["tag"] = product.tags
        prod["image"] = product.image
        self.DB.insert(prod)

    def Remove(self,id):
        item = self.DB.get(self.User.id==id)
        print(item.doc_id)
        self.DB.remove(doc_ids=[item.doc_id])

    def Search(self,tags:list):
        return self.DB.search(self.User.tag.any(tags))

    def Show(self):
        return self.DB.all()

    def Buy(self,id,amount):
        
        self.DB.update(subtract('amount',amount),self.User.id==id)
    
        

# prod1 = Product("test2",100,200,"/images/test.jpg",["l"])
# Catalog().Add(prod1) 
# print(Catalog().Search(["l"]))
# Catalog().Remove("5b9e94d8-24f7-11ed-96d3-088fc321660a") 
# Catalog().Show()
# Catalog().Buy("328d0829-24fb-11ed-896f-088fc321660a",1)
# Catalog().Show()

