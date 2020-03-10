import struct
import math

def float_to_hex(f):
    a = struct.pack('d',f)
    # print('a',a)
    return a
def hex_to_float(h):
    # i = int(h,16)
    print('hhh',h)
    return struct.unpack('d',h)[0]

data_float=33337.3
print('被转换浮点数为：',data_float)

hhh=float_to_hex(data_float)
print(hhh)  #0x43c80000
print(type(hhh))  #str


print(hex_to_float(hhh))




# def transfer(hexStr):  # 这个转换准确度好像还低一些
#     ret = str()
#     for x in range(0,len(hexStr),2):
#         a = hexStr[x:x+2]
#         intItem = int(a,16)
#         binnaryStr = bin(intItem)[2:len(bin(intItem))]
#         binnaryStr = "%(binnary)08d"%{'binnary':int(binnaryStr)}
#         ret = ret+binnaryStr
#     s= int(ret[0])
#     n = int(ret[1:9],2)
#     mStr = ret[9:len(ret)-1]
#     m = float()
#     print(mStr)
#     for x in range(1,len(mStr)-1,1):
#         if mStr[x-1] == "1":
#             print(x)
#             m=m+math.pow(0.5,x)

#     val = math.pow(-1,s)*(math.pow(2,n-127))*(1+m)
#     print(val)
#     return ret

# transfer(hhh[2:])