import requests

url = "http://127.0.0.1:5000/process"
data = {"get_hint":{"module":"maths", "paper_no":1, "question_no":1}}
response = requests.post(url, json=data)
print(response.json())