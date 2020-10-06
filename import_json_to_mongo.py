
# -*- coding: utf-8 -*-
from datetime import datetime
import os
import json
import config
from services import mongodb_api

document = config.MONGO_LOG_DOCUMENT
db = mongodb_api.document

dir_path = os.path.dirname(os.path.realpath(__file__))
quotes_file = os.path.join(dir_path, 'quotes.json')

mongo_document = db.quotes
with open(quotes_file) as file: 
    file_data = json.load(file) 
    
if isinstance(file_data, list): 
    mongo_document.insert_many(file_data)   
else: 
    mongo_document.insert_one(file_data) 
