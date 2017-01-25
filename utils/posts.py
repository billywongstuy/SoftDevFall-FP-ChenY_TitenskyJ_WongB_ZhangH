import csv
import sqlite3

def addPost(user, title, content, language):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT MAX(postID) FROM posts"
	c.execute(q)
	lastPostID=c.fetchall()[0][0]
	if lastPostID is None:
		lastPostID=0
                print "Nothing"
        else:
                lastPostID += 1
	print lastPostID
        utitle = title
        utitle.encode("utf-8")
        ucon = content
        ucon.encode("utf-8")
	q="INSERT INTO posts VALUES (\'"+user+"\', "+ str(lastPostID) + ", \'" + utitle+ "\', \'" + ucon + "\', \'"+language+"\')"
	#print q
	c.execute(q)
	db.commit()
	db.close()

def viewPost(postID):
	db=sqlite3.connect('data/info.db')
	c=db.cursor()
	q="SELECT * from posts where postID="+str(postID)+""
	c.execute(q)
	postTuple=c.fetchall()[0]
	post=[]
        #append each item
        for item in postTuple:
                try:
                        u = str(item)
                        u.decode("utf-8")
                except:
                        u = item
                post.append(u)
	c.execute(q)
	db.commit()
	db.close()
	return post

