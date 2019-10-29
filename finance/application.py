import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT * FROM users WHERE id = :id",
                        id=session["user_id"])
    cash = int(rows[0]["cash"])
    stocks = db.execute("SELECT symbol, SUM(shares) as sum_shares FROM transactions WHERE id = :user_id GROUP BY symbol HAVING sum_shares > 0", user_id = session["user_id"])
    prices = list()
    values = list()
    for counter, stock in enumerate(stocks):
        quote = lookup(stocks[counter]["symbol"])
        prices.append(quote["price"])
        value = int(quote["price"] * stocks[counter]["sum_shares"])
        values.append(value)
    total_value = sum(values)
    return render_template("index.html", stocks = stocks, prices = prices, values = values, total_value = total_value, cash = cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        #  Ensure quote and shares was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)
        if not request.form.get("shares"):
            return apology("must provide amount of shares", 400)

        # Ensure shares is a positive integer
        shares = request.form.get("shares")
        if not shares.isdigit():
            return apology("must enter a positive integer", 400)

        shares = int(request.form.get("shares"))
        # Get quote
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("please enter a valid quote", 400)

        # Ensure cost is not too high
        share_price = quote["price"]
        cost = share_price * shares
        rows = db.execute("SELECT * FROM users WHERE id = :id",
                            id=session["user_id"])
        cash = rows[0]["cash"]

        if cost > cash:
            return apology("not enough cash")

        symbol = quote["symbol"]
        # If successful update database cash amount
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id", cost = cost, id = session["user_id"])
        # Add transaction to history
        db.execute("Insert INTO transactions (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :cost)",
                    id = session["user_id"], symbol = quote["symbol"], shares = shares, cost = cost)
        return redirect("/")

        if quote == None:
            return apology("please enter a valid quote", 200)
    else:
        return render_template("buy.html")

@app.route("/trending", methods=["GET", "POST"])
@login_required
def trending():
    stocks = db.execute("SELECT COUNT(id) as count_id, symbol, SUM(shares) as sum_shares FROM transactions GROUP BY symbol ORDER BY count_id DESC")
    prices = list()
    for counter, stock in enumerate(stocks):
        quote = lookup(stocks[counter]["symbol"])
        prices.append(quote["price"])
    return render_template("trending.html", stocks = stocks, prices = prices)

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    usernames = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    if username and not usernames:
        return jsonify(True)
    else:
        return jsonify(False)

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT symbol, price, date, shares FROM transactions WHERE id=:user_id", user_id=session["user_id"])
    values = list()
    boo = list()
    shares = list()
    for counter, stock in enumerate(stocks):
        price = stocks[counter]["price"]
        shares_count = stocks[counter]["shares"]
        if shares_count < 0:
            boo.append("Sold")
            price = price * (-1)
            shares_count = shares_count * (-1)
            shares.append(shares_count)
            values.append(price)
        else:
            boo.append("Bought")
            values.append(price)
            shares.append(shares_count)

    return render_template("history.html", stocks = stocks, boo = boo, values = values, shares = shares)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        #  Ensure quote was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("please enter a valid quote", 400)

        return render_template("quoted.html", quote = quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Create hash for password
        hash = generate_password_hash(request.form.get("password"))

        # Insert username into database
        result = db.execute("Insert INTO users (username, hash) VALUES(:username, :hash)", username = request.form.get("username"), hash = hash)

        # Check if username is already taken
        if not result:
            return apology("Username has been taken", 400)

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT symbol, SUM(shares) as sum_shares FROM transactions WHERE id = :user_id GROUP BY symbol HAVING sum_shares > 0", user_id = session["user_id"])
    if request.method == "POST":
        # Ensure symbol and shares are submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must choose a symbol", 400)
        shares = request.form.get("shares")
        if not shares:
            return apology("must enter shares amount", 400)


        # Ensure shares is a positive integer
        shares = int(request.form.get("shares"))
        if not type(shares) == int:
            return apology("must enter an integer", 400)
        if shares < 1 :
            return apology("must enter a positive integer", 400)

        # Ensure proper amount of shares
        sum_shares = stocks[0]["sum_shares"]
        if shares > sum_shares:
            return apology("invalid shares amount", 400)

        # Get quote
        quote = lookup(request.form.get("symbol"))

        # Log loss of shares and increase in cash
        share_price = quote["price"]
        cost = share_price * shares * (-1)
        shares = shares * (-1)

        symbol = quote["symbol"]
        # If successful update database cash amount
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id", cost = cost, id = session["user_id"])
        # Add transaction to history
        db.execute("Insert INTO transactions (id, symbol, shares, price) VALUES(:id, :symbol, :shares, :cost)",
                    id = session["user_id"], symbol = quote["symbol"], shares = shares, cost = cost)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
