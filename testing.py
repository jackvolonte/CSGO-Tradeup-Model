import time

import pandas as pd
import numpy as np
import itertools
import pandas as pd
from itertools import combinations
from collections import defaultdict
import pprint
from itertools import combinations_with_replacement
from statistics import mean
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score


# variables
itemTypes = np.array(["bs-items.csv", "ww-items.csv", "ft-items.csv", "mw-items.csv", "fn-items.csv",
                         "st-bs-items.csv", "st-ww-items.csv", "st-ft-items.csv", "st-mw-items.csv", "st-fn-items.csv"])
suffixList = np.array([" (Battle-Scarred)", " (Well-Worn)" , " (Field-Tested)", " (Minimal Wear)", " (Factory New)", " (Battle-Scarred)",
                       " (Well-Worn", " (Field-Tested)", " (Minimal Wear)", " (Factory New)"])
wearList = np.array([0,1,2,3,4,0,1,2,3,4])


def getData():
    data = pd.read_csv("all-rarity-items.csv")
    return data


def profitable_combinations(c):
    # Load data from CSV file
    path = "F:\pycharmProjects\steamTesting\itemPricesByType/" + itemTypes[c]
    df = pd.read_csv(path)


    # get all of each rarity
    for i in range(3):
        # get lowest priced item of each rarity
        max_collection = df['Collection'].max()
        for b in range(max_collection+1):
            max_collection_df = df[df["Collection"] == b]

            rarity_entries = max_collection_df[max_collection_df['Rarity'] == i]
            rarityHigher = max_collection_df[max_collection_df['Rarity'] == i + 1]
            # print(rarity_entries)
            # print(rarityHigher)

            df_lower_sorted = rarity_entries.sort_values('Lowest Price')
            lowest_price_item = df_lower_sorted.iloc[0]
            df_higher_sorted = rarityHigher.sort_values('Lowest Price')
            # print(lowest_price_item)
            # print(df_higher_sorted)

            n = 10
            highest_mean = df_higher_sorted.head(n)['Lowest Price'].mean()
            # print(highest_mean)

            if highest_mean < 100000:
                if highest_mean > (lowest_price_item['Lowest Price'] * 10 * 1.05):
                    print("Expected EV :" + str(highest_mean - (lowest_price_item['Lowest Price'] * 10 * 1.05)))
                    print("Expected Outcome: " + str(highest_mean))
                    print("Lowest Priced Item: " + str(
                        df_lower_sorted.sort_values('Lowest Price').iloc[0]['Item']) + " Price: " + str(
                        lowest_price_item['Lowest Price']) + " Total Cost: " + str(
                        lowest_price_item['Lowest Price'] * 10))
                    print("Collection ='s " + str(df_lower_sorted.sort_values('Lowest Price').iloc[0]['Collection']))
                    print("File ='s " + itemTypes[c])
                    print("")







def main():
    for i in range(len(itemTypes)):
        profitable_combinations(i)


