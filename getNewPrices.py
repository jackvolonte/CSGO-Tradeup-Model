import hashlib
import urllib

import pandas as pd
import numpy as np
import time
import requests
import json
import re
import steammarket as sm


# csgo app id
from steammarket import get_csgo_item

AppID = "730"
YourSecretAPIKey = "VZ2LZoHa215X5l_0XYs8IeTdAkY"

statTrak = 'StatTrak%E2%84%A2%20'

# csv fils for each item type
itemTypes = np.array(["bs-items.csv", "ww-items.csv", "ft-items.csv", "mw-items.csv", "fn-items.csv",
                         "st-bs-items.csv", "st-ww-items.csv", "st-ft-items.csv", "st-mw-items.csv", "st-fn-items.csv"])
suffixList = np.array([" (Battle-Scarred)", " (Well-Worn)" , " (Field-Tested)", " (Minimal Wear)", " (Factory New)", " (Battle-Scarred)",
                       " (Well-Worn", " (Field-Tested)", " (Minimal Wear)", " (Factory New)"])
wearList = np.array([0,1,2,3,4,0,1,2,3,4])


def generate_market_hash_name(item_name):

    item_name = item_name.replace(' ', '%20')
    item_name = item_name.replace('|', '%7C')

    return item_name


def get_csgo_item2(item_id):
    market_hash_name = generate_market_hash_name(item_id)
    url = f"https://api.steamapis.com/market/item/{ AppID }/{ market_hash_name }?api_key={ YourSecretAPIKey }"
    # Send the API request and get the response
    response = requests.get(url)
    data = response.json() # load json
    print(response)
    print(data)
    time.sleep(0.125)

    if response.status_code == 200:
        # Parse the JSON response and retrieve the lowest price field
        data = response.json()
        if data is not None:
            lowest_price = data['histogram']['sell_order_array'][0]
            price = lowest_price['price']
            return(price)
            if lowest_price is not None:
                print(f"The lowest price of the item is {lowest_price}")
            else:
                print("Lowest price not available for this item.")
        else:
            print("Invalid response received from the Steam API.")
    else:
        print(f"API request failed with error code {response.status_code}.")

    return 1000000

# get price of item
def getPriceOfItem(item_name):
    data = get_csgo_item2(item_name)
    #time.sleep(1.00)
    return(data)


def getNewPricesToCsv(outputFile, suffixCount):
    path = "F:\pycharmProjects\steamTesting\itemPricesByType/" + outputFile
    data = pd.read_csv(path)
    names_list = data['Item']

    count = 0
    for i in names_list:
        newString = names_list[count]

        if newString != "Item":
            if suffixCount < 5:
                print(getPriceOfItem(newString))
                print(newString)
                data.loc[count, "Lowest Price"] = getPriceOfItem(newString)
                count = count + 1
            #else:
                #data.loc[count, "Lowest Price"] = getPriceOfItem(str("StatTrak™ " + newString))
                #count = count + 1
    print(data)
    print("")
    data.to_csv(path, index=False)

def updateAllPrices():
    suffixCount = 0
    for outputFile in itemTypes:
        getNewPricesToCsv(outputFile, suffixCount)
        suffixCount = suffixCount + 1

def updateAllCsvs():
    count = 0
    for i in itemTypes:
        updateEachCsvByTier(i, suffixList[count], count, count)
        count = count + 1

def updateEachCsvByTier(outputFile, suffixList, suffixCount, wearCount):
    data = pd.read_csv('allCsgoItems.csv')
    names_list = data['Item']

    count = 0
    for i in names_list:
        newString = names_list[count]
        if newString != "Item":
            if suffixCount >= 0: # change to < 5 for stattrack checks
                newString = newString + suffixList
                data.loc[count, "Item"] = newString
                data.loc[count, "Wear"] = wearList[suffixCount] # wear = suffixcount 0-4
                #data.loc[count, 'ST'] = 0
                count = count + 1
            #else:
                #newString = "StatTrak™ " + newString + suffixList
                #data.loc[count, "Name"] = newString
                #newString = newString + suffixList
                #data.loc[count, "Name"] = newString
                #data.loc[count, 'Wear'] = wearList[suffixCount]  # wear = suffixcount 0-4
                #data.loc[count, 'ST'] = 1
                #count = count + 1

    path = "F:\pycharmProjects\steamTesting\itemPricesByType/" + outputFile
    data.to_csv(path, index=False)



    path = "F:\pycharmProjects\steamTesting\itemPricesByType/" + outputFile
    data.to_csv(path, index=False)

def moveToMasterCsv():
    path2 = "all-rarity-items.csv"
    #data = pd.read_csv(path2)
    count = 0
    for outputFile in itemTypes:
        path = "F:\pycharmProjects\steamTesting\itemPricesByType/" + outputFile
        data2 = pd.read_csv(path)
        data2.to_csv(path2, mode='a', header=False, index=False)


def main():

    updateAllCsvs()
    print("Updated all csv names...")
    updateAllPrices()
    print("Updated all csv prices...")
    moveToMasterCsv()
    print("All items of all rarities moved to master csv...")
    print("Finished Updating Csvs")