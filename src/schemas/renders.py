from typing import Annotated, Literal, List
from pydantic import BaseModel, Field, field_serializer, field_validator

class SizeEngine:
    @field_validator("size")
    @classmethod
    def size_check(cls, value: str):
        if not "x" in value:
            raise ValueError("Not valid size")
        
        sizes_str = "".join(value.split("x"))
        if not (sizes_str.isdigit() or sizes_str == "fullfull"):  
            raise ValueError("Invalid size")

        return value
    
    @field_serializer("size", return_type=Annotated[List[str], 2])
    def size_serializer(self, value: str, info_):
        return value.split("x")

class RenderImage(BaseModel, SizeEngine):
    url: str
    selector: str = Field("body")
    format: Literal["png", "jpg", "bin", "base64"] = Field("png")
    size: str = Field("1920x1080")
    timeout: float = Field(2.5)


class RenderSource(BaseModel, SizeEngine):
    elements: str
    css: str = Field("")
    js: str = Field("")
    selector: str = Field("body")
    format: Literal["png", "jpg", "bin", "base64"] = Field("png")
    size: str = Field("1920x1080")
    timeout: float = Field(2.5)
