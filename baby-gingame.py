print("6자리 수입력")
i = input()
arr = []
for e in range(len(i)):
    arr += i[e]

samesamstack = 0
consamstack = 0

run = 0
triplet = 0

for index1, name1 in enumerate(arr):
    for index2, name2 in enumerate(arr):
        if name1 == name2:
            print("index",index1, index2)
            print("name",name1, name2)
            samesamstack = samesamstack+1
            if samesamstack == 3:
                samesamstack = 0
                triplet = triplet+1
        elif name1 != name2:
            print("ss")
print(arr)
print(run, triplet)
if triplet == 1 and run == 1:
    print("baby-gin")