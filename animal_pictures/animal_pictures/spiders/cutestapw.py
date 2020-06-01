# -*- coding: utf-8 -*-
import os
import scrapy
from urllib import request
from lxml import etree
# from animal_pictures.items import AnimalPicturesItem
from ..items import AnimalPicturesItem


# 列表缩略图
# http://www.cutestpaw.com/wp-content/uploads/2016/01/s-Newborns..jpg
# http://www.cutestpaw.com/wp-content/uploads/2016/01/Newborns..jpg

# xpath
# 获取当前页面所有的图片 url
# //div[@id='photos']/a/img/@src
# 获取图片标题
# //div[@id='photos']/a/@title
# 获取所有的图片 a 节点
# //div[@id='photos']/a


class CutestapwSpider(scrapy.Spider):
    name = 'cutestapw'
    allowed_domains = ['http://www.cutestpaw.com/']
    start_urls = [f'http://www.cutestpaw.com/page/{i}/' for i in range(2, 203)]
    data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p_save_dir = os.path.join(data_dir, "downloads")

    def download_img(self, url, save_path):
        """ 下载一张图片，保存到指定位置 """

        if os.path.exists(save_path):
            print(f"跳过: {url}")
            return "success"

        try:
            response = request.urlopen(url, timeout=20)
            with open(save_path, 'wb') as f:
                f.write(response.read())
            print(f"下载成功: {save_path}")
            return "success"
        except Exception as e:
            print(f"{url} 下载失败 {e}")
            return f"{e}"

    def parse(self, response):
        """ 解析页面 """

        if not os.path.exists(self.p_save_dir):
            os.makedirs(self.p_save_dir)

        selector = etree.HTML(response.body)
        s_list = selector.xpath("//div[@id='photos']/a")

        for s in s_list:

            item = AnimalPicturesItem(name="", status="Downloading")
            item['title'] = s.xpath("@title")[0] if s.xpath("@title") else ""
            url = s.xpath("img/@src")[0] if s.xpath("img/@src") else ""
            if url:
                url_prefix, p_name = url.rsplit("/", maxsplit=1)
                name = p_name.split('-', maxsplit=1)[-1]
                url = url_prefix + "/" + name
                item['name'] = name
                item['url'] = url
                item['status'] = self.download_img(url, os.path.join(self.p_save_dir, name))
                yield item
