from django.apps import AppConfig
from .eth import Account, Contract, web3
import os


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    nft_addr = open(os.path.join(os.getcwd(), 'contract_addr.txt'), 'rb').read().strip().decode('utf-8')

