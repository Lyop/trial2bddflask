from flask import g
import sqlite3 as sql


#  Function to connect

def connecter_bdd():
    conn = sql.connect('app.db')
    conn.row_factory = sql.Row # a dictionary is sent back
    return conn

def obtenir_bdd():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connecter_bdd()
    return d.sqlite_db