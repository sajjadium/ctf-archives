from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.core.validators import URLValidator, validate_ipv4_address
from .models import User
from .apps import AccountConfig
from .eth import Account, Contract, web3
import ipaddress
import pyseto
import base64
import string
import requests
import json
import hashlib
import os



nft_path = os.path.join('account', 'storages')

def pyseto_decode(token, token_key):
    token_obj = pyseto.Key.new(
        version=4, purpose="local", key=token_key
    )
    return pyseto.decode(token_obj, token).payload.decode('utf-8')


def get_contract():
    with open('./PrivateNFT.json', 'rb') as f:
        build_json = json.load(f)

    contract = Contract(build_json)
    return contract.at(AccountConfig.nft_addr)

def get_response(uri):
    if uri.startswith('http://') or uri.startswith('https://'):
        validator = URLValidator()
        result = requests.get(uri, timeout=3)
        try:
            validator(uri)
            result = requests.get(uri, timeout=3)
        except:
            return

        return result.text

    elif any([uri.startswith(str(i)) for i in range(1, 10)]) and uri.find('/') != -1:
        ip = uri.split('/')[0]

        if uri.find('..') != -1 or not uri.startswith(os.path.join(ip, nft_path + '/')):
            return

        try:
            validate_ipv4_address(ip)
        except:
            return

        ipv4 = ipaddress.IPv4Address(ip)
        if str(ipv4) not in ['127.0.0.1', '0.0.0.0']:
            return

        nft_file = uri.split(nft_path + '/')[-1]
        if nft_file.find('.') != -1 and nft_file.split('.')[-1]:
            path = os.path.join(os.getcwd(), nft_path, nft_file)

            with open(path, 'rb') as f:
                return f.read()

        return


def index(request):
    if not request.session.get('user_id', ''):
        return HttpResponse("login first %s" % AccountConfig.name)

    user_id = request.session.get('user_id', '')
    token = request.session.get('token', '')
    token_key = request.session.get('token_key', '')
    private_key = pyseto_decode(token, token_key)

    account = Account(private_key=private_key)

    return HttpResponse("Hello, %s\nprivate key: %s\ncontract address: %s" % (user_id, private_key, account.address))


def login(request):
    user_id = request.GET.get('user_id', '')
    user_pw = request.GET.get('user_pw', '')
    if not user_id or not user_pw:
        return HttpResponse("empty parameter")

    try:
        user_obj = User.objects.get(user_id=user_id)
        if user_obj.user_pw != user_pw:
            return HttpResponse("user id or user pw is incorrect");

    except:
        return HttpResponse("user id or user pw is incorrect");

    request.session['user_id'] = user_obj.user_id
    request.session['token'] = user_obj.token
    request.session['token_key'] = user_obj.token_key

    return HttpResponseRedirect("/")


def regist(request):
    user_id = request.GET.get('user_id', '')
    user_pw = request.GET.get('user_pw', '')
    if not user_id or not user_pw:
        return HttpResponse("empty parameter")

    if any([user_id.count(data) for data in list(string.punctuation + ' ')]):
        return HttpResponse("invalid user id");

    if User.objects.filter(user_id=user_id).exists():
        return HttpResponse("exist user id");

    account = Account()
    assert account.private_key

    with open('/dev/urandom', 'rb') as f:
        token_key = base64.b64encode(f.read(128)).decode('utf-8')[:64]
        token_obj = pyseto.Key.new(
            version=4, purpose="local", key=token_key
        )

    token = pyseto.encode(token_obj, payload=account.private_key).decode('utf-8')

    u = User(user_id=user_id, user_pw=user_pw, token=token, token_key=token_key)
    u.save()

    return HttpResponse("registered successfully")

def nfts(request, user_id):
    if not User.objects.filter(user_id=user_id).exists():
        return HttpResponse("no exist");

    if request.session.get('user_id', '') != user_id:
        return HttpResponse("no authorzation");

    user = User.objects.get(user_id=user_id)
    token = request.session.get('token', '')
    token_key = request.session.get('token_key', '')
    private_key = pyseto_decode(token, token_key)

    account = Account(private_key=private_key)
    contract = get_contract()
    ids = contract.getIDs().call({'from':account.address})
    result = ""

    cache_path = os.path.join(os.getcwd(), nft_path, 
                  user_id + hashlib.sha1(bytes(private_key.encode('utf-8'))).hexdigest()
    )
    if not user.is_cached:
        for tid in ids:
            uri = contract.getTokenURI(tid).call({'from':account.address})
            if not uri:
                continue

            resp = get_response(uri)
            if not resp:
                continue

            try:
                json_res = json.loads(resp)
                for key in list(json_res.keys()):
                    if key in ['name', 'description']:
                        result += f'<br/>{key}: {json_res[key]}'
                    elif key == 'image':
                        result += f'<br/>{key}: <img src=\"{json_res[key]}\"/>'
                result += "<br/>"


            except:
                result += f"<br/>malformed {uri}: {resp}"


        if len(ids) == 3:
            with open(cache_path, 'wb') as f:
                f.write(result.encode('utf-8'))

            user.is_cached = True
            user.save()
    else:
        with open(cache_path, 'rb') as f:
            result = f.read().decode('utf-8')



    return HttpResponse("= NFT list =" + result)


def logout(request):
    session_keys = list(request.session.keys())[::]
    for key in session_keys:
        del request.session[key]

    return HttpResponseRedirect("/")
