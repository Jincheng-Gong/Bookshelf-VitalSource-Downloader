# Bookshelf-VitalSource-Downloader

在 limited printing 和 application only 的情况下，想了一个半无痛的方法来打印 ebook。

脚本的原理比较简单，从官方打印的方法出发，每次打印至多打印两页，打印的请求是通过一个POST命令由application发送到服务器，再由本地GET回打印所需要的API和KEY代码，所以脚本在运行之前需要输入以下三个参数。

IBAN = '000000000000000000000000'

VitalSourceAPIKey = '000000000000000000000000'

VitalSourceAccessToken = '000000000000000000000000000000'

第一个参数很简单获取，在bookshelf的官网打开你买的那本ebook就可以看到。

但是第二个和第三个值是要通过application调用打印命令时和服务器对话才能解析出来的，所以你需要一个抓包工具。测试了几款，推荐 fiddler。找到对应的header在里面找到相关的值就行了。

直接运行脚本，中间可能会出现empty的提示，最好再添加一个日志的功能，方便监控出现问题的页面。

把get下来的图片合成pdf就大功告成了。
