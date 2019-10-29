import os

from math import *
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import numpy as np
import sympy as sp
from sympy import *
from latex2sympy import *
from sympy.parsing.latex import parse_latex



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
def index():
    """Intro to website"""
    return render_template("index.html")

@app.route("/differentiation", methods=["GET", "POST"])
@login_required
def differentiation():
    if request.method == "POST":
        # Check if inputs were given
        if not request.form.get("function"):
            return apology("must provide a function", 400)
        f = request.form.get("function")
        x = symbols('x')
        f = sympify(f)

        # Differentiate and return latex expressions
        fprime = latex(f.diff(x))
        value = latex(f)
        return render_template("differentiated.html", value=value, fprime=fprime)
    else:
        return render_template("differentiation.html")

@app.route("/integration", methods=["GET", "POST"])
@login_required
def integration():
    if request.method == "POST":
        # Check if inputs were given
        if not request.form.get("function"):
            return apology("must provide a function", 400)

        # Integrate and return latex expressions
        f = request.form.get("function")
        x = symbols('x')
        f = sympify(f)
        fintegral = latex(f.integrate(x))
        value = latex(f)
        return render_template("integrated.html", value=value, fintegral=fintegral)
    else:
        return render_template("integration.html")

@app.route("/riemann", methods = ["GET", "POST"])
@login_required
def riemann():
    if request.method == "POST":
        # Check if inputs were given
        if not request.form.get("function"):
            return apology("must provide a function", 400)
        if not request.form.get("lowerbound"):
            return apology("must provide a lower bound", 400)
        if not request.form.get("upperbound"):
            return apology("must provide an upper bound", 400)
        if not request.form.get("subintervals"):
            return apology("must provide a number of subintervals", 400)
        if not request.form.get("sumtype"):
            return apology("must choose left or right", 400)

        # Get inputs, check for validity and sympify
        f = request.form.get("function")
        sumtype = request.form.get("sumtype")
        lb = int(request.form.get("lowerbound"))
        ub = int(request.form.get("upperbound"))
        si = int(request.form.get("subintervals"))
        x = symbols('x')
        f = sympify(f)
        dx = (ub - lb) / si
        value = latex(f)

        # Run through Riemann Sum algorithm, creatings lists for display
        #           of inputs, outputs, and areas (their products)
        inputs = list()
        if sumtype == "1":
            for i in range(0, si):
                inputs.append(dx * (i))
        if sumtype == "2":
            for i in range(0, si):
                inputs.append(dx * (i + 1))
        outputs = list()
        for input in inputs:
            temp = f.subs(x, input)
            outputs.append(temp)
        rectangles = list()
        for output in outputs:
            temp = output * dx
            rectangles.append(temp)
        result = sum(rectangles)

        # Choose template based on left or right sum
        if sumtype == "1":
            return render_template("summed.html", value=value, sumtype=sumtype, lb=lb, ub=ub, si=si, dx=dx,
                                   inputs=inputs, outputs=outputs, rectangles=rectangles, result=result)
        else:
            return render_template("rightSummed.html", value=value, sumtype=sumtype, lb=lb, ub=ub, si=si, dx=dx,
                                   inputs=inputs, outputs=outputs, rectangles=rectangles, result=result)
    else:
        return render_template("riemann.html")


@app.route("/maxmin", methods=["GET", "POST"])
def maxmin():
    if request.method == "POST":
        # Check if inputs were given
        if not request.form.get("function"):
            return apology("must provide a function", 400)
        if not request.form.get("lowerbound"):
            return apology("must provide a lower bound", 400)
        if not request.form.get("upperbound"):
            return apology("must provide an upper bound", 400)

        # Get input from form
        f = request.form.get("function")
        lb = sympify(request.form.get("lowerbound"))
        ub = sympify(request.form.get("upperbound"))

        # Prep input for numpy / sympy
        x = symbols('x')
        f = sympify(f)

        # Get Derivative, solve for real solutions, update candidates list
        fprime = f.diff(x)
        solutions = list()
        solutions.append(f.subs(x,0))
        candidates = list()
        for solution in solutions:
            candidates.append(solution)
        candidates.append(lb)
        candidates.append(ub)

        # Fill values list with solutions
        values = list()
        for candidate in candidates:
            temp = f.subs(x, candidate)
            values.append(temp)

        # Find max/min of values
        maximum = max(values)
        newvar = min(values)

        # Turn all into latex
        value = latex(f)
        fprime = latex(fprime)
        for i, solution in enumerate(solutions):
            solutions[i] = latex(solution)
        return render_template("optimized.html", value=value, fprime=fprime, solutions=solutions, lb=lb, ub=ub,
                               candidates=candidates, newvar=newvar, values=values, maximum=maximum)
    else:
        return render_template("maxmin.html")

@app.route("/aprox", methods=["GET", "POST"])
def aprox():
    if request.method == "POST":
        # Check if inputs were given
        if not request.form.get("function"):
            return apology("must provide a function", 400)
        if not request.form.get("easy"):
            return apology("must provide an easy value", 400)
        if not request.form.get("hard"):
            return apology("must provide a difficult value", 400)

        # Get inputs, sympify them, and check to see if valid
        f = request.form.get("function")
        a = request.form.get("easy")
        h = request.form.get("hard")
        x = symbols('x')
        f = sympify(f)
        a = sympify(a)
        h = sympify(h)
        if not a.is_number:
            return apology("easy value must be a number", 400)
        if not h.is_number:
            return apology("difficult value must be a number", 400)

        # Run through Linearization algorithm
        fprime = f.diff(x)
        fa = f.subs(x, a)
        fprimea = fprime.subs(x, a)
        lh = fa + fprimea*(float(h)-float(a))

        # Convert to latex for MathJax reading
        value = latex(f)
        fprime = latex(fprime)
        fa = latex(fa)
        lh = latex(lh)

        return render_template("aproxd.html", value=value, fprime=fprime, a=a, h=h, fa=fa, fprimea=fprimea, lh=lh)
    else:
        return render_template("aprox.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    usernames = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    if username and not usernames:
        return jsonify(True)
    else:
        return jsonify(False)

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

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
