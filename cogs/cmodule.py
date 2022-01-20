import re
import requests
import random

catass = "https://cataas.com/"

def get_random_cat():

    htm = requests.get(url=f"{catass}api/cats")
    html = str(htm.content)
    x = re.findall(r'id":(.+?)"', html)
    f = open('asd.txt', 'w')
    f.write(str(htm.content))
    y = []
    for i in x:
        o = str(i).replace('"', '')
        y.append(o)

    ranid = y[random.randint(1, 150)]
    url = f'{catass}cat/{ranid}'

    return url

def get_cat_tag(tag):
    url = f"{catass}cat/{tag}"
    htm = requests.get(url=url)
    html = str(htm.content)
    if str(html).replace("'", "") == 'b':
        return False
    else:
        return url


