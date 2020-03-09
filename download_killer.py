import os
import time
import json
import random
import requests

IBAN = '000000000000000000000000'
VitalSourceAPIKey = '000000000000000000000000'
VitalSourceAccessToken = '000000000000000000000000000000'
DownloadFolder = os.path.expanduser('~/Downloads/'+IBAN+'/')

if os.path.exists(DownloadFolder):
	pass
else:
	try:
		os.mkdir(DownloadFolder)
	except:
		print('Creation of the directory failed')
		exit()

while(True):
	try:
		FirstPage = int(input('First page: '))
		LastPage = int(input('Last page: '))
		if (type(FirstPage) != int) or (type(LastPage) != int):
			print('Please enter valid page numbers.\n')
			continue
		elif (FirstPage > LastPage):
			print('First page must be less than last page.\n')
			continue                    
		else:
			break          
	except:
		print('Please enter valid page numbers.\n')

for i in range(int(FirstPage), int(LastPage)+1, 2):
	r = requests.get(
		'https://print.vitalsource.com/print/'+IBAN+'?license_type=download&brand=vitalsource&from='+str(i)+'&to='+str(i+1)+'&appName=VitalSource%20Bookshelf&appVersion=9.0.0&mc=0123456789AB&mn=YourMom',
		headers={
			'X-VitalSource-API-Key': VitalSourceAPIKey,
			'X-VitalSource-Access-Token': VitalSourceAccessToken,
			'Accept': 'application/json',
			'User-Agent': 'Bookshelf-Mac/9.0.0 (MacOS/10.14.6; MacBookPro14,2) vitalsource',
			'Accept-Language': 'en-us'
		}
	)
	js = r.json()

	try:
		print(str(i)+'\t'+js[u'images'][0])
		r = requests.get(
				js[u'images'][0],
				headers={
					'Accept': '*/*',
					'Accept-Language': 'en-us',
					'User-Agent': 'VitalSource%20Bookshelf/1204 CFNetwork/978.1 Darwin/18.7.0 (x86_64)'
				}
			)
		open(DownloadFolder+str(i)+'.png', 'wb').write(r.content)
	except:
		print(str(i)+'\tempty page')

	try:
		print(str(i+1)+'\t'+js[u'images'][1])
		r = requests.get(
				js[u'images'][1],
				headers={
					'X-VitalSource-API-Key': VitalSourceAPIKey,
					'X-VitalSource-Access-Token': VitalSourceAccessToken,
					'Accept': 'application/json',
					'User-Agent': 'Bookshelf-Mac/9.0.0 (MacOS/10.14.6; MacBookPro14,2) vitalsource',
					'Accept-Language': 'en-us'
				}
			)
		open(DownloadFolder+str(i+1)+'.png', 'wb').write(r.content)
	except:
		print(str(i+1)+'\tempty page')

	time.sleep(random.randint(1, 10))