# Import flask and its components.
from flask import *

# Import the pymysql module - It helps us to create a connection between python flask and mysql database.
import pymysql

# Create an flask application and give it a name.
app = Flask (__name__)


# Below is the sign up route.
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method == "POST":
        # Extract the different details entered on the form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # By use of the print function lets print all those details sent with the upcoming request
        # print(username, email, password, phone)

        # Establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # Create a cursor to execute the sql queries
        cursor = connection.cursor()

        # Structure an sql to insert the details received from the form
        # The %s is a placeholder -> A placeholder stands in places of actual values i.e. we shall replace later on
        sql = "INSERT INTO users(username,email,phone,password) VALUES(%s, %s, %s, %s)"

        # Create a tuple that will hold all the data gotten from the form
        data = (username, email, phone, password)

        # By use of the cursor execute the sql as you replace the placeholder with the actual values
        cursor.execute(sql, data) 

        # commit the changes to the database
        connection.commit()


        return jsonify({"message" : "User registered successfully"})




# Below is the login/sign In Route
@app.route("/api/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        # Extract the two details entered
        email = request.form["email"]
        password = request.form["password"]

        # Print out the details entered
        # print(email, password)

        # Create/establish a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # Create cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Structure the sql query that will check whether the email and tha password entered are correct
        sql = "SELECT * FROM users WHERE email = %s AND password = %s;"

        # Put the data received from the form into a tuple
        data = (email, password)

        # By use of the cursor execute the sql
        cursor.execute(sql, data)

        # Check whether there are rows returned and store them on a variable
        count = cursor.rowcount


        # If there are records returned it means that the password and the email are correct otherwise they are wrong.
        if count == 0:
            return jsonify({"message" : "Login Failed"})
        else:
            # There must be a user so we create a variable that will hold the details of the users fetched from the database
            user=cursor.fetchone()
            # Return the details to the front end as well as the message
            return jsonify({"message" : "User Loggged In successfully", "user":user})
            













# Run the application.
app.run(debug=True)