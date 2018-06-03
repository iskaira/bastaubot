import requests


with open('сала таңдаудың төрт шеңбері.jpg', 'rb') as f:
    print(
        requests.post(
            'http://telegra.ph/upload',
            files={'file': ('file', f, 'image/jpeg')}
        ).json()
    )
