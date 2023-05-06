import urllib.parse
import urllib.request
import json
import hashlib
import socket
import datetime
import os


def send_request(url, data=None, post=False, is_json=False):
    form_data = urllib.parse.urlencode(data) if data else ''
    if post:
        response = urllib.request.urlopen(url, form_data.encode()).read().decode()
    else:
        response = urllib.request.urlopen(url + '?' + form_data).read().decode()

    return response if not is_json else json.loads(response)


def convert_32to64(steamid):
    # [U:1:61367470]
    # STEAM_0:0:30683735
    if steamid[1] == 'U':  # steam3
        return 76561197960265728 + int(steamid[5:-1])
    elif steamid[0] == 'S':  # steam 2
        return 76561197960265728 + int(steamid[8]) + (int(steamid[10:])*2)
    return 0


class TF2:
    def __init__(self, dir=None):
        self.key = 'E340348F2FAC64C68C8BE48CE1253A62'  # Get from: https://steamcommunity.com/dev/apikey
        self.language = 'pl'
        if dir is not None:
            os.chdir(dir)

    def save_items(self):
        # This is broken :(
        # Valve deprecate this endpoint.
        # Ref: https://www.reddit.com/r/tf2/comments/8glw2m/website_operators_and_update_enthusiasts_that/

        response = send_request('http://api.steampowered.com/IEconItems_440/GetSchema/v0001/', {
            'key': self.key,
            'language': self.language,
            'format': 'json'
        }, is_json=True)

        if response['result']['status'] != 1:
            return False

        with open('hats.txt', 'wt', encoding='utf-8') as fp, \
                open('hats_info_pl.txt', 'wt', encoding='utf-8') as fp2, \
                open('paint_info.txt', 'wt', encoding='utf-8') as fp3:

            fp_items = list()
            fp2_items = list()
            fp3_items = list()

            for item in response['result']['items']:
                if ('item_slot' in item and item['item_slot'] == 'head') or \
                        ('craft_material_type' in item and item['craft_material_type'] == 'hat') or \
                        ('item_type_name' in item and item['item_type_name'] == 'Nakrycie głowy'):

                    hat_type = (1 << 1)
                    if 'capabilities' in item and 'paintable' in item['capabilities'] and \
                            item['capabilities']['paintable']:
                        hat_type |= (1 << 0)

                    fp_items.append(str(item['defindex']))
                    fp2_items.append('{0} ; {1} ; {2}'.format(item['defindex'], item['item_name'], hat_type))

                elif 'tool' in item and 'type' in item['tool'] and item['tool']['type'] == 'paint_can':
                    has_attrib = dict()
                    for attrib in item['attributes']:
                        if attrib['class'] == 'set_item_tint_rgb' or attrib['class'] == 'set_item_tint_rgb_2':
                            has_attrib[attrib['class']] = attrib['value']

                    if len(has_attrib) == 1:
                        fp3_items.append('{0} ; {1} ; {1}'.format(item['item_name'], has_attrib['set_item_tint_rgb']))
                    elif len(has_attrib) == 2:
                        fp3_items.append('{0} ; {1} ; {2}'.format(item['item_name'], has_attrib['set_item_tint_rgb'],
                                                                  has_attrib['set_item_tint_rgb_2']))

            fp.write(','.join(fp_items))
            fp2.write('\n'.join(fp2_items))
            fp3.write('\n'.join(fp3_items))

        effect_name = {
            "Attrib_KillStreakEffect2002": "Ogniste Rogi",
            "Attrib_KillStreakEffect2003": "Mózgowe Wyładowanie",
            "Attrib_KillStreakEffect2004": "Tornado",
            "Attrib_KillStreakEffect2005": "Płomienie",
            "Attrib_KillStreakEffect2006": "Osobliwość",
            "Attrib_KillStreakEffect2007": "Spopielacz",
            "Attrib_KillStreakEffect2008": "Hipno-Promień",

            "Attrib_KillStreakIdleEffect1": "Blask Drużyny",
            "Attrib_KillStreakIdleEffect2": "Nieludzki Narcyz",
            "Attrib_KillStreakIdleEffect3": "Manndarynka",
            "Attrib_KillStreakIdleEffect4": "Złośliwa Zieleń",
            "Attrib_KillStreakIdleEffect5": "Bolesny Szmaragd",
            "Attrib_KillStreakIdleEffect6": "Perfidna Purpura",
            "Attrib_KillStreakIdleEffect7": "Hot Rod",
        }

        with open('efekt_info.txt', 'wt', encoding='utf-8') as fp:
            fp_items = list()

            for effect in response['result']['attribute_controlled_attached_particles']:
                if 'id' not in effect:
                    continue

                if effect['name'] == 'Attrib_Particle55':
                    effect['name'] = 'Orbitujące Karty'

                # unusual hats
                if 2001 > effect['id'] >= 4:
                    fp_items.append('{0} ; {1}'.format(effect['id'], effect['name']))

                # unusual killstreak
                elif 3001 > effect['id'] >= 2002:
                    try:
                        name = effect_name['Attrib_KillStreakEffect' + str(effect['id'])]
                        fp_items.append('{0} ; {1}'.format(effect['id'], name))
                    except:
                        pass

                # unusual taunt
                elif 4001 > effect['id'] >= 3001:
                    fp_items.append('{0} ; {1}'.format(effect['id'], effect['name']))

                # unusual sheen
                elif 23001 > effect['id'] >= 22002:
                    try:
                        name = effect_name['Attrib_KillStreakIdleEffect' + str(effect['id'] - 22001)]
                        fp_items.append('{0} ; {1}'.format(effect['id'], name))
                    except:
                        pass

            fp.write('\n'.join(fp_items))

        return True

    def get_client(self, steamid):
        response = send_request('http://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001/', {
            'key': self.key,
            'steamid': steamid,
            'format': 'json'
        }, is_json=True)

        if response['result']['status'] != 1:
            return self.api_status(response['result']['status']) + ','

        all_hats = [int(x) for x in open('hats.txt', 'rt', encoding='utf-8').read().split(',')]
        all_hats_name = {int(x.split(' ; ')[0]): x.split(' ; ')[1] for x in open('hats_info_pl.txt', 'rt', encoding='utf-8').read().split('\n')}

        ret_items = dict()
        for item in response['result']['items']:
            item['defindex'] = int(item['defindex'])
            if item['defindex'] in all_hats:
                ret_items[all_hats_name[item['defindex']]] = str(item['defindex'])

        return self.api_status(response['result']['status']) + ',' + ' '.join(ret_items.values())

    @staticmethod
    def api_status(status):
        if status == 1:
            return '1'
        elif status == 8:
            return '2'
        elif status == 15:
            return '3'
        elif status == 18:
            return '4'
        else:
            return '5'


class TF2Colors:
    @staticmethod
    def generate_hash(ip, port):
        hash_pub = b'c17e7d02ef1bbd2f87d269143bfeef7983e33124'
        hash_priv = TF2Colors.generate_priv_hash(ip, port).encode()
        hash_new = list(hashlib.sha1(hash_pub + hash_priv).hexdigest())

        hash_new[12], hash_new[5] = hash_new[5], hash_new[12]
        hash_new = ''.join(hash_new)
        return hash_new

    @staticmethod
    def generate_priv_hash(ip, port):
        ret_hash = 'hj13abx{0}:{1}{2}6hasb14as'.format(ip, (int(port) - 25555), datetime.date.today().strftime('%Y-%m-%d'))
        return hashlib.sha1(ret_hash.encode()).hexdigest()

    @staticmethod
    def send_socket(ip, port, dane):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as s:
                s.connect((ip, int(port)))
                s.settimeout(2)

                s.send(b'open:' + TF2Colors.generate_hash(ip, port).encode())
                s.send(dane.encode())
                return s.recv(256)
        except:
            return None
