import requests

data = requests.get('http://127.0.0.1:8080').json()

all_v = []
top = 0
best = 0

for i, row in enumerate(data):
    c = len([n for n in row if 11 <= n <= 21])
    if c >= best:
        best = c
        top = i
    all_v += row

print(top)
print(*sorted(set([x for x in all_v if 11 <= x <= 21])))
print(max(all_v) - min(all_v))  