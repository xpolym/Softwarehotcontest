#coding=utf-8
from multiprocessing import Process

def target_function(index,sublist):
    print(index,sublist)


if __name__=="__main__":
    TXT_FILE = "123.txt"
    n_processes = 2 #number of processes
    f = open(TXT_FILE,'r')
    image_list = f.readlines()
    f.close()
    n_total = len(image_list)
    processes=[]
    x=10
    for i in range(n_processes):
        processes.append(Process(target=target_function,args=(i,x)))

    for p in processes:
        p.start()
    # for p in processes:
    #     p.join() #join 的作用是用来阻塞主线程的使用方案