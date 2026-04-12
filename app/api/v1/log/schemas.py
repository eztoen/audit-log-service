from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

class LogCreateSchema(BaseModel):
    service:   str = Field(..., max_length=100)
    level:     Literal['INFO', 'WARNING', 'ERROR', 'CRITICAL']
    message:   str = Field(..., max_length=5000)
    timestamp: datetime
    
class LogReadSchema(BaseModel):
    id:        int
    service:   str
    level:     str
    message:   str
    timestamp: datetime
    
    model_config = {
        'from_attributes': True
    }