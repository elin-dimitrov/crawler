import scrapy
import json
import os.path
from scrapy.http.request import Request


class PoliticSpider(scrapy.Spider):
    name = "parlament"
    start_urls = ['https://www.parliament.bg/bg/MP']

    def parse (self, response):

        """This method generates all needed links and passed
           to "parse_minister" method!
        """

        par_url = 'https://www.parliament.bg'
        urls = response.css('div.MPinfo a::attr(href)').getall()
        for url in urls:
            url = f"{par_url}{url}"
            yield Request(url, self.parse_minister)


    def parse_minister(self, response):

        """This method extract basic data for each minister 
           in the current government!
        """
        minister_name = response.css('div.MProwD strong::text').getall()
        minister = response.css( 'ul.frontList li::text').getall()
        email = response.css('.MPinfo ul.frontList li a::text').getall()
        yield{
                 'Minister name': minister_name,
                 'Minister Info': minister,
                 'Minister email': email}