from .database import Base
from sqlalchemy import *
class Post(Base):
    __tablemane__="posts"

    id=Column(Integer , primary_key= True , nullable=False)
    title=Column(String , nullable=False)
    content=Column(String , nullable=False)
    published=Column(Boolean , default=True)
    