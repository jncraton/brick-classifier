from urllib.parse import unquote 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from urllib import request
from urllib.error import HTTPError

def get_part_urls(part):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)

    driver.get(f'https://duckduckgo.com/?q=lego+part+{part}&iar=images&iaf=layout%3ASquare%2Csize%3AMedium%2Ctype%3Aphoto&iax=images&ia=images')

    # For now it's working with this class, not sure if it will never change
    img_tags = WebDriverWait(driver, timeout=5).until(lambda d: d.find_elements_by_class_name('tile--img__img'))

    for tag in img_tags:
        src = tag.get_attribute('data-src')
        src = unquote(src)
        src = src.split('=', maxsplit=1)
        src = src[1]
        yield src

    driver.close()

def save_top_n(part, n=10):
    img_urls = list(get_part_urls(part))[:n]

    print(f"Saving {len(img_urls)} images for {part}")

    for i, url in enumerate(img_urls):
        r = request.urlopen(url)

        with open(f'train/{part}/ddg-{i}.png', 'wb') as f:
            f.write(r.read())

if __name__ == '__main__':
    import json
    
    with open('parts.json', 'r') as f:
        parts = json.load(f)

    for part in parts:
        save_top_n(part, 10)

