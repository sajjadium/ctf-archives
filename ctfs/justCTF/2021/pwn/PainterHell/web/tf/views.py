import os
import hashlib
import random
import time
import re

from pathlib import Path
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from ipware.ip import get_ip

from utils import steam

TF2_TEMP_DIR = settings.TF2_TEMP_DIR


def get_tf2_file(file):
    return str(Path(TF2_TEMP_DIR) / Path(file))


class HatsView(View):
    def get(self, request, *args, **kwargs):
        ip = get_ip(request)
        port = request.GET.get('port')

        if not ip or not port:
            return HttpResponse(b'<header>Invalid date')

        if 'update' in request.GET:
            obj = steam.TF2(dir=TF2_TEMP_DIR)
            if obj.save_items():
                return HttpResponse(b'<header>1')
            else:
                return HttpResponse(b'<header>2')

        elif 'file' in request.GET:
            file = request.GET.get('file', '')
            allowed_files = ['efekt_info.txt', 'hats_info_pl.txt', 'paint_info.txt']

            filename = get_tf2_file(file)
            if file in allowed_files and os.path.isfile(filename):
                return HttpResponse(open(filename, 'rb').read(), content_type="text/plain; charset=utf-8")

        else:
            sid = request.GET.get('sid', '')
            if sid:
                obj = steam.TF2(dir=TF2_TEMP_DIR)
                str_items = obj.get_client(steam.convert_32to64(sid))
                return HttpResponse(b'<header>' + str_items.encode())

        return HttpResponse(b'<header>Invalid date')


class ColorsView(TemplateResponseMixin, View):
    template_name = 'tf/colors.html'

    def dispatch(self, request, *args, **kwargs):
        ip_server = get_ip(request)
        if not ip_server:
            return HttpResponse(b'<header>Invalid date')

        ip_client = request.GET.get('ip', None)
        port = request.GET.get('port', None)
        sid = request.GET.get('sid', None)

        obj = steam.TF2Colors()
        if sid is not None and port is not None and ip_client is not None:
            hash_priv = hashlib.sha1(str(random.random()).encode()).hexdigest()  # fake hash
            if sid and ip_client:
                file_data = '{0} ; {1} ; {2} ; {3} ; {4}'.format(ip_server, port, ip_client, sid, int(time.time()))

                with open(get_tf2_file('cookie/{}.txt'.format(sid)), 'wt') as fp:
                    fp.write(file_data)
            else:
                hash_priv = obj.generate_priv_hash(ip_server, port)  # not sid and client ip

            return HttpResponse(b'<header>' + hash_priv.encode())

        if sid:
            file_name = get_tf2_file('cookie/{}.txt'.format(sid))
            if not os.path.isfile(file_name):
                return HttpResponse(b'<header>Invalid date')

            file_data = open(file_name, 'rt').read().split(' ; ')

            if file_data[2] != ip_server or file_data[3] != sid or (int(time.time()) - int(file_data[4])) > 600:
                return HttpResponse(b'<header>Invalid date')

            if 'rgb1' in request.POST and 'rgb2' in request.POST:
                color_name = request.POST.get('nazwa', 'nazwa-' + str(random.randint(1, 100000)))
                rgb1 = request.POST.get('rgb1', '')
                rgb2 = request.POST.get('rgb2', '')

                color_name = re.sub("[^ęóąśłżźćńĘÓĄŚŁŻŹĆŃA-Z0-9a-z -]+", "", color_name)
                color_name = color_name[0:15]

                rgb1 = int(rgb1[1:], 16)
                rgb2 = int(rgb2[1:], 16)

                data_socket = 'kolory:{0};{1};{2};{3}'.format(sid, color_name, rgb1, rgb2)
                data_response = obj.send_socket(file_data[0], file_data[1], data_socket)
                if not data_response:
                    data_response = "Błąd serwera!"

                return self.render_to_response({'msg': data_response})

            return self.render_to_response({})

        return HttpResponse(b'<header>Invalid date')
