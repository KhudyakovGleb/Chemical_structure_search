import uuid
from pydantic import BaseModel


class Smile(BaseModel):
    component: str
    id: str = str(uuid.uuid4())
