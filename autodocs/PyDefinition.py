from typing import Optional
from pydantic import BaseModel
from enum import Enum


class PyDefinitionTypeEnum(str, Enum):
    function = "def"
    class_ = "class"


class PyDefinition(BaseModel):
    type: PyDefinitionTypeEnum
    name: str
    docstring: Optional[str] = None
