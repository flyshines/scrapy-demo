# -*- coding: UTF-8 -*-
import scrapy
import sys
from scrapy.http import Request
from bs4 import BeautifulSoup
from miao.items import MiaoItem


class MySpider(scrapy.Spider):
    # 项目名称
    name = "MySpider"
    # 主域名
    allowed_domains = ['23us.so']
    # 前缀
    start_url = 'http://www.23us.so/list/'
    # 后缀
    end_url = '.html'

    isPrint = 1

    def start_requests(self):
        for i in range(1, 2):
            url = self.start_url + str(i) + '_1' + self.end_url
            print url
            yield Request(url, self.parse)

    def parse(self, response):
        # 找到最大页码
        max_num = BeautifulSoup(response.text, 'lxml').find_all('a', class_="last")[-1].get_text()
        # 拼接请求URL
        bashUrl = str(response.url)[:-6]
        for num in range(1, int(max_num)+1):
            url = bashUrl + str(num) + self.end_url
            yield Request(url, self.get_name)

    def get_name(self, response):
        # 1	Python标准库	    BeautifulSoup(html,’html.parser’)	Python内置标准库；执行速度快	容错能力较差
        # 2	lxml HTML解析库	BeautifulSoup(html,’lxml’)	        速度快；容错能力强	需要安装，需要C语言库
        # 3	lxml XML解析库	BeautifulSoup(html,[‘lxml’,’xml’])	速度快；容错能力强；支持XML格式	需要C语言库
        # 4	htm5lib解析库	BeautifulSoup(html,’htm5llib’)	    以浏览器方式解析，最好的容错性	速度慢
        # 查找标签为：<tr bgcolor="#FFFFFF">
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        for td in tds:
            # 查找第一个
            novelName = td.find('a').get_text()
            novelUrl = td.find('a')['href']
            print novelName, novelUrl
            yield Request(novelUrl, callback=self.get_chapter_url, meta={'name': novelName, 'url': novelUrl})

    def get_chapter_url(self, response):
        item = MiaoItem()
        # \xa0 是不间断空白符  \u3000 是全角的空白符
        item['name'] = str(response.meta['name'])
        item['novelUrl'] = str(response.url)
        soup = BeautifulSoup(response.text, 'lxml')
        bashUrl = soup.find('p', class_="btnlinks").find('a', class_="read")['href']
        category = str(soup.find('table').find_all('td')[0].find('a').get_text())
        author = str(soup.find('table').find_all('td')[1].get_text())
        status = str(soup.find('table').find_all('td')[2].get_text())
        nameId = str(bashUrl)[-16: -10].replace('/', '');
        item['category'] = str(category).replace('/', '')
        item['author'] = str(author).replace('/', '')
        item['name_id'] = nameId.replace('/', '')
        item['serialStatus'] = status.replace('/', '')
        return item
