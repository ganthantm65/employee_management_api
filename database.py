from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE="mysql+pymysql://root:griffin%402006@localhost:3306/blog"
engine=create_engine(URL_DATABASE)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

base=declarative_base()