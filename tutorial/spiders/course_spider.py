import scrapy

from tutorial.CourseItems import CourseItem
from tutorial.CourseItems import TimeItem


class TimesOnly(scrapy.Spider):
    name = "time_scraper"
    allowed_domains = ["webdev.cislabs.uncw.edu"]
    start_urls = [
        "http://webdev.cislabs.uncw.edu/~gag8520/ClassList.html"
    ]

    def parse(self, response):
        for sel in response.xpath('/html/body/div[4]/form/table/tbody/tr'):
            item = TimeItem()
            if not sel.xpath('th/text()').extract() and sel.xpath('td[10]/text()'):
                item['day'] = sel.xpath('td[9]/text()').extract()
                item['time'] = sel.xpath('td[10]/text()').extract()
                yield item


class CourseSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["webdev.cislabs.uncw.edu"]
    start_urls = [
        "http://webdev.cislabs.uncw.edu/~gag8520/ClassList.html"
        ]

    def parse(self, response):
        for sel in response.xpath('/html/body/div[4]/form/table/tbody/tr'):
            item = CourseItem()
            if not sel.xpath('th/text()').extract():
                # item['selectable'] = sel.xpath('td[1]/abbr/text()').extract()
                item['course_reference_number'] = sel.xpath('td[2]/a/text()').extract()
                item['subject_code'] = sel.xpath('td[3]/text()').extract()
                item['course_number'] = sel.xpath('td[4]/text()').extract()
                item['section_number'] = sel.xpath('td[5]/text()').extract()
                # item['campus'] = sel.xpath('td[6]/text()').extract()
                # item['credit_hours'] = sel.xpath('td[7]/text()').extract()
                # item['course_title'] = sel.xpath('td[8]/text()').extract()
                item['days'] = sel.xpath('td[9]/text()').extract()
                item['time_start'] = sel.xpath('td[10]/text()').extract()
                item['time_end'] = sel.xpath('td[10]/text()').extract()
                # item['section_capacity'] = sel.xpath('td[11]/text()').extract()
                # item['section_actual'] = sel.xpath('td[12]/text()').extract()
                # item['section_remaining'] = sel.xpath('td[13]/text()').extract()
                # item['waitlist_capacity'] = sel.xpath('td[14]/text()').extract()
                # item['waitlist_actual'] = sel.xpath('td[15]/text()').extract()
                # item['waitlist_remaining'] = sel.xpath('td[16]/text()').extract()
                # item['reserved_remaining'] = sel.xpath('td[17]/text()').extract()
                # item['instructor'] = sel.xpath('td[18]/text()').extract()
                # item['date'] = sel.xpath('td[19]/text()').extract()
                # item['location'] = sel.xpath('td[20]/text()').extract()
                # item['attribute'] = sel.xpath('td[21]/text()').extract()
                yield item
