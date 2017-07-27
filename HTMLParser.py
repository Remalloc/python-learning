from html.parser import HTMLParser
from collections import OrderedDict
import urllib.request


class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.flag=None
        self.tag=('event-title','datetime','event-location')
        self.result=OrderedDict()


    def handle_starttag(self, tag, attrs):
        for i in attrs:
            if i[0] in self.tag:
                self.flag=i[0]
            elif i[1] in self.tag:
                self.flag=i[1]

    def handle_data(self, data):
        if self.flag:
            if self.flag == self.tag[0]:
                self.result[data]=None
            elif self.flag==self.tag[1]:
                key=self.result.popitem()
                self.result[key[0]]=data
            elif self.flag==self.tag[2]:
                key,value=self.result.popitem()
                self.result[key]=(value,data)
            self.flag=None

    def get_result(self):
        return self.result

url="https://www.python.org/events/python-events/"
request=urllib.request.Request(url)
response=urllib.request.urlopen(request)
data=response.read().decode('utf-8')

parser = MyHTMLParser()
parser.feed(data)
for name,info in parser.result.items():
    print("name: %s,time: %s,location: %s"%(name,info[0],info[1]))