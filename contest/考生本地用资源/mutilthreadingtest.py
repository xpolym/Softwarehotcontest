import math
from multiprocessing import Pool
import threading
import datetime


dataaaa=[]
def run(data,start):


    # return_dict.append(start)
    tmpfeats = []
    tmplabels=[]
    # print('id  ',i,'start   ',start,'end  ',end)
    label_existed_flag = 1
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
            tmplabels.append(temp)

        # return_labels[start+index]=tmplabels
        # return_feats[start+index]=tmpfeats
    # for i in range(1000000000):
    #     a =  23* 23

    # if i ==1 :
    #     time.sleep(10)
    print('this is done',start)


    return tmpfeats,tmplabels
    #
    #

def test():

    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)

    file_name = "./data/train_data.txt"
    # file_name = "123.txt"
    fr = open(file_name)
    lines = fr.readlines()
    lines = lines
    print('linessss', len(lines))

    n = len(lines)

    processor = 4
    res = []
    p = Pool(processor)


    feats=[]
    labels=[]
    n = len(lines)
    size = int(n / processor)

    from  multiprocessing import  Process,Manager
    manager = Manager()

    return_feats = manager.dict()
    return_labels=manager.dict()
    print('actual size ',size)

    getjoin=[]
    for i in range(processor):

        start = size * i
        end = (i + 1) * size if (i + 1) * size < n else n
        # p.close()
        # tmpf,tmpl=p.apply_async(run, args=(lines, i, processor,))
        res.append(p.apply_async(run, args=(lines[start:end], start)))
        # labels.append(tmpl)

        #process part
        # p = Process(target=run, args=(lines[start:end],start,return_feats,return_labels))
        # p.start()
        # getjoin.append(p)

        print(str(i) + ' processor started !')
    p.close()


    # p.join()
    feats=[]
    labels=[]
    for i in res:
        # feats.append(i.get())
        a,b = i.get()
        feats.extend(a)
        labels.extend(b)
    import numpy as np

    feats= np.array(feats)
    labels=np.array(labels)
    print('featssss:',feats.shape)  # 使用get获得多进程处理的结果
    print('labelsss:',labels.shape)



    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)

    # import numpy as np
    # # print('return dict',return_dict)
    # a=np.array(return_feats.values())
    # b=np.array(return_labels.values())
    # print('a',a.shape)
    # print('b',b.shape)


    # p.join()
    # print(feats)
    #
    #
    # feats=[]
    # res[0].get()
    # for i in res:
    #     feats.append(i.get())
    # print(i.get())  # 使用get获得多进程处理的结果
    #



if __name__ =='__main__':

    test()