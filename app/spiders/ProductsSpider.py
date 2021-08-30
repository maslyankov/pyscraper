from re import sub
from json import loads
from urllib import request, error

from scrapy import Request, Spider
from scrapy.loader import ItemLoader

from app.items import Product


def strip_str(str):
    return sub(r"[\n\t\s]*", "", str)


def parse_specs(response):
    specs = dict()

    specs_selector = response.css('div.product-classifications table.table tbody tr')
    for row in specs_selector:
        item_name = row.xpath('td[1]//text()').extract_first()
        item_val = strip_str(row.xpath('td[2]//text()').extract_first())

        specs[item_name] = item_val

    return specs


class ProductsSpider(Spider):
    name = "products"
    start_urls = [
        'https://mr-bricolage.bg/instrumenti/elektroprenosimi-instrumenti/vintoverti/c/006003013?q=%3Arelevance&page=0&priceValue=',
    ]
    current_node = None
    total_availability = dict()

    def parse(self, response):
        page = response.url.split("page=")[-1].split("&price")[0]

        # Get products urls list
        prod_urls = response.css('div.product div.title a.name::attr(href)').getall()

        # Parse every product separately
        yield from response.follow_all(prod_urls, self.parse_product)

        # Iterate through all pages...
        is_last_page = response.xpath(
            "//li[contains(@class, 'pagination-next') and contains(@class, 'disabled')]").get()
        if not is_last_page:
            next_page = response.css('li.pagination-next a').attrib['href']
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)

    def parse_product(self, response):
        print(f">>> Parsing product...")

        p_specs = parse_specs(response)
        p_name = response.css('h1.js-product-name::text').get()

        # If there is Brand in the specs dict...
        if "Марка" in p_specs:
            p_name = f"{p_specs['Марка']} {p_name}"

        # Get product availability
        p_availability = self.get_availability(response)
        if p_availability:
            self.save_to_global_availability(p_availability)

            lowest_avail = self.get_lowest_availability_store(p_availability)
            if not isinstance(lowest_avail[1], list):
                print(f"storename is: {p_availability[lowest_avail[1]]['store_name']}")
                print(f"Type is: {type(p_availability[lowest_avail[1]]['store_name'])}")
            
            try:
                lowest_stores = [p_availability[store]['store_name'] for store in lowest_avail[1]] if isinstance(lowest_avail[1], list) else p_availability[lowest_avail[1]]['store_name']

                p_lowest_availability = {
                    'store': lowest_stores,
                    'stock': lowest_avail[0]
                }
            except TypeError:
                print("Errored!")
                print(f"lowest avail[1]: {lowest_avail[1]}")
                print(f"availability: {p_availability}")

                # print(f"storename is: {p_availability[lowest_avail[1]]['store_name']}")
                # print(f"Type is: {type(p_availability[lowest_avail[1]]['store_name'])}")

        print(f'for {p_name} we got this avaibalility: {p_availability}')

        # Add data to item
        l = ItemLoader(item=Product(), response=response)
        l.add_value('name', p_name)
        l.add_css('price', 'p.js-product-price::attr(data-price-value)')
        l.add_css('images', 'div.popup-gallery img::attr(src)')
        l.add_value('specs', p_specs)
        l.add_value('url', response.url)

        if p_availability:
            l.add_value('availability', p_availability)

            l.add_value('lowest_stock', p_lowest_availability)

        return l.load_item()

    def get_availability(self, response):
        # Product info
        p_url = response.url
        p_id = p_url.split('/')[-1]

        url = f'https://mr-bricolage.bg/store-pickup/{p_id}/pointOfServices'

        print(f"Fetching and (maybe) parsing availability data for {url}")


        fetched = self.get_data(url, response)

        if fetched:
            return self.parse_availability(fetched)
        else:
            return None

    def get_data(self, url, response):
        csrf_token = response.xpath('//input[@name="CSRFToken"]/@value').get()
        cookie_string = response.headers['Set-Cookie'].split()[0].decode() + f"cb-enabled=enabled; "

        headers = dict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

        data_raw = {
            'locationQuery': '',
            'cartPage': 'false',
            'latitude': '42.6641056',
            'longitude': '23.3233149',
            'CSRFToken': str(csrf_token)
        }
        data = self.dict2str(data_raw, '&')

        nodes = [f".node{i}" for i in range(4)]

        while len(nodes):
            if self.current_node is None:
                self.current_node = nodes[0]
            
            headers['Cookie'] = cookie_string + f"ROUTEID={self.current_node};"
            try:
                r = request.Request(
                    url,
                    headers=headers,
                    data=data.encode(),
                    method="POST"
                )
                resp = request.urlopen(r)
            except error.HTTPError as e:
                print(f"len is: {len(nodes)}")
                if len(nodes) > 2:
                    print(f"Tried with {self.current_node}, with no success! :( Trying next...")

                    nodes.remove(self.current_node)
                    self.current_node = None

                    continue
                else:
                    print(e)
                    print(">>> Tried sending request with...")
                    print(f">>  URL: {url}")
                    print(f">>  CSRFToken: {csrf_token}")
                    print(f">>  Cookie String: {cookie_string}")
                    print(f">>  Headers: {headers}")
                    print(f">>  Data (decoded): {data}")

                    self.current_node = None

                    return
            else:
                print(f"Success with node: {self.current_node}")

                break

        ret = resp.read()

        # print(f">>> Request got resp: {ret}")

        return ret
    
    @staticmethod
    def parse_availability(raw_data):
        if not raw_data:
            return

        data = loads(raw_data)['data']

        availability = dict()

        for entry in data:
            availability[entry['name']] = {
                'store_name': entry['displayName'],
                'store_address': entry['line1'],
                'stock': entry['stockLevel']
            }

        return availability

    @staticmethod
    def dict2str(input: dict, delim: str):
        return delim.join('='.join([k, v]) for k, v in input.items())

    def save_to_global_availability(self, availability):
        for store in availability:
            if store not in self.total_availability:
                self.total_availability[store] = availability[store]
            else:
                self.total_availability[store]['stock'] = int(self.total_availability[store]['stock']) + int(availability[store]['stock'])

    @staticmethod
    def get_lowest_availability_store(availability):
        lowest = (None, None)

        for store in availability:
            current = int(availability[store]['stock'])

            if lowest[0] is None or current < lowest[0]:
                lowest = (current, store)
            elif lowest[0] == current:
                if isinstance(lowest[1], list):
                    lowest[1].append(store)
                else:
                    lowest = (current, [lowest[1]])
            
        return lowest
    
    def closed(self, reason):
        # will be called when the crawler process ends
        lowest_availability_total = self.get_lowest_availability_store(self.total_availability)

        print(f"Lowest availability is in: '{self.total_availability[lowest_availability_total[1]]['store_name']}' with only available {lowest_availability_total[0]} of all parsed products!")


