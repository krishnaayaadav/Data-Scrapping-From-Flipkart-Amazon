import requests, time
from bs4 import BeautifulSoup
from csv_writter import CSVHandlers

class AmazonScrapper:

    def __init__(self, url:str):
        self.url = url
    
    def get_soup_data(self,url=None):
        """This method will return beautiful soup object of requested page.
           Which is parsed as lxml ok.
        """

        if url is None:
            url = self.url 

        # user client headers
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        
        # making request and getting response as html page
        try:
            web_page = requests.get(url = url, headers = headers)
        except:
            print('Error: While making request to targeted url')
        else:
            # data parsing using beautifulsoup
            soup     = BeautifulSoup(web_page.content, 'lxml') 
            return soup
    
    def soup_data_extractor(self,soup=None):
        # this is function which will handle exceptions
        def try_except(trys=None, excepts=None):

            try:
                data = trys
            except:
                excepts
                pass
            else:
                return data

        if soup is None:
            soup = self.get_soup_data()

            myclass ="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"
            # Normal products
            products = soup.find_all('div', attrs={'class': myclass})
            
            # blank list to store products
            extracted_products = []

            # keys are
            prodcut_keys = ['title', 'price', 'rating', 'image']

            for i in range(len(products)):
                p1 = products[i]

                name_div = p1.find('span', attrs = {'class':"a-size-medium a-color-base a-text-normal"}).text.strip()           
                price_div = p1.find('span', attrs ={'class': 'a-price'}).find('span', attrs={'class':'a-offscreen'}).text.strip()[1:]
                image_div  = p1.find('div', class_="a-section aok-relative s-image-fixed-height").find('img', class_ = 's-image')['src']
                ratings_div = p1.find('span', class_ ="a-declarative").find('span', class_="a-icon-alt").text
                
                name    =  try_except(trys=name_div)
                price   =  try_except(trys=price_div)
                image   =  try_except(trys=image_div)
                ratings =  try_except(trys=ratings_div)

                prod = {
                    'title':  name,
                    'price':  price,
                    'rating': ratings,
                    'image':  image
                }
                extracted_products.append(prod)
            
            return prodcut_keys,extracted_products


# driver function
def no__of_pages_scrpp(page_no:int):

    # target url
    URL = 'https://www.amazon.in/s?k=mobiles&crid=1MNPUKWLVTIEQ&sprefix=mobile%2Caps%2C300&ref=nb_sb_noss_'

    # csv file to store the data
    filename = 'amazon_products.csv'

    for i in range(1,page_no+1):
        URL += f'{i}'

        amz = AmazonScrapper(url=URL) # obj creation 
        
        # getting product key and data as dict
        keys, products = amz.soup_data_extractor()

        initial =False # initial here

        if i == 1:
            initial = True

        csvfile = CSVHandlers(filename=filename, mode='a') #objs creation
        
        # data writting into csv file
        csvfile.dict_csv_writer(keys=keys, dict_datas=products, is_initial=initial)
        time.sleep(10)


no__of_pages_scrpp(7)