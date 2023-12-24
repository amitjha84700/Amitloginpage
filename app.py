from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="123456", database="login"
)
cursor = mydb.cursor()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("SELECT * FROM signup WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        stored_password = result[3]
        if password == stored_password:
            return f"Hi {result[1]}, welcome to our world"
        else:
            return "Incorrect password. Please try again."
    else:
        return "Username not found. Please sign up."


@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    cont = request.form["cont"]
    mail = request.form["mail"]
    gender = request.form["gender"]
    username = request.form["username"]
    create_pswd = request.form["create_pswd"]
    cnfirm_pswd = request.form["cnfirm_pswd"]

    if create_pswd == cnfirm_pswd:
        sql = "INSERT INTO signup (name, cont, mail, gender, username, create_pswd, cnfirm_pswd) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (name, cont, mail, gender, username, create_pswd, cnfirm_pswd)
        cursor.execute(sql, values)
        mydb.commit()
        return "Thank you for sign-up, your credentials are saved"
    else:
        return "Check your password"


if __name__ == "__main__":
    app.run(debug=True)
