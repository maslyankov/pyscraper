from urllib import request, parse
import ssl
import certifi


def fetch_data():
    url_rightmove = 'https://mr-bricolage.bg/store-pickup/934403/pointOfServices'

    cookie_string = 'SESSIONID=5F93CE77BA13539AAEBE51B2EE0F54A1; bricolage-customerLocation="|42.6641056,23.3233149"; JSESSIONID=D1690F1114AA6B1F9AA17A0D3FC2E4EF; ROUTEID=.node2; cb-enabled=enabled'
    csrf_token = 'b0643b01-505e-441e-80eb-f653612c9880'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': str(cookie_string)
    }
    print(f"Headers are: {headers}")

    data_raw = {
        'locationQuery': '',
        'cartPage': 'false',
        'latitude': '42.6641056',
        'longitude': '23.3233149',
        'CSRFToken': str(csrf_token)
    }

    data = '&'.join('='.join([k, v]) for k, v in data_raw.iteritems())
    data = data.encode()

    r = request.Request(
        url_rightmove,
        headers={'Content-Type': 'application/json'},
        data=data,
        method="POST"
    )
    gcontext = ssl.SSLContext()  # Only for gangstars
    response = request.urlopen(r, context=gcontext)

    print(response.read())


if __name__ == '__main__':
    print("Starting...")
    fetch_data()
