import  requests, time
from bs4 import BeautifulSoup
from csvfileshanlers import CSVHandlers

class FlipkartScrapper:
    """This class perform taks like getting beautifulsoup data, then data extraction, dict data writing in csv file and others related to scrapping """

    def __init__(self,target_url):
        self.url = target_url

    def get_soup_data(self,url=None):
        """This method will make http request to targeted url and return soup object """
        
        # header means user agent for browser
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

        if url is None:
            url = self.url
        
        # web page content by making request to webpage
        wep_page = requests.get(url=url, headers=headers)
        
        # beautifulsoup object
        soup      = BeautifulSoup(wep_page.content, 'html5lib')
        return soup # returning sousp obj

    def soup_data_extractor(self, soup=None):
        """This method will provide features of data extractions of beautifulsoup object"""
        
        # getting soup data here
        if soup is None:
            soup = self.get_soup_data()


        # all product to store
        extracted_product  = [] 

        # product field name like product name, price,rating,review etc.
        product_fields_name = ['prod_name', 'total_price', 'dis_price', 'dis_perncetage', 'prod_rating', 'prod_reviews', 'image_src', 'prod_short_desc']


        ##### product extraction start #####

        # all product divs
        all_products = soup.find(class_ = "_1YokD2 _3Mn1Gg").find_all('div', attrs={'class': '_1AtVbE col-12-12'})[0:-2]

        prod_len = len(all_products)

        for inx in range(prod_len):
                # product name 
                try:
                    prod_name  = all_products[inx].find(class_ ="_4rR01T").text.strip()
                except:
                    prod_name = 'None'
                    pass

                # product total price without discount
                try:
                    totl_price  = all_products[inx].find(class_ ="_3I9_wc _27UcVY").text.strip()[1:]
                except:
                    totl_price = 'None'
                    pass

                 # product  price with discount
                try:
                    discount_price = all_products[inx].find(class_="_30jeq3 _1_WHN1").text.strip()[1:]
                except:
                    discount_price = 'None'
                    pass

                # product discount percentage
                try:
                    discount_percentage    = all_products[inx].find(class_ = "_3Ay6Sb").text.strip()
                except:
                    discount_percentage = 'None'
                    pass

                
                # product  ratings
                try:
                    prod_rating = all_products[inx].find(class_ = '_3LWZlK').text
                except:
                    prod_rating = 'None'
                    pass
                
                # product reviews 
                try:
                    prod_review = all_products[inx].find('span', attrs = {'class':"_2_R_DZ"}).find('span').find_all('span')[0].text
                except:
                    prod_review = 'None'
                    pass

                # product image src 
                try:
                    prod_image_src = all_products[inx].find('img', attrs={'class':"_396cs4"})['src']
                except:
                    prod_image_src = 'None'
                    pass

                # descrtiption div
                try:
                    all_desc    = all_products[inx].find('div', class_ = 'fMghEO').find('ul').find_all('li')
                except:
                    all_desc = 'None'
                    pass
                
                    # product short descrtiption
                try:
                    des_len = len(all_desc)  # just getting len
               
                    prod_short_desc = []     
                    for index in range(des_len):
                        prod_short_desc.append(
                            all_desc[index].text.strip()
                        )
                except:
                    prod_short_desc = 'None'
                    pass
                    

                
                product_details ={
                    'prod_name': prod_name,
                    'total_price': totl_price,
                    'dis_price': discount_price,
                    'dis_perncetage': discount_percentage,
                    'prod_rating':  prod_rating,
                    'prod_reviews': prod_review,
                    'image_src': prod_image_src,
                    'prod_short_desc': prod_short_desc
                }
                # print()

                # print(product_details)


                extracted_product.append(product_details) # appending each product in list

        return extracted_product,product_fields_name
    

# target url
URL = 'https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1'


# csv file name 
# filename = 'filpkart_products.csv'

# obj creation
# f1 = FlipkartScrapper(target_url=URL)

# obj creation
# csvs = CSVHandlers(filename=filename, mode = 'w')



# extracting all data here 
# products_dict, keys = f1.soup_data_extractor()

# saving into csv file
# csvs.dict_csv_writer(keys=keys, dict_datas=products_dict, is_initial=True)


def no_pages_extractor(total_pages:int):
        
    
    for i in range(1,total_pages+1):

        # csv file name 
        filename = 'filpkart_products.csv'
        URL = 'https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page='
        # obj creation
        f1 = FlipkartScrapper(target_url=URL)
        # obj creation
        csvs = CSVHandlers(filename=filename, mode = 'a')

        URL += f'{i}'                    # making url for new pages
        soup = f1.get_soup_data(url=URL) # getting soup data 
        products, keys = f1.soup_data_extractor(soup=soup) # extracting soup data
        
        initial= False

        if i == 1:
            initial = True
        
        # #saving into csv files
        csvs.dict_csv_writer(filename=filename, mode='a', dict_datas=products, keys=keys, is_initial=initial)
        time.sleep(7)


no_pages_extractor(10)

######## Just Checking here ##### 

# keys = ['name', 'price', 'delivery']
# products_dict = [
#     {
#       'name': 'Mobile234',
#       'price': 2334,
#       'delivery': 'free'
#     },
#     {
#       'name': 'Mobile234',
#       'price': 2334,
#       'delivery': 'free'
#     },
#     {
#       'name': 'Mobile234',
#       'price': 2334,
#       'delivery': 'free'
#     },

#     {
#       'name': 'Mobile234',
#       'price': 2334,
#       'delivery': 'free'
#     },

#     {
#       'name': 'Mobile234',
#       'price': 2334,
#       'delivery': 'free'
#     },

     
# ]
