'''
ORM
用于生成数据库中的表
'''

# class Book():
#     def __init__(self, id, name, price):
#         self.id = id
#         self.name = name
#         self.price = price
#
#     def __str__(self):
#         return "id:%s,name:%s,price:%s" % (self.id, self.name, self.price)


from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                       encoding='utf8', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(bind=engine)

from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)

    def __str__(self):
        return self.username, self.id


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    desc = Column(String(120), nullable=False)
    userid = Column(Integer, ForeignKey("user.id"), nullable=False)


if __name__ == "__main__":
    # 创建表，必须
    Base.metadata.create_all(bind=engine)
