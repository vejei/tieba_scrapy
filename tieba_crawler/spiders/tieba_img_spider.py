import scrapy
from tieba_crawler.items import ImageItem


class TiebaSpider(scrapy.Spider):
    name = 'tbimg'

    def start_requests(self):
        url = 'http://tieba.baidu.com/f?kw=%E6%B8%A1%E8%BE%B9%E9%BA%BB%E5%8F%8B'
        yield scrapy.Request(url=url, callback=self.parse_post)

    def parse_post(self, response):
        post_list = response.css('ul#thread_list li.j_thread_list')
        for item in post_list:
            title = item.css('a.j_th_tit::text').extract_first()
            url = 'http://tieba.baidu.com' \
              + item.css('a.j_th_tit::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_image)
        page_list = response.css('div#frs_list_pager a::attr(href)').extract()
        if not page_list:
            return
        else:
            next_page = page_list[-2]
            if next_page:
                yield response.follow(next_page, callback=self.parse_post)

    def parse_image(self, response):
        img_urls = response.css('div#j_p_postlist img.BDE_Image::attr(src)').extract()
        yield ImageItem(image_urls=img_urls)
        page_list = response.css('ul.l_posts_num li.pb_list_pager a::attr(href)').extract()
        if not page_list:
            return
        else:
            next_page = page_list[-2]
            if next_page:
                yield response.follow(next_page, callback=self.parse_image)
