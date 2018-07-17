import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

engine = create_engine("postgresql://luxtfbnmwwyols:7cec2fdc13db20125040ec2208f2b0cb7e61c9cd58339aeadf58694a43e459a3@ec2-54-235-196-250.compute-1.amazonaws.com:5432/d6m66v7t3a4p80")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    i = 0
    for isbn, title, author, year in reader:
        i+=1
        db.execute("INSERT INTO books (isbn, title, author , year) VALUES (:isbn, :title, :author ,:year)",
                    {"isbn": isbn, "title": title, "author": author , "year":year})
        print(f"{isbn} , {title} , {author} , {year}")
        if i > 20:
            db.commit()
            break
        
if __name__ == "__main__":
    main()





"""This is the sql command for creating books table"""
# CREATE TABLE books (
#     id SERIAL PRIMARY KEY,
#     isbn VARCHAR NOT NULL,
#     title VARCHAR NOT NULL,
#     author VARCHAR NOT NULL,
#     year VARCHAR NOT NULL
# );