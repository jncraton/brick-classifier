from urllib import request
from urllib.error import HTTPError
import re
import os
import random
import subprocess
import json

backgrounds = [3*c for c in ['9f', 'af', 'bf', 'cf', 'df', 'ef', 'ff']]

def get_part_url(part):
    """ 
    >>> get_part_url('3023')
    'https://www.brickowl.com/catalog/lego-plate-1-x-2-3023-6225'
    """
    
    r = request.urlopen(f"https://www.brickowl.com/search/catalog?query={part}")

    content = r.read().decode('utf8')

    m = re.search('/catalog/lego.*?"', content)

    return "https://www.brickowl.com" + m.group(0)[:-1]

def get_imgs(part, part_url):
    r = request.urlopen(part_url)

    content = r.read().decode('utf8')

    imgs = re.findall('https://img.brickowl.com/files/image_cache/small/.*?.png', content)

    imgs = [i for i in imgs if 'placeholder' not in i]

    print(f"Downloading {len(imgs)} images for {part} {part_url}")

    for i, img_url in enumerate(imgs):
        img = request.urlopen(img_url).read()

        filename = f"train/{part}/brickowl-{i}.png"
        
        with open(filename, 'wb') as out:
            out.write(img)

        subprocess.run([
            'convert',
            filename,
            '-background', '#ffffff',
            '-gravity', 'center',
            '-extent', '256x256',
            '-colorspace', 'Gray',
            filename,
        ])

    return len(imgs)

if __name__ == '__main__':
    with open('parts.json', 'r') as f:
        parts = json.load(f)

    total = 0

    for part in parts:
        total += get_imgs(part, get_part_url(part))

    print(f"Downloaded {total} images")
