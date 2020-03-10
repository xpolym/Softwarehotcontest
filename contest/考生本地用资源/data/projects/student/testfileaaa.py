f = open('./result.txt')
line = f.readline()
count = 0
rightcase = 0
print('we are getting here')
print(line)
lines = f.readlines()
for line in lines:
    print(line)

f.close()
print('实际的准确率', rightcase / count)





