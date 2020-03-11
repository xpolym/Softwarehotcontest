import math
from multiprocessing import Pool
import datetime

def run(data, index, size):  # data 传入数据，index 数据分片索引，size进程数
    # print('data',data)
    # print(len(data)/size)
    # size = math.ceil(len(data) / size)
    # print('actual size ',size)
    # start = size * index
    # end = (index + 1) * size if (index + 1) * size < len(data) else len(data)
    tmpfeats=[]
    tmplabels=[]
    label_existed_flag = 1
    # lines = data[start:end]
    print('current id',index)

    for line in data:
        temp = []
        allInfo = line.strip().split(',')
        dims = len(allInfo)
        # print('current diminsions',dims)
        # if label_existed_flag == 1:
        for index in range(dims-1):
            temp.append(float(allInfo[index]))
        tmpfeats.append(temp)
        tmplabels.append(float(allInfo[dims-1]))
        # else:
        #     for index in range(dims):
        #         temp.append(float(allInfo[index]))
        #     tmplabels.append(temp)





    # start = 0
    # end=index
    # print('actual start  ',start,'actual  end  ',end)

    # do something
    return tmpfeats  # 可以返回数据，在后面收集起来

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

    processor = 4
    res = []
    p = Pool(processor)
    feats=[]
    labels=[]
    for i in range(processor):
        # p.close()
        # tmpf,tmpl=p.apply_async(run, args=(lines, i, processor,))
        res.append(p.apply_async(run, args=(lines, i, processor,)))
        # labels.append(tmpl)
        print(str(i) + ' processor started !')

    p.close()
    # p.join()
    # print(feats)
    #
    #
    # feats=[]
    # res[0].get()
    for i in res:
        feats.append(i.get())
        # print(i.get())  # 使用get获得多进程处理的结果
    #
    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)