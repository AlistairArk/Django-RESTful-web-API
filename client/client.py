import requests

payload = { 'username': 'sc17jhd',
            'password': 'blakew',
            "email": "abc#def@mail.com"}
# r = requests.get('http://127.0.0.1:8000/api/register', params=payload)
r = requests.post('http://127.0.0.1:8000/api/register', data=payload)

print(r.url)
print("..")
print(r.text)