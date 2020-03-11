import math
from multiprocessing import Pool
import threading
import datetime

def run(data,i, size):


    size = int(len(data) / size)
    print('actual size ',size)
    start = size * i
    end = (i + 1) * size if (i + 1) * size < len(data) else len(data)

    tmpfeats = []
    tmplabels=[]
    print('id  ',i,'start   ',start,'end  ',end)
    label_existed_flag = 1
    for line in data[start:end]:
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
    # for i in range(1000000000):
    #     a =  23* 23

    # if i ==1 :
    #     time.sleep(10)
    print('this is done',i)

    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)

    #
    #

if __name__ =='__main__':

    #
    # for i in range(1000000000):
    #     a = 12+ 12

    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)

    file_name = "./data/train_data.txt"
    # file_name = "123.txt"
    fr = open(file_name)
    lines = fr.readlines()
    print('linessss', len(lines))

    n = len(lines)

    processor = 2
    res = []
    # p = Pool(processor)
    feats=[]
    labels=[]

    for i in range(processor):
        # p.close()
        # tmpf,tmpl=p.apply_async(run, args=(lines, i, processor,))
        # res.append(p.apply_async(run, args=(lines, i, processor,)))
        # labels.append(tmpl)

        p = threading.Thread(target=run, args=(lines, i, processor))
        p.start()

        print(str(i) + ' processor started !')

    # p.close()
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

