from flask import Flask
import mysql.connector

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SUPER SECURE'
    
    from .views import views

    app.register_blueprint(views, url_prefix = '/')

    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root"
    )

    db = mydb.cursor()

    db.execute("CREATE DATABASE IF NOT EXISTS mymatch")

    db.execute("CREATE TABLE IF NOT EXISTS mymatch.users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(150), password VARCHAR(150))")

    db.execute("CREATE TABLE IF NOT EXISTS mymatch.types (uid INT, type VARCHAR(150), val INT, FOREIGN KEY (uid) REFERENCES Users(id))")

    db.execute("CREATE TABLE IF NOT EXISTS mymatch.matches (uid INT, person_name VARCHAR(150), score INT NOT NULL, mytypes JSON, typevals JSON, FOREIGN KEY (uid) REFERENCES Users(id))")

    return app

