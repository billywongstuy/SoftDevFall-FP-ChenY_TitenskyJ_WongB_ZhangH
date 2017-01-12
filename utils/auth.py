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
            if(pw==password[0][0]):
                return ['True', 'success']
            else:
                return ['False', 'bad pass']
    db.close()
    return ['False', 'bad user']

def special(user):
    return any((ord(char)<48 or (ord(char)>57 and ord(char)<65) or (ord(char)>90 and ord(char)<97) or ord(char)>123) for char in user)



#testing cases
#print addUser("test","funTimesAhead","funTimesAhead","Spanish,Chinese","English")

#print addUser("&test","funTimesAhead","funTimesAhead","Spanish,Chinese","English")

#print addUser("test","fun","fun","Spanish,Chinese","English")

#print addUser("test","funTimesAhead","funtimesAhead","Spanish,Chinese","English")

#print userLogin("test","funTimesAhead")

#print userLogin("apple","apple")

#print userLogin("test","funny")
