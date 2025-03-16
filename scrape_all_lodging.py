from requests_html import HTMLSession
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import os
import pandas as pd

def get_details(lodging_list, lodging_url, name, author, date_since):
   print(lodging_url)
   res = session.get(lodging_url, 
                     # headers
                     )
   soup = BeautifulSoup(res.content, 'html.parser')
   lodging_data = {}
   lodging_data['lodging_url'] = lodging_url
   lodging_data['name']        = name
   lodging_data['author']      = author
   lodging_data['date_since']  = date_since

   try :
      address_section = soup.find('div','property-address-wrap')
   except :
      pass
   else :
      try    : lodging_data['gmap_url'] = address_section.select_one('div.block-title-wrap a')['href']
      except : pass
      try    : lodging_data['address']  = address_section.select_one('li.detail-address>span').text
      except : pass
      try    : lodging_data['city']     = address_section.select_one('li.detail-city>span').text
      except : pass
      try    : lodging_data['state']    = address_section.select_one('li.detail-state>span').text
      except : pass
      try    : lodging_data['zip']      = address_section.select_one('li.detail-zip>span').text
      except : pass
      try    : lodging_data['area']     = address_section.select_one('li.detail-area>span').text
      except : pass
      try    : lodging_data['country']  = address_section.select_one('li.detail-country>span').text
      except : pass
         
   try    : lodging_data['last_update'] = soup.find('h2', string='Details').find_next_sibling('span').get_text(strip=True)
   except : pass
   
   try :
      other_detail = soup.select_one('div.detail-wrap')
   except :
      pass
   else :
      try    : lodging_data['property_id']     = other_detail.find('strong', string='Property ID:').find_next_sibling('span').text
      except : pass
      try    : lodging_data['price']           = other_detail.find('strong', string='Price:').find_next_sibling('span').text   
      except : pass
      try    : lodging_data['bedroom']         = other_detail.find('strong', string='Bedrooms:').find_next_sibling('span').text   
      except : pass
      try    : lodging_data['rooms']           = other_detail.find('strong', string='Rooms:').find_next_sibling('span').text   
      except : pass
      try    : lodging_data['bathrooms']       = other_detail.find('strong', string='Bathrooms:').find_next_sibling('span').text   
      except : pass
      try    : lodging_data['garage']          = other_detail.find('strong', string='Garage:').find_next_sibling('span').text   
      except : pass
      try    : lodging_data['property_type']   = other_detail.find('strong', string='Property Type:').find_next_sibling('span').text   
      except : pass
      try    : lodging_data['property_status'] = other_detail.find('strong', string='Property Status:').find_next_sibling('span').text   
      except : pass
      try    : lodging_data['guest_number']    = other_detail.find('strong', string='Guest Number:').find_next_sibling('span').text   
      except : pass
   
   try    : lodging_data['airbnb_url'] = soup.select_one('a:-soup-contains("Book")')['href']
   except : pass
   
   try    : lodging_data['description'] = soup.select_one('.property-description-wrap .block-content-wrap').get_text(' ', True)
   except : pass
      
   lodging_list.append(lodging_data)
   print(len(lodging_list), lodging_data['name'])

session = HTMLSession()
lodging_list = []

page_num = 1
while True:
   # headers = {'User-Agent':UserAgent().random}
   url = f'https://www.bukitvista.com/search-results/page/{page_num}'
   print(url)
   res = session.get(url, 
                     # headers
                     )
   soup = BeautifulSoup(res.content, 'html.parser')
   lodgings = soup.select('.item-listing-wrap')
   for lodging in lodgings:
      lodging_url = lodging.select_one('h2.item-title>a')['href']
      name        = lodging.select_one('h2.item-title>a').get_text(strip=True)
      author      = lodging.select_one('div.item-author').get_text(strip=True)
      date_since  = lodging.select_one('div.item-date').get_text(strip=True)
      get_details(lodging_list, lodging_url, name, author, date_since)
   count = soup.select_one('.listing-tools-wrap strong').text
   count = int(count.split()[0])
   if 1+count//9 == page_num:
      break
   page_num += 1

# simpan data sebagai dataframe
df = pd.DataFrame(lodging_list)

# buat folder 'data' jika belum ada
os.makedirs("data", exist_ok=True)

# simpan dataframe ke dalam folder 'data'
df.to_csv("data/penginapan_bukitvista.csv", index=False)