import re, os, sys
import json
import logging
import logging.handlers
import configparser
import pandas as pd
import pymongo
from flask import Flask, request


'''
Created on Apr 24, 2018

@author: lshi
'''

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s [%(name)s.%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.handlers.TimedRotatingFileHandler('log//rei-poc.log', when='midnight'), logging.StreamHandler()])

app = Flask(__name__)
config = configparser.ConfigParser()
mongo_db = None

@app.route("/")
def hello():
    return 'Hello, World1!'

@app.route("/partners")
def get_partners():
    global mongo_db
    try:
        if mongo_db == None:
            get_mongo_db()
        if mongo_db == None:
            return '{status:"error", message:"mongo_db is null"}'
        list = []
        for doc in mongo_db.partner.find({},{'_id':1}):
            list.append(doc)
        return json.dumps(list)
    except:
        logging.error('pymongo error: {}'.format(sys.exc_info()))
        mongo_db = None
        return '{status:"error", message:"pymongo error"}'


@app.route("/partner/<id>")
def get_partner(id):
    global mongo_db
    try:
        if mongo_db == None:
            get_mongo_db()
        if mongo_db == None:
            return '{status:"error", message:"mongo_db is null"}'
        print(id)
        for doc in mongo_db.partner.find({'_id':id}):
            return json.dumps(doc)
        return '{status:"error", message:"not found"}'    
    except:
        logging.error('pymongo error: {}'.format(sys.exc_info()))
        mongo_db = None
        return '{status:"error", message:"pymongo error"}'

@app.route("/loaddata")
def load_data():
    global mongo_db
    fname = request.args.get('fname')
    folder = config.get('Default','input_data')
    path = folder+'/'+fname
    if not os.path.isfile(path) or not os.access(path, os.R_OK):
        return '{status:"Error", message:"File is not exist or not readable!"}'
    conf = re.sub(r'\.\w+$','.conf', path)
    keys = []
    columns = []
    if os.path.isfile(conf) and os.access(conf, os.R_OK):
        f = open(conf)
        while True:
            line = f.readline()
            if not line:
                break
            m = re.match(r'Key\s+=\s+(.*)\s+$', line)
            if m:
                keys = [k.strip() for k in m.group(1).split(',')]
                continue
                
            m = re.match(r'Column Names\s+=\s+(.*)\s+$', line)
            if m:
                columns = [c.strip() for c in m.group(1).split(',')]
                continue
        f.close()
    #print(keys)
    #print(columns)
    
    logging.info(path)
    logging.info(keys)
    logging.info(columns)
    
    df = pd.read_excel(path)
    for col in range(len(df.columns)):
        if col<len(columns) and columns[col]:
            df.columns._data[col] = columns[col]
        else:
            df.columns._data[col] = df.columns._data[col].strip() 

    if len(keys):
        _id = df[keys[0]]
        for k in range(1, len(keys)):
            _id = _id + '+' + df[keys[k]]
        df.insert(0,'_id', _id)    
    num_load = 0
    num_dup = 0
    try:
        if mongo_db == None:
            get_mongo_db()
        if mongo_db != None:
            for idx, row in df.iterrows():
                js = row.to_json(orient='columns')
                try:
                    mongo_db.partner.insert_one(json.loads(js))
                    logging.info('insert_one {}'.format(js))
                    num_load += 1
                except pymongo.errors.DuplicateKeyError as err:
                    logging.info('DuplicateKeyError {}'.format(err))
                    num_dup += 1
    except:
        logging.error('pymongo error: {}'.format(sys.exc_info()))
        mongo_db = None
        return '{status:"error", message:"pymongo error"}'

    msg = '{} records loaded'.format(num_load)
    if num_dup:
        msg = '{} records loaded (ignored {} duplications)'.format(num_load, num_dup)
    else:
        msg = '{} records loaded'.format(num_load) 
    return '{status:"ok", message:"'+msg+'"}'                   


def get_mongo_db():
    global mongo_db, config
    if mongo_db == None:
        mongo_conn_str = 'mongodb://{}:{}@{}:{}'.format(config.get('MongoDB','user'),
                                                            config.get('MongoDB','psw'),
                                                            config.get('MongoDB','host'),
                                                            config.get('MongoDB','port'))
        client = pymongo.MongoClient(mongo_conn_str)
        if client:
            mongo_db = client['reipoc']
     
if __name__=="__main__":
    config.read('config.ini')
    logging.info('=== flask start ===')
    #print(load_data('PartnerInfo.xlsx'))
    app.run(host=config.get('Default','host'), port=config.getint('Default', 'port'), debug=config.getboolean('Default', 'debug'))
    
    