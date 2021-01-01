
from typing import Dict
import json
import os
import os.path
import threading
import time



class CRDData:
    #ADDS DATA TO DATASTORE
    def create(data:Dict,time_to_live:int,data_store_path):
        with open(data_store_path) as f:
            file_data = json.load(f)
            temp = file_data["datastore"][0]
            temp[data["key"]] =data["value"]
        write_json(file_data,data_store_path)
        if time_to_live!=None:
            t = threading.Thread(target=ttl_set_remove, args=(data["key"],data_store_path,time_to_live))
            t.start()

    #CREATES DATASTORE IN WORKING DIRECTORY IF IT DOES NOT EXIST AND ADDS DATA
    def create_if_not_exist(data ,time_to_live:int, data_store_path):
        with open(data_store_path, 'w') as f1 :
            f1.write('{"datastore":[{}]}')
            f1.close()
            create1(data,time_to_live, data_store_path)
    #READS DATA FROM DATA STORE
    def read(data_store_path):
        with open(data_store_path) as f:
            file_data = json.load(f)
            temp = file_data["datastore"][0]
            return temp[data["key"]]

   #DELETES DATA FROM DATASTORE
    def delete(key,data_store_path):
        with open(data_store_path) as f:
            file_data = json.load(f)
            temp = file_data["datastore"][0]
            del temp[key]
        write_json(file_data , data_store_path)
        return 'deleted'
    #FUNCTION TO CHECK SIZE OF DATASTORE
    def check_size(data_store_path):
        size=os.path.getsize(data_store_path)
        return size
   #FUNCTION TO CHECK IF
    def check_key_exist(key:str,data_store_path):
        with open(data_store_path) as f:
            file_data = json.load(f)
            temp = file_data["datastore"][0]
            if key in temp:
                return temp[key]
            else:
                return 'not_exist'
CRD=CRDData


# To maintain modularity repeatedely called functions has been saved ouside CRD class as public fucntions
def write_json(data , data_store_path) :
    with open(data_store_path, 'w') as f :
        json.dump(data , f , indent=4)

def create1(data:Dict,ttl:int,data_store_path):
    with open(data_store_path) as f3:
        file_data = json.load(f3)
        temp = file_data["datastore"][0]
        temp[data["key"]] =data["value"]
    write_json(file_data,data_store_path)
    if time_to_live != None :
        t = threading.Thread(target=ttl_set_remove , args=(data["key"] , data_store_path ,time_to_live))
        t.start()

#Threaded function that gets called by CREATE method when a new key is added and TTL is set and deleted the key after TTL
def ttl_set_remove(key,data_store_path,ttl):
    time.sleep(ttl)
    with open(data_store_path) as f :
        file_data = json.load(f)
        temp = file_data["datastore"][0]
        del temp[key]
    write_json(file_data , data_store_path)
