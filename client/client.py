import requests

s = requests.Session()

payload = { 'username': 'sc17jhd',
            'password': 'blakew',
            "email": "abcdef@mail.com"}
# r = requests.get('http://127.0.0.1:8000/api/register', params=payload)
r = s.post('http://127.0.0.1:8000/api/login', data=payload)
print(r.text)

# r = s.get('http://127.0.0.1:8000/api/rate', data=payload)
# print(r.text)

# r = s.post('http://127.0.0.1:8000/api/logout', data=payload)
# print(r.text)

# r = s.get('http://127.0.0.1:8000/api/rate', data=payload)
# print(r.text)


r = s.get('http://127.0.0.1:8000/api/list', data=payload)
print(r.text)


# COMP4568: Programming For The Web, 2017, Semester 2, JS0, SW0
# COMP4568: Programming For The Web, 2005, Semester 2, KM0
# COMP4568: Programming For The Web, 2004, Semester 1, JS0
# COMP4568: Programming For The Web, 2005, Semester 1, ZH0
payload = { "moduleCode" : "COMP4568",
            "professorID": "SW0",
            "year"       : 2017,
            "semester"   : 2,
            "rating"     : 4}

r = s.post('http://127.0.0.1:8000/api/rate', data=payload)
print(r.text)