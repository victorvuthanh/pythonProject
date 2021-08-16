# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
# конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

user = 'victorvuthanh'

github_repo = requests.get(f'https://api.github.com/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(github_repo.json(), f)

for i in github_repo.json():
    print(i['name'])