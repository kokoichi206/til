import numpy as np
import matplotlib.pyplot as plt


def sigmoid(a):
    return 1 / (1 + np.exp(-a))

# forward propagation
def forward(X, W1, b1, W2, b2):
    Z = sigmoid(X.dot(W1) + b1)
    A = Z.dot(W2) + b2
    # softmax fun
    expA = np.exp(A)
    Y = expA / expA.sum(axis=1, keepdims=True)
    return Y, Z

def classification_rate(Y, P):
    n_correct = 0
    n_total = 0
    for i in range(len(Y)):
        n_total += 1
        if Y[i] == P[i]:
            n_correct += 1
    return float(n_correct) / n_total

def derivative_w2(Z, T, Y):
    N, K = T.shape
    M = Z.shape[1]

    # slow
    # ret1 = np.zeros((M, K))
    # for n in range(N):
    #     for m in range(M):
    #         for k in range(K):
    #             ret1[m,k] += (T[n,k] - Y[n,k])*Z[n,m]
    # ret2 = np.zeros((M,K))
    # for n in range(N):
    #     for k in range(K):
    #         ret2[:,k] += (T[n,k] - Y[n,k])*Z[n,:]
    # assert(np.abs(ret1 - ret2).sum() < 10e-10)

    # ret3 = np.zeros((M, K))
    # for n in range(N):
    #     ret3 += np.outer(Z[n], T[n] - Y[n])

    # ret4 = Z.T.dot(T - Y)
    return Z.T.dot(T - Y)

def derivative_b2(T, Y):
    return (T - Y).sum(axis=0)

def derivative_w1(X, Z, T, Y, W2):
    N, D = X.shape
    M, K = W2.shape

    # # slow
    # ret1 = np.zeros((D, M))
    # for n in range(N):
    #     for k in range(K):
    #         for m in range(M):
    #             for d in range(D):
    #                 ret1[d,m] += (T[n,k] - Y[n,k])*W2[m,k]*Z[n,m]*(1 - Z[n,m])*X[n,d]
    # return ret1
    dZ = (T - Y).dot(W2.T) * Z * (1 - Z)
    return X.T.dot(dZ)

def derivative_b1(T, Y, W2, Z):
    return ((T - Y).dot(W2.T) * Z * (1 - Z)).sum(axis=0)

def cost(T, Y):
    tot = T * np.log(Y)
    return tot.sum()

def main():
    # create the data
    Nclass = 500

    D = 2
    M = 3   # hidden layer size
    K = 3   # number of classes

    X1 = np.random.randn(Nclass, D) + np.array([0, -2])
    X2 = np.random.randn(Nclass, D) + np.array([2, 2])
    X3 = np.random.randn(Nclass, D) + np.array([-2, 2])
    X = np.vstack([X1, X2, X3])

    Y = np.array([0]*Nclass + [1]*Nclass + [2]*Nclass)
    N = len(Y)

    T = np.zeros((N, K))
    for i in range(N):
        T[i, Y[i]] = 1

    # plt.scatter(X[:, 0], X[:, 1], c=Y, s=100, alpha=0.5)
    # plt.show()

    # initialize parameters
    W1 = np.random.randn(D, M)
    b1 = np.random.randn(M)
    W2 = np.random.randn(M, K)
    b2 = np.random.randn(K)

    learning_rate = 10e-7
    costs = []
    print("start")
    for epoch in range(100000):
        output, hidden = forward(X, W1, b1, W2, b2)
        if epoch % 100 == 0:
            c = cost(T, output)
            P = np.argmax(output, axis=1)
            r = classification_rate(Y, P)
            print("cost: ", c, "classification_rate: ", r)
            costs.append(c)

        W2 += learning_rate * derivative_w2(hidden, T, output)
        b2 += learning_rate * derivative_b2(T, output)
        W1 += learning_rate * derivative_w1(X, hidden, T, output, W2)
        b1 += learning_rate * derivative_b1(T, output, W2, hidden)

    plt.plot(costs)
    plt.show()


if __name__ == "__main__":
    main()
