import hashlib, sqlite3, string


def addUser(user, password, prefLang, nativeLang):
    if (special(user)):
        return 2
        #Error: Invalid character in username
    if (len(password)<8):
        return 3
        #"Error: Password too short"
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    q='SELECT * FROM users'
    c.execute(q)
    userInfo=c.fetchall()
    for data in userInfo:
        if (user in data):
            db.close()
            return 4
            #Error: Username already in use
    q="INSERT INTO users VALUES (\""+user+'\", \"'+myHashObj.hexdigest()+'\",' +prefLang+"\",\""+ nativeLang + "\")"
    print q
    c.execute(q)
    db.commit()
    db.close()
    return 1
    #Account successfully created

def userLogin(user, password):
    db=sqlite3.connect('data/info.db')
    c=db.cursor()
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    q='SELECT username FROM users'
    c.execute(q)
    data=c.fetchall()
    for stuff in data:
        if(user in stuff):
            q='SELECT password FROM users WHERE username = "'+user+'";'
            c.execute(q)
            password=c.fetchall()
            q='SELECT userID From users WHERE username = "'+user+'";'
            c.execute(q)
            stuff=c.fetchall()
            db.close()
            if(myHashObj.hexdigest()==password[0][0]):
                return ['True', str(stuff[0][0])]
    db.close()
    return ['False', 'bad user/pass']

def special(user):
    return any((ord(char)<48 or (ord(char)>57 and ord(char)<65) or (ord(char)>90 and ord(char)<97) or ord(char)>123) for char in user)
