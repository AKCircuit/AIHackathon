import requests


def testRequest(data):
    url = "http://127.0.0.1:5000/process"
    response = requests.post(url, json=data)
    print(response.json())

if __name__ == "__main__":
    #testRequest({"register_user":{"user_name":"TestUser1", "pw":"defg", "role":"student"}})
    testRequest({"get_num_questions":{}})
    testRequest({"authenticate":{"user_name":"TestUser1", "pw":"defg"}})
    testRequest({"get_hint":{"module":"ac_power", "paper_no":1, "question_no":4, "hint_no":2, "user_name":"TestUser1"}})
    testRequest({"get_hint":{"module":"mech_vib", "paper_no":1, "question_no":4, "hint_no":2, "user_name":"TestUser1"}})
    testRequest({"user_seen_hint":{"module":"ac_power", "paper_no":1, "question_no":4, "hint_no":2, "user_name":"TestUser1"}})
    testRequest({"user_seen_hint":{"module":"ac_power", "paper_no":1, "question_no":4, "hint_no":1, "user_name":"TestUser1"}})