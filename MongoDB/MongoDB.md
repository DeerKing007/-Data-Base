# MongoDB

```python
安装MongoDB

# mac使用 brew 来安装 mongodb
brew install mongodb

# 安装最新开发版本：
brew install mongodb --devel

# MongoDB 的可执行文件位于 bin 目录下，所以可以将其添加到 PATH 路径中
export PATH=/usr/local/mongodb/bin:$PATH

# MongoDB的数据存储在data目录的db目录下，但是这个目录在安装过程不会自动创建，所以你需要手动创建data目录，并在data目录中创建db目录。
mkdir -p /data/db

# 在mongo安装目录中的bin目录执行mongod命令来启动mongdb服务（注意：如果你的数据库目录不是/data/db，可以通过 --dbpath 来指定）
sudo mongod --dbpath /data/db

# 启动 MongoDB
sudo mongod
# 如果没有创建全局路径 PATH，需要进入以下目录
cd /usr/local/mongodb/bin
sudo mongo

# 使用用户 admin 使用密码 123456 连接到本地的 MongoDB 服务上
 mongodb://admin:123456@localhost/

# 创建数据库（如果数据库不存在，则创建数据库，否则切换到指定数据库）
> use test
switched to db test

show dbs
查看所有的数据库

db.table（集合名）.insert({"key":"value"})
插入数据

db.table(集合名).find().pretty()
查看数据

use database（数据库名）
db.dropDatabase()
删除数据库（需先切换到想要删除的数据库再执行上面的命令）

use database（库名）
show tables
or
show collections
查看集合（表）

db.table（表名）.drop()
删除集合（mysql中的表，mongodb里叫集合）

db.createCollection(name, options)
创建集合
例：
db.createCollection('news', { capped : true, autoIndexId : true, size : 
 6142800, max : 10000 })
创建了一个名为news的集合整个集合空间大小 6142800 KB, 文档最大个数为 10000 个

参数：
capped(布尔):（可选）如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。当该值为 true 时，必须指定 size 参数。

autoIndexId（布尔）:（可选）如为 true，自动在 _id 字段创建索引。默认为 false。

size（数值）:（可选）为固定集合指定一个最大值（以字节计）。如果 capped 为 true，也需要指定该字段。

max（数值）:（可选）指定固定集合中包含文档的最大数量。

```



# python操作mongodb

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

# 连接mongodb
conn = MongoClient('192.168.0.113', 27017)
db = conn.mydb  #连接mydb数据库，没有则自动创建
my_set = db.test_set　　#使用test_set集合，没有则自动创建


# 插入数据（insert插入一个列表多条数据不用遍历，效率高， save需要遍历列表，一个个插入）
my_set.insert({"name":"zhangsan","age":18})
# 或
my_set.save({"name":"zhangsan","age":18})

# 插入多条
# 添加多条数据到集合中
users=[{"name":"zhangsan","age":18},{"name":"lisi","age":20}]  
my_set.insert(users) 
# 或
my_set.save(users) 


# 查询数据（查询不到则返回None）
# 查询全部
for i in my_set.find():
    print(i)
# 查询name=zhangsan的
for i in my_set.find({"name":"zhangsan"}):
    print(i)
print(my_set.find_one({"name":"zhangsan"}))


# 更新数据
my_set.update(
   <query>,    #查询条件
   <update>,    #update的对象和一些更新的操作符
   {
     upsert: <boolean>,    #如果不存在update的记录，是否插入
     multi: <boolean>,        #可选，mongodb 默认是false,只更新找到的第一条记录
     writeConcern: <document>    #可选，抛出异常的级别。
   }
)
#　　把上面插入的数据内的age改为20
my_set.update({"name":"zhangsan"},{'$set':{"age":20}})


# 删除数据
my_set.remove(
   <query>,    #（可选）删除的文档的条件
   {
     justOne: <boolean>,    #（可选）如果设为 true 或 1，则只删除一个文档
     writeConcern: <document>    #（可选）抛出异常的级别
   }
)

#删除name=lisi的全部记录
my_set.remove({'name': 'zhangsan'})

#删除name=lisi的某个id的记录
id = my_set.find_one({"name":"zhangsan"})["_id"]
my_set.remove(id)

#删除集合里的所有记录
db.users.remove()


# mongodb的条件操作符
#    (>)  大于 - $gt
#    (<)  小于 - $lt
#    (>=)  大于等于 - $gte
#    (<= )  小于等于 - $lte
#例：查询集合中age大于25的所有记录
for i in my_set.find({"age":{"$gt":25}}):
    print(i)

    
# type(判断类型)
# 找出name的类型是String的
for i in my_set.find({'name':{'$type':2}}):
    print(i)
    
    
# 排序
# 　　在MongoDB中使用sort()方法对数据进行排序，sort()方法可以通过参数指定排序的字段，并使用 1 和 -1 来指定排序的方式，其中 1 为升序，-1为降序。
for i in my_set.find().sort([("age",1)]):
    print(i)

    
# limit和skip
# limit()方法用来读取指定数量的数据
# skip()方法用来跳过指定数量的数据
# 下面表示跳过两条数据后读取6条
for i in my_set.find().skip(2).limit(6):
    print(i)

    
# IN
#找出age是20、30、35的数据
for i in my_set.find({"age":{"$in":(20,30,35)}}):
    print(i)

    
# OR
#找出age是20或35的记录
for i in my_set.find({"$or":[{"age":20},{"age":35}]}):
    print(i)

    
# all
'''
dic = {"name":"lisi","age":18,"li":[1,2,3]}
dic2 = {"name":"zhangsan","age":18,"li":[1,2,3,4,5,6]}

my_set.insert(dic)
my_set.insert(dic2)
'''
for i in my_set.find({'li':{'$all':[1,2,3,4]}}):
    print(i)
    

#查看是否包含全部条件
#输出：{'_id': ObjectId('58c503b94fc9d44624f7b108'), 'name': 'zhangsan', 'age': 18, 'li': [1, 2, 3, 4, 5, 6]}

# push/pushAll
my_set.update({'name':"lisi"}, {'$push':{'li':4}})
for i in my_set.find({'name':"lisi"}):
    print(i)
# 输出：{'li': [1, 2, 3, 4], '_id': ObjectId('58c50d784fc9d44ad8f2e803'), 'age': 18, 'name': 'lisi'}

my_set.update({'name':"lisi"}, {'$pushAll':{'li':[4,5]}})
for i in my_set.find({'name':"lisi"}):
    print(i)
# 输出：{'li': [1, 2, 3, 4, 4, 5], 'name': 'lisi', 'age': 18, '_id': ObjectId('58c50d784fc9d44ad8f2e803')}


# pop/pull/pullAll
#pop
#移除最后一个元素(-1为移除第一个)
my_set.update({'name':"lisi"}, {'$pop':{'li':1}})
for i in my_set.find({'name':"lisi"}):
    print(i)
#输出：{'_id': ObjectId('58c50d784fc9d44ad8f2e803'), 'age': 18, 'name': 'lisi', 'li': [1, 2, 3, 4, 4]}


#pull （按值移除）
# 移除3
my_set.update({'name':"lisi"}, {'$pop':{'li':3}})

# pullAll （移除全部符合条件的）
my_set.update({'name':"lisi"}, {'$pullAll':{'li':[1,2,3]}})
for i in my_set.find({'name':"lisi"}):
    print(i)
#输出：{'name': 'lisi', '_id': ObjectId('58c50d784fc9d44ad8f2e803'), 'li': [4, 4], 'age': 18}


# 多级路径元素操作
dic = {"name":"zhangsan",
       "age":18,
       "contact" : {
           "email" : "1234567@qq.com",
           "iphone" : "11223344"}
       }
my_set.insert(dic)


#多级目录用. 连接
for i in my_set.find({"contact.iphone":"11223344"}):
    print(i)
#输出：{'name': 'zhangsan', '_id': ObjectId('58c4f99c4fc9d42e0022c3b6'), 'age': 18, 'contact': {'email': '1234567@qq.com', 'iphone': '11223344'}}

result = my_set.find_one({"contact.iphone":"11223344"})
print(result["contact"]["email"])
#输出：1234567@qq.com
 
  
#多级路径下修改操作
result = my_set.update({"contact.iphone":"11223344"},{"$set":{"contact.email":"9999999@qq.com"}})
result1 = my_set.find_one({"contact.iphone":"11223344"})
print(result1["contact"]["email"])
#输出：9999999@qq.com


# 还可以对数组用索引操作
dic = {"name":"lisi",
       "age":18,
       "contact" : [
           {
           "email" : "111111@qq.com",
           "iphone" : "111"},
           {
           "email" : "222222@qq.com",
           "iphone" : "222"}
       ]}
my_set.insert(dic)

#查询
result1 = my_set.find_one({"contact.1.iphone":"222"})
print(result1)
#输出：{'age': 18, '_id': ObjectId('58c4ff574fc9d43844423db2'), 'name': 'lisi', 'contact': [{'iphone': '111', 'email': '111111@qq.com'}, {'iphone': '222', 'email': '222222@qq.com'}]}


#修改
result = my_set.update({"contact.1.iphone":"222"},{"$set":{"contact.1.email":"222222@qq.com"}})
print(result1["contact"][1]["email"])
#输出：222222@qq.com

```

## 实例

```python
import pymongo

def initDB(usname_usid):
 	conn=pymongo.MongoClient(host='118.25.52.106',port=27027,username='admin',password='appisbest',authMechanism='SCRAM-SHA-1')
    db = conn.jinritoutiao #指定数据库
    guanzhu = db.guanzhu  #指定表
    guanzhu.insert(usname_usid) #保存
    
    
# 链接马甲号的数据库 mongodb
def majiaDB():
    listuser=[]
    conn = pymongo.MongoClient(host='118.25.52.106',port=27027,username='admin',password='appisbest',authMechanism='SCRAM-SHA-1')
    db = conn.jinritoutiao #指定数据库
    majia = db.majia  #指定表
    ass = majia.find()
    for i in ass:
        username = i["accounts"]
        password=i["password"]
        listuser.append(username)
        listuser.append(password)
    return listuser
```

## Django 读取 Mongodb 数据：

#### 安装包
```
pip3 install mongoengine
```

#### 配置 settings
```
DATABASES = {
    'default': {
        'ENGINE': None,
    }
}
# 连接mongodb数据库
from mongoengine import connect
connect('database name',
        host='127.0.0.1',
        port=27017
        # username='',
        # password=''
        )
```

#### 在models.py里创建模型类
```
from mongoengine import *

class NewsModel(Document):
	# 定义数据库中的所有字段
 	title = StringField()
	details = StringField()
 	like = StringField()
	comment = StringField()

	# 指明连接的数据表名
	meta = {'collection': 'table name'}
```


#### 在views.py里实现增删改查
```
from django.shortcuts import render

# Create your views here.

from .models import NewsModel

class CreateView():
 def __init__:
     pass

	# 增
	def post(self, request):
    	title = request.data.get('title', None)
    	details = request.data.get('details', None)
   	 like = request.data.get('like', None)
    	comment = request.data.get('comment', None)

    	result = NewsModel(title=title, details=details, like=like, comment=comment)
    	result.save()
    	return Response({'msg: ok'})

	# 查
	def get(self, request):

    	id = request.GET.get('id', None)

    	result = NewsModel.objects.filter(id=id).all()

    	serializer = self.get_serializer(result, many=True)

    	return Response(data=serializer.data)

	# 改
	def put(self, request):

   	 	id = request.data.get('id', None)

    	details = request.data.get('details', None)

    	NewsModel.objects.filter(id=id).update(details=details)
    
    return Response({'msg': 'ok'})

	# 删
 	def delete(self, request):

    	id = request.GET.get('id', None)

    	NewsModel.objects.filter(id=id).delete()

    	return Response({'msg': 'ok'})
```










