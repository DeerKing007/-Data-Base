import MySQLdb
conn=MySQLdb.connect(
    host="localhost",       #主机IP
    port=3306,               #端口
    user="root",            #用户名
    password="123456",      # 密码
    db="lianxi",            #数据库名称
    charset="utf8"          #字符集
)
# 获取游标对象：增删改查
cursor=conn.cursor()
row_count=cursor.execute("select * from users where id>2")    #获取的是表中数据行数#
p=cursor.fetchone()
# p=cursor.fetchmany(2)
# p=cursor.fetchall()
# for i in p:
#     print(i)
print(p)
conn.commit()
cursor.close()
conn.close()


