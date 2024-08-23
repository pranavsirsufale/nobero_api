from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import pandas as pd
import requests 
from bs4 import BeautifulSoup
# act as a browser requesting a web page 
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebkit/537.36 (KHTML,like Gecko) Chrome/80.0.3987.162 safari/537.36'}
url = 'https://nobero.com/products/lunar-echo-oversized-t-shirt-1?variant=45663963218086'





def home(request):
    return HttpResponse('this is home ')

def members(request):
    return HttpResponse("Hello world!")

def get_api(request):
    class NoberoSpider:
        def __init__(self,headers,url):
            self.headers = headers
            self.url = url
        
        def get_data(self):
            try:
                # send an HTTP GET request to the web browser
                response = requests.get(self.url,headers=self.headers)
            
                # parse the HTML code using BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
            
            
                pro_dict = {}
            
                for i in soup.find_all('h1',class_='capitalize'):
                    # print(i.text.strip())
                    pro_dict['category'] = i.text.strip()
                    pro_dict['url'] = url
                    pro_dict['title'] = i.text.strip()
            
                size_list = []
                for i in soup.find_all('label',class_='size-select'):
                    size_list.append(i.text.strip())
                size_list = set(size_list)
                size_list = list(size_list)
            
                pro_dict['price'] = soup.find(id= 'variant-price').text.strip()[1:]
            
                pro_dict['product_urls'] = ['....']
                pro_dict['MRP'] = soup.find(id="variant-compare-at-price").text.strip()[1:]
                # pro_dict['last_7_day_sale'] = 
                last_sale = []
                for i in soup.find_all('span',class_='text-[#D51E20]'):
                    last_sale.append(i.text.strip().split(' '))
                pro_dict['last_7_day_sale'] = last_sale[0][0]
                pro_dict['available_skus']=[{'color':soup.find(id='selected-color-title').text.strip()[2:],'size':size_list} ,{'color':soup.find(id='selected-color-title').text.strip()[2:],'size':[]}]
            
                pro_desc = []
                pro_des = []
                for i in soup.find_all('h4',class_='capitalize'):
                    pro_desc.append(i.text.strip())
                for i in soup.find_all('p',class_='text-[#000000]'):
                    pro_des.append(i.text.strip())
                for i in range(len(pro_desc)):
                    pro_dict[pro_desc[i]] = pro_des[i]
                pro_dict['description'] = soup.find(id='description_content').text.strip()
            
                return pro_dict
            except Exception as err:
                return f'{err.message}'
    scrapped_obj = NoberoSpider(headers,url)
    scraped_data = scrapped_obj.get_data()
    return JsonResponse(scraped_data)


def page_not_found(request):
    return HttpResponse('page not found 404')