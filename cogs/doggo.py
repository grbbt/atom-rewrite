import requests
import dictpy
import re


def getbreed(string):
    dictionary = dict(requests.get('https://dog.ceo/api/breeds/list/all').json())
    a = dictpy.DictSearch(data=dictionary, target=string)
    if not a.result:
        return None
    return a.result



def doggo(tag=None):
    if tag is None:
        htm = requests.get("https://dog.ceo/api/breeds/image/random")
        html = dict(htm.json())
        link = html.get('message')

    if tag is not None:
        a = getbreed(tag)
        if a is not None:
            if '}' in str(a):
                l = f"https://dog.ceo/api/breed/{tag}/images/random"
                htm = requests.get(l)
                html = dict(htm.json())
                link = html.get('message')

            else:
                res = re.findall(r"'message(.+?)',", str(a))
                r = str(res).replace('[', '').replace(']', '').replace("'", "").replace(".", "")
                l = f"https://dog.ceo/api/breed/{r}/{tag}/images/random"
                htm = requests.get(l)
                html = dict(htm.json())
                link = html.get('message')

        else:
            link = "https://th.bing.com/th/id/OIP.eaohbN4jI152vWHz4v0Z0gHaHa?w=201&h=201&c=7&r=0&o=5&dpr=1.25&pid=1.7"


    return link

