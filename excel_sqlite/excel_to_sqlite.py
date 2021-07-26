import sqlite3
import pandas as pd

conn = sqlite3.connect('D:\\listmap\\db.sqlite3')
co = conn.cursor()
f1 = pd.ExcelFile("C:\\Users\\wu411299174\\Desktop\\世界一流学科高校世界地图（B及以上学科）.xlsx")
f = f1.sheet_names
import time
def is_chinese(uchar):
    if uchar >= '\u4e00' and uchar <= '\u9fa5':
        return True
    else:
        return False
def reserve_chinese(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str += i
    return content_str
f0 = []
for i in f:
    f0.append(reserve_chinese(i))


fd = pd.read_excel("C:\\Users\\wu411299174\\Desktop\\世界一流学科高校世界地图（B及以上学科）.xlsx", sheet_name=3)
for i in range(0, fd.shape[0]):
    if isinstance(fd.values[i][1], str):
            co.execute("insert into country_firstcollege (college_name, college_nameE, cname, subject_name)\
                                        values (?, ?, ?, ?)",
                      (fd.values[i][1].strip(), " ", "中国", f0[3]))



    conn.commit()
conn.close()
