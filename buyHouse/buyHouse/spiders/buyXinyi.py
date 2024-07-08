import scrapy


class BuyxinyiSpider(scrapy.Spider):
    name = "buyXinyi"
    allowed_domains = ["www.sinyi.com.tw"]
    taipei_city = [f"https://www.sinyi.com.tw/buy/list/Taipei-city/default-desc/{i}" for i in range(1, 307)]
    new_taipei_city = [f"https://www.sinyi.com.tw/buy/list/NewTaipei-city/default-desc/{i}" for i in range(1, 247)]
    keelong = [f"https://www.sinyi.com.tw/buy/list/Keelung-city/default-desc/{i}" for i in range(1, 96)]
    yilan_county = [f"https://www.sinyi.com.tw/buy/list/Yilan-county/default-desc/{i}" for i in range(1, 135)]
    hsinchu_city = [f"https://www.sinyi.com.tw/buy/list/Hsinchu-city/default-desc/{i}" for i in range(1, 40)]
    hsinchu_county = [f"https://www.sinyi.com.tw/buy/list/Hsinchu-county/default-desc/{i}" for i in range(1, 95)]
    taoyuan_city = [f"https://www.sinyi.com.tw/buy/list/Taoyuan-city/default-desc/{i}" for i in range(1, 615)]
    miaoli_county = [f"https://www.sinyi.com.tw/buy/list/Miaoli-county/default-desc/{i}" for i in range(1, 133)]
    taichung_city = [f"https://www.sinyi.com.tw/buy/list/Taichung-city/default-desc/{i}" for i in range(1, 687)]
    changhua_county = [f"https://www.sinyi.com.tw/buy/list/Changhua-county/default-desc/{i}" for i in range(1, 338)]
    nantou_county = [f"https://www.sinyi.com.tw/buy/list/Nantou-county/default-desc/{i}" for i in range(1, 60)]
    yunlin_county = [f"https://www.sinyi.com.tw/buy/list/Yunlin-county/default-desc/{i}" for i in range(1, 82)]
    chiayi_city = [f"https://www.sinyi.com.tw/buy/list/Chiayi-city/default-desc/{i}" for i in range(1, 51)]
    chiayi_county = [f"https://www.sinyi.com.tw/buy/list/Chiayi-county/default-desc/{i}" for i in range(1, 72)]
    tainan_city = [f"https://www.sinyi.com.tw/buy/list/Tainan-city/default-desc/{i}" for i in range(1, 574)]
    kaohsiung_city = [f"https://www.sinyi.com.tw/buy/list/Kaohsiung-city/default-desc/{i}" for i in range(1, 363)]
    pingtung_county = [f"https://www.sinyi.com.tw/buy/list/Pingtung-county/default-desc/{i}" for i in range(1, 177)]
    penghu_county = [f"https://www.sinyi.com.tw/buy/list/Penghu-county/default-desc/{i}" for i in range(1, 10)]
    taitung_county = [f"https://www.sinyi.com.tw/buy/list/Taitung-county/default-desc/{i}" for i in range(1, 57)]
    hualien_county = [f"https://www.sinyi.com.tw/buy/list/Hualien-county/default-desc/{i}" for i in range(1, 74)]
    kinmen_county = [f"https://www.sinyi.com.tw/buy/list/Kinmen-county/default-desc/{i}" for i in range(1, 7)]

    start_urls = taipei_city + new_taipei_city + keelong + yilan_county + hsinchu_city + hsinchu_county + taoyuan_city + miaoli_county + taichung_city + changhua_county + nantou_county + yunlin_county + chiayi_city + chiayi_county + tainan_city + kaohsiung_city + pingtung_county + penghu_county + taitung_county + hualien_county + kinmen_county
    # start_urls = ["https://www.sinyi.com.tw/buy/list/Taipei-city/default-desc/1"]

    def parse(self, response):
        urls = response.xpath('//div[@class="buy-list-item "]/a/@href').getall()
        for url in urls:
            full_url = f'https://www.sinyi.com.tw{url}'
            yield scrapy.Request(full_url, callback=self.parse_case_page)

    def parse_case_page(self, response):
        name = response.xpath('//span[@class="buy-content-title-name"]/text()').get()
        address = response.xpath('//span[@class="buy-content-title-address"]/text()').get()
        price = ''.join(response.xpath('//div[@class="buy-content-title-total-price"]/text()').getall())
        space = ' '.join(response.xpath('//div[@class="buy-content-detail-area"]/div/div/span/text()').getall())
        layout = response.xpath('//div[@class="buy-content-detail-layout"]/div/text()').get()
        house_type = ''.join(response.xpath('//div[@class="buy-content-detail-type"]/div/div/span/text()').getall())
        floors = response.xpath('//div[@class="buy-content-detail-floor"]/text()').get()
        basic_infos = response.xpath('//div[@class="buy-content-basic-cell"]')
        basic_info_dict = {}
        for basic_info in basic_infos:
            try:
                title = basic_info.xpath('.//div[@class="basic-title"]/text()').get().strip()
                value = basic_info.xpath('.//div[@class="basic-value"]/text()').get().strip()
                basic_info_dict[title] = value
            except Exception as e:
                try:
                    title = basic_info.xpath('.//div[@class="basic-title"]/text()').get().strip()
                    value = basic_info.xpath('.//div[@class="basic-value"]/span/text()').get().strip()
                    basic_info_dict[title] = value
                except Exception as e:
                    continue
        features = response.xpath('//div[@class="buy-content-obj-feature"]//div[@class="description-cell-text"]/text()').getall()
        tags = response.xpath('//div[@class="tags-cell"]/text()').getall()

        neighbor_history = []
        neighbor_history_rows = response.xpath(
            '//div[@id="trade-table-list-buyTradeBodyLg"]/div/div[contains(@class, "trade-obj-card-web")]')

        images = response.xpath('//div[@class="carousel-thumbnail-img "]/img/@src').getall()

        for row in neighbor_history_rows:
            neighbor_data = {
                "year_month": ''.join(row.xpath('.//div[1]//text()').getall()).strip().split('月')[0] + '月',
                "address": ''.join(row.xpath('.//div[2]//text()').getall()).strip(),
                "type_parking": ''.join(row.xpath('.//div[3]//text()').getall()).strip(),
                "total_price": ''.join(row.xpath('.//div[4]//text()').getall()).strip(),
                "unit_price": ''.join(row.xpath('.//div[5]//text()').getall()).strip(),
                "building_area": ''.join(row.xpath('.//div[6]//text()').getall()).strip(),
                "land_area": ''.join(row.xpath('.//div[7]//text()').getall()).strip(),
                "age": ''.join(row.xpath('.//div[8]//text()').getall()).strip(),
                "floor": ''.join(row.xpath('.//div[9]//text()').getall()).strip(),
                "layout": ''.join(row.xpath('.//div[10]//text()').getall()).strip()
            }
            if neighbor_data['address'] != '':
                neighbor_history.append(neighbor_data)

        yield {
            'url': response.url,
            'name': name,
            'images': images,
            'address': address,
            'price': price,
            'space': space,
            'layout': layout,
            'type': house_type,
            'floors': floors,
            'basic_info': basic_info_dict,
            'features': features,
            'tags': tags,
            'neighbor_history': neighbor_history,
        }