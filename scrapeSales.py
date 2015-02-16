import urllib.request
import time
from datetime import datetime
from bs4 import BeautifulSoup
 
#strips stupid \x00-\x7f chars from stupid str so it doesn't look like an alien wrote it
def stripped(x):
    return "".join([i for i in x if 31 < ord(i) < 127])

#soups up the steam specials page
steampage = BeautifulSoup(urllib.request.urlopen('http://store.steampowered.com/search/?specials=1').read())

todaySales = open('steamSales.csv', 'a')
todaySales.write('{0}\n'.format(time.strftime("%d/%m/%Y")))

#iterates through steam specials page to find listings
for row in steampage.find_all('a', {'class': 'search_result_row ds_collapse_flag'}):
    #converts the steamID to a string to strip the b' ' from result set
    steamAppID =str(row['data-ds-appid'].strip('b').encode('utf-8')).strip("'[]b")
    #same as above, after retrieving Game Title, and calls stripped to remove stupid chars
    steamGameName = stripped(row.find('span', {'class':'title'}).get_text())
    steamGameName = str(steamGameName.encode('utf-8')).strip("'[]b")
    steamDiscountPercent = str(row.find('div', {'class':'col search_discount'}).get_text().encode('utf-8')).strip("'\\n[]b[]'")
    steamPrices = str(row.find('div', {'class':'col search_price discounted'}).get_text().encode('utf-8')).strip("\\n[]b[]'[]\\t")
    steamOriginalPrice = steamPrices.split('$')[1]
    steamDiscountedPrice = steamPrices.split('$')[2]

    print(steamGameName)
    print(steamAppID)
    print(steamDiscountPercent)
    print(steamOriginalPrice)
    print(steamDiscountedPrice)
    
    todaySales.write('{0},{1},"{2}","{3}","{4}"\n'.format(steamGameName, steamAppID, steamDiscountPercent, steamOriginalPrice, steamDiscountedPrice))
todaySales.close()
