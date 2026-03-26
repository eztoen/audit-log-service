from pydantic import BaseModel, Field, field_serializer

from datetime import datetime

class ProjectCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)

class ProjectResponseSchema(BaseModel):
    id: int
    name: str 
    created_at: datetime
    
    model_config = {
        'from_attributes': True
    }
    
    @field_serializer('created_at')
    def serialize_created_at(self, v: datetime):
        return v.strftime('%d-%m-%y')
    
class ProjectCreatedSchema(BaseModel):
    id: int
    name: str
    api_key: str
    created_at: datetime
    
class ProjectChangeNameSchema(ProjectCreateSchema):
    pass
