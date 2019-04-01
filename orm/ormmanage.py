from orm import model

from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                       encoding='utf8', echo=True)

# 构造会话对象
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=engine)()


# 构造会话对象之后可以进行增删改查

def insertUser(username, password):
    result = session.add(model.User(username=username, password=password))
    session.commit()
    session.close()
    print(result)


def checkUser(username, password):
    result = session.query(model.User).filter(model.User.username == username).filter(
        model.User.password == password).first()

    return result


# 添加函数
def insertBook(name, price, desc, userid):
    book = model.Book(name=name,price=price,desc=desc, userid=userid)
    print(book)
    print(book.id, book.name)
    result = session.add(book)
    session.commit()
    print("################################")
    session.close()
    print(result)


# 查询函数
def checkBook(id):
    result = session.query(model.Book.id, model.Book.name, model.Book.price, model.Book.desc).all()
    session.commit()
    return result


# 删除函数
def deleteBook(id):
    result = session.query(model.Book).filter(model.Book.id == id).delete()
    session.commit()
    session.close()
    print(result)


# 修改函数
def updateBook(id, name, price, desc):
    result = session.query(model.Book).filter(model.Book.id == id).update({
        "name": name, "price": price, "desc": desc
    })
    session.commit()
    return result
