f = open('./projects/student/result.txt')
lines = f.readlines()
count = 0
rightcase = 0
print('we are getting here')
# lines = f.readlines()
for line in lines:
    print('line', line)
    print('lineee',len(line))
    print('leixing', type(line))
    count = count + 1

    if line[0] == str(1):
        rightcase = rightcase + 1

f.close()
print('right case', rightcase, '   count', count)
print('实际的准确率', rightcase / count)