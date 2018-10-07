from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Home page"""
    result = db.execute("SELECT cash from users where id = :ID",ID=session["user_id"])
    cash = result[0].get("cash")
    items =  db.execute("SELECT Price, Name, Symbol, Total, Shares,transactions_id  FROM transactions" +
    " WHERE transactions_id = :user_id",user_id=session["user_id"])
    
    
    return render_template("index.html",items=items,cash=cash)
    
    

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        # check quote
        if not request.form.get("symbol"):
            return apology("Empty quote?!")
        info = lookup(request.form.get("symbol"))    
        if (info == None):
            return apology("Invalid symbol!!")
        
        # check shares    
        shares = int(request.form.get("shares"))
        if shares <= 0 or shares == None:
            return apology("+ve shares!")
        
        # check cash    
        price = info.get("price") 
        result = db.execute("SELECT cash from users where id = :ID",ID=session["user_id"])
        cash = result[0].get("cash")
        if ( cash < price * shares):
            return apology("Too Poor!")
        
        # update cash
        ID = session["user_id"]
        ins_2 = db.execute("UPDATE 'users' SET cash = cash - :sum  where id = :id",sum=price*shares,id=session["user_id"])
        
        
        
        # check existing shares
        shr = db.execute("SELECT Shares from transactions where transactions_id = :ID"
        + " and Symbol = :symb",ID = session["user_id"],symb=info["symbol"])
        
        
        if len(shr) >= 1:
            # update existing stocks
            shrno = shr[0].get("Shares") + shares
            ins_3 = db.execute("UPDATE 'transactions' SET Shares = :shrs where transactions_id = :tid"
            + " and Symbol = :symb",shrs=shrno,tid=session["user_id"],symb=info["symbol"])
            history = db.execute("INSERT INTO 'history' ('history_id','Symbol','Type','Price','Shares')" +
            " VALUES (:h_id,:symbol,:type,:price,:shares)",h_id=session["user_id"],symbol=info["symbol"],type="BOUGHT",price=price,shares=shares)
        else:
            # insert stocks
            ins = db.execute("INSERT INTO 'transactions' ('Symbol','Name','Shares','Price','Total','transactions_id') VALUES(:symbol,:name,"
            + ":share,:price,:total,:t_id)",symbol=info["symbol"],name=info["name"],share=shares,price=price,total=price*shares,t_id=session["user_id"])
            history = db.execute("INSERT INTO 'history' ('history_id','Symbol','Type','Price','Shares')" +
            " VALUES (:h_id,:symbol,:type,:price,:shares)",h_id=session["user_id"],symbol=info["symbol"],type="BOUGHT",price=price,shares=shares)
        
        return redirect(url_for("index")) 
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    items =  db.execute("SELECT * FROM history" +
    " WHERE history_id = :user_id",user_id=session["user_id"])
    return render_template("history.html",items=items)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("quote"):
            return apology("Empty quote?!")
        info = lookup(request.form.get("quote"))    
        if (info == None):
            return apology("Invalid quote!!")
        return render_template("results.html",info=info) 
    else:
        return render_template("quote.html")
 

@app.route("/money", methods=["GET", "POST"])
def money():
    ins_2 = db.execute("UPDATE 'users' SET cash = cash + :sum  where id = :id",sum=5000,id=session["user_id"])
    return render_template("money.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST" :

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        elif not request.form.get("confirm_password"):
            return apology("must retype password")
        
        hash_pwd2 = pwd_context.encrypt(request.form.get("confirm_password"))
        hash_pwd = pwd_context.encrypt(request.form.get("password"))  
        
        if request.form.get("confirm_password") != request.form.get("password"):
            return apology("Passwords must match :|") 
        
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username,:hash)",
        username=request.form.get("username"),hash=hash_pwd)
       
        
        if not result:
            return apology("You exist previously -_-")
        
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    return apology("ERROR 404 :O")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        # check quote
        if not request.form.get("symbol"):
            return apology("Empty quote?!")
        info = lookup(request.form.get("symbol"))    
        if (info == None):
            return apology("Invalid symbol!!")
        
        # check shares    
        shares = int(request.form.get("shares"))
        if shares < 0 or shares == None:
            return apology("+ve shares!")
        
        # check cash    
        t_id = session["user_id"]
        price = info.get("price") 
        result = db.execute("SELECT cash from users where id = :ID",ID=t_id)
        cash = result[0].get("cash")
        
        
        # do you even have those shares?!
        # symbol_info = db.execute("SELECT Symbol from transactions where symbol = :SYMB" +
        # " and transactions_id=:t_id",SYMB=lookup(request.form.get("symbol")),t_id=t_id )
        # if symbol_info == None :
        #     return apology("Non existent shares!")
        share_info = db.execute("SELECT Shares from 'transactions' where Symbol = :SYMB and transactions_id=:t_id",SYMB=info["symbol"],t_id=t_id) 
        
        print(share_info,info,t_id)
        if share_info == None or len(share_info)== 0:
            return apology("SHARE KARO!")
        curr_shr = share_info[0].get("Shares")
        
        if shares > curr_shr:
            return apology("Insufficient shares")
        
        # update cash
        ins_2 = db.execute("UPDATE 'users' SET cash = cash + :sum  where id = :id",sum=price*shares,id=t_id)
        
        if shares != curr_shr:
            rem_1 = db.execute("UPDATE 'transactions' SET Shares = :shrs where transactions_id = :tid"
            + " and Symbol = :symb",shrs= curr_shr - shares,tid=t_id,symb=info["symbol"])
            history = db.execute("INSERT INTO 'history' ('history_id','Symbol','Type','Price','Shares')" +
            " VALUES (:h_id,:symbol,:type,:price,:shares)",h_id=t_id,symbol=info["symbol"],type="SOLD",price=price,shares=shares)
        else:
            rem_2 = db.execute("DELETE FROM 'transactions' WHERE Symbol = :SYMB and transactions_id=:t_id",SYMB=info["symbol"],t_id=t_id)
        
        return redirect(url_for("index"))    
                    
    else:
        return render_template("sell.html")
    
        