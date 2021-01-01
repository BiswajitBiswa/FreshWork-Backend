from fastapi import APIRouter,HTTPException
from typing import List, Optional
from app.api.models import File
from fastapi.responses import JSONResponse
from app.api.CRD_data_store import CRD
from os import path
import sys
import os
import os.path

api =APIRouter()

@api.post('/', response_model=List[File])
async def create(payload: File,time_to_live:Optional[int] = None):
        data = payload.dict()
        value_size=(sys.getsizeof(data["value"]))/1024
        #check size of key if its capped at 32 chars or not
        if len(data["key"]) > 32 :
            raise HTTPException(status_code=401 , detail="Invalid key size!")
        #check if provided value has length less than 16 or not
        elif value_size>16:
            raise HTTPException(status_code=402 , detail="Size of Value must be less than or equal to 16kb.")
        #check if file doesn't exist
        elif not path.exists(data_store_path) :
            CRD.create_if_not_exist(data , time_to_live , data_store_path)
            return JSONResponse(content=f'{data["key"]}:{data["value"]} stored in file1')
        #check if key exists in the datastore already
        elif CRD.check_key_exist(data["key"], data_store_path) != 'not_exist':
            raise HTTPException(status_code=405 , detail="key already present")
        #Check if datastore memory has not exceeded 1GB
        elif (CRD.check_size(data_store_path)/(1024*1024*1024))>1:
            raise HTTPException(status_code=403 , detail="Memory limit exceeded")
        #store the data with CRD fucntions if the input is well defined and no error is encountered
        else:
            CRD.create(data,time_to_live,data_store_path)
            return JSONResponse(content=f'{data["key"]}:{data["value"]} stored in file')




#GET data from data store using a key
@api.get('/{key}')
async def read(key:str):
    read_data=CRD.check_key_exist(key , data_store_path)
    if  read_data== 'not_exist' :
        raise HTTPException(status_code=405 , detail="key not present")
    else:
        return JSONResponse(content=f'{read_data}')

#api to delete data from data store using a key
@api.delete('/{key}')
async def delete(key: str):
    read_data = CRD.check_key_exist(key , data_store_path)
    if read_data == 'not_exist' :
        raise HTTPException(status_code=405 , detail="key not present")
    deleted_data = CRD.delete(key , data_store_path)
    if deleted_data=='deleted':
        return JSONResponse(content=f'{key} deleted')

#function that gives the absolute path to datastore //Can be set to any path where the file is to be created
def return_file_path() -> str:
    cwd = os.getcwd()
    path = "app/api"
    file_path = os.path.join(cwd, path, 'data_store.json')
    return file_path
data_store_path=return_file_path()