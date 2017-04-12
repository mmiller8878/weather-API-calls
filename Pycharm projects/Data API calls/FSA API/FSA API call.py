import requests

uri = "http://api.ratings.food.gov.uk/Help/Api/GET-Authorities/1"
r = requests.get(uri)
print(r.content)
#dataset.write(r.content)
