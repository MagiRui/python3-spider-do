import re
import time

content1 = "今天 01:28 来自慧博投资分析"
timeAndSource = re.search("(.*?)来自(.*)", content1)
print(timeAndSource.group(1))
print(timeAndSource.group(2))

content1 = "11月21日 22:37 来自红米Note4"
timeAndSource = re.search("(.*?)来自(.*)", content1)
print(timeAndSource.group(1))
print(timeAndSource.group(2))

content1 = "1分钟前 来自微博 weibo.com"
timeAndSource = re.search("(.*?)来自(.*)", content1)
print(timeAndSource.group(1))
print(timeAndSource.group(2))

content1 = "35分钟前"
print(re.match("\d+分钟前", content1))
if re.match("\d+分钟前", content1):

    minute = re.match("(\d+)", content1).group(1)
    print(minute)
    beforeTime = time.localtime(time.time() - float(minute) * 60)
    print(beforeTime)
    datetime = time.strftime("%Y年%m月%d日 %H:%M", beforeTime)
    print(datetime)

    datetime = time.strftime("%Y年%m月%d日 %H:%M", time.localtime())
    print(datetime)
