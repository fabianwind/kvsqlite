kvsqlite
========

A simple key-value sqlite database manager develop with Python language. Easy to use, simple code, and pure 100% Python.

In several situation, the database might be simple as key-value schema. Author defined a flexible schema for developement. If follow the manual, you can simplely create a useful key-value database.

The database schema with 4 columns, the first is id column which is auto inceasement columns by using statement:
>"id" integer NOT NULL PRIMARY KEY

The second to fourth columns you can define your own name (default is "function", "config", and "value")

In order to easy to use, author considered the key-value database as a json or RESTful. We can "select" data from the database, and modify the data, and then "update" the data without any change. Just like "PUT" method of RESTful.


========

#Version:
0.1.1


#The feature of next version:
1. Where Statement for select function
2. Bug fix


#Develop Environment:
1. Python 2.7.5 with sqlite3 module


#Uage:


import:

> from kvsqlite import KVManager


initial:

Give the path of database you want to use
> kv = KVManager(‘/tmp/test.db’)


create table:

create a table name
> kv.create_table('test_table’)


The schema of sqlite database will be:

> CREATE TABLE "test_table” (
    "id" integer NOT NULL PRIMARY KEY,
    "function" varchar(30) NOT NULL,
    "config" varchar(60) NOT NULL UNIQUE,
    "value" varchar(90) NOT NULL );

function , config, value is set as default.
if you need to change names of columns, do this:

> kv = KVManager('/tmp/test.db', c1='column1’, c2='column2', c3='column3')

if you want change the length of column and unique column, do this:

> kv.create_table('test_table’, c1_len=80, c2_len=100, c3_len=120, unique=0)

The schema of sqlite database will be:

> CREATE TABLE "test_table” (
"id" integer NOT NULL PRIMARY KEY,
“column1” varchar(80) NOT NULL UNIQUE,
"column2” varchar(100) NOT NULL,
"column3” varchar(120) NOT NULL );



insert:

For one data

> kv.insert('test_table', [('c1', 'c2', 'c3')])


For more data (if you insert ('c1', 'c2', 'c3') again, you will get "column is not unique" warning)

> kv.insert('test_table', [('a1', 'a2', 'a3'), ('b1', 'b2', 'b3')])



select:

In this version, select will return all data from the table

> kv.select('test_table')

[(1, u'c1', u'c2', u'c3'), (2, u'a1', u'a2', u'a3'), (3, u'c1', u'c2', u'c3')]


update:

Author recommands that using update function with select return data.


> data = kv.select('test_table')

[(1, u'c1', u'c2', u'c3'), (2, u'a1', u'a2', u'a3'), (3, u'c1', u'c2', u'c3')]

> new_data = list(data[0])

[1, u'c1', u'c2', u'c3']

> new_data[2] = 'modify'

[1, u'c1', 'modify', u'c3']

> data[0] = new_data

[(1, u'c1', 'modify', u'c3'), (2, u'a1', u'a2', u'a3'), (3, u'c1', u'c2', u'c3')]

> kv.update('test_table', data)

> kv.select('test_table')

[(1, u'c1', u'modify', u'c3'), (2, u'a1', u'a2', u'a3'), (3, u'c1', u'c2', u'c3')]


Note: 
Because tuple is imutable type, we have to change type to list to modify the values. To update data easy, a new function will be added in the future version.





delete:

Author recommands that using delete function with select return data.
>>> data = kv.select('test_table')

[(1, u'c1', u'c2', u'c3'), (2, u'a1', u'a2', u'a3'), (3, u'c1', u'c2', u'c3')]

The second param has to be list
> kv.delete('test_table', [data[1], data[2]])

> kv.select('test_table')
[(1, u'c1', u'c2', u'c3')]

The index 1 and 2 data has been deleted



drop table:
> kv.drop_table('test_table')
