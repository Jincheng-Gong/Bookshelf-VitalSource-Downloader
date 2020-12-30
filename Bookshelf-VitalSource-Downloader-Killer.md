# Bookshelf-VitalSource-Downloader-Killer

## 背景

2019 年 11 月考完 FRM Part I，凭借着应试教育的功底，刷了一大堆的题目，最后拿到了 2 1 1 1 Pass 的残缺成绩。2020 年伊始 GARP 协会邀请四位大佬为 FRM 编写新教材，从原来几千页的大部头到现在几百页的精华教材书，无不让人感到心痒。在狂热学习分子 Henry Liang 的极力鼓动下，我打算在毕业之前精读完 FRM 的原版教材，同时也将此次精读原版教材作为自救计划的第一步。

## 问题

FRM 官方教材 Ebook 的版权保护极为严苛，GARP 协会指定其只能在 Bookshelf 公司开发的 VitalSource 应用里阅读，格式为加密 .vbk 格式。虽然有助于打击盗版，但这也严重影响消费者的阅读体验，于是在 Limited Printing and Application Only 的情况之下，我需要想出一个无痛的办法将其虚拟打印成 PDF 文档。

## 分析

官方打印程序比较奇葩，在网页上选择打印时，发送打印命令后每次至多允许打印两页。打印的请求时通过一个 POST 命令发送到服务器，再 GET 回打印的 API 和 KEY 到本地，最后发回服务器进行打印处理，因此打算做 Python 自动化处理。

## 程序

运行脚本之前需要输入以下三个参数：

- IBAN

- VitalSourceAPIKey

- VitalSourceAccessToken

第一个参数获取很简单，在 Bookshelf 官网打开购买的 Ebook 即可获得。

第二个参数和第三个参数的获取略微麻烦，我的解决方案如下：使用 Bookshelf 官方应用调用打印命令，趁本地与服务器对话的时候拦截数据包进行解析。此时需要一个抓包工具，这里推荐使用 Fiddler4 进行抓包。找到 Bookshelf 发送的数据包，将 Header 里面的相应参数输入即可运行脚本。

脚本设计如下：

```python
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
		'https://print.vitalsource.com/print/'+IBAN+'？license_type=download&brand=vitalsource&from='+str(i)+'&to='+str(i+1)+'&appName=VitalSource%20Bookshelf&appVersion=9.0.0&mc=0123456789AB&mn=YourMom',
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
```

## 注意事项

在使用脚本和服务器进行对话的时候，由于 Bookshelf 官方的保护机制，可能会出现 Empty 的提示，最好自己再添加一个日志的功能，方便监控并记录下出现问题的页面。 最后将打印出来的图片合成 PDF 就大功告成了。 

## 后记

第一次用 Markdown 在知乎上写文章，简单排版了一下，使用起来不是很熟练，请海涵。脚本纯属自娱自乐，需要的人应该也不多，有问题或改进需求欢迎留言。