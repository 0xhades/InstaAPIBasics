import hashlib, random, string, uuid, requests, json, time, calendar

def RandomString(n = 10):
    letters = string.ascii_lowercase + '1234567890'
    return ''.join(random.choice(letters) for i in range(n))

def RandomStringUpper(n = 10):
    letters = string.ascii_uppercase + '1234567890'
    return ''.join(random.choice(letters) for i in range(n))

def RandomStringChars(n = 10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))

def randomStringWithChar(stringLength=10):
    letters = string.ascii_lowercase + '1234567890'
    result = ''.join(random.choice(letters) for i in range(stringLength - 1))
    return RandomStringChars(1) + result

def hex_digest(*args):
    m = hashlib.md5()
    m.update(b''.join([arg.encode('utf-8') for arg in args]))
    return m.hexdigest()

def generate_device_id(seed):
    volatile_seed = "12345"
    m = hashlib.md5()
    m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + m.hexdigest()[:16]

def randDevice() -> str:

    dpi = [
    '480', '320', '640', '515', '120', '160', '240', '800'
    ]
    manufacturer = [
        'HUAWEI', 'Xiaomi', 'samsung', 'OnePlus', 'LGE/lge', 'ZTE', 'HTC',
        'LENOVO', 'MOTOROLA', 'NOKIA', 'OPPO', 'SONY', 'VIVO', 'LAVA'
    ]
    
    randResolution = random.randrange(2, 9) * 180
    lowerResolution = randResolution - 180

    DEVICE = {
        'android_version': random.randrange(18, 25),
        'android_release': f'{random.randrange(1, 7)}.{random.randrange(0, 7)}',
        'dpi': f'{random.choice(dpi)}dpi',
        'resolution': f'{lowerResolution}x{randResolution}',
        'manufacturer': random.choice(manufacturer),
        'device': f'{random.choice(manufacturer)}-{RandomStringUpper(5)}',
        'model': f'{randomStringWithChar(4)}',
        'cpu': f'{RandomStringChars(2)}{random.randrange(1000, 9999)}'
    }

    if random.randrange(0, 2):
        DEVICE['android_release'] = f'{random.randrange(1, 7)}.{random.randrange(0, 7)}.{random.randrange(1, 7)}'

    USER_AGENT_BASE = (
        'Instagram (VERSION) '
        'Android ({android_version}/{android_release}; '
        '{dpi}; {resolution}; {manufacturer}; '
        '{device}; {model}; {cpu}; en_US)'
    )

    return USER_AGENT_BASE.format(**DEVICE)

''' -------------------------------------------------- '''

def UserAgent(): # "user-agent"
    version = f'{random.randint(3, 138)}.{random.randint(5, 10)}.{random.randint(0, 10)}'
    if random.randint(0, 1):
        version = f'{random.randint(4, 138)}.{random.randint(0, 10)}.{random.randint(0, 10)}'
    if random.randint(0, 1):
        version = '155.0.0.37.107' #last version

    return randDevice().replace('(VERSION)', version)

def DeviceID(username, password): # "device_id"
    return generate_device_id(hex_digest(username, password))

def guid(): return str(uuid.uuid4()) # "phone_id", "guid", "adid"

def fetch_headers() -> dict:
    url = 'https://i.instagram.com/api/v1/si/fetch_headers/'

    headers = {}
    headers['Host'] = 'i.instagram.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Language'] = 'ar,en-US;q=0.7,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Connection'] = 'close'

    return requests.get(url, headers=headers).cookies # use it as cookies or dict [ cookies.get_dict() ]

init_cookies = fetch_headers()
TimeStamp = calendar.timegm(time.gmtime())

headers = {}
headers['User-Agent'] = UserAgent()
headers['Host'] = 'i.instagram.com'
headers['x-ig-app-locale'] = 'en_SA'
headers['x-ig-device-locale'] = 'en_SA' 
headers['x-ig-mapped-locale'] = 'en_US'
headers['x-pigeon-session-id'] = guid()
headers['x-pigeon-rawclienttime'] = f'{TimeStamp}'
headers['x-ig-connection-speed'] = '643kbps'
headers['x-ig-bandwidth-speed-kbps'] = '1236.889'
headers['x-ig-bandwidth-totalbytes-b'] = '6672937'
headers['x-ig-bandwidth-totaltime-ms'] = '7015'
headers['x-ig-app-startup-country'] = 'SA'
headers['x-bloks-version-id'] = '85e371bf185c688d008ad58d18c84943f3e6d568c4eecd561eb4b0677b1e4c55'
headers['x-ig-www-claim'] = '0'
headers['x-bloks-is-layout-rtl'] = 'false'
headers['x-ig-device-id'] = guid()
headers['x-ig-android-id'] = DeviceID('username', 'password')
headers['x-ig-connection-type'] = 'WIFI'
headers['x-ig-capabilities'] = '3brTvw8='
headers['x-ig-app-id'] = '567067343352427'
headers['accept-language'] = 'en-SA, en-US'
headers['x-mid'] = init_cookies['mid']
headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8' 
headers['accept-encoding'] = 'gzip, deflate'
headers['x-fb-http-engine'] = 'Liger'
headers['Connection'] = 'keep-alive' 
# keep-alive keep the connection between the client and the server alive, so you don't need to reconnect every time you send a request
# == make it faster

#example for the data you will send "POST", in "GET" you don't need to do this 'duhh' {

data = {} # init dict

# here you put the request parameters, every request has its unique parameters (data) for example: {
# login has (username, password) so you put:
#
# data['username'] = username
# data['password'] = password
#
# }
data['key'] = 'value'

#the signed_body:
signed_body = f'SIGNATURE.{json.dumps(data)}' #dict to json string
# hashed_data . json data
# in the new versions of instagram, you don't have to hash the data anymore
# instead you replace it with anything or by default 'SIGNATURE'

# }

#finally you make the postData, you can make it dict or string:

postData = {}

postData['signed_body'] = signed_body
#postData['ig_sig_key_version'] = '4'/'5' you don't need to put the key version in the new versions of instagram

#or to string

postData = f'signed_body={signed_body}'

#then you send it using whatever method you want to send it (requests, urllib, socket)

response = requests.post('https://i.instagram.com/api/v1/ your request path', headers=headers, data=data, cookies='if you want to')

print(response.text)
