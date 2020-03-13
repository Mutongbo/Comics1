import scrapy,re
from Comics.items import ComicsItem
from scrapy import Selector

class ComicsSpider(scrapy.Spider):
    #爬虫的名字
    name = "Comics"
    #允许的域名
    allowed_domains = ["xieedang123.com"]
    start_urls = [
        "https://www.xieedang123.com/snmh/"
    ]
    def parse(self,response):
        Baseurl = "https://www.xieedang123.com/"
        contents = response.xpath("//div[@class='mainleft']/ul/li")
        for content in contents:
            comicsurl = content.xpath(".//a/@href").extract()[0]
            comicsurl = Baseurl + str(comicsurl)
            name = content.xpath(".//a/@title").extract()

            request = scrapy.Request(url = comicsurl,callback=self.ComicsInfomation)
            request.meta['comicsurl'] = comicsurl
            request.meta['name'] = name
            yield request
        next_page = Selector(response).re('<a href="(.*?)">下一页</a>')
        if next_page:
            preurl = "https://www.xieedang123.com/snmh/"
            url = preurl + next_page[0]
            yield scrapy.Request(url = url,callback=self.parse)

    def ComicsInfomation(self,response):

        comicsurl = response.meta['comicsurl']
        name = response.meta['name']
        imageurl = response.xpath("//ul[@class='mnlt']/li/img/@src").extract()
        pages = response.xpath("//ul[@class='pagelist']")[1].xpath(".//li[1]/a/text()").extract()

        print(pages[0])
        pages1=re.search('共(.*?)页:',pages[0])
        for i in range(int(pages1.group(1))):
            #
            if i==0:
                item = ComicsItem(comicsurl=comicsurl, name=name[0], imageurl=imageurl[0], pages=pages1.group(1), ppage=1)
                yield item
            else:
                url1 = comicsurl.replace(".html", "_%s.html" % (i + 1))
                print(url1)
                request = scrapy.Request(url = url1, callback=self.ComicspageInfomation)
                request.meta['comicsurl'] = url1
                request.meta['name'] = name
                #request.meta['imageurl']=imageurl
                request.meta['pages'] = pages1.group(1)
                request.meta['ppage'] = int(i+1)
                yield request

        # for i in range(int(pages1.group(1))):
        #     preurl = comicsurl
        #     url = preurl.replace(".html","_%s.html"%(i+1))
        #     print("url:",url)
        #     yield scrapy.Request(url = url,callback=self.parse)


    def ComicspageInfomation(self, response):
        comicsurl = response.meta['comicsurl']
        name = response.meta['name']
        pages = response.meta['pages']
        ppage = response.meta['ppage']
        print("ppagefinal:",ppage)
        imageurl = response.xpath("//ul[@class='mnlt']/li/img/@src").extract()
        print("image:",imageurl)
        item = ComicsItem(comicsurl = comicsurl,name = name[0],imageurl = imageurl[0],pages = pages,ppage=ppage)
        yield item









