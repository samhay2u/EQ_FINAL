from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import json



class XmlModel(BaseModel):
    _key: int
    type: str
    additional_data_blob: Dict[str, Any]

    @validator('*', pre=True)
    def decode_json_strings(cls, v):
        if isinstance(v, str) and v.strip().startswith('{'):
            try: return json.loads(v)
            except json.JSONDecodeError: return v
        return v