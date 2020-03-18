from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, String, Integer, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(10))

class UserCopy(Base):
    __tablename__ = 'user_copy'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(10))

class UserJNL(Base):
    __tablename__ = 'user_jnl'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    OPERATION = Column(String(1))
    old_id = Column(Integer())
    new_id = Column(Integer())
    created_at = Column(DateTime())

def create_session(host, user, password, database):
    db = URL(
        drivername='mysql+pymysql',
        host=host,
        username=user,
        password=password,
        database=database,
    )

    engine = create_engine(
        name_or_url=db,
        connect_args={'charset': 'utf8'},
        pool_recycle=60,
        encoding='utf8'
    )

    return sessionmaker(bind=engine)()


if __name__ == '__main__':
    from_session = create_session(
        environ['SAMPLE_FROM_HOST'],
        environ['SAMPLE_FROM_USER'],
        environ['SAMPLE_FROM_PASSWORD'],
        environ['SAMPLE_FROM_DATABASE'],
    )

    user_jnls = from_session.query(
        UserJNL
    ).all()

    to_session = create_session(
        environ['SAMPLE_TO_HOST'],
        environ['SAMPLE_TO_USER'],
        environ['SAMPLE_TO_PASSWORD'],
        environ['SAMPLE_TO_DATABASE'],
    )
    
    for user_jnl in user_jnls:
        if user_jnl.OPERATION=='I':
            new_user = from_session.query(User).filter(User.id==user_jnl.new_id).first()
            user_insert = UserCopy()
            user_insert.id = new_user.id
            user_insert.name = new_user.name
            to_session.add(user_insert)
        elif user_jnl.OPERATION=='U':
            new_user = from_session.query(User).filter(User.id==user_jnl.new_id).first()
            user_update = to_session.query(
                UserCopy
            ).filter(
                UserCopy.id == user_jnl.old_id
            ).first()
            user_update.id = new_user.id
            user_update.name = new_user.name 
            to_session.add(user_update)
        elif user_jnl.OPERATION=='D':
            user_del = to_session.query(
                UserCopy
            ).filter(
                UserCopy.id == user_jnl.old_id
            ).first()
            to_session.delete(user_del)
        from_session.delete(user_jnl)

    from_session.commit()
    to_session.commit()
    from_session.close()
    to_session.close()


