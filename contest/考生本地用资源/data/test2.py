import multiprocessing
import os

def run_proc(name):
    print('Child process {0} {1} Running '.format(name, os.getpid()))
    for i in range(10000000000000000):
        a = 4 * 23

if __name__ == '__main__':
    print('Parent process {0} is Running'.format(os.getpid()))
    for i in range(2):
        p = multiprocessing.Process(target=run_proc, args=(str(i),))
        print('process start')
        p.start()
    p.join()
    print('Process close')