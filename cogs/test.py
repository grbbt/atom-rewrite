import json

Name = "name"
ID = "69420"
Region = "pooland"

p = {}

with open('varStorage.json', 'r') as v:
    p = json.load(v)


print(p)
p[Name].update({"id": ID, "region": Region})


with open('varStorage.json', 'w') as b:
    json.dump(p, b)

print(p)
print(p[Name]['id'])
