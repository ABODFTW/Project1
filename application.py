from flask import Flask , render_template ,request , redirect , url_for , session ,flash
from flask_session import Session


# for data base access 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#local csv import from database 

# import csvimporter

"""Here is the end of the import"""


# Connect to the database 
engine = create_engine("postgresql://luxtfbnmwwyols:7cec2fdc13db20125040ec2208f2b0cb7e61c9cd58339aeadf58694a43e459a3@ec2-54-235-196-250.compute-1.amazonaws.com:5432/d6m66v7t3a4p80")
db = scoped_session(sessionmaker(bind=engine))




# for search funs 
# @app.route("/search", methods=["GET", "POST"])
# def index():
#     if session.get("notes") is None:
#         session["notes"] = []
#     if request.method == "POST":
#         note = request.form.get("note")
#         session["notes"].append(note)

    # return render_template("index.html", notes=session["notes"])

app = Flask(__name__)



# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response



app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# lists books from the database
@app.route("/")
def index():
    books = db.execute("SELECT * FROM books").fetchall()
    print(books)
    return render_template('/index.html' , books=books)
        
    
@app.route("/register")
def register():
    return render_template('/register.html')



@app.route("/registered", methods=["POST"])
def registered():
    user = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password and user != "":
        print("your email is {} , and the password is {}".format(email , password , user))
        db.execute("INSERT INTO accounts (name ,email , password) VALUES (:name ,:email , :password )" ,{
            "name" : user , "email" : email , "password" : password
        })
        db.commit()
        return render_template('/success.html')
    else:
        return redirct(url_for('register'))

@app.route("/login")
def login():
    return render_template('/login.html')

@app.route("/myaccount", methods=["POST" , "GET"])
def myaccount():
    print(request.method)
    if request.method == "POST":
        user = request.form.get('user')
        password = request.form.get('password')
        try:
            data = db.execute("SELECT * from accounts WHERE lower(name) = lower(:name)" , {"name" : user}).fetchone()
        except:
            return render_template('/login.html' , message="Password or email is wrong")
        try:
            if user == data[1] and password == data[3]:
                print("The email is {} the password is {}".format(data[2] , data[3]))
                session['user']= request.form['user']
                return render_template('/myaccount.html' , user=user)
        except:
            return render_template('/login.html' , message="Password or email is wrong")
    else :
        return render_template('/unloggedin.html')

@app.route("/<string:isbn>")
def details(isbn):
    books = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if books is None:
        return render_template("error.html", message="No such books.")
    return render_template("book.html" , book=books)



"""This is Search Functionality"""
@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/results" , methods=["POST"])
def results():
    # Fetch data from the database 
    rsl = request.form.get('search')
    search = f"%{rsl}%"
    chkisbn = db.execute("SELECT * FROM books WHERE isbn like :isbn", {"isbn": search}).fetchall()
    chkauthor = db.execute("SELECT * FROM books WHERE author Ilike :author", {"author": search}).fetchall()
    chktitle = db.execute("SELECT * FROM books WHERE title Ilike :title", {"title": search}).fetchall()

    if chkisbn != []:
        return render_template("results.html" , results=chkisbn)
    elif chkauthor != []:
        return render_template("results.html" , results=chkauthor)
    elif chktitle != []:
        return render_template("results.html" , results=chktitle)
    else : 
        return render_template('search.html' , error="No such a book!")
    
    # else:
    #     return render_template("results.html" , results="There is no results" )

    # chkisbn = db.execute("SELECT * FROM books WHERE isbn contain :isbn " , {"isbn" : search}).fetchall()
    # chktitle =  db.execute("SELECT * FROM books WHERE title = :title", {"title": search}).fetchall()
    # chkauthor =  db.execute("SELECT * FROM books WHERE author = :author", {"author": search}).fetchall()
    # SELECT * FROM mytable
    # WHERE column1 LIKE '%word1%'
    # AND column1 LIKE '%word2%'
    # AND column1 LIKE '%word3%'
    # print(chkisbn)

    