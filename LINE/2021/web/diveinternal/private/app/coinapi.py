import json,os,sys, random
import requests, urllib.parse,subprocess,time
from requests.auth import HTTPBasicAuth
from requests_toolbelt.utils import dump
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('KillCoinapi')


headers = {'content-encoding': 'gzip','content-type':'application/json'}


"""
Coin Dataset.
coinData = [
    {"symbol" : "BTCUSDT", "price" : btcusdt},
    {"symbol" : "XRPUSDT", "price" : xrpusdt},
    {"symbol" : "ADAUSDT", "price" : adausdt},
    {"symbol" : "LINKUSDT", "price" : linkusdt}
]
"""

def getCoinInfo():
    try:
        url  = ''  #-----> Find your favorite api provider.

        resp = requests.get(url,headers=headers)
        
        if resp.status_code >= 200:
            if resp.status_code < 300:
                try:
                    json_data = json.loads(resp.text)
                    return(json_data)
                except:
                    logger.debug('Request of KillCoinapi')
            else:
                logger.error(resp.text)
    except Exception as e:
        logger.error('coinapi Error : {c}, Message, {m}, Error on line {l}'.format(c = type(e).__name__, m = str(e), l = sys.exc_info()[-1].tb_lineno))
        pass

getCoinInfo()