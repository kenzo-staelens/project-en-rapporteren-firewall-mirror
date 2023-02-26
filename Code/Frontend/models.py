import sqlite3 as sql

def retrieveUsers(username, password):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users where username=? and password=?",(username, password))
	user = cur.fetchone()
	con.close()
	return user

def builddb():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.executescript("""
drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);
insert into users(username,password) values('default','creds')
    """)

if __name__ == "__main__":
    builddb()