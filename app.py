from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:postgres123@localhost/height_collector" #- local
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ennugparwshacb:73a3495de9a7808010dce1b136c44ca33bd907a7cf5efc111cf4972772de4baa@ec2-54-208-233-243.compute-1.amazonaws.com:5432/dbdmf771at3jue?sslmode=require"
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id = db.Column(db.Integer, primary_key = True)
    email_ = db.Column(db.String(120), unique=True)
    height_ =  db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def success():
    if request.method =="POST":
        email = request.form["email_name"]
        height = request.form["height_name"]

        if db.session.query(Data).filter(Data.email_==email).count() ==0:
            data= Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height,1)
            count= db.session.query(Data.height_).count()
            send_email(email,height, average_height, count)
            return render_template("success.html")

    average_height = db.session.query(func.avg(Data.height_)).scalar()
    average_height = round(average_height, 1)
    count = db.session.query(Data.height_).count()
    send_email(email, height, average_height, count)

    return render_template("index.html", text="Your e-mail is already in the database. We sent you an e-mail without updating the data.")

if __name__ =="__main__":
    app.debug = True
    app.run()



# Wersja z plikami

# from flask import Flask, render_template, request, send_file
# from flask_sqlalchemy import SQLAlchemy
# from send_email import send_email
# from sqlalchemy.sql import func
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:postgres123@localhost/height_collector" #- local
# # app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ennugparwshacb:73a3495de9a7808010dce1b136c44ca33bd907a7cf5efc111cf4972772de4baa@ec2-54-208-233-243.compute-1.amazonaws.com:5432/dbdmf771at3jue?sslmode=require"
# db = SQLAlchemy(app)
#
# class Data(db.Model):
#     __tablename__="data"
#     id = db.Column(db.Integer, primary_key = True)
#     email_ = db.Column(db.String(120), unique=True)
#     height_ =  db.Column(db.Integer)
#
#     def __init__(self, email_, height_):
#         self.email_ = email_
#         self.height_ = height_
# @app.route("/")
# def index():
#     return render_template("index.html")
#
# @app.route("/success", methods=["POST"])
# def success():
#     global file
#     if request.method =="POST":
#         file = request.files["file"]
#         file.save(secure_filename("uploaded" + file.filename))
#         with open("uploaded"+file.filename, "a") as f:
#             f.write("This was added later!")
#         return render_template("index.html", btn="download.html")
#
# @app.route("/download")
# def download():
#     return send_file("uploaded"+file.filename, attachment_filename="yourfile.csv", as_attachment = True)
#
# if __name__ =="__main__":
#     app.debug = True
#     app.run()
