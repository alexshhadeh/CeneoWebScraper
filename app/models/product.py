#import sys
#import os
#sys.path.append(os.path.abspath('...'))
from app.utils import extractComponent
import requests
from bs4 import BeautifulSoup
import json
from app.models.opinion import Opinion

class Product:
    def __init__(self, productId, productName=None, opinions=[]) -> None:
        self.productId=productId
        self.productName=productName
        self.opinions=opinions
    def extractProduct(self):
        response=requests.get(f'https://www.ceneo.pl/{self.productId}#tab=reviews')
        page=2

        while response:
            pageDOM=BeautifulSoup(response.text, 'html.parser')
            opinions=pageDOM.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extractOpinion(opinion).transformOpinion())
            response=requests.get(f'https://www.ceneo.pl/{self.productId}/opinie-{str(page)}', allow_redirects=False)
            if response.status_code==200:
                page+=1
            else:
                break
    def exportProduct(self):
        with open(f"app/products/{self.productId}.json", "w", encoding="UTF-8") as f:
            json.dump(self.toDict(), f, indent=4, ensure_ascii=False)
    def toDict(self):
        return {
            "productId": self.productId,
            "productName": self.productName,
            "opinions": [opinion.toDict() for opinion in self.opinions]
        }
    def __str__(self) -> str:
        return f"productId: {self.productId}<br>productName: {self.productName}<br>opinions:<br><br>" + "<br><br>".join(str(opinion) for opinion in self.opinions)
    def __repr__(self) -> str:
        return f"Product(productId={self.productId}, productName={self.productName}, opinions=[" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])"
