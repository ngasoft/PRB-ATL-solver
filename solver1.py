import copy

b = [2,2] # input bound
n = 5 # number of states

def cal_size(x):
    s = 1
    for i in x:
        s = s * (i + 1)
    return s

nb = cal_size(b)

X = []
Y = []

for i in range(nb):
    X += [[0.0] * n]
    Y += [[0.0] * n]

def copyXY():
    for i in range(nb):
        for j in range(n):
            Y[i][j] = X[i][j]

def oneStep():
    copyXY();
    delta = -1
    for i in range(nb):
        for j in range(n):
            assignXY(i, j)
            delta = max(abs(X[i][j] - Y[i][j]),delta)

    return delta

def assignXY(i,j):
    ax = single_to_multi(i)
    # state 0
    if j == 0:
        if ax[0]>=1:
            X[i][j] = max(min(X[m2s(ax)][4],X[m2s(ax)][1]), min(X[m2s([ax[0]-1,ax[1]])][1],X[m2s([ax[0]-1,ax[1]])][2]))
        else:
            X[i][j] = min(X[m2s(ax)][4], X[m2s(ax)][1])
    # state 1
    elif j == 1:
        if ax[0]>=1 and ax[1]>=1:
            X[i][j] = max(min(X[m2s(ax)][4], 0.2 * X[m2s(ax)][4] + 0.8 * X[m2s(ax)][3]),
                          min(0.2 * X[m2s([ax[0] - 1, ax[1] - 1])][4] + 0.8 * X[m2s([ax[0] - 1, ax[1] - 1])][3],
                              0.1 * X[m2s([ax[0] - 1, ax[1] - 1])][4] + 0.9 * X[m2s([ax[0] - 1, ax[1] - 1])][3]))
        else:
            X[i][j] = min(X[m2s(ax)][4],0.2*X[m2s(ax)][4]+0.8*X[m2s(ax)][3])
    # state 2
    elif j == 2:
        if ax[0] >= 1 and ax[1] >= 1:
            X[i][j] = max(min(X[m2s(ax)][4], 0.1 * X[m2s(ax)][4] + 0.9 * X[m2s(ax)][3]),
                          min(0.1 * X[m2s([ax[0] - 1, ax[1] - 1])][4] + 0.9 * X[m2s([ax[0] - 1, ax[1] - 1])][3],
                              0.01 * X[m2s([ax[0] - 1, ax[1] - 1])][4] + 0.99 * X[m2s([ax[0] - 1, ax[1] - 1])][3]))
        else:
            X[i][j] = min(X[m2s(ax)][4], 0.1 * X[m2s(ax)][4] + 0.9 * X[m2s(ax)][3])
    # state 3
    elif j == 3:
        X[i][j] = 1
    # state 4
    else:
        X[i][j] = X[i][j]

def single_to_multi(i):
    ax = copy.copy(b)
    ti = i
    for k in range(len(b)-1, -1, -1):
        ax[k] = ti // cal_size(b[:k])
        ti -= ax[k] * cal_size(b[:k])
    return ax

def m2s(x):
    return multi_to_single(x)

def multi_to_single(x):
    i = 0
    for k in range(len(b)-1, -1, -1):
        i += x[k] * cal_size(b[:k])
    return i

def next_bound(x):
    for i in range(len(x)):
        if x[i]>0:
            x[i] -= 1
            return x
        if x[i]==0:
            x[i] = b[i]
    return None

def iterate(epsilon):
    i = 0
    while True:
        delta = oneStep()
        i += 1
        print(i)
        if delta <= epsilon:
            break
    return X[nb-1][0]

print(iterate(0.00000000000000001))
            
