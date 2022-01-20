from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "#%^@#&*2923248734249)@(#&@^_wwwre2u45lp"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes = 10)

 
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    tb_name = db.Column("name", db.String(100))
    tb_email = db.Column("email", db.String(100)) #You dont need to write the name since if name is not written the database takes the name of the variable as the default row name

    def __init__(self, name, email):
        self.tb_name = name
        self.tb_email = email



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/view")
def view():
    return render_template("view.html", view_var = users.query.all())

@app.route("/delete")
def delete():
    if "user_key" and "email_key" in session:
        del_user = session["user_key"]
        del_email = session["email_key"]
        users.query.filter_by(tb_name = del_user).delete()
        users.query.filter_by(tb_email = del_email).delete()
        db.session.commit()
        flash("Record Deleted Successfully!")

    elif "user_key" in session and "email_key" not in session:
        del_user = session["user_key"]

        if not users.query.filter_by(tb_name = del_user).first():
            flash("Unable to delete since there is no record found!")

        else:
            users.query.filter_by(tb_name = del_user).delete()
            db.session.commit()
            flash("Record Deleted Successfully!")

    else:
        flash("Unable to delete Record")

    return redirect(url_for("user_method"))

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user_key"] = user

        found_user = users.query.filter_by(tb_name = user).first()

        if found_user: #if user query is returned
            session["email_key"] = found_user.tb_email
        
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user_method"))
    else:
        if "user_key" in session:
            flash("Already Logged In!")
            return redirect(url_for("user_method"))
        else:
            return render_template("login.html")


@app.route("/user", methods = ["POST", "GET"])
def user_method():
    email = None
    if "user_key" in session:
        user = session["user_key"]

        if request.method == "POST":
            email = request.form["email"]
            session["email_key"] = email 
            found_user = users.query.filter_by(tb_name = user).first()
            found_user.tb_email = email
            db.session.commit()
            flash("Email was saved successfully!")
        else:
            if "email_key" in session:
                email = session["email_key"]

        return render_template("user.html", email_var = email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user_key" in session:
        user = session["user_key"]
        flash(f"{user} has been logged out successfully!", "info")
    session.pop("user_key", None)
    session.pop("email_key", None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    db.create_all()
    app.run(port = 5004, debug=True)
    
