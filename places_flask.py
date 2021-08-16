  
#This code is  created by Zilong Wu on the 05/05/2021

#These code is where i'll be importing things from
from flask import Flask,g,render_template,request,redirect,logging
import sqlite3
import os

app = Flask(__name__)

#This is where it'll get the file path from
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#This is where the database will be import it from
DATABASE = 'shoes.db'

#This function will create a db conneciton and checks whether the g already has the attribute of underscore database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#This function will get called when the server finishes or stop running, it will close the connection to th database, and will only open when it's required
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#This route will create all the data in my SQL and will be displayed onto a website 
@app.route("/")
def home():
    return render_template("home.html")

#This route will be a about page for my website 
@app.route("/about")
def about():
    return render_template("about.html")

#This route will be a explore page for my website
@app.route("/explore")
def explore():
    cursor = get_db().cursor()
    sql = "SELECT * FROM contents"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("explore.html", results=results)

#This route will let users be able to upload an image of the famous place on to the website 
@app.route('/upload', methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for  file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
    return redirect("/explore")

#The purpose of this route is so that a user can add famous places to the current table
@app.route('/add',methods=["GET","POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_places = request.form["places"]
        new_places_description = request.form["description"]
        new_image=request.form["image"]
        sql = "INSERT INTO contents(name,description,filename) VALUES (?,?,?)"
        cursor.execute(sql,(new_places,new_places_description,new_image))
        get_db().commit()
    return redirect('/explore')

#The purpose of the route is so that user can delete a famous place they desire
@app.route('/delete', methods=["GET","POST"])
def delete():
    if request.method == "POST":
        #get the item and delete from database
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM contents WHERE id =?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/explore')

#The purpose of this route is to sort famous places in continents, e.g. europe
@app.route('/Continent/<int:id>')
def continent(id):
    cursor = get_db().cursor()   
    sql = "SELECT contents.id,contents.Name,contents.description,contents.filename,continent.continentname FROM contents JOIN continent ON contents.Continent=continent.id WHERE contents.Continent=? "
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor = get_db().cursor()
    sql = "SELECT continent.id,continent.continentname FROM continent "
    cursor.execute(sql)
    Continent= cursor.fetchall()
    return render_template("continent.html")





@app.route("/contacts")
def contact():
    return render_template("contacts.html")

#The purpose of this route is so that if a user has a question about my website they can ask questions about it and will be stored in my database
@app.route("/message", methods=["POST"])
def message():
    cursor = get_db().cursor()
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    email=request.form["email"]
    message=request.form["message"]
    sql="INSERT INTO contacts(first_name,last_name,email,message) VALUES (?,?,?,?)"
    cursor.execute(sql,(first_name,last_name,email,message))
    get_db().commit()
    return redirect("/contacts")




        









if __name__ =="__main__":
    app.run(debug=True)

