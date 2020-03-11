import requests

s = requests.Session()

payload = { 'username': 'sc17jhd',
            'password': 'blakew',
            "email": "abcdef@mail.com"}
# r = requests.get('http://127.0.0.1:8000/api/register', params=payload)
r = s.post('http://127.0.0.1:8000/api/login', data=payload)
print(r.text)

r = s.get('http://127.0.0.1:8000/api/rate', data=payload)
print(r.text)

# r = s.post('http://127.0.0.1:8000/api/logout', data=payload)
# print(r.text)

r = s.get('http://127.0.0.1:8000/api/rate', data=payload)
print(r.text)


r = s.get('http://127.0.0.1:8000/api/list', data=payload)
print(r.text)
