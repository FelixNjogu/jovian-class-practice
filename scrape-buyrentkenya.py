import requests
from bs4 import BeautifulSoup
import pandas as pd

url_list=[]
start_url= 'https://www.buyrentkenya.com/houses-for-sale/nairobi'
base_url= 'https://www.buyrentkenya.com/houses-for-sale/nairobi?page='

def populate_urls(i):
    url_list.append(start_url)
    valid_url= True
    while valid_url:
        next_url=base_url+str(i)
        response=requests.get(next_url)
        soup=BeautifulSoup(response.text,'html.parser')
        exit=soup.find('h1',class_='text-center text-xl max-w-lg')
        if exit is None:
            url_list.append(next_url)
            i+=1
        else:
            valid_url=False
            print('Done appending urls')


def get_details(url_list):
    listings_list = []
    for url in url_list:
        the_response = requests.get(url)
        the_soup = BeautifulSoup(the_response.text, 'html.parser')
        listings_tags = the_soup.find_all(
            'div', class_='flex flex-col items-stretch md:flex-row')
        listings_list.extend(listings_tags)
    return listings_list

def get_listing_title(listing):
    title=listing.find('a',class_='no-underline text-black').text.strip()
    return title

def get_listing_location(listing):
    location=listing.find('p',class_='text-md md:text-sm font-normal text-grey-darker mt-1 md:mt-0').text.strip()
    return location

def get_bedrooms(listing):
    bedroom_tags=listing.find_all('span',class_='text-sm mr-5')
    if len(bedroom_tags[0].text.strip())>2:
         bedrooms= bedroom_tags[1].text.strip()
    else:
        bedrooms= bedroom_tags[0].text.strip()
    return bedrooms
def get_bathrooms(listing):
    bathroom_tag=listing.find_all('span',class_='text-sm')
    a=len(bathroom_tag)
    bathrooms=bathroom_tag[a-1].text.strip()
    if len(bathrooms)>2:
        bathrooms=bathroom_tag[a-2].text.strip()
    return bathrooms


def get_price(listing):
    price = listing.find('a', class_='no-underline').text.strip()
    return price

def get_link(listing):
    extension=listing.find('a')['href']
    base_url='https://www.buyrentkenya.com'
    full_url=base_url+extension
    return full_url


def get_listing_details(listings):
    #start with an empty list
    results_list = []
    for listing in listings:
        title = get_listing_title(listing)
        location = get_listing_location(listing)
        bedrooms = get_bedrooms(listing)
        bathrooms = get_bathrooms(listing)
        price = get_price(listing)
        link = get_link(listing)
        results_list.append({
            'title': title,
            'location': location,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'link': link
        })
    return results_list

#Let us call populate urls from page two
populate_urls(2)
listings_list = get_details(url_list)
df = pd.DataFrame(get_listing_details(listings_list))
df.shape
df.to_csv('housing.csv', index=None)
