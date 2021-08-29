import scrapy
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
import json
from urllib import parse, request


# spider class
class HeadersCookies(scrapy.Spider):
    # spider name
    name = 'headerscookies'

    # urls
    url_req = 'https://mr-bricolage.bg/store-pickup/995334/pointOfServices'

    cookies = {
        "JSESSIONID": "20DF3E0602520F2BA7F813342D9DCE89",

        # "rxVisitor": "16302605757078SEF2R6PU3NTJRNECKVA946582RGED15",
        # "rxvt": "1630262425598|1630260575725",

        # "dtPC": "6$60575695_355h-vGPAJGAUFHCUNHSMMFUOHHPNGCQURIEPH-0e0",
        # "dtCookie": "v_4_srv_6_sn_0C1DD6FEC14736EC212EFA67589A0933_perc_100000_ol_0_mul_1_app-3A18ca1205c3b0a1f9_1_rcs-3Acss_0",
        # "dtLatC": "58",
        # "dtSa": "-",
        
        # Static
        "bricolage-customerLocation": "\"|42.6641056,23.3233149\"",
        "ROUTEID": ".node1",
        "cb-enabled": "enabled",

        # "_ym_visorc": "w",
        # "__utmb": "149670890.1.10.1630260601",
        # "__utmc": "149670890",
        # "__utmt": "1",
        # "_gid": "GA1.2.1776304751.1630260576",
        # "_ym_isad": "2",
        # "__utma": "149670890.884021372.1630260576.1630260601.1630260601.1",
        # "__utmz": "149670890.1630260601.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        # "_fbp": "fb.1.1630238726086.1257482489",
        # "_ga": "GA1.1.1030181028.1630238724",
        # "_ga_2E6XGN78KC": "GS1.1.1630260576.1.0.1630260576.0",
        # "_gac_UA-8419844-1": "1.1630238724.EAIaIQobChMI-L3kt5jW8gIVTvlRCh0BSQNKEAAYASAAEgLEbfD_BwE",
        # "_gcl_au": "1.1.1148094791.1630238724",
        # "_gcl_aw": "GCL.1630238724.EAIaIQobChMI-L3kt5jW8gIVTvlRCh0BSQNKEAAYASAAEgLEbfD_BwE",
        # "_ym_d": "1630238726",
        # "_ym_uid": "16302387261073241853",
    }

    csrf_token = '36b09f33-f2e9-45b4-98dc-19db96f71c09'

    # custom headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'mr-bricolage.bg'
    }

    # crawler's entry point
    def start_requests(self):
        data_raw = {
            'locationQuery': '',
            'cartPage': 'false',
            'latitude': '42.6641056',
            'longitude': '23.3233149',
            'CSRFToken': str(self.csrf_token)
        }
        # data = '&'.join('='.join([k, v]) for k, v in data_raw.items())
        data = self.dict2str(data_raw, '&')

        # Add cookies to headers
        self.headers['Cookie'] = self.dict2str(self.cookies, '; ')
        # self.headers['Cookie'] = '_fbp=fb.1.1630260576345.1411446093; dtCookie=v_4_srv_6_sn_0C1DD6FEC14736EC212EFA67589A0933_perc_100000_ol_0_mul_1_app-3A18ca1205c3b0a1f9_1_rcs-3Acss_0; dtLatC=1; rxVisitor=16302605757078SEF2R6PU3NTJRNECKVA946582RGED15; _ym_isad=2; dtPC=6$60575695_355h-vGPAJGAUFHCUNHSMMFUOHHPNGCQURIEPH-0e0; rxvt=1630262425598|1630260575725; cb-enabled=enabled; __utma=149670890.884021372.1630260576.1630260601.1630260601.1; __utmb=149670890.1.10.1630260601; __utmc=149670890; __utmt=1; __utmz=149670890.1630260601.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gcl_au=1.1.955118920.1630260601; _ym_visorc=w; _ym_d=1630260578; _ym_uid=1630260578809856298; _ga=GA1.2.884021372.1630260576; _ga_2E6XGN78KC=GS1.1.1630260576.1.0.1630260576.0; _gat_UA-8419844-1=1; _gid=GA1.2.1776304751.1630260576; dtSa=-; JSESSIONID=E43A44BD8BA10F9F242C0E8F0B78DC51; ROUTEID=.node0'
        # self.headers['Cookie'] = 'JSESSIONID=E43A44BD8BA10F9F242C0E8F0B78DC51; ROUTEID=.node0; dtCookie=v_4_srv_6_sn_0C1DD6FEC14736EC212EFA67589A0933_perc_100000_ol_0_mul_1_app-3A18ca1205c3b0a1f9_1_rcs-3Acss_0; dtLatC=1; dtPC=6$60575695_355h-vGPAJGAUFHCUNHSMMFUOHHPNGCQURIEPH-0e0; rxvt=1630262425598|1630260575725; cb-enabled=enabled; '

        print(f"Cookies string is: {self.headers['Cookie']}")
        print(f"Headers are: {self.headers}")

        # headers1 = self.headers.copy()
        
        # data = 'locationQuery=&cartPage=false&latitude=42.6641056&longitude=23.3233149&CSRFToken=43526f13-7dbc-4804-8f34-c32e85de700a'
        # self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'JSESSIONID=4E9FBC7837547C914B34DA5C274DFFDB; ROUTEID=.node2; cb-enabled=enabled;'}
        
        # print(f"old data: {data1}, new data: {data}")
        # print(f"old headers: {headers1}, new headers: {self.headers}")

        
        print(f"the formdata we are sending is: {data}")
        
        # Add content length to headers
        self.headers['Content-Length'] = len(data)
        data = data.encode()

        print('>>> Sending urllib request!')
        resp = self.get_data(self.url_req, self.headers, data)
        print(resp)
        return resp
        # print(">>> Sending request!")

        # yield scrapy.Request(
        #     url=self.url_rightmove,
        #     headers=self.headers,
        #     body=data,
        #     method="POST",
        #     # cookies=self.cookies
        # )

    @staticmethod
    def get_data(url, headers, data):
        r = request.Request(
            url,
            headers=headers,
            data=data,
            method="POST"
        )

        resp = request.urlopen(r)
        print(f"Response headers: {resp.headers}")
        return resp.read().decode()
    
    @staticmethod
    def dict2str(input: dict, delim: str):
        return delim.join('='.join([k, v]) for k, v in input.items())



# main driver
if __name__ == '__main__':
    # run spider
    process = CrawlerProcess()
    process.crawl(HeadersCookies)
    process.start()
