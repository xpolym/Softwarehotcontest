from multiprocessing import Process
import time





# readseek(10)
if __name__ == "__main__":
    with open('train_data.txt', 'r') as f:
        def readseek(num):
            f.seek(num)
            print(time.time(), f.read(10))
            time.sleep(10)
        p1 = Process(target = readseek, args = (20,))
        # p2 = Process(target = readseek, args = (60,))
        # p3 = Process(target = readseek, args = (120,))
        # p4 = Process(target = readseek, args = (160,))
        p1.start()
        # p2.start()
        # p3.start()
        # p4.start()
        # p1.join()
        # p2.join()
        # p3.join()
        # p4.join()
        print(time.time())