from qdls.data import load_json, save_json

data = load_json("/home/qing/raid/paperwork/kgtool/data/kqa/full/train.json")

L = [ len(s['program']) for s in data ]
m = max(L)
print(m)
for s in data:
    l = len(s['program'])
    if l == m :
        # print(s )
        save_json(s, "./longest.json")
        break 

# from collections import Counter

# c = Counter(L)