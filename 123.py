import requests
import json
from bs4 import BeautifulSoup


url="https://www.google.com/search?q=endocare,%20inc"
page=requests.get(url)
b=str(BeautifulSoup(page.text,'html.parser'))
start = b.find('Parent organization')
end = b.find('</div>', start)
b=b[start:end][::-1]
start = b.find('>a/<')+4
end = b.find('>"', start)
c=b[start:end][::-1]

print(c)
