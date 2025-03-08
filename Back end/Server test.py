import requests

url = "http://127.0.0.1:5000/process"
data = {"get_hint":{"module":"ac_power", "paper_no":0, "question_no":3}}#{"get_hint":{"module":"mech_vib", "paper_no":1, "question_no":1}}

# {"authenticate":{"user_name":"abcd", "pw":"defg"}}
# {"register_user":{"user_name":"abcd", "pw":"defg"}}
# {"user_hint":{"user_name", "module":"maths", "paper_no":1, "question_no":1}}
response = requests.post(url, json=data)
print(response.json())