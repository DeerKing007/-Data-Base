# elasticsearch 模块

Elasticsearch低级客户端。提供从Python到ES REST端点的直接映射。

### 连接集群节点

```python
# 指定连接
es = Elasticsearch(
    ['172.16.153.129:9200'],
    # 认证信息
    # http_auth=('elastic', 'changeme')
)


# 动态连接
es = Elasticsearch(
    ['esnode1:port', 'esnode2:port'],
    # 在做任何操作之前，先进行嗅探
    sniff_on_start=True,
    # 节点没有响应时，进行刷新，重新连接
    sniff_on_connection_fail=True,
    # 每 60 秒刷新一次
    sniffer_timeout=60
)


# 对不同的节点，赋予不同的参数
es = Elasticsearch([
    {'host': 'localhost'},
    {'host': 'othernode', 'port': 443, 'url_prefix': 'es', 'use_ssl': True},
])


# 假如使用了 ssl
es = Elasticsearch(
    ['localhost:443', 'other_host:443'],
    # 打开SSL 
    use_ssl=True,
    # 确保我们验证了SSL证书（默认关闭）
    verify_certs=True,
    # 提供CA证书的路径
    ca_certs='/path/to/CA_certs',
    # PEM格式的SSL客户端证书
    client_cert='/path/to/clientcert.pem',
    # PEM格式的SSL客户端密钥
    client_key='/path/to/clientkey.pem'
)
```

### 获取相关信息

```python
# 测试集群是否启动
In [40]: es.ping()
Out[40]: True


# 获取集群基本信息
In [39]: es.info()
Out[39]:
  {'cluster_name': 'sharkyun',
   'cluster_uuid': 'rIt2U-unRuG0hJBt6BXxqw',
   'name': 'master',
   'tagline': 'You Know, for Search',
   'version': {'build_date': '2017-10-06T20:33:39.012Z',
               'build_hash': '1a2f265',
               'build_snapshot': False,
               'lucene_version': '6.6.1',
               'number': '5.6.3'}}


# 获取集群的健康状态信息
In [41]: es.cluster.health()
Out[41]:
  {'active_primary_shards': 6,
   'active_shards': 6,
   'active_shards_percent_as_number': 50.0,
   'cluster_name': 'sharkyun',
   'delayed_unassigned_shards': 0,
   'initializing_shards': 0,
   'number_of_data_nodes': 1,
   'number_of_in_flight_fetch': 0,
   'number_of_nodes': 1,
   'number_of_pending_tasks': 0,
   'relocating_shards': 0,
   'status': 'yellow',
   'task_max_waiting_in_queue_millis': 0,
   'timed_out': False,
   'unassigned_shards': 6}
 

# 获取当前连接的集群节点信息
In [43]: es.cluster.client.info()


# 获取集群目前所有的索引
In [55]: print(es.cat.indices())
yellow open logstash-2017.11.04 Zt2K7k0yRZaIwmEsZ9H3DA 5 1 301000 0 162.3mb 162.3mb
yellow open .kibana             1Epb3nPFRimFJoRwKHtXIg 1 1      2 0  13.4kb  13.4kb


# 获取集群的更多信息
es.cluster.stats()

# 利用实例的 cat 属性得到更简单易读的信息
In [85]: es.cat.health()
Out[85]: '1510431262 04:14:22 sharkyun yellow 1 1 6 6 0 0 6 0 - 50.0%\n'

In [86]: es.cat.master()
Out[86]: 'VXgFbKAaTtGO5a1QAfdcLw 172.16.153.129 172.16.153.129 master\n'

In [87]: es.cat.nodes()
Out[87]: '172.16.153.129 27 49 0 0.02 0.01 0.00 mdi * master\n'

In [88]: es.cat.indices()
Out[88]: 'yellow open logstash-2017.11.04 Zt2K7k0yRZaIwmEsZ9H3DA 5 1 301000 0 162.3mb 162.3mb\nyellow open .kibana             1Epb3nPFRimFJoRwKHtXIg 1 1      2 0  13.4kb  13.4kb\n'

In [89]: es.cat.count()
Out[89]: '1510431323 04:15:23 301002\n'

In [90]: es.cat.plugins()
Out[90]: ''

In [91]: es.cat.templates()
Out[91]: 'logstash logstash-* 0 50001\nfilebeat filebeat-* 0 \n'
```

### 任务

```python
es.tasks.get()

es.tasks.list()
```

### 查询

```python
# 发送查询请求
es = Elasticsearch(
        ['172.16.153.129:9200']
    )
    
response = es.search(
    index="logstash-2017.11.14", # 索引名
    body={             # 请求体
      "query": {       # 关键字，把查询语句给 query
          "bool": {    # 关键字，表示使用 filter 查询，没有匹配度
                "must": [      # 表示里面的条件必须匹配，多个匹配元素可以放在列表里
                    {
                        "match": {  # 关键字，表示需要匹配的元素
                            "TransId": '06100021650016153'   # TransId 是字段名， 06100021650016153 是此字段需要匹配到的值
                        }
                    },
                    {
                        "match": {
                            "Ds": '2017-05-06'
                        }
                    },
                    {
                        "match": {
                            "Gy": '2012020235'
                        }
                    }, ],
                 "must_not": {   # 关键字，表示查询的结果里必须不匹配里面的元素
                        "match": {  # 关键字
                            "message": "M("    # message 字段名，这个字段的值一般是查询到的结果内容体。这里的意思是，返回的结果里不能包含特殊字符 'M('
                        }
                 }
            }
        },
        
        # 下面是对返回的结果继续排序
        "sort": [{"@timestamp": {"order": "desc"}}],
        "from": start,  # 从匹配到的结果中的第几条数据开始返回，值是匹配到的数据的下标，从 0 开始
        "size": size    # 返回多少条数据
      }
)


# 得到返回结果的总条数
total = res['hits']['total']

# 循环返回的结果，得到想要的内容
res_dict={}
for hit in res['hits']['hits']:
    log_time = "%s|%s" % (hit['_source']['Ds'], hit['_source']['Us'])
    res_dict[log_time] = "%s|%s|%s|%s" % (hit['_source']['beat']['hostname'],hit['_source']['FileName'], hit['_source']['FileNum'],hit['_source']['Messager'])


# 实例查询7天之内的流水号为：06100021650016153 的日志信息
query_body={
    'bool': {
        'must_not': {'match': {'message': 'M('}}, 
        'must': [
            {'match': {'TransId': '06100021650016153'}}, 
            {'range': {'@timestamp': {'gte': u'now-7d', 'lte': 'now'}}}
        ]
    }
}

res = es.search(
    index='logstash-2017.11.14',
    body={
        "query": query_body,
        "sort":[{"@timestamp": {"order": "desc"}}]})
    }
)
```



# 更高级的 elasticsearch_dsl 模块

### 单一字段查询

```python
es = Elasticsearch(
        ['172.16.153.129:9200']
    )
s = Search(using=es,
    index="logstash-2017.11.14").filter("match",Gy='20160521491').query("match", TransId='06100021650016153').exclude("match", message="M(")
    
response = s.execute()    

using  
    指明用那个已经连接的对象
query  
    接收的是查询体语句
exclude
    接收的是不匹配的字段 就像 must_not
    
filter
    接收的是过滤语句 ，过滤的条件意思是在返回结果中有这些条件的信息       


# 统计结果总数
s.count()
response = sexecute()
response.hits.total


# 获取结果
res_dict={}
for hit in s:
    log_time = "%s|%s" % (hit.Ds, hit.Us')
    res_dict[log_time] = "%s|%s|%s|%s" % (hit.beat['hostname'],hit.FileName, hit.FileNum,hit.Messager)
```

### 设置连接

```python
	# 有几种方法来配置库的连接。
		最简单的选择，也是最有用的，就是定义一个默认连接，每次调用API时都会使用这个连接，而不需要显式传递其他连接。除非要从应用程序访问多个群集，否则强烈建议您使用该 create_connection 方法创建一个默认连接，所有操作都将自动使用该连接。
	# 显式传递一个连接
	如果你不想提供全局配置(也就是默认连接)，你可以传入你自己的连接（实例elasticsearch.Elasticsearch）作为参数， 使用 using 接受它：
  		s = Search(using=Elasticsearch('localhost'))

	甚至你可以下面的方式来覆盖一个对象已经关联的任何连接
			s = s.using(Elasticsearch('otherhost:9200'))
```

### 默认链接

```python
# 默认连接
# 要定义全局使用的默认连接，请使用 connections模块和create_connection方法：
from elasticsearch_dsl.connections import connections

client = connections.create_connection(hosts=['172.16.153.129:9200'], 
    http_auth=('elastic', 'changeme'), timeout=20)


# 执行搜索就不必再传连接对象了

s = Search(index="logstash-2017.11.14").filter("match",Gy='20160521491').query("match", TransId='06100021650016153').exclude("match", message="M(")
```

### 多集群环境的连接

```python
# 多个集群
# 您可以使用以下配置方法同时定义到多个群集的多个连接：
from elasticsearch_dsl.connections import connections

clients = connections.configure(
    default={'hosts': 'localhost'},
    dev={
        'hosts': ['esdev1.example.com:9200'],
        'sniff_on_start': True
    }
)

# 上面的情况是适用于第一次连接时的情况
```

### 运行中设置连接

```python
# if you have configuration to be passed to Elasticsearch.__init__
# 直接传递一个配置信息给 Elasticsearch
connections.create_connection('qa', hosts=['esqa1.example.com'], sniff_on_start=True)

# if you already have an Elasticsearch instance ready
# 追加一个已经准备好的连接对象
connections.add_connection('qa', my_client)

# 使用连接对象的别名
# 当使用多个连接时，您可以使用您在下面注册的字符串别名来引用它们：
s = Search(using='qa')


# 如果在该别名下没有注册的连接，KeyError 异常将会被抛出。
KeyError: "There is no connection with alias 'qa'."
```

# Search DSL

### 该Search对象

```python
# 该Search对象代表整个搜索请求：
  查询（queries）
  过滤器（filters）
  聚合（aggregations）
  排序（sort）
  分页（pagination）
  附加的参数（additional parameters）
  关联客户端（associated client）
```

```python
		# API 被设计为可链接的。除了聚合功能以外，这意味着Search对象是不可变的（对对象的所有更改都将导致创建（拷贝）一个包含更改的副本）。这意味着您可以安全地将Search对象传递给外部代码，而不必担心这个对象会被修改。
		# 实例化对象时，您可以传递低级别的elasticsearch客户端实例Search：

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

s = Search(using=client)

# 所有的方法都会返回一个对象的副本，从而安全地传递给外部代码。
# API 是可连接的，允许你在一个语句中调用多个方法：

s = Search().using(client).query("match", title="python")


# 要将请求发送到Elasticsearch：

s.execute()


# 如果您只是想遍历搜索返回的匹配，则可以遍历该Search对象：

for hit in s:
    print(log_time = "%s|%s" % (hit.Ds, hit.Us'))
    print(hit.beat['hostname'],hit.FileName, hit.FileNum,hit.Messager)

# DS、US、beat、FileName等都是映射好的字段名，就是用 elasticsearch 模块的 search 方法得到的结果里的 hit['_source'] 里面的内容。
# 搜索结果将被缓存。随后调用execute或试图遍历已经执行的Search对象将不会触发额外的请求发送到Elasticsearch。强制请求时指定 ignore_cache=True调用execute。

# 这个 Search 的对象也可以转换为之前的 Query DSL 格式

s.to_dict()
```

### 查询

```python
# Elasticsearch_dsl 的 query 类为所有Elasticsearch查询类型提供类。 传递所有参数作为关键字参数。 这些类接受任何关键字参数，然后dsl将传递给构造函数的所有参数作为结果字典中的顶级关键字序列化（因此生成的json被发送到elasticsearch）。 这意味着在DSL中原始查询和其等价物之间存在明确的一对一映射：

from elasticsearch_dsl.query import MultiMatch, Match

# {"multi_match": {"query": "python django", "fields": ["title", "body"]}}
MultiMatch(query='python django', fields=['title', 'body'])

# {"match": {"title": {"query": "web framework", "type": "phrase"}}}
Match(title={"query": "web framework", "type": "phrase"})

# 在某些情况下，由于python对标识符的限制，这种方法不支持字段中含有特殊字符的情况，比如：@timestamp。
# 在这种情况下，你必须史使用原来的字典形式：Range(** {'@timestamp': {'lt': 'now'}})
```

### 强大的 Q

```python
# 您可以使用Q快捷方式可以把带参数的名称或原始数据的dict构建成 Search 对应类的实例：

from elasticsearch_dsl import Q

Q("multi_match", query='python django', fields=['title', 'body'])
Q({"multi_match": {"query": "python django", "fields": ["title", "body"]}})

# 这两种方式最后转换的结果是一致的
MultiMatch(fields=['title', 'body'], query='python django')


# 要将查询添加到Search对象，请使用以下.query()方法：

q = Q("multi_match", query='python django', fields=['title', 'body'])
s = s.query(q)


# 当然，Q 接收的参数，，query 方法都支持

s = s.query("multi_match", query='python django', fields=['title', 'body'])
```

##### 用 Q 实现组合查询

```python
# Q 对象可以使用逻辑运算符进行组合：

Q("match", title='python') | Q("match", title='django')
# {"bool": {"should": [...]}}
# 匹配到任意条件即可

Q("match", title='python') & Q("match", title='django')
# {"bool": {"must": [...]}}
# 列表里的条件必须同时匹配

Q("match", title="python")
# {"bool": {"must_not": [...]}}
# 非
```

### 实现组合查询的另一种方法

```python
# query 方法可以被连续调用
In [193]: sa = Search().query().query('match',title='python').query('match',body='django')

In [194]: sa.to_dict()
Out[194]:
{
    "query": {
        "bool": {
            "must": [
                {"match": {
                    "title": "python"}
                },
                {"match": {
                    "body": "django"}
                }
            ]
        }
    }
}


# 假如你希望对查询的条件进行精确的控制，请使用 Q 构造组合查询：

q = Q('bool',
    must=[Q('match', title='python')],
    should=[Q(...), Q(...)],
    minimum_should_match=1
)
s = Search().query(q)
```

### 过滤器

```python
# 过滤请使用 filter 方法
s = Search()
s = s.filter('terms', tags=['search', 'python'])
# {'query': {'bool': {'filter': [{'terms': {'tags': ['search', 'python']}}]}}}

# 在幕后，这将产生一个Bool查询并将指定的 terms查询放入其filter分支，使其等价于：
s = Search()
s = s.query('bool', filter=[Q('terms', tags=['search', 'python'])])
# {'query': {'bool': {'filter': [{'terms': {'tags': ['search', 'python']}}]}}}


# 如果您想使用post_filter元素进行分面导航，请使用该 .post_filter()方法。
# 你也可以用 exclude() 排除查询项目：
s = Search()
s = s.exclude('terms', tags=['search', 'python'])

# 官网上说下面是简写，简直不敢相信
s = s.query('bool', filter=[~Q('terms', tags=['search', 'python'])])
```

### 聚合

```python
# 定义一个聚合，请使用 A
A('terms', field='tags')
# {"terms": {"field": "tags"}}


# 嵌套聚合,可以使用.bucket()，.metric()和 .pipeline()方法：

a = A('terms', field='category')
# {'terms': {'field': 'category'}}

a.metric('clicks_per_category', 'sum', field='clicks')\
    .bucket('tags_per_category', 'terms', field='tags')
# {
#   'terms': {'field': 'category'},
#   'aggs': {
#     'clicks_per_category': {'sum': {'field': 'clicks'}},
#     'tags_per_category': {'terms': {'field': 'tags'}}
#   }
# }


# 要将聚合添加到Search对象，请使用.aggs充当顶级聚合的属性

s = Search()
a = A('terms', field='category')
s.aggs.bucket('category_terms', a)
# {
#   'aggs': {
#     'category_terms': {
#       'terms': {
#         'field': 'category'
#       }
#     }
#   }
# }

# 或者下面这样的，有点儿变态
s = Search()
s.aggs.bucket('articles_per_day', 'date_histogram', field='publish_date', interval='day')\
    .metric('clicks_per_day', 'sum', field='clicks')\
    .pipeline('moving_click_average', 'moving_avg', buckets_path='clicks_per_day')\
    .bucket('tags_per_day', 'terms', field='tags')

s.to_dict()
# {
#   "aggs": {
#     "articles_per_day": {
#       "date_histogram": { "interval": "day", "field": "publish_date" },
#       "aggs": {
#         "clicks_per_day": { "sum": { "field": "clicks" } },
#         "moving_click_average": { "moving_avg": { "buckets_path": "clicks_per_day" } },
#         "tags_per_day": { "terms": { "field": "tags" } }
#       }
#     }
#   }
# }


# 您可以通过名称访问现有存储桶

s = Search()

s.aggs.bucket('per_category', 'terms', field='category')
s.aggs['per_category'].metric('clicks_per_category', 'sum', field='clicks')
s.aggs['per_category'].bucket('tags_per_category', 'terms', field='tags')

# 当链接多个聚合时，什么.bucket()和.metric()方法返回之间是有区别的
# .bucket()返回新定义的存储区，同时.metric()返回其父容器以允许进一步链接。
# 与Search对象上的其他方法相反，定义聚合是在原地完成的（不返回副本）。
```

### 排序

```python
# 要指定排序顺序，请使用 .sort() 方法：
s = Search().sort(
    'category',
    '-title',
    {"lines" : {"order" : "asc", "mode" : "avg"}}
)

# 它接受可以是字符串或字典的位置参数。字符串值是一个字段名称，可以用-符号前缀来指定降序。

# 恢复排序使用无参的 sort() 方法

s = s.sort()
```

### 分页

```python
# 要指定from / size参数，请使用Python切片AP
s = s[10:20]
# {"from": 10, "size": 10}


# 如果要访问与查询匹配的所有文档，可以使用 scan使用扫描/滚动弹性搜索API的方法

for hit in s.scan():
    print(hit.title)

# 请注意，在这种情况下，结果将不会被排序。
```

### 突出高亮

```python
# 要设置突出显示的常用属性，请使用以下highlight_options方法：

s = s.highlight_options(order='score')


# 为各个字段启用突出显示使用以下highlight方法完成：

s = s.highlight('title')
# or, including parameters:
s = s.highlight('title', fragment_size=50)


# 返回的结果将在被赋值到一个对象(变量)上可用，.meta.highlight.FIELD 将包含结果的列表：

response = s.execute()
for hit in response:
    for fragment in hit.meta.highlight.title:
        print(fragment)
```

### Suggestions 建议

```python
# 要在Search对象上指定建议请求，请使用以下suggest方法：
s = s.suggest('my_suggestion', 'pyhton', term={'field': 'title'})

# 第一个参数是建议名称（它将返回的名称），第二个是你希望建议者处理的实际文本，关键字参数将被添加到建议的json中，这意味着它应该成为其中一个term，phrase或者completion指出应该使用哪种类型的建议者。
# 如果您只希望运行搜索的建议部分（通过_suggest 端点），您可以通过execute_suggest以下方式进行：
s = s.suggest('my_suggestion', 'pyhton', term={'field': 'title'})
suggestions = s.execute_suggest()

print(suggestions.my_suggestion)
```

### 额外的属性和参数

```python
# 要设置搜索请求的额外属性，请使用该.extra()方法。这可以被用于定义在不能经由像特定的API方法来限定所述主体的键explain或search_after：

s = s.extra(explain=True)


# 要设置查询参数，请使用以下.params()方法：

s = s.params(search_type="count")


# 如果您需要限制elasticsearch返回的字段，请使用以下 source()方法：

# 只返回选定的字段
s = s.source(['title', 'body'])

# 不返回任何字段，只是元数据
s = s.source(False)

# 明确包含/排除字段
s = s.source(include=["title"], exclude=["user.*"])

# 重置字段选择
s = s.source(None)
```

### 序列化和反序列化

```python
# Search 的对象可以使用 .to_dict() 方法序列化为一个字典
# 您也可以使用 Search 类的 .from_dict() 方法创建一个Search对象。
# 这将创建一个新的对象，并使用字典中的数据填充这个新的对象
s = Search.from_dict({"query": {"match": {"title": "python"}}})

# 如果要修改现有的Search对象，并重写它的属性，可以使用这个实例的 update_from_dict() 方法，改变是实时生效的：
In [2]: s = Search()

In [4]: s.to_dict()
Out[4]: {'query': {'match_all': {}}}

In [5]: s.update_from_dict({"query": {"match": {"title": "python"}}, "size": 42}
   ...: )
Out[5]: <elasticsearch_dsl.search.Search at 0x10a7c8550>

In [6]: s.to_dict()
Out[6]: {'query': {'match': {'title': 'python'}}, 'size': 42}

# 返回结果
# 您可以通过调用 Search 对象的 .execute() 方法来执行搜索，之后将返回一个 Response 对象。
# 你可以将这个返回的对象(结果)赋值给一个对象。
# 该 Response 对象允许您通过属性访问的方式(也就是 . )来访问 Response 对象字典中的任何键。
# 它还提供了一些方便的帮手：
response = s.execute()

print(response.success())
# 是否成功
# True

print(response.took)
# 命中数
# 12

print(response.hits.total)

print(response.suggest.my_suggestions)

# 如果要检查response对象的内容，只需使用其 to_dict方法访问原始数据即可打印。
# Hits
# 要访问搜索返回的匹配对象，请访问该hits属性或只是遍历该Response对象：
response = s.execute()
print('Total %d hits found.' % response.hits.total)
for h in response:
    print(h.title, h.body)

# 结果
# 单独的命中包装在一个便利的类，允许属性访问返回的字典中的键。结果的所有元数据都可以通过meta（不带下划线开头 _ ）访问：
response = s.execute()
h = response.hits[0]
print('/%s/%s/%s returned with score %f' % (
    h.meta.index, h.meta.doc_type, h.meta.id, h.meta.score))

响应 =  s.执行（）
h  =  响应.命中[ 0 ]
打印（'/ ％S / ％S / ％S 与得分返回％F '  ％ （
ħ.元.指数， ħ.元.DOC_TYPE ， ħ.元。ID ， ħ.元.得分））
注意
==如果刚好文档中有一个字段叫 meta ，可以使用字典的键方法来访问它：hit['meta']。==

# 聚合
# 聚合可通过aggregations属性获得：
for tag in response.aggregations.per_tag.buckets:
    print(tag.key, tag.max_lines.value)

# MultiSearch
# 如果您需要同时执行多个搜索，则可以使用 MultiSearch 类，这将使用该类的 _msearch  API ：
from elasticsearch_dsl import MultiSearch, Search

ms = MultiSearch(index='blogs')

ms = ms.add(Search().filter('term', tags='python'))
ms = ms.add(Search().filter('term', tags='elasticsearch'))

responses = ms.execute()

for response in responses:
    print("Results for query %r." % response.search.query)
    for hit in response:
        print(hit.title)


```

### 持久化

```python
# 您可以使用dsl库为应用程序定义映射和基本的持久层。

# 映射定义遵循与查询dsl类似的模式：
from elasticsearch_dsl import Keyword, Mapping, Nested, Text

# name your type
m = Mapping('my-type')

# add fields
m.field('title', 'text')

# you can use multi-fields easily
m.field('category', 'text', fields={'raw': Keyword()})

# you can also create a field manually
comment = Nested()
comment.field('author', Text())
comment.field('created_at', Date())

# and attach it to the mapping
m.field('comments', comment)

# you can also define mappings for the meta fields
m.meta('_all', enabled=False)

# save the mapping into index 'my-index'
m.save('my-index')

# ==注意==
# 默认情况下，所有的字段（除了Nested）都会有单个值。
# 您可以在创建/定义字段期间，通过向构造函数传入 multi=True（m.field('tags', Keyword(multi=True))）来始终覆盖此期望值。
# 那么，即使字段没有被设置，字段的值也将是一个空的列表，使您能够写入。
doc.tags.append('search')

# 特别是如果您使用动态映射，则可以根据Elasticsearch中的现有类型更新映射，或直接从现有类型创建映射：

# get the mapping from our production cluster
m = Mapping.from_es('my-index', 'my-type', using='prod')

# update based on data in QA cluster
m.update_from_es('my-index', using='qa')

# update the mapping on production
# 在生产上更新映射
m.save('my-index', using='prod')
```

### 常用字段选项：

```python
multi
# 如果设置True为该字段的值将被设置为[]第一次访问。
required
# 指示字段是否需要文档的有效值。
Analysis
# 要指定字段的analyzer值，Text您可以使用分析仪的名称（作为字符串），并依靠定义的分析仪（如内置分析仪）或手动定义分析仪。
# 或者，您可以创建自己的分析器并让持久层处理其创建：
from elasticsearch_dsl import analyzer, tokenizer

my_analyzer = analyzer('my_analyzer',
    tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
    filter=['lowercase']
)
# 每个分析对象需要有一个名字（my_analyzer和trigram在我们的例子）和断词，令牌过滤器和过滤器炭还需要指定类型（nGram在我们的例子）。
# 在创建依赖于自定义分析器的映射时，索引必须不存在或被关闭。要创建多个DocType定义的映射，您可以使用Index对象
```

### DocType

```python
 # 如果你想在你的文档中创建一个类似于模型的包装，请使用 DocType类：
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text

html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

class Comment(InnerObjectWrapper):
    def age(self):
        return datetime.now() - self.created_at

class Post(DocType):
    title = Text()
    title_suggest = Completion()
    created_at = Date()
    published = Boolean()
    category = Text(
        analyzer=html_strip,
        fields={'raw': Keyword()}
    )

    comments = Nested(
        doc_class=Comment,
        properties={
            'author': Text(fields={'raw': Keyword()}),
            'content': Text(analyzer='snowball'),
            'created_at': Date()
        }
    )

    class Meta:
        index = 'blog'

    def add_comment(self, author, content):
        self.comments.append(
          {'author': author, 'content': content})

    def save(self, ** kwargs):
        self.created_at = datetime.now()
        return super().save(** kwargs)
```

### 文档生命周期 （Document life cycle）

```python
# 在首次使用Post文档类型之前，您需要在Elasticsearch中创建映射。为此，您可以使用Index对象或通过调用init类方法直接创建映射：

# create the mappings in Elasticsearch
Post.init()

# 要创建一个新Post文档只需实例化这个类并传入你想要设置的任何字段，就可以使用标准属性设置来改变/添加更多的字段。请注意，您不限于显式定义的字段：

# instantiate the document
first = Post(title='My First Blog Post, yay!', published=True)
# assign some field values, can be values or lists of values
first.category = ['everything', 'nothing']
# every document has an id in meta
first.meta.id = 47


# save the document into the cluster
first.save()


# 所有的元数据字段（id，parent，routing，index等等）可以被访问（和设置）。
# 通过meta属性或直接用下划线变体访问它们：
post = Post(meta={'id': 42})

# prints 42, same as post._id
print(post.meta.id)

# override default index, same as post._index
post.meta.index = 'my-blog'


To retrieve(检索，得到) an existing document use the get class method:

# retrieve the document
first = Post.get(id=42)
# now we can call methods, change fields, ...
first.add_comment('me', 'This is nice!')
# and save the changes into the cluster again
first.save()

# you can also(也) update just individual fields which will call the update API
# and also(并且) update the document in place（首先）
first.update(published=True, published_by='me')


If the document is not found in elasticsearch an exception (elasticsearch.NotFoundError) will be raised. If you wish to return None instead just pass in ignore=404 to suppress the exception:

p = Post.get(id='not-in-es', ignore=404)
p is None


# 当您想要同时检索多个文档时，id 您可以使用以下mget方法：

posts = Post.mget([42, 47, 256])

# mgetNotFoundError如果有任何文件没有找到，并且RequestError文件中有任何内容导致错误，将会默认提出。您可以通过设置参数来控制此行为：
raise_on_error
    # 如果True（默认），那么任何错误都会引发异常。否则，包含错误的所有文档将被视为丢失。
missing
    # 可以有三个可能的值：（'none'默认）'raise'和 'skip'。如果文档丢失或出错，将被替换为None，将引发异常或文档将完全跳过。

# 所有有关的信息DocType，包括它的信息Mapping都可以通过_doc_type类的属性来访问：
# name of the type and index in elasticsearch
Post._doc_type.name
Post._doc_type.index

# the raw Mapping object
# 原始映射对象
Post._doc_type.mapping

# the optional name of the parent type (if defined)
# 父类型的可选名称（如果已定义）
Post._doc_type.parent


The _doc_type attribute is also home to the refresh method which will update the mapping on the DocType from elasticsearch.

# _doc_type 属性也是可以通过 refresh 方法来更新elasticsearch的DocType上的映射。
# 假如你使用的是动态映射，并希望类知道这些字段，（比如，你希望日期字段能被正确的序列化）你这样将会是很有用的：
Post._doc_type.refresh()


To delete a document just call its delete method:

first = Post.get(id=42)
first.delete()

Search
To search for this document type, use the search class method:
# by calling .search we get back a standard Search object
# 通过调用 .search()， 我们得到一个标准的搜索对象
s = Post.search()
# the search is already limited to the index and doc_type of our document
s = s.filter('term', published=True).query('match', title='first')


results = s.execute()

# when you execute the search the results are wrapped in your document class (Post)
for post in results:
    print(post.meta.score, post.title)


# 或者，您可以只取一个Search对象，并限制它返回我们的文档类型，用正确的类包装：

s = Search()
s = s.doc_type(Post)


# 您也可以将文档类与标准文档类型（只是字符串）结合起来，这将像以前一样处理。您也可以传入多个DocType 子类，响应中的每个文档将被包装在它的类中。

If you want to run suggestions, just use the suggest method on the Search object:
s = Post.search()
s = s.suggest('title_suggestions', 'pyth', completion={'field': 'title_suggest'})

# you can even execute just the suggestions via the _suggest API
suggestions = s.execute_suggest()

for result in suggestions.title_suggestions:
    print('Suggestions for %s:' % result.text)
    for option in result.options:
        print('  %s (%r)' % (option.text, option.payload))
```

### class Meta 选项

```python
# class Meta 选项
# 在Meta文档定义的类中，您可以为文档定义各种元数据：
doc_type
# elasticsearch中的doc_type的名称。默认情况下，它将从类名（MyDocument - > my_document）
index
# 文档的默认索引，默认情况下它是空的，并且每个操作（比如get或save需要一个明确的index参数）
using
# 默认使用的连接别名，默认为 'default'
mapping
# Mapping类的可选实例，用作从文档类本身上的字段创建的映射的基础。
# 在任何属性Meta是的实例类MetaField将被用于控制元字段（的映射_all，_parent等等）。只需将参数（不带前导下划线）命名为要映射的字段并将任何参数传递给MetaField类：
class Post(DocType):
    title = Text()

    class Meta:
        all = MetaField(enabled=False)
        parent = MetaField(type='blog')
        dynamic = MetaField('strict')
```

### 索引(Index)

```python



# 索引(Index)
# Index是一个类，负责在elasticsearch映射和设置中保存与索引有关的所有元数据。
# 在定义 index 时最为有用，因为它允许同时轻松创建多个 index。在迁移中设置弹性搜索对象时，这非常有用：
from elasticsearch_dsl import Index, DocType, Text, analyzer

blogs = Index('blogs')

# define custom settings
blogs.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# define aliases
blogs.aliases(
    old_blogs={}
)

# register a doc_type with the index
blogs.doc_type(Post)

# can also be used as class decorator when defining the DocType
@blogs.doc_type
class Post(DocType):
    title = Text()

# You can attach custom analyzers to the index

html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

blogs.analyzer(html_strip)

# delete the index, ignore if it doesn't exist
blogs.delete(ignore=404)

# create the index in elasticsearch
blogs.create()


# 您还可以为您的索引设置模板，并使用该clone方法创建特定的副本：

blogs = Index('blogs', using='production')
blogs.settings(number_of_shards=2)
blogs.doc_type(Post)

# create a copy of the index with different name
company_blogs = blogs.clone('company-blogs')

# create a different copy on different cluster
dev_blogs = blogs.clone('blogs', using='dev')
# and change its settings
dev_blogs.setting(number_of_shards=1)

```

