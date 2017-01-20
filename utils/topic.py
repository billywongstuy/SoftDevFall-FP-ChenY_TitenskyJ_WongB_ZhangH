import csv
import sqlite3

def displayPosts():
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * FROM posts"
	c.execute(q)
	var=c.fetchall()
	print var
	posts=[]
	for x in var:
		temp=[]
		for y in x:
			temp.append(str(y))
		posts.append(temp)
	db.commit()
	db.close()
	return posts
	db.commit()
	db.close()

#First item in returned list is the user's native language
def getLanguages(username):
	langs=[]
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT nativeLang FROM users WHERE username=\'"+username+"\'"
	c.execute(q)
	nativeLang=c.fetchall()[0][0]
	langs.append(str(nativeLang))

	q="SELECT prefLang FROM users WHERE username=\'"+username+"\'"
	c.execute(q)
	pref=c.fetchall()[0][0]
	prefLangs=pref.split(',')
	for x in prefLangs:
		langs.append(str(x))
	return langs

#DOES NOT WORK YET ---- TAKES IN EITHER STRING OR LIST OF STRINGS (LANGUAGES)
def selectPosts(language):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * FROM posts"
	c.execute(q)
	var=c.fetchall()
	print var
	posts=[]
	for x in var:
		temp=[]
		for y in x:
			temp.append(str(y))
		posts.append(temp)
	db.commit()
	db.close()
	return posts

	


