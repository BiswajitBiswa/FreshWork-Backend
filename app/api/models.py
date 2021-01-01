#models that defines the structure of data stored in the datastore
from typing import Dict
from pydantic import BaseModel
class File(BaseModel):
    key:str
    value:Dict