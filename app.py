from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3, hashlib, os, utils
from utils import auth, posts, topic, comments, revisions

app = Flask(__name__)
app.secret_key=os.urandom(32)

@app.route("/", methods=['POST','GET'])
def home():
    if 'username' in session:
        if 'lang' in request.form:
            posts=topic.selectPosts(request.form['lang'])
        else:
            posts=topic.displayPosts()
        posts.reverse()
        return render_template("home.html",posts=posts,optList=languageList(),uLangs = topic.getLanguages(session["username"]))
    return render_template("login.html",message="")


@app.route("/login", methods=['POST'])
def login():
    password = hashlib.sha256(request.form['pw'])
    x=auth.userLogin(request.form['username'],password.hexdigest())
    if x[0]=='True':
        session['username'] = request.form['username']
        return redirect("/")
    if x[0]=='False':
        return render_template("login.html",message=x[1])

@app.route("/register", methods=['GET','POST'])
def register():
    m = request.args.get("message")
    if m == None:
        m = ""
    return render_template("register.html",langs=languageListAll(),message=m)

@app.route("/createAccount", methods=['POST'])
#routing is still messed up
def createAccount():
    if (request.form['plang2'] == None):
        plangs = request.form['plang1']
    else:
        plangs = request.form['plang1'] + "," + request.form['plang2']
    x=auth.addUser(request.form['username'],request.form['pw'],request.form['pwc'],plangs,request.form['nlang'])
    if x==1:
        return redirect(url_for("login",message = "Account successfully created"))
        #return render_template("login.html",message="account successfully created")
    if x==2:
        #return render_template("register.html",message="invalid character in username")
        return redirect(url_for("register",message="Invalid character in username"))
    if x==3:
        #return render_template("register.html",message="password too short")
        return redirect(url_for("register",message="Password too short"))
    if x==4:
        #return render_template("register.html",message="username already in use")
        return redirect(url_for("register",message="Username already in use"))
    if x==5:
        #return render_template("register.html",message="passwords do not match")
        return redirect(url_for("register",message="Passwords do not match"))

@app.route("/logout")
def logout():
    if not 'username' in session:
        return redirect("/")
    session.pop('username')
    return render_template("login.html",message="logged out")

@app.route("/viewPost", methods=['POST'])
def viewPost():
    if not 'username' in session:
        return redirect("/")
    #print request.form['c']
    #post=[request.form['e'],request.form['a'],request.form['b'],request.form['c'],request.form['d']]
    p = posts.viewPost(request.form['a'])
    c=comments.getComments(request.form['a'])
    e=revisions.getRevisions(request.form['a'])
    print "CCCCCCC"
    print c
    return render_template("viewPost.html",post=p,comments=c,edits=e,optList=languageList(),defaultKeyboard="English")


@app.route("/writeComment", methods=['POST'])
def writeComment():
    if not 'username' in session:
        return redirect("/")
    comments.addComment(session['username'],request.form['pid'],request.form['com'])
    p=posts.viewPost(request.form['pid'])
    c=comments.getComments(request.form['pid'])
    e=revisions.getRevisions(request.form['pid'])
    return render_template("viewPost.html",post=p,comments=c,edits=e,defaultKeyBoard=getKeyboard(p[4]))

@app.route("/makeEdit",methods=['POST'])
def makeEdit():
    if not 'username' in session:
        return redirect("/")
    revisions.addRevision(session['username'],request.form['pid'],request.form['rev'])
    p=posts.viewPost(request.form['pid'])
    c=comments.getComments(request.form['pid'])
    e=revisions.getRevisions(request.form['pid'])
    print "EEEE"
    print e
    return render_template("viewPost.html",post=p,comments=c,edits=e)    

@app.route("/changeLang",methods=['POST'])
def changeLang():
    if not 'username' in session:
        return redirect('/')
    print "RRRRRRR"
    print request.form["plang1"]
    y=[]
    y.append(request.form["plang1"])
    y.append(request.form["plang2"])
    auth.changeLanguages(y,session['username'])
    return redirect('/account')


@app.route("/account")
def account():
    if not 'username' in session:
        return redirect("/")
    #Example of array
    #posts=[["username",0,"This is Title","Post Content blah","language"],["username",0,"This is Title","Post Content blah","language"]]
    postss=auth.getPostsByUser(session['username'])
    postss.reverse()
    c=auth.getContributionsByUser(session['username'])
    c.reverse()
    langs = topic.getLanguages(session['username'])
    native = langs.pop(0)
    return render_template("account.html",posts=postss,comments=c,prefs = langs,native = native, optList = languageListAll())

@app.route("/createPost")
def createPost():
    if not 'username' in session:
        return redirect("/")
    return render_template("writePost.html",optList=languageListAll())

@app.route("/writePost",methods=['POST'])
def writePost():
    if not 'username' in session:
        return redirect("/")
    posts.addPost(session['username'],request.form['title'],request.form['words'],request.form['postLang'])
    return redirect("/")

languageKeysAll={
    'ALBANIAN': 'sq',
    'ARABIC': 'ar',
    'ARMENIAN_EASTERN': 'hy_east',
    'ARMENIAN_WESTERN': 'hy_west',
    'BASQUE': 'eu',
    'BELARUSIAN': 'be',
    'BENGALI_PHONETIC': 'bn_phone',
    'BOSNIAN': 'bs',
    'BRAZILIAN_PORTUGUESE': 'pt_br',
    'BULGARIAN': 'bg',
    'CATALAN': 'ca',
    'CHEROKEE': 'chr',
    'CROATIAN': 'hr',
    'CZECH': 'cs',
    'CZECH_QWERTZ': 'cs_qwertz',
    'DANISH': 'da',
    'DARI': 'prs',
    'DUTCH': 'nl',
    'DEVANAGARI_PHONETIC': 'deva_phone',
    'ENGLISH': 'en',
    'ESTONIAN': 'et',
    'ETHIOPIC': 'ethi',
    'FINNISH': 'fi',
    'FRENCH': 'fr',
    'GALICIAN': 'gl',
    'GEORGIAN_QWERTY': 'ka_qwerty',
    'GEORGIAN_TYPEWRITER': 'ka_typewriter',
    'GERMAN': 'de',
    'GREEK': 'el',
    'GUJARATI_PHONETIC': 'gu_phone',
    'GURMUKHI_PHONETIC': 'guru_phone',
    'HEBREW': 'he',
    'HINDI': 'hi',
    'HUNGARIAN_101': 'hu_101',
    'ICELANDIC': 'is',
    'ITALIAN': 'it',
    'KANNADA_PHONETIC': 'kn_phone',
    'KAZAKH': 'kk',
    'KHMER': 'km',
    'KOREAN': 'ko',
    'KYRGYZ': 'ky_cyrl',
    'LAO': 'lo',
    'LATVIAN': 'lv',
    'LITHUANIAN': 'lt',
    'MACEDONIAN': 'mk',
    'MALAYALAM_PHONETIC': 'ml_phone',
    'MALTESE': 'mt',
    'MONGOLIAN_CYRILLIC': 'mn_cyrl',
    'MONTENEGRIN': 'srp',
    'NORWEGIAN': 'no',
    'ORIYA_PHONETIC': 'or_phone',
    'PAN_AFRICA_LATIN': 'latn_002',
    'PASHTO': 'ps',
    'PERSIAN': 'fa',
    'POLISH': 'pl',
    'PORTUGUESE': 'pt_pt',
    'ROMANI': 'rom',
    'ROMANIAN': 'ro',
    'RUSSIAN': 'ru',
    'SANSKRIT_PHONETIC': 'sa_phone',
    'SERBIAN_CYRILLIC': 'sr_cyrl',
    'SERBIAN_LATIN': 'sr_latn',
    'SINHALA': 'si',
    'SLOVAK': 'sk',
    'SLOVAK_QWERTY': 'sk_qwerty',
    'SLOVENIAN': 'sl',
    'SOUTHERN_UZBEK': 'uzs',
    'SPANISH': 'es_es',
    'SWEDISH': 'sv',
    'TAMIL_PHONETIC': 'ta_phone',
    'TATAR': 'tt',
    'TELUGU_PHONETIC': 'te_phone',
    'THAI': 'th',
    'TURKISH_F': 'tr_f',
    'TURKISH_Q': 'tr_q',
    'UIGHUR': 'ug',
    'UKRAINIAN_101': 'uk_101',
    'URDU': 'ur',
    'UZBEK_LATIN': 'uz_latn',
    'UZBEK_CYRILLIC_PHONETIC': 'uz_cyrl_phone',
    'UZBEK_CYRILLIC_TYPEWRITTER': 'uz_cyrl_type',
    'VIETNAMESE_TCVN': 'vi_tcvn',
    'VIETNAMESE_TELEX': 'vi_telex',
    'VIETNAMESE_VIQR': 'vi_viqr'
}


languageKeys = {
    'ARABIC': 'ar',
    'BENGALI_PHONETIC': 'bn_phone',
    'CHEROKEE': 'chr',
    'DUTCH': 'nl',
    'ENGLISH': 'en',
    'FINNISH': 'fi',
    'FRENCH': 'fr',
    'GERMAN': 'de',
    'ITALIAN': 'it',
    'KOREAN': 'ko',
    'RUSSIAN': 'ru',
    'SPANISH': 'es_es',
    'URDU': 'ur',
    'VIETNAMESE_TELEX': 'vi_telex',
}


def languageListAll():
    optStr = []
    for key in languageKeys:
        pair = [languageKeys[key],key[0]+key[1:].lower()]
        print pair
        optStr.append(pair)
    #return optStr
    return sorted(optStr, key=lambda x: x[1])

def languageList():
    optStr = []
    langKeys = languageKeys.copy()
    uLangs = topic.getLanguages(session["username"])
    for lang in uLangs:
        langKeys.pop(lang.upper(),None)
    for key in langKeys:
        pair = [langKeys[key],key[0]+key[1:].lower()]
        print pair
        optStr.append(pair)
    #return optStr
    return sorted(optStr, key=lambda x: x[1])

def getKeyboard(lang):
    return languageKeys[lang.upper()]


if __name__ == "__main__":
    app.debug = True
#    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    app.run()
