from allnews.items import AllnewsItem
import scrapy
import time
import csv

class NewsUrlSpider(scrapy.Spider): #기사 제목과 링크
    name="newsUrlCrawler"

    def start_requests(self):
        keyword = input('검색어를 입력하세요 : ')
        news_num = int(input('총 필요한 뉴스기사 수를 입력하세요 : '))
        keyword = keyword.replace(' ', '+')

        url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query={}'.format(keyword)

        yield scrapy.Request(url,self.parse_news)

    def parse_news(self,response):
        for sel in response.xpath('//*[@id="mArticle"]/div[2]/ul/li/div'):
            item=AllnewsItem()
            item['company']=sel.xpath('strong/span[@class="info_news"]/text()').extract()[0]
            item['category']='IT'
            item['title']=sel.xpath('strong[@class="tit_thumb"]/a/text()').extract()[0]
            item['url']=sel.xpath('strong[@class="tit_thumb"]/a/@href').extract()[0]
            item['date']=sel.xpath('strong[@class="tit_thumb"]/span/span[@class="info_time"]/text()').extract()[0]

            print('*'*100)
            print(item['title'])
            print(item['url'])

            time.sleep(5)
            yield item

class NewsSpider(scrapy.Spider): #기사 내용
    name="newsCrawler"

    def start_requests(self):
        with open('newsUrlCrawl.csv') as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                yield scrapy.Request(row['url'],self.parse_news)
    def parse_news(self,response):
        item=AllnewsItem()

        item['company'] = response.xpath('//*[@id="cSub"]/div[1]/em/a/img/@alt').extract()[0]
        item['category'] = 'IT'
        item['title'] = response.xpath('//*[@id="cSub"]/div[1]/h3/text()').extract()[0]
        item['date'] = response.xpath('/html/head/meta[contains(@property, "og:regDate")]/@content').extract()[0][:8]
        item['article'] = response.xpath(
            '//*[@id="harmonyContainer"]/section/div[contains(@dmcf-ptype, "general")]/text()').extract() \
                          + response.xpath(
            '//*[@id="harmonyContainer"]/section/p[contains(@dmcf-ptype, "general")]/text()').extract()
        print('*'*100)
        print(item['title'])
        print(item['url'])

        time.sleep(5)
        yield item
