
# coding: utf-8

# In[ ]:

# mongo.py 
from flask import Flask 
from flask import jsonify 
from flask import request 
from flask_pymongo import PyMongo 
import os
import pymongo
import ssl
import re


app = Flask(__name__) 

#app.config['MONGO_URI'] = pymongo.MongoClient('mongodb://arsi:123456@aws-us-east-1-portal.25.dblayer.com:20720,aws-us-east-1-portal.26.dblayer.com:20720/arsalan?ssl=true',ssl_cert_reqs=ssl.CERT_NONE)
app.config['MONGO_DBNAME'] = 'arsalan' 
app.config['MONGO_URI'] = 'mongodb://arsi:123456@aws-us-east-1-portal.25.dblayer.com:20720,aws-us-east-1-portal.26.dblayer.com:20720/arsalan?ssl=true&ssl_cert_reqs=CERT_NONE' 
#app.config['MONGO_URI'] = ('Test1')

mongo = PyMongo(app) 


    
@app.route('/bbc', methods=['GET']) 
def get_all_stars1(): 
    star = mongo.db.isentiascrapybbc 
    output = [] 
    for s in star.find({}):
       output.append({'article_title' : s['article_title'],'article_url' : s['article_url'],'body' : s['body'],'url' : s['url']}) 
       #print output
    return jsonify({'result' : output}) 

@app.route('/bbc/<article>', methods=['GET', 'POST']) 
def get_one_star1(article): 
  star = mongo.db.isentiascrapybbc 
  output = []
  #pat = re.compile('us')'article_title' : {"$regex" : article ,"$options":""}
  for s in star.find({'article_title' : {"$regex" : article ,"$options":""}}):
       output.append([s['article_title'], s['article_url'], s['body'], s['url']]) 
       #print output
  return jsonify({'result' : output})  



if __name__ == '__main__': 
    app.run()


# In[ ]:



