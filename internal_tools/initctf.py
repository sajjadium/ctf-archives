#!/usr/bin/env python3

import os
import sys
import re
import subprocess
import time
import tempfile
import shutil
import requests
from bs4 import BeautifulSoup
import datetime
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--url", type=str)
  parser.add_argument('--browser', action='store_true')
  args = parser.parse_args()

  if args.url:
    if args.browser:
      page_content = subprocess.check_output(f'node {os.path.dirname(sys.argv[0])}/readctf.js {args.url}', shell=True)
    else:
      event_id = re.search(r'ctftime\.org/event/(\d+)', args.url).group(1)
      # request the ctf event page
      page_content = requests.get(args.url,
                       allow_redirects=True,
                       headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
                        }).content
  else:
    page_content = '\n'.join([l for l in sys.stdin.readlines()])

  soup = BeautifulSoup(page_content, 'html.parser')
  for link in soup.find_all('a'):
    if not link.get('href'):
      continue

    m = re.fullmatch(r'/ctf/(\d+)', link.get('href'))
    if m:
      ctf_id = m.group(1)

      break

  title = soup.find_all('title')[0].text.replace('CTFtime.org / ', '').replace('अस्त्र', 'Astra')
  ctf_name = ''
  for t in title.split():
    if t.lower() in ['ctf', 'ctfs', 'online', 'quals', 'qualifying', 'teaser', 'qualifiers', 'qualifier', 'preliminary', 'prequal', 'qualification']:
      break
    if re.fullmatch(r'q\d', t.lower()):
      break
    ctf_name += t[0].upper() + t[1:]

  for meta in soup.find_all('meta'):
    if meta.get('property') != 'og:url':
      continue

    event_id = re.search(r'ctftime\.org/event/(\d+)', meta.get('content')).group(1)

    break

  ctf_name = re.sub(r'[^0-9a-zA-Z_@+\.+]+', '', ctf_name.replace('Preliminary', '').replace('Qualifiers', '').replace('Qualifier', '').strip().replace('å', 'a').replace('$', 'S').replace('/', ''))
  ctf_name = ctf_name.strip('.')
  assert ctf_name != ''

  ctf_year = datetime.date.today().year
  full_path = f'{ctf_name}/{ctf_year}'
  full_title = str(ctf_year)
  title = soup.find_all('title')[0].text.lower()
  if 'teaser' in title or 'qualifier' in title or 'quals' in title or 'preliminary' in title or 'prequal' in title or 'qualification' in title or 'qualifying' in title:
    full_path += '/Quals'
    full_title += ' Quals'
  elif 'finals' in title:
    full_path += '/Finals'
    full_title += ' Finals'

  if os.path.isdir(f'ctfs/{full_path}'):
    print(full_path)
    sys.exit(0)

  soup = BeautifulSoup(open('README.md').read(), 'html.parser')
  found = False
  tr_elements = soup.tbody.find_all('tr')
  for tr in tr_elements:
    td = tr.find_all('td')[0]
    if td.has_attr('rowspan'):
      curr_ctf_name = td.a['href'].split('/')[1]
      if ctf_name < curr_ctf_name:
        found = True
        new_tr = BeautifulSoup(f'''
          <tr>
              <td rowspan=1><a href="ctfs/{ctf_name}">{ctf_name}</a></td>
              <td><a href="ctfs/{full_path}">{full_title}</a></td>
              <td><a href="https://ctftime.org/event/{event_id}/tasks/" target="_blank">CTFtime</a></td>
          </tr>
        ''', "html.parser")
        tr.insert_before(new_tr.tr)
        break
      elif ctf_name == curr_ctf_name:
        found = True
        new_tr = BeautifulSoup(f'''
          <tr>
              <td rowspan={int(td['rowspan']) + 1}><a href="ctfs/{ctf_name}">{ctf_name}</a></td>
              <td><a href="ctfs/{full_path}">{full_title}</a></td>
              <td><a href="https://ctftime.org/event/{event_id}/tasks/" target="_blank">CTFtime</a></td>
          </tr>
        ''', "html.parser")
        tr.insert_before(new_tr.tr)
        td.decompose()
        break

  if not found:
    new_tr = BeautifulSoup(f'''
      <tr>
          <td rowspan=1><a href="ctfs/{ctf_name}">{ctf_name}</a></td>
          <td><a href="ctfs/{full_path}">{full_title}</a></td>
          <td><a href="https://ctftime.org/event/{event_id}/tasks/" target="_blank">CTFtime</a></td>
      </tr>
    ''', "html.parser")
    tr_elements[-1].insert_after(new_tr.tr)

  open('README.md', 'w').write(soup.prettify())

  for category in ['crypto', 'web', 'pwn', 'rev', 'misc', 'forensic', 'osint', 'net', 'steg', 'mobile', 'blockchain', 'hw', 'ppc', 'ai', 'jail', 'recon']:
    os.system(f'mkdir -p ctfs/{full_path}/{category}')

  open(f'ctfs/{ctf_name}/README.md', 'w').write(f'[CTFtime Page](https://ctftime.org/ctf/{ctf_id})\n')
  open(f'ctfs/{full_path}/README.md', 'w').write(f'[CTFtime Page](https://ctftime.org/event/{event_id})\n')

  print(full_path)
