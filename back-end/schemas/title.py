from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator, model_validator, StringConstraints

from .basic import ORMModel, QueryModel

class Genre(ORMModel):
    name: str = Field(..., alias="genreName")

class TitleAka(ORMModel):
    title_name: str = Field(..., alias="akaTitle")
    region: Optional[str] = Field(..., alias="regionAbbrev")

class Principal(ORMModel):
    nconst: str = Field(..., alias="nameID")
    primaryName: str
    category_name: str = Field(..., serialization_alias="category")

    @model_validator(mode='before')
    @classmethod
    def get_fields(cls, data):
        data.primaryName = data.person.primary_name
        data.category_name = data.category.name
        return data

class Rating(BaseModel):
    avRating: Optional[str]
    nVotes: Optional[str]

class TitleObject(ORMModel):
    tconst: str = Field(..., alias="titleID")
    title_type: str = Field(..., alias="type")
    originalTitle: str = Field(..., alias="original_title")
    image_url: Optional[str] = Field(..., alias="titlePoster")
    start_year: str = Field(..., alias="startYear")
    end_year: str = Field(..., alias="endYear")
    genres: list[Genre]
    aliases: list[TitleAka] = Field(..., alias="titleAkas")
    principals: list[Principal]
    rating: Rating

    @model_validator(mode='before')
    @classmethod
    def get_ratings(cls, values):
        values.rating = Rating(avRating=values.average_rating and f"{values.average_rating:.1f}", nVotes=values.num_votes and str(values.num_votes))
        return values
    
    @field_validator('start_year', 'end_year', mode="before")
    @classmethod
    def int_to_str(cls, value: int) -> str:
        return str(value)


class TqueryObject(QueryModel):
    titlePart: str

class GqueryObject(QueryModel):
    qgenre: str
    minrating: Annotated[str, StringConstraints(pattern=r'^1?[0-9](.[0-9])?$')]
    yrFrom: Optional[Annotated[str, StringConstraints(pattern=r'^[0-9]*$')]] = None
    yrTo: Optional[Annotated[str, StringConstraints(pattern=r'^[0-9]*$')]] = None

    @model_validator(mode='before')
    @classmethod
    def check_both_or_none(cls, values):
        if "yrFrom" in values and values["yrFrom"] is not None and ("yrTo" not in values or values["yrTo"] is None):
            raise ValueError("Both yrFrom and yrTo must be set or neither.")
        if "yrTo" in values and values["yrTo"] is not None and ("yrFrom" not in values or values["yrFrom"] is None):
            raise ValueError("Both yrFrom and yrTo must be set or neither.")

        return values

