#!/usr/bin/env python3
import os
import re
import sys
import requests
import argparse
requests.packages.urllib3.disable_warnings()
import random
apikey = os.getenv('BULKVSAPIKEY')
parser = argparse.ArgumentParser(description='Get Caller ID Name')
parser.add_argument('phone_number', type=str, help='10 or 11 digit number for us or intl number with CC')
args = parser.parse_args()

agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'
]

def random_agent():
    return random.choice(agents)

def name_lookup(tn):
    user_agent = random_agent()
    headers = {'User-Agent': user_agent}
    baseuri = 'https://cnam.bulkcnam.com'
    payload = {'did': tn, 'id': apikey}
    name = requests.get(baseuri, params=payload, headers=headers, verify=False)
    print(name.text)

def lrn_lookup(tn):
    user_agent = random_agent()
    headers = {'User-Agent': user_agent}
    baseuri = 'https://lrn.bulkcnam.com'
    payload = {'did': tn, 'id': apikey, 'ani': tn, 'format': 'text'}
    name = requests.get(baseuri, params=payload, headers=headers, verify=False)
    print(name.text)

def add_one_if_needed(number):
    num_check = re.compile('^([0-9]{10}|1[0-9]{10}|[0-9]{11}|[0-9]{12}|[0-9]{13}|[0-9]{14}|[0-9]{15}|[0-9]{16})$')
    if num_check.match(number):
        no_one_test = re.compile('^[0-9]{10}$')
        if no_one_test.match(number):
            one_plus_number = '1' + number
        else:
            one_plus_number = number
    else:
        print("%s is not a format I understand" % number)
        sys.exit(1)
    return one_plus_number

if __name__ == '__main__':
    name_lookup(add_one_if_needed(args.phone_number))
    lrn_lookup(add_one_if_needed(args.phone_number))
