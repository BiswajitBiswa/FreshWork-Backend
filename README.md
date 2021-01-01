# CRD-operations-of-a-file-based-key-value-data-store

This is a file which can be exposed as a library that supports the basic CRD(create, read, write) operations. Data store is meant to local storage for one single process on single laptop

The data store will support the following :

1.I have set the file location to current working directory but it can be set to any location in laptop/pc.

2.data is stored in the datastore as key-value pair but with an additional key "datastore" ,that points to all the data,for ease of reference .

(3,4,5)ANS---either accessing data store through apis or through library as defined in below processes performs as mentioned 
and even raise appropriate errors.

6. ANS--TTL property if not provided stores  the data permanently or else upon key creation a thread gets executed,that deletes the key automatically from datastore after given seconds of time. 

9.The file is accessed by multi-threading
ANS--used asynchronous calls to api to allow clients to send multiple requests to datastore at the same time without waiting for response of the first call
10.The file must not allow more than one client process to access datastore at any given time
ANS-- using fastapi to make api calls the problems 9 and 10 doesnt seem to be an issue 

**IMPROVEMENTS**

The datastore could be made more efficient with background tasks
and multiple workers like using celery and message brokers like RABBIT-MQ
and the memory enhancemnet could be done with caching like redis

**I achieved it with two process**

**[process1]**

(Please refer to api1.png,api2.png,api3.png to get idea of how to access the apis)
#steps-
1.clone the repository

2.cd into the cloned directory--FreshWork-Backend

3.activate virtual evn-venv

4.RUN command uvicorn app.main:app --reload to load the live loading server

5.visit the url--"http://127.0.0.1:8000/docs

6.you will find POST,GET,DELETE RSET API endpoints in swagger docs .

7.you can access different endpoints by clicking on the methods and the clicking on "try it out".


**[process2]**

(please refer to process2.png for clear idea)
#steps-
1.clone the repository

2.cd into the cloned directory--FreshWork-Backend

3.Then follow the steps below to access the CRD methods in the CRD class defined inside "app/api/CRD_as_library.py"

>>>from app.api.CRD_as_library import CRD
#STORE DATA

>>> data={"key":"key4","value":{}}

 #store your input as json  with "key" and "value" as keys

>>> CRD.create(data)

'key already present'

>>> data={"key":"key5","value":{"name":"biswajit"}}

>>> CRD.create(data)

'datastored'

 #READ DATA FROM DATASTORE WITH KEY

>>> CRD.read("key1")

'Key does not exist'

>>> CRD.read("key4")

{}

>>> CRD.read("key5")

{'name': 'biswajit'}

 #DELETE KEY FROM DATASTORE

>>> CRD.delete("key5")

'key deleted'

 #TRY READING THE DELETED KEY AGAIN

>>> CRD.read("key5")

'Key does not exist'
