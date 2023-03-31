import testing as t
import pandas as pd
import numpy as np
import requests
import time


AppID = "730"
YourSecretAPIKey = "VZ2LZoHa215X5l_0XYs8IeTdAkY"

statTrak = 'StatTrak%E2%84%A2%20'

# csv fils for each item type
itemTypes = np.array(["bs-items.csv", "ww-items.csv", "ft-items.csv", "mw-items.csv", "fn-items.csv",
                         "st-bs-items.csv", "st-ww-items.csv", "st-ft-items.csv", "st-mw-items.csv", "st-fn-items.csv"])
suffixList = np.array([" (Battle-Scarred)", " (Well-Worn)" , " (Field-Tested)", " (Minimal Wear)", " (Factory New)", " (Battle-Scarred)",
                       " (Well-Worn", " (Field-Tested)", " (Minimal Wear)", " (Factory New)"])


def findFloatsMatching():
    a = 1