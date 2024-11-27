import requests
import csv
from bs4 import BeautifulSoup

session = requests.session()

url = 'https://jumia.co.ke'

prdraw = session.get(url)

soup = BeautifulSoup(prdraw.content, 'html.parser')

prd_box = soup.find_all('article', class_="prd _box col _hvr")

content = []
reviews = []
for prd in prd_box:
    spec = 'https://jumia.co.ke' + prd.find('a').get('href')
    specurl = session.get(spec)
    specsoup = BeautifulSoup(specurl.content, 'html.parser')

    review_box = specsoup.find('div', class_="row -fw-nw")

    num_reviews = review_box.find('h2', class_='-fs14 -m -upp -ptm')
    num_reviewstxt = num_reviews.text if num_reviews else 0
    rev_num = int(num_reviewstxt.split('(')[1].split(')')[0]) if num_reviewstxt != 0 else 0

    rating = review_box.find('span', class_='-b')
    ratingtxt = rating.text if rating else "Not found"

    discount = specsoup.find('span').get('data-disc')

    name = prd.find('div', class_='name').text

    brand = name.split()[0]

    price = prd.find('div', class_='prc').text

    content.append([name, brand, price, discount, num_reviewstxt, ratingtxt])
    reviews.append(rev_num)

with open('jumia.csv', 'w') as jumia:
    writer = csv.writer(jumia)
    writer.writerow(['Name', 'Brand', 'Price', 'Discount', 'Number of reviews', 'Rating'])
    writer.writerows(content)

max_rev = reviews.index(max(reviews))

print(f'Best product to sell is: {content[max_rev][0]}')