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
            temp.append(str(y))
        comments.append(temp)
    db.commit()
    db.close()
    return comments

def getContributionsByUser(username):
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    q="SELECT postID from comments where username=\'"+str(username)+"\'"
    c.execute(q)
    var=c.fetchall()
    comments=[]
    for x in var:
        for y in x:
            comments.append(str(y))
    q="SELECT postID from comments where username=\'"+str(username)+"\'"
    c.execute(q)
    var=c.fetchall()
    for x in var:
        for y in x:
            comments.append(str(y))
    db.commit()
    db.close()
    return list(set(comments))

#testing cases
#print addUser("test","funTimesAhead","funTimesAhead","Spanish,Chinese","English")

#print addUser("&test","funTimesAhead","funTimesAhead","Spanish,Chinese","English")

#print addUser("test","fun","fun","Spanish,Chinese","English")

#print addUser("test","funTimesAhead","funtimesAhead","Spanish,Chinese","English")

#print userLogin("test","funTimesAhead")

#print userLogin("apple","apple")

#print userLogin("test","funny")
