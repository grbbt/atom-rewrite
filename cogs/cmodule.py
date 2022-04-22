import requests as r
import difflib



base_url = "https://api.thecatapi.com/v1/images/search"
CATegories = "https://api.thecatapi.com/v1/categories"
breeds = "https://api.thecatapi.com/v1/breeds"



def check_cate(sample="None"):
    page = r.get(CATegories)
    pagelist = page.json()
    names = []
    sample = sample.lower()
    for category in pagelist:
        name = category.get('name')
        names.append(name)

    result = difflib.get_close_matches(sample, names)
    for category1 in pagelist:
        if category1.get('name') == str(result)[2:-2]:
            return category1.get('id')
        else:
            continue


def check_breed(sample="None"):
    sample = sample.lower()
    names = []
    page = r.get(breeds)
    pagelist = page.json()
    for cats in pagelist:
        names.append(cats.get('name'))
    result = difflib.get_close_matches(sample, names)
    for cat1 in pagelist:
        if cat1.get('name') == str(result)[2:-2]:
            return cat1.get('id')
        else:
            continue




def get_cat(url=None):
    if url is not False:
        page = r.get(url)
        page_dict = page.json()[0]
        image = page_dict.get("url")
        return image
    else:
        return False



def specify(query=None):

    cate = check_cate(query)
    breed = check_breed(query)

    if cate or breed is not None:
        if cate is not None:
            url = f"https://api.thecatapi.com/v1/images/search?category_ids={cate}"
        else:
            pass
        if breed is not None:
            url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed}"
        else:
            pass
    else:
        url = None

    return url


def cat(tags=None):
    if tags is None:
        url = base_url
    else:
        url = specify(tags)

    if url is None:
        url = False
    else:
        pass

    image = get_cat(url)

    return image