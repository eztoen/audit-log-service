from pydantic import BaseModel, Field

from datetime import datetime

class ProjectCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)

class ProjectReadSchema(BaseModel):
    id: int
    name: str 
    created_at: datetime
    
    model_config = {
        'from_attributes': True
    }
    
class ProjectCreatedSchema(BaseModel):
    id: int
    name: str
    api_key: str
    created_at: datetime