import requests
from lxml import etree
import re
import time
import pandas as pd


base_url = 'https://movie.douban.com/top250'
#url_9 = 'https://movie.douban.com/top250?start=200&filter='
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}

movies = []

###请求网址函数
def get_url(url,headers):
    r = requests.get(url=url,headers=headers)
    return r.text


###爬取内容函数
def get_contents(r):
    html = etree.HTML(r)
    this_page = html.xpath('//div[@class="paginator"]/span'
                           '[@class="thispage"]/text()')[0]
    print('正在爬取第{}页。。。'.format(this_page))
    its = html.xpath('//ol[@class="grid_view"]/li/div[@class="item"]/'
                     'div[@class="info"]')
    for it in its:
        title = str(it.xpath('div[@class="hd"]/a/span/text()')[0]).split(',')[0]  #名称
        movie_url = it.xpath('div[@class="hd"]/a/@href')[0]  #电影网址
        actor = " ".join(str(it.xpath('div[@class="bd"]/p/text()')[0]).split())  #导演&主演
        year = " ".join(str(it.xpath('div[@class="bd"]/p/text()')[1]).split())  #年份&类型
        star = it.xpath('div[@class="bd"]/div[@class="star"]/span[2]/text()')[0]  #评分
        conts = re.findall('\d+', str(it.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0]))[0]  #评分人数
        # conts = str(it.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0])
        text_n = it.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')  #评语
        if text_n:
            text = text_n[0]
        else:
            text = None
        print(title, movie_url, actor, year, star,
              conts, text)
        movies.append([title, movie_url, actor, year, star,
              conts, text])

        time.sleep(1)
    n_url = html.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href')  #爬取下一页
    if n_url:
        next_url = next_page(n_url[0])
        next_r = get_url(next_url,headers)
        get_contents(next_r)
    else:
        print('爬取结束——_——')
    return movies

###构造下一页网址
def next_page(n_url):
    next_url = base_url + n_url
    return next_url

	
###下载并保存csv文件
def download_csv(movie):
    movie_df = pd.DataFrame(movie)
    filename = ['电影', 'URL', '导演&主演', '年份&类型', '评分', '评分人数', '评语']
    movie_df.columns = filename
    movie_df.to_csv('movies.csv',encoding='utf_8_sig')

if __name__ == '__main__':
    star_time = time.time()
    r = get_url(base_url,headers)
    movie = get_contents(r)
    download_csv(movie)
    end_time = time.time()
    print('爬取时间{}秒(•́へ•́╬)'.format((end_time-star_time)))