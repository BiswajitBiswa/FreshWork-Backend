from typing import Dict
import json
import os
import os.path
import threading
import time
from os import path
import sys

class CRDlibrary:
    #ADDS DATA TO DATASTORE
    def create(data:Dict,time_to_live=None):
        # check size of key if its capped at 32 chars or not
        if len(data["key"]) > 32 :
            return "Invalid key size!"
        # check if provided value has length less than 16 or not
        elif value_size(data["value"])>16:
            return "Size of Value must be less than or equal to 16kb."
        # check if file doesn't exist
        elif not path.exists(data_store_path) :
            #create_if_not_exist(data , time_to_live , data_store_path)
            with open(data_store_path , 'w') as f :
                f.write('{"datastore":[{}]}')
                f.close()
                with open(data_store_path) as f1 :
                    file_data = json.load(f1)
                    temp = file_data["datastore"][0]
                    temp[data["key"]] = data["value"]
                write_json(file_data , data_store_path)
                if time_to_live != None :
                    t = threading.Thread(target=ttl_set_remove , args=(data["key"] , data_store_path , time_to_live))
                    t.start()
            return "Data Stored"
        # check if key exists in the datastore already
        elif check_key_exist(data["key"],data_store_path) != 'not_exist':
            return"key already present"
        #Check if datastore memory has not exceeded 1GB
        elif (check_size(data_store_path)/(1024*1024*1024))>1:
            return "Memory limit exceeded"
        else:
            with open(data_store_path) as f:
                file_data = json.load(f)
                temp = file_data["datastore"][0]
                temp[data["key"]] =data["value"]
            write_json(file_data,data_store_path)
            if time_to_live!=None:
                t = threading.Thread(target=ttl_set_remove, args=(data["key"],data_store_path,time_to_live))
                t.start()
            return "datastored"



    #READS DATA FROM DATA STORE
    def read(key:str):
        data_store_path = return_file_path()
        if check_key_exist(key, data_store_path)=='not_exist' or not path.exists(data_store_path) :
            return "Key does not exist"
        else:
            with open(data_store_path) as f:
                file_data = json.load(f)
                temp = file_data["datastore"][0]
                return temp[key]

   #DELETES DATA FROM DATASTORE
    def delete(key):
        data_store_path = return_file_path()
        if check_key_exist(key, data_store_path)=='not_exist' or not path.exists(data_store_path) :
            return "Key does not exist"
        else:
            with open(data_store_path) as f:
                file_data = json.load(f)
                temp = file_data["datastore"][0]
                del temp[key]
            write_json(file_data , data_store_path)
            return 'key deleted'


CRD=CRDlibrary

# To maintain modularity repeatedely called functions has been saved ouside CRD class as public fucntions

#function to create datastore if it does not exist
def return_file_path() -> str:
    cwd = os.getcwd()
    path = "app/api"
    file_path = os.path.join(cwd, path, 'data_store.json')
    return file_path

# FUNCTION TO CHECK SIZE OF DATASTORE
def check_size(data_store_path) :
    size = os.path.getsize(data_store_path)
    return size

def value_size(value:Dict) :
    value_size = (sys.getsizeof(value)) / 1024
    return value_size


# FUNCTION TO CHECK IF
def check_key_exist(key: str , data_store_path) :
    with open(data_store_path) as f :
        file_data = json.load(f)
        temp = file_data["datastore"][0]
        if key in temp :
            return 'key_exist'
        else :
            return 'not_exist'

#appends data to datastore
def write_json(data , data_store_path) :
    with open(data_store_path, 'w') as f :
        json.dump(data , f , indent=4)


#Threaded function that gets called by CREATE method when a new key is added and TTL is set and deleted the key after TTL
def ttl_set_remove(key,data_store_path,ttl):
    time.sleep(ttl)
    with open(data_store_path) as f :
        file_data = json.load(f)
        temp = file_data["datastore"][0]
        del temp[key]
    write_json(file_data , data_store_path)