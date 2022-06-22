import numpy as np
import matplotlib.pyplot as plt
n = 1000
m = 80

start = 100
q = 10
rate = n/q

w = np.zeros([n,n])

xlist = []
for i in range(m):                
        all_1 = np.ones(n, dtype=np.int32)
        random_1 = -2*np.random.randint(0,2,n)
        x = all_1+random_1
        V_x = x.reshape([n, 1])
        H_x = x.reshape([1, n])
        xlist.append(H_x)
        w += np.dot(V_x, H_x)
w = w/m

for count in range(q-1):
    t = np.copy(xlist[0][0])
    m = np.copy(xlist[0][0])
    for i in range(int((count*rate)+start)):
        t[i] = -1*t[i]

    round = 0
    datalist = []

    while(1):
        #false_count = 0
        #for i in range(n):
        #    if t[i] != m[i]:
        #        false_count += 1
        #data = 1-(false_count/n)
        #datalist.append(data)

        datalist.append((np.dot(t,m))/n)

        t = np.copy(np.sign(np.dot(w,t)))

        if round == 20:
            break
        round += 1
    print(datalist)
    plt.plot(datalist,marker="o")

plt.ylim(-1,1)
plt.xlim(0,20)
plt.show()
