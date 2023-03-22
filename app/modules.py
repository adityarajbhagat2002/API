from .database import Base
from sqlalchemy import *
class Post(Base):
    __tablemane__="posts"

    id=Column(Integer , )