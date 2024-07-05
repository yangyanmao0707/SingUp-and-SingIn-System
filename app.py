import pymongo
from flask import *

client=pymongo.MongoClient("mongodb+srv://yangyanmao0909:<password>@cluster0.6v6xga9.mongodb.net/") #換成你的mongodb註冊的金鑰
db=client.member_system

print("資料庫連線成功")




app=Flask(
__name__,
static_folder="public",
static_url_path="/"
)

app.secret_key="any string but secret"



@app.route("/")
def index():
    return render_template("index.html")



@app.route("/data")
def member():


    if "nickname" in session:
        return render_template("data.html")
    else:

        return redirect("/")

@app.route("/error")
def error():
    message=request.args.get("msg","發生錯誤,請聯繫客服")
    return render_template("error.html", message=message)

@app.route("/signup",methods=["POST"])
def signup():

    nickname=request.form["nickname"]
    email=request.form["email"]
    password=request.form["password"]

    collection=db.user

    result=collection.find_one({
    "email":email
    })
    if result !=None:
        return redirect("/error?msg=帳號已經被註冊")

    collection.insert_one({
    "nickname":nickname,
    "email":email,
    "password":password
    })
    return redirect("/")

@app.route("/signin", methods=["POST"])
def signin():

    email=request.form["email"]
    password=request.form["password"]

    collection=db.user

    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })  

    if result is None:
      return redirect("/error?msg=帳號或密碼輸入錯誤")

    session["nickname"]=result["nickname"]

    return redirect("/data")


@app.route("/signout")
def signout():

    del session["nickname"]
    return redirect("/")

app.run(port=3000)