import requests
import json

# res = requests.get('http://127.0.0.1:5000/api/task/4', headers={'Content-Type': 'application/json', "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzk5NzAxMSwianRpIjoiYjc2MjRlODEtODRkNi00NWUwLWFkZjQtZTAzOTE3MGY1ZDJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk3OTk3MDExLCJleHAiOjE2OTc5OTc5MTF9.GVASzCztekZE1NUTqd7BQnQV4REDef6YJhze46wJdMo"})
d = {'name': 'Task Json', 'category_id': 1}
res = requests.post('http://127.0.0.1:5000/api/task', data=json.dumps(d), headers={'Content-Type': 'application/json', "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzk5NzAxMSwianRpIjoiYjc2MjRlODEtODRkNi00NWUwLWFkZjQtZTAzOTE3MGY1ZDJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk3OTk3MDExLCJleHAiOjE2OTc5OTc5MTF9.GVASzCztekZE1NUTqd7BQnQV4REDef6YJhze46wJdMo"})
print(res)