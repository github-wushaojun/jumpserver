from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, UniqueConstraint

engine = create_engine("mysql+pymysql://root:12345678@127.0.0.1:3306/test?charset=utf8", encoding='utf-8', echo=True)

metadata = MetaData()

ceshi = Table('ceshi', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(20)),
        UniqueConstraint('name')
    )


conn = engine.connect()
result = conn.execute(
    "insert into ceshi(name)values(%(name)s)",name=None
)
# print(result.fetchall())