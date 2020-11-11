#coding=utf-8
import requests, csv, pymysql

def output_databases():
    conn = pymysql.connect(host='localhost', user='pyconn', password='123456',database='carlmax', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from answers;"
    cursor.execute(sql)
    data = cursor.fetchall()
    fp = open('./answer.csv', 'w')
    wt = csv.writer(fp)
    for i in data:
        tmp = [i['questionid'], i['questiondetail'].encode('utf-8'), i['answer'].encode('utf-8')]
        wt.writerow(tmp)
    fp.close()

if __name__ == '__main__':
    '''
    print "1. 导出数据库为 csv 文件"
    print "2. 爬取本次考试的答案"
    print "请输入选项: "
    inp = input()
    if inp == 1:
    '''
    output_databases()