# # # _*_coding:utf-8_*_
# # import time, threading, ConfigParser
# #
# # '''
# # Reader类，继承threading.Thread
# # @__init__方法初始化
# # @run方法实现了读文件的操作
# # '''
# #
# #
# # class Reader(threading.Thread):
# #     def __init__(self, file_name, start_pos, end_pos):
# #         super(Reader, self).__init__()
# #         self.file_name = file_name
# #         self.start_pos = start_pos
# #         self.end_pos = end_pos
# #
# #     def run(self):
# #         fd = open(self.file_name, 'r')
# #         '''
# #         该if块主要判断分块后的文件块的首位置是不是行首，
# #         是行首的话，不做处理
# #         否则，将文件块的首位置定位到下一行的行首
# #         '''
# #         if self.start_pos != 0:
# #             fd.seek(self.start_pos - 1)
# #             if fd.read(1) != '\n':
# #                 line = fd.readline()
# #                 self.start_pos = fd.tell()
# #         fd.seek(self.start_pos)
# #         '''
# #         对该文件块进行处理
# #         '''
# #         while (self.start_pos <= self.end_pos):
# #             line = fd.readline()
# #             '''
# #             do somthing
# #             '''
# #             self.start_pos = fd.tell()
# #
# #
# # '''
# # 对文件进行分块，文件块的数量和线程数量一致
# # '''
# #
# #
# # class Partition(object):
# #     def __init__(self, file_name, thread_num):
# #         self.file_name = file_name
# #         self.block_num = thread_num
# #
# #     def part(self):
# #         fd = open(self.file_name, 'r')
# #         fd.seek(0, 2)
# #         pos_list = []
# #         file_size = fd.tell()
# #         block_size = file_size / self.block_num
# #         start_pos = 0
# #         for i in range(self.block_num):
# #             if i == self.block_num - 1:
# #                 end_pos = file_size - 1
# #                 pos_list.append((start_pos, end_pos))
# #                 break
# #             end_pos = start_pos + block_size - 1
# #             if end_pos >= file_size:
# #                 end_pos = file_size - 1
# #             if start_pos >= file_size:
# #                 break
# #             pos_list.append((start_pos, end_pos))
# #             start_pos = end_pos + 1
# #         fd.close()
# #         return pos_list
# #
# #
# # if __name__ == '__main__':
# #     '''
# #     读取配置文件
# #     '''
# #     config = ConfigParser.ConfigParser()
# #     config.readfp(open('conf.ini'))
# #     # 文件名
# #     file_name = config.get('info', 'fileName')
# #     # 线程数量
# #     thread_num = int(config.get('info', 'threadNum'))
# #     # 起始时间
# #     start_time = time.clock()
# #     p = Partition(file_name, thread_num)
# #     t = []
# #     pos = p.part()
# #     # 生成线程
# #     for i in range(thread_num):
# #         t.append(Reader(file_name, *pos[i]))
# #     # 开启线程
# #     for i in range(thread_num):
# #         t[i].start()
# #     for i in range(thread_num):
# #         t[i].join()
# #     # 结束时间
# #     end_time = time.clock()
# #     print
# #     "Cost time is %f" % (end_time - start_time)
# #
# #
#
# # -*- coding: GBK -*-
# import urlparse
# import datetime
# import os
# from multiprocessing import Process,Queue,Array,RLock
# """
# 多进程分块读取文件
# """
# WORKERS = 4
# BLOCKSIZE = 100000000
# FILE_SIZE = 0
# def getFilesize(file):
#   """
#     获取要读取文件的大小
#   """
#   global FILE_SIZE
#   fstream = open(file,'r')
#   fstream.seek(0,os.SEEK_END)
#   FILE_SIZE = fstream.tell()
#   fstream.close()
# def process_found(pid,array,file,rlock):
#   global FILE_SIZE
#   global JOB
#   global PREFIX
#   """
#     进程处理
#     Args:
#       pid:进程编号
#       array:进程间共享队列，用于标记各进程所读的文件块结束位置
#       file:所读文件名称
#     各个进程先从array中获取当前最大的值为起始位置startpossition
#     结束的位置endpossition (startpossition+BLOCKSIZE) if (startpossition+BLOCKSIZE)<FILE_SIZE else FILE_SIZE
#     if startpossition==FILE_SIZE则进程结束
#     if startpossition==0则从0开始读取
#     if startpossition!=0为防止行被block截断的情况，先读一行不处理，从下一行开始正式处理
#     if 当前位置 <=endpossition 就readline
#     否则越过边界，就从新查找array中的最大值
#   """
#   fstream = open(file,'r')
#   while True:
#     rlock.acquire()
#     print 'pid%s'%pid,','.join([str(v) for v in array])
#     startpossition = max(array)
#     endpossition = array[pid] = (startpossition+BLOCKSIZE) if (startpossition+BLOCKSIZE)<FILE_SIZE else FILE_SIZE
#     rlock.release()
#     if startpossition == FILE_SIZE:#end of the file
#       print 'pid%s end'%(pid)
#       break
#     elif startpossition !=0:
#       fstream.seek(startpossition)
#       fstream.readline()
#     pos = ss = fstream.tell()
#     ostream = open('/data/download/tmp_pid'+str(pid)+'_jobs'+str(endpossition),'w')
#     while pos<endpossition:
#       #处理line
#       line = fstream.readline()
#       ostream.write(line)
#       pos = fstream.tell()
#     print 'pid:%s,startposition:%s,endposition:%s,pos:%s'%(pid,ss,pos,pos)
#     ostream.flush()
#     ostream.close()
#     ee = fstream.tell()
#   fstream.close()
# def main():
#   global FILE_SIZE
#   print datetime.datetime.now().strftime("%Y/%d/%m %H:%M:%S")
#   file = "/data/pds/download/scmcc_log/tmp_format_2011004.log"
#   getFilesize(file)
#   print FILE_SIZE
#   rlock = RLock()
#   array = Array('l',WORKERS,lock=rlock)
#   threads=[]
#   for i in range(WORKERS):
#     p=Process(target=process_found, args=[i,array,file,rlock])
#     threads.append(p)
#   for i in range(WORKERS):
#     threads[i].start()
#   for i in range(WORKERS):
#     threads[i].join()
#   print datetime.datetime.now().strftime("%Y/%d/%m %H:%M:%S")
# if __name__ == '__main__':
#   main()
#
#

# from multiprocessing import Pool
# import time
#
#
# def mycallback(x):
#     with open('123.txt', 'a+') as f:
#         for i in range(1000000):
#             f.writelines(str(x))
#
#
# def sayHi(num):
#     return num
#
#
# if __name__ == '__main__':
#     e1 = time.time()
#     pool = Pool()
#
#     for i in range(10):
#         pool.apply_async(sayHi, (i,), callback=mycallback)
#
#     pool.close()
#     pool.join()
#     e2 = time.time()
#     print(float(e2 - e1))

from multiprocessing import Process, Manager
import  time

# 每个子进程执行的函数
# 参数中，传递了一个用于多进程之间数据共享的特殊字典
def func(data,i, size):


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

    #
    #
    # d[i] = i + 100
    # print(d.values())
if __name__ == '__main__':
    # 在主进程中创建特殊字典
    m = Manager()
    d = m.dict()

    file_name = "./data/train_data.txt"
    # file_name = "123.txt"
    fr = open(file_name)
    lines = fr.readlines()
    n=len(lines)
    print('linessss', len(lines))
    import  datetime
    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S.%f'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)
    procesors=4
    for i in range(procesors):
        # 让子进程去修改主进程的特殊字典
        p = Process(target=func, args=(lines,i, procesors))
        p.start()
        print('this is in main')
    p.join()

    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    print(theTime)