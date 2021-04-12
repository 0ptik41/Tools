from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
from threading import Thread
import string
import utils
import time
import json
import sys 

btc_api = 'api.coindesk.com/v1/bpi/currentPrice/USD'
ltc_api = 'api.blockchain.com/v3/exchange/tickers/LTC-USD'
xmr_api = 'min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=USD'
big_api = api = 'pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

def get_btc_price():
	link = 'https://%s' % btc_api
	data = json.loads(requests.get(link).text)['bpi']
	return data['bpi']['USD']['rate_float']

def get_ltc_price():
	link = 'https://%s'%ltc_api
	return json.loads(requests.get(link).text)

def get_xmr_price():
	link = 'https://%s'%xmr_api
	return json.loads(requests.get(url=link).text)['USD']

def pull_market():
	url = 'https://%s' % big_api
	parameters = {'start':'1','limit':'5000','convert':'USD'}
	headers = {
	  'Accepts': 'application/json',
	  'X-CMC_PRO_API_KEY': 'GET_AN_API_TOKEN_FROM_COINMARKETCAP',
	}

	session = Session()
	session.headers.update(headers)

	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
	  	pass
	return data

def parse_full_market():
	data = pull_market()
	market = {'btc': data['data'][0],
			  'eth': data['data'][1],
			  'fil': data['data'][3],
			  'ltc': data['data'][7],
			  'dsh': data['data'][43],
			  'bat': data['data'][59],
			  'doge': data['data'][15],
			  'mana': data['data'][67]}
	return market

def parse_cmc_data(dat):
	price = dat['quote']['USD']['price']
	return price 

def collect_data():
	running = True
	crypto = {}
	collected = 0
	try:
		while running:
			ld, lt = utils.create_timestamp()
			mkt = parse_full_market()
			print('[*] Market Data Collected [%s - %s]' % (ld,lt))
			parsed = {}
			for asset in mkt.keys():
				value = parse_cmc_data(mkt[asset])
				print('- %s is $%f' % (asset, value))
				parsed[asset] = value
			crypto[ld+' '+lt] = parsed
			if collected%10==0:
				print('[*] Backing Up Data collected...')
				open('crypto_market.json','w').write(json.dumps(crypto))
			time.sleep(60)
			collected += 1
	except KeyboardInterrupt:
		running = False
		pass

def main():
	collect_data()

if __name__ == '__main__':
	main()
