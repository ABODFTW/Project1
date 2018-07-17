from flask import Flask , render_template ,request , redirect , url_for


# for data base access 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#local csv import from database 

# import csvimporter

"""Here is the end of the import"""


# Connect to the database 
engine = create_engine("postgresql://luxtfbnmwwyols:7cec2fdc13db20125040ec2208f2b0cb7e61c9cd58339aeadf58694a43e459a3@ec2-54-235-196-250.compute-1.amazonaws.com:5432/d6m66v7t3a4p80")
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# lists books from the goodreads api and the database
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

@app.route("/myaccount", methods=["POST"])
def myaccount():
    # if request.method == ["GET"]:
    #     return render_template('/unloggedin.html')
    user_email = request.form.get('email_user')
    password = request.form.get('password')
    data = db.execute("SELECT email , password from accounts WHERE email = :email" , {"email" : user_email}).fetchone()
    user_data = db.execute("SELECT user from accounts WHERE name = :user ", {"user" : user_email}).fetchone()

    if user_email == data[0] or user_email == user_data and password == data[1]:
        print("The email is {} the password is {}".format(data[0] , data[1]))
        print("user_email = {}".format(user_email))
        return render_template('/myaccount.html' , email=user_email)
    else :
        return render_template('/login.html')
    
    
@app.route("/<string:isbn>")
def details(isbn):
    books = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if books is None:
        return render_template("error.html", message="No such books.")
    return render_template("book.html" , book=books)