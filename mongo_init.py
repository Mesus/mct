#coding:utf-8

import pymongo
import pymongo.results

def get_db():
    # 建立连接
    host = '10.0.100.128'
    dbname = 'nsjl'
    client = pymongo.MongoClient(host=host, port=27017)
    db = client[dbname]
    return db


def get_collection(db,coll):
    # 选择集合（mongo中collection和database都是延时创建的）
    # collection = getConfig('mongodb','collection')
    coll = db[coll]
    print db.collection_names()
    return coll


def insert_doc(coll,dic):
    # 插入一个document
    c = db[coll]
    _id = c.insert(dic)
    print _id
    if _id:
        return True


def insert_multi_docs(db):
    # 批量插入documents,插入一个数组
    coll = db['informations']
    information = [{"name": "xx", "age": "25"}, {"name": "xx", "age": "24"}]
    information_id = coll.insert(information)
    print information_id


def get_one_doc(coll,dic):
    # 有就返回一个，没有就返回None
    c = db[coll]
    # print coll.find_one()  # 返回第一条记录
    # print coll.find_one({"name": "xx"})
    # print coll.find_one({"name": "none"})
    return c.find_one(dic)


def get_one_by_id(db):
    # 通过objectid来查找一个doc
    coll = db['informations']
    obj = coll.find_one()
    obj_id = obj["_id"]
    print "_id 为ObjectId类型，obj_id:" + str(obj_id)

    print coll.find_one({"_id": obj_id})
    # 需要注意这里的obj_id是一个对象，不是一个str，使用str类型作为_id的值无法找到记录
    print "_id 为str类型 "
    print coll.find_one({"_id": str(obj_id)})
    # 可以通过ObjectId方法把str转成ObjectId类型
    from bson.objectid import ObjectId

    print "_id 转换成ObjectId类型"
    print coll.find_one({"_id": ObjectId(str(obj_id))})


def get_many_docs(coll,dic,cond):
    # mongo中提供了过滤查找的方法，可以通过各种条件筛选来获取数据集，还可以对数据进行计数，排序等处理
    c = db[coll]
    #ASCENDING = 1 升序;DESCENDING = -1降序;default is ASCENDING
    # .sort("age", pymongo.DESCENDING)
    list = []
    for item in c.find(dic,cond):
        list.append(item)
    return list
    # count = coll.count()
    # print "集合中所有数据 %s个" % int(count)
    #
    # #条件查询
    # count = coll.find({"name":"quyang"}).count()
    # print "quyang: %s"%count

def get_docs_paging_sort(coll,dic,cond,pos,page,sortname,sort):
    c = db[coll]
    #ASCENDING = 1 升序;DESCENDING = -1降序;default is ASCENDING
    # .sort("age", pymongo.DESCENDING)
    ss = pymongo.ASCENDING
    if sort == 0:
        ss = pymongo.DESCENDING
    list = []
    for item in c.find(dic,cond).skip(pos).limit(page).sort(sortname,ss):
        list.append(item)
    return list

def clear_all_datas(db):
    #清空一个集合中的所有数据
    db["informations"].remove()

def count(coll,dic):
    c = db[coll]
    result = c.count(dic)

    return result

def update_docs(coll,dic,cond):
    c = db[coll]
    print 'update_docs=='
    print dic
    print cond
    print '====end'
    up = c.update(dic,cond,upsert=True)
    return up

def delete_docs(coll,obj_id):
    c= db[coll]
    from bson.objectid import ObjectId
    filter = {"_id": ObjectId(str(obj_id))}
    de = c.delete_one(filter)
    r = de.raw_result
    return r
db = get_db()
if __name__ == '__main__':
    db = get_db()
    c= db['goods']
    up = c.update({"fk":"200"},{"$set":{"fk":"8"}})
