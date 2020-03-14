import math
import datetime
import matplotlib.pyplot as plt
import sys
import numpy as np
from  multiprocessing import  Process,Pool



class LR:
    def __init__(self, train_file_name, test_file_name, predict_result_file_name):
        self.train_file = train_file_name
        self.predict_file = test_file_name
        self.predict_result_file = predict_result_file_name
        self.max_iters = 50
        self.rate = 0.01
        self.lam = 0.03
        self.feats = []
        self.labels = []
        self.feats_test = []
        self.labels_predict = []
        self.param_num = 0
        self.weight = []

    def processdata(self,data,start,label_existed_flag):



        # return_dict.append(start)
        tmpfeats = []
        tmplabels=[]
        # print('id  ',i,'start   ',start,'end  ',end)
        # label_existed_flag = 1
        index=0
        for line in data:
            temp = []
            allInfo = line.strip().split(',')
            dims = len(allInfo)
            # print('current diminsions',dims)
            if label_existed_flag == 1:
                for index in range(dims-1):
                    temp.append(float(allInfo[index]))
                tmpfeats.append(temp)
                tmplabels.append(float(allInfo[dims-1]))
            else:
                for index in range(dims):
                    temp.append(float(allInfo[index]))
                tmpfeats.append(temp)

            # return_labels[start+index]=tmplabels
            # return_feats[start+index]=tmpfeats
        # for i in range(1000000000):
        #     a =  23* 23

        # if i ==1 :
        #     time.sleep(10)
        # print('this is done',start)


        return tmpfeats,tmplabels

    def loadDataSet(self, file_name, label_existed_flag):
        print('read data time')
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        print(theTime)

        fr = open(file_name)
        lines = fr.readlines()
        print('linessss',len(lines))


        processor = 1
        n = len(lines)
        size = int(n / processor)

        p = Pool(processor)

        getjoin=[]
        res = []
        for i in range(processor):

            start = size * i
            end = (i + 1) * size if (i + 1) * size < n else n
            # p.close()
            # tmpf,tmpl=p.apply_async(run, args=(lines, i, processor,))
            res.append(p.apply_async(self.processdata, args=(lines[start:end], start,label_existed_flag)))
            # labels.append(tmpl)

            #process part
            # p = Process(target=run, args=(lines[start:end],start,return_feats,return_labels))
            # p.start()
            # getjoin.append(p)

            # print(str(i) + ' processor started !')
        p.close()



        feats=[]
        labels=[]

        for i in res:
            # feats.append(i.get())
            a,b = i.get()
            feats.extend(a)
            labels.extend(b)

        feats= np.array(feats)
        labels=np.array(labels)


        fr.close()
        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        print(theTime)
        print('---leixing',feats.shape)
        print('---leixing',labels.shape)
        return feats,labels

    def loadDataSetold(self,file_name,label_existed_flag):
        print("The time cosr")
        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        print(theTime)
        feats = []
        labels = []
        fr = open(file_name)
        lines = fr.readlines()
        for line in lines:
            temp = []
            allInfo = line.strip().split(',')
            dims = len(allInfo)
            if label_existed_flag == 1:
                for index in range(dims-1):
                    temp.append(float(allInfo[index]))
                feats.append(temp)
                labels.append(float(allInfo[dims-1]))
            else:
                for index in range(dims):
                    temp.append(float(allInfo[index]))
                feats.append(temp)
        fr.close()
        feats = np.array(feats)
        labels = np.array(labels)
        print('---leixing',feats.shape)
        print('---leixing',labels.shape)
        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        print(theTime)
        return feats, labels

    def loadTrainData(self):
        self.feats, self.labels = self.loadDataSetold(self.train_file, 1)

    def loadTestData(self):
        self.feats_test, self.labels_predict = self.loadDataSetold(
            self.predict_file, 0)

    def savePredictResult(self):
        print(self.labels_predict)
        f = open(self.predict_result_file, 'w')
        for i in range(len(self.labels_predict)):
            f.write(str(self.labels_predict[i])+"\n")
        f.close()
        print("we have save the result")
        # self.getpredictprecise()
    def getpredictprecise(self):
        f = open(self.predict_result_file)
        predictlines = f.readlines()
        h=open('./data/answer.txt')
        answerlines =h.readlines()
        count = 0
        rightcase=0
        print('we are getting here')

        n=len(predictlines)
        for i in range(n):
            # print('line',line)
            # print('leixing',type(line))
            count = count + 1

            if predictlines[i][0] == answerlines[i][0] :
                rightcase = rightcase + 1

        f.close()
        print('right case',rightcase, '   count',count)
        print('实际的准确率', rightcase / count)
    def sigmod(self, x):
        return 1/(1+np.exp(-x))

    def printInfo(self):
        print(self.train_file)
        print(self.predict_file)
        print(self.predict_result_file)
        print(self.feats)
        print(self.labels)
        print(self.feats_test)
        print(self.labels_predict)

    def initParams(self):
        self.weight = np.ones((self.param_num,), dtype=np.float)
        # self.weight=[]
        # print('selfweight',self.weight)

    def compute(self, recNum, param_num, feats, w):
        return self.sigmod(np.dot(feats, w))

    def error_rate(self, recNum, label, preval):
        return np.power(label - preval, 2).sum()

    def predict(self):
        self.loadTestData()
        print('预测的时候',self.feats_test.shape)
        print('weight--',self.weight.shape)
        preval = self.compute(len(self.feats_test),self.param_num, self.feats_test, self.weight)
        self.labels_predict = (preval+0.3).astype(np.int)
        self.savePredictResult()

    def train(self):
        self.loadTrainData()
        recNum = len(self.feats)
        print('rec num',recNum)
        #关于数据的说明
        # 1000 维 的数据，
        #总共有8000 个数据 每个数据1000维数 也就是 para_num


        self.param_num = len(self.feats[0])
        self.initParams()
        costs=[]
        iterations=[]
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
        for i in range(self.max_iters):
            preval = self.compute(recNum, self.param_num,
                                  self.feats, self.weight)
            #根据权重计算得到当前估计的数值
            #feats
            #
            #
            sum_err = self.error_rate(recNum, self.labels, preval)
            if i%30 == 0:
                print("Iters:" + str(i) + " error:" + str(sum_err))
                theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                print(theTime)
                print('50;;;;;', self.rate)
            #为了画图
            costs.append(sum_err)
            iterations.append(i)
            err = self.labels - preval
            # if i>=30:
            #     self.rate = 0.03
            # elif 30>i and \
            # if i>10:
            #     self.rate = 0.002
            # else:
            #     self.rate = 0.5*(0.97**i)

            delt_w = np.dot(self.feats.T, err)  #.T 表示的是转置的意思
            delt_w /= recNum
            self.weight = self.weight + self.rate*delt_w -self.weight*(1-self.rate*self.lam/recNum)

        # print('self.weigth',self.weight)
        plt.plot(iterations,costs)
        plt.show()

    def alphA(self,x, y, theta, pk,itertime):  # 选取前20次迭代cost最小的alpha
        c = float("inf")
        t = theta
        #theta  的默认的数值是1的列向量
        print('itertime:',itertime)
        if itertime==1:
            for k in range(1, 50):
                # a = (0.03/itertime**3) / k  #

                # if itertime==2:
                a = 1.2/k**2
                theta = t + a * pk  # 比重 传入的pk  是一次线性方程的解
                #t=theta ,对theta 进行更新 。  theta =  t + 学习率 * theta 把其
                f = np.sum(np.dot(x.T, self.sigmod(np.dot(x, theta)) - y))
                # print('f',f)
                if abs(f) > c:
                    print('last k',k)
                    break
                else:
                    c = abs(f)
                alpha = a
                # print('alpha变化', alpha)
        else:
            for k in range(1, 50):
                # a = (0.03/itertime**3) / k  #

                # if itertime==2:
                a = 1.2 / k ** 2
                theta = t + a * pk  # 比重 传入的pk  是一次线性方程的解
                # t=theta ,对theta 进行更新 。  theta =  t + 学习率 * theta 把其
                f = np.sum(np.dot(x.T, self.sigmod(np.dot(x, theta)) - y))
                # print('f', f)
                if abs(f) > c:
                    print('last k', k)
                    break
                else:
                    c = abs(f)
                alpha = a
                # print('alpha变化',alpha)
        return alpha
    def bfgstrain(self):
        self.loadTrainData()

        # print('feats',self.feats


        self.weight,costs=self.BFGS(self.feats,self.labels,self.max_iters)
        # self.weight = self.weight
        # self.weight = self.weight
        # print(self.weight.shape)
        # print('self')
        # a=self.weight.T
        # print(a.shape)
        # print('aaaa--',a[0])
        a=np.array(self.weight.reshape([-1]))
        # print('a',a)
        self.weight=a[0]
        # b = a[0]
        # print(self.weight)

        # print('weight---',self.weight)
    def BFGS(self,x, y, iter):  # BFGS拟牛顿法
        n = len(x[0])
        theta = np.ones((n, 1))
        # theta = np.ones((n,), dtype=np.float)
        # print('this theta',theta)
        y = np.mat(y).T
        Bk = np.eye(n, n)  # 生成对角单位矩阵
        grad_last = np.dot(x.T, self.sigmod(np.dot(x, theta)) - y)  # 逻辑回归模型的代价函数的求导，我们得到其导数的根，也就是最小点
        cost = []
        for it in range(iter):
            pk = -1 * np.linalg.solve(Bk, grad_last)  # 求解线性方程组

            rate = self.alphA(x, y, theta, pk,it+1)
            theta = theta + rate * pk
            grad = np.dot(x.T, self.sigmod(np.dot(x, theta)) - y)
            delta_k = rate * pk
            y_k = (grad - grad_last)
            Pk = y_k.dot(y_k.T) / (y_k.T.dot(delta_k))
            Qk = Bk.dot(delta_k).dot(delta_k.T).dot(Bk) / (delta_k.T.dot(Bk).dot(delta_k)) * (-1)
            Bk += Pk + Qk
            grad_last = grad
            cost.append(np.sum(grad_last))
        return theta, cost


def print_help_and_exit():
    print("usage:python3 main.py train_data.txt test_data.txt predict.txt [debug]")
    sys.exit(-1)


def parse_args():
    debug = True
    if len(sys.argv) == 2:
        if sys.argv[1] == 'debug':
            print("test mode")
            debug = True
        else:
            print_help_and_exit()
    return debug


if __name__ == "__main__":
    debug = parse_args()
    #Upload file path
    # train_file = "/data/train_data.txt"
    # test_file = "/data/test_data.txt"
    # predict_file = "/projects/student/result.txt"
    # local file path
    train_file = "./data/train_data.txt"
    test_file = "./data/test_data.txt"
    predict_file = "./projects/student/result.txt"
    #

    # f = open("../train_data.txt")
    # line = f.readline()
    # while line:
    #     print(line)
    #     line = f.readline()
    # f.close()


    #lr  logics regression
    # lr = LR(train_file, test_file, predict_file)
    # lr.train()
    # lr.predict()

    # lr bfgs
    lr = LR(train_file, test_file, predict_file)
    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)
    # lr.bfgstrain()
    lr.train()
    lr.predict()
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)
    # debug=False
    if debug:
        answer_file ="./projects/student/answer.txt"
        f_a = open(answer_file, 'r')
        f_p = open(predict_file, 'r')
        a = []
        p = []
        lines = f_a.readlines()
        for line in lines:
            a.append(int(float(line.strip())))
        f_a.close()

        lines = f_p.readlines()
        for line in lines:
            p.append(int(float(line.strip())))
        f_p.close()

        print("answer lines:%d" % (len(a)))
        print("predict lines:%d" % (len(p)))

        errline = 0
        for i in range(len(a)):
            if a[i] != p[i]:
                errline += 1

        accuracy = (len(a)-errline)/len(a)
        print("accuracy:%f" %(accuracy))