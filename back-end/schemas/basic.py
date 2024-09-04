from pydantic import BaseModel, ConfigDict

from datetime import date

class ORMModel(BaseModel):
    model_config = ConfigDict(
            from_attributes = True,
            populate_by_name = True
            )

class QueryModel(BaseModel):
    model_config = ConfigDict(
            extra = "forbid"
            )


class UserObject(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    birtday: date
    
