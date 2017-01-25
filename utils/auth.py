import hashlib, sqlite3, string

def addUser(user, password, cPass, prefLang, nativeLang):
    if (special(user)):
        return 2
        #Error: Invalid character in username
    if (len(password)<8):
        return 3
        #"Error: Password too short"
    if (password!=cPass):
        return 5
        #Error: Passwords do not match
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    myHashObj=hashlib.sha256()
    myHashObj.update(password)
    print "pc: " + myHashObj.hexdigest()
    q='SELECT * FROM users'
    c.execute(q)
    userInfo=c.fetchall()
    for data in userInfo:
        if (user in data):
            db.close()
            return 4
            #Error: Username already in use
    q="INSERT INTO users VALUES (\""+user+'\", \"'+myHashObj.hexdigest()+'\",' + "\"" + prefLang+"\",\""+ nativeLang + "\")"
    #print q
    c.execute(q)
    db.commit()
    db.close()
    return 1
    #Account successfully created

def userLogin(user, pw):
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    q='SELECT username FROM users'
    c.execute(q)
    data=c.fetchall()
    for stuff in data:
        if(user in stuff):
            q='SELECT password FROM users WHERE username = "'+user+'";'
            c.execute(q)
            password=c.fetchall()
            #q='SELECT userID From users WHERE username = "'+user+'";'
            #c.execute(q)
            #stuff=c.fetchall()
            db.close()
            print password[0][0]
            print pw
            if(pw==password[0][0]):
                return ['True', 'Login Successful']
            else:
                return ['False', 'Incorrect Password']
    db.close()
    return ['False', 'Username Does Not Exist']

def special(user):
    return any((ord(char)<48 or (ord(char)>57 and ord(char)<65) or (ord(char)>90 and ord(char)<97) or ord(char)>123) for char in user)

def getPostsByUser(username):
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    q="SELECT * from posts where username=\'"+str(username)+"\'"
    c.execute(q)
    var=c.fetchall()
    comments=[]
    for x in var:
        temp=[]
        for y in x:
            try:
                u = str(y)
                u.decode("utf-8")
            except:
                u = y
	    temp.append(u)
        comments.append(temp)
    db.commit()
    db.close()
    print comments
    print "YEEEEEEEEEE"
    return comments

def getContributionsByUser(username):
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    q="SELECT postID from comments where username=\'"+str(username)+"\'"
    c.execute(q)
    var=c.fetchall()
    pids = []
    for item in var:
        if item[0] not in pids:
            pids.append(item[0])
    q="SELECT postID from revisions where username=\'"+str(username)+"\'"
    c.execute(q)
    var2 = c.fetchall()
    for item in var2:
        if item[0] not in pids:
            pids.append(item[0])
    pids.sort()
    posts =[]
    for pid in pids:
        q="SELECT * from posts where postId=" + str(pid)
        c.execute(q)
        pt = c.fetchall()[0]
        p = []
        for item in pt:
            try:
                u = str(item)
                u.decode("utf-8")
            except:
                u = item
            p.append(u)
        posts.append(p)
    return posts
    

def changeLanguages(newLangs, username):
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    q="UPDATE users SET prefLang=\'"+ str(newLangs[0]+','+newLangs[1]) + "\' where username=\'"+str(username)+"\'"
    print q
    c.execute(q)
    db.commit()
    db.close()


#testing cases
#print addUser("test","funTimesAhead","funTimesAhead","Spanish,Chinese","English")

#print addUser("&test","funTimesAhead","funTimesAhead","Spanish,Chinese","English")

#print addUser("test","fun","fun","Spanish,Chinese","English")

#print addUser("test","funTimesAhead","funtimesAhead","Spanish,Chinese","English")

#print userLogin("test","funTimesAhead")

#print userLogin("apple","apple")

#print userLogin("test","funny")
