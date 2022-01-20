import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

async def welcome(url=None, name=None, guild=None):
    iurl = url
    av = Image.open(requests.get(iurl, stream=True).raw)
    av = av.resize((254, 254), resample=0, box=None)



    img = Image.open("cogs/src/Und.png")
    I1 = ImageDraw.Draw(img)
    custom = str(guild)
    cs = str(name)
    fs1 = 100
    fs2 = 155
    for i in custom:
        if fs1 < 0:
            fs1 = fs1
            break
        else:
            fs1 -= 5
    for x in cs:
        if fs2 < 0:
            fs1 = fs1
            break
        else:
            fs2 -= 4.1

    font1 = ImageFont.truetype("cogs/src/Uni Sans Heavy.otf", size=int(fs1))
    font = ImageFont.truetype("cogs/src/Uni Sans Heavy.otf", size=int(fs2))

    I1.text((594, 330), text=f"To {custom}", fill=(255, 255, 255), font=font1, align='center', anchor='ms')
    I1.text((594, 197), text=f"{cs}", fill=(255, 255, 255), font=font, align='center', anchor='mm')

    mask_im = Image.new("L", av.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, 255, 255), fill=255)
    back_im = Image.new("RGB", av.size, 0)
    back_im.paste(av, (0, 0), mask_im)
    img.paste(back_im, (68, 59), mask_im)

    return img

