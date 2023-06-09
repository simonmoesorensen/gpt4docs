from typing import Optional
from pydantic import BaseModel
from enum import Enum


class PyDefinitionTypeEnum(str, Enum):
    function = "def"
    class_ = "class"


class PyDefinition(BaseModel):
    type: PyDefinitionTypeEnum
    name: str
    docstring_start_line: Optional[int] = None
    docstring_end_line: Optional[int] = None
    docstring: Optional[str] = None
