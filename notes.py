from flask import Flask,render_template,redirect,request,url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key = "dev-secret"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/sign_up",methods = ["GET","POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        useremail = request.form.get('useremail')

        conn = sqlite3.connect("notes.db")
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE user_name  =  ?  AND user_password = ? AND user_email = ?",(username,password,useremail))

        result = c.fetchone()
        result = result[0]

        if result:
            return "Account Already Exists"
            conn.close()
        else :
            c.execute("INSERT INTO users(user_name,user_email,user_password) VALUES(?,?,?)",(username,useremail,password))
            return "Account has been created"
            conn.commit()
            conn.close()



    return render_template("sign_up.html")

@app.route("/user_authentication", methods = ["POST"])
def user_authentication():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return("Invalid data",400)

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT user_id,user_name, user_password FROM users WHERE user_name = ? AND user_password = ?",(username,password))


    result = c.fetchone()
    conn.close()
    
    if not result:
        return redirect(url_for("sign_up"))

    if result:
        uid = result[0]
        session["uid"]  = uid
        
        return redirect(url_for("notes_menu"))




@app.route("/notes_menu")
def notes_menu():
    if "uid" not in session:
        return redirect(url_for("user_authentication"))
    return render_template("notes.html")


@app.route("/add_notes",methods = ["GET","POST"])
def add_notes():
    if "uid" not in session:
          return redirect(url_for("user_authentication"))
       
    if session["uid"]:
        uid = session["uid"]

    if request.method == "POST":
        content = request.form.get('content')
        if not content:
            return("Cannot create empty note",400)
      
        conn = sqlite3.connect("notes.db")
        c = conn.cursor()
        c.execute("INSERT INTO notes(user_id,note_content) VALUES(?,?)",(uid,content))
        conn.commit()
        conn.close()
        return redirect(url_for("notes_menu"))    
    return render_template("add_notes.html")




   





if __name__ == "__main__":
    app.run(debug = True)

    


