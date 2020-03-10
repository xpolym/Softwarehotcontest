# BFGS算法实现
# 通过Armijo Rule确定迭代步长

import numpy
from matplotlib import pyplot as plt


# 目标函数0阶信息
def func(x1, x2):
    funcVal = 5 * x1 ** 2 + 2 * x2 ** 2 + 3 * x1 - 10 * x2 + 4
    return funcVal


# 目标函数1阶信息
def grad(x1, x2):
    gradVal = numpy.array([[10 * x1 + 3], [4 * x2 - 10]])
    return gradVal


class BFGS(object):

    def __init__(self, seed=None, epsilon=1.e-6, maxIter=300):
        self.__seed = seed  # 迭代起点
        self.__epsilon = epsilon  # 计算精度
        self.__maxIter = maxIter  # 最大迭代次数

        self.__xPath = list()  # 记录优化变量之路径
        self.__fPath = list()  # 记录目标函数值之路径

    def solve(self):
        self.__init_path()

        xCurr = self.__init_seed(self.__seed)
        fCurr = func(xCurr[0, 0], xCurr[1, 0])
        gCurr = grad(xCurr[0, 0], xCurr[1, 0])
        DCurr = self.__init_D(xCurr.shape[0])  # 矩阵D初始化 ~ 此处采用单位矩阵
        self.__save_path(xCurr, fCurr)

        for i in range(self.__maxIter):
            if self.__is_converged(gCurr):
                self.__print_MSG()
                break

            dCurr = -numpy.matmul(DCurr, gCurr)
            alpha = self.__calc_alpha_by_ArmijoRule(xCurr, fCurr, gCurr, dCurr)

            xNext = xCurr + alpha * dCurr
            fNext = func(xNext[0, 0], xNext[1, 0])
            gNext = grad(xNext[0, 0], xNext[1, 0])
            DNext = self.__update_D_by_BFGS(xCurr, gCurr, xNext, gNext, DCurr)

            xCurr, fCurr, gCurr, DCurr = xNext, fNext, gNext, DNext
            self.__save_path(xCurr, fCurr)
        else:
            if self.__is_converged(gCurr):
                self.__print_MSG()
            else:
                print("BFGS not converged after {} steps!".format(self.__maxIter))

    def show(self):
        if not self.__xPath:
            self.solve()

        fig = plt.figure(figsize=(10, 4))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        ax1.plot(numpy.arange(len(self.__fPath)), self.__fPath, "k.")
        ax1.plot(0, self.__fPath[0], "go", label="starting point")
        ax1.plot(len(self.__fPath) - 1, self.__fPath[-1], "r*", label="solution")
        ax1.set(xlabel="$iterCnt$", ylabel="$iterVal$")
        ax1.legend()

        x1 = numpy.linspace(-100, 100, 500)
        x2 = numpy.linspace(-100, 100, 500)
        x1, x2 = numpy.meshgrid(x1, x2)
        f = func(x1, x2)
        ax2.contour(x1, x2, f, levels=36)
        x1Path = list(item[0] for item in self.__xPath)
        x2Path = list(item[1] for item in self.__xPath)
        ax2.plot(x1Path, x2Path, "k--", lw=2)
        ax2.plot(x1Path[0], x2Path[0], "go", label="starting point")
        ax2.plot(x1Path[-1], x2Path[-1], "r*", label="solution")
        ax2.set(xlabel="$x_1$", ylabel="$x_2$")
        ax2.legend()

        fig.tight_layout()
        fig.savefig("bfgs.png", dpi=300)
        plt.close()

    def __print_MSG(self):
        print("Iteration steps: {}".format(len(self.__xPath) - 1))
        print("Seed: {}".format(self.__xPath[0].reshape(-1)))
        print("Solution: {}".format(self.__xPath[-1].reshape(-1)))

    def __is_converged(self, gCurr):
        if numpy.linalg.norm(gCurr) <= self.__epsilon:
            return True
        return False

    def __update_D_by_BFGS(self, xCurr, gCurr, xNext, gNext, DCurr):
        sk = xNext - xCurr
        yk = gNext - gCurr
        rk = 1 / numpy.matmul(yk.T, sk)[0, 0]

        term1 = rk * numpy.matmul(sk, yk.T)
        term2 = rk * numpy.matmul(yk, sk.T)
        I = numpy.identity(term1.shape[0])
        term3 = numpy.matmul(I - term1, DCurr)
        term4 = numpy.matmul(term3, I - term2)
        term5 = rk * numpy.matmul(sk, sk.T)

        Dk = term4 + term5
        return Dk

    def __calc_alpha_by_ArmijoRule(self, xCurr, fCurr, gCurr, dCurr, c=1.e-4, v=0.5):
        i = 0
        alpha = v ** i
        xNext = xCurr + alpha * dCurr
        fNext = func(xNext[0, 0], xNext[1, 0])

        while True:
            if fNext <= fCurr + c * alpha * numpy.matmul(dCurr.T, gCurr)[0, 0]: break
            i += 1
            alpha = v ** i
            xNext = xCurr + alpha * dCurr
            fNext = func(xNext[0, 0], xNext[1, 0])

        return alpha

    def __init_D(self, n):
        D = numpy.identity(n)
        return D

    def __init_seed(self, seed):
        if seed is None:
            seed = numpy.random.uniform(-100, 100, 2)

        seed = numpy.array(seed).reshape((2, 1))
        return seed

    def __init_path(self):
        self.__xPath.clear()
        self.__fPath.clear()

    def __save_path(self, xCurr, fCurr):
        self.__xPath.append(xCurr)
        self.__fPath.append(fCurr)


if __name__ == "__main__":
    obj = BFGS()
    obj.solve()
    obj.show()