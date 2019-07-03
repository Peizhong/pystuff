def test1():
    for i in range(1,169):
        for j in range(1,169):
            if (i+j) * (i-j) == 168:
                # print(i,j)
                x = j**2-100
                if x>0:
                    print(x)

def test2():
    l = []
    for i in range(101,201):
        for j in range(2,i):
            if i%j == 0:
                l.append(i)
                break
    lst = [item for item in range(101,201) if item not in l]
    print(lst)

def test3():
    for i in range(0,10):
        for j in range(0,10):
            for k in range(0,10):
                if i**3 + j**3 + k**3 == 100*i+10*j+k:
                    print("%d%d%d" % (i,j,k))

def func(n):
    if n==10:
        return 1
    else:
        return 2*(func(n+1)+1)

def test4():
    v = func(1)
    # print(v)

test4()