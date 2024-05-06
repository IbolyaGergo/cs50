import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd, is_password_correct

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    shares = {}
    names = {}
    prices = {}
    for row in db.execute("SELECT symbol, shares FROM purchases WHERE user_id = ?", session["user_id"]):
        if not row["symbol"] in shares:
            shares[row["symbol"]] = row["shares"]
            names[row["symbol"]] = lookup(row["symbol"])["name"]
            prices[row["symbol"]] = lookup(row["symbol"])["price"]
        else:
            shares[row["symbol"]] += row["shares"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    total = cash
    for key in shares:
        total += shares[key] * prices[key]

    return render_template("index.html", shares=shares, names=names, prices=prices, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the field is empty
        if not request.form.get("symbol"):
            return apology("Please enter a symbol", 400)

        # Check if symbol is valid
        if not lookup(request.form.get("symbol")):
            return apology("Invalid symbol", 400)

        # Check if field shares is empty
        if not request.form.get("shares"):
            return apology("Enter number of shares", 400)

        # Check that the number of shares is a positive integer
        if not request.form.get("shares").isnumeric() or float(request.form.get("shares")) < 0:
            return apology("Not a positive integer", 400)

        # Price of the selected share
        price = lookup(request.form.get("symbol"))["price"]

        # Full price of the selected shares
        full_price = int(request.form.get("shares")) * price

        # User's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Check abailable cash
        if full_price > cash:
            return apology("Not enough cash", 403)

        # Update cash of the buyer
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - full_price, session["user_id"])

        shares = request.form.get("shares")
        symbol = lookup(request.form.get("symbol"))["symbol"]
        now = datetime.now()

        db.execute("INSERT INTO purchases (user_id, shares, symbol, dtime, price) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], shares, symbol, now, price)

        # Redirect user to home page
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = []
    for row in db.execute("SELECT symbol, shares, price, dtime FROM purchases WHERE user_id = ?", session["user_id"]):
        # print(row)
        history.append(row)

    return render_template("history.html", history=history)

    return apology("TODO")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the text field is blank
        if not request.form.get("symbol"):
            return apology("Please enter a symbol", 400)

        # Check if symbol is valid
        if not lookup(request.form.get("symbol")):
            return apology("Invalid symbol", 400)

        # Looking up the name, price and symbol of stock

        name = lookup(request.form.get("symbol"))["name"]
        price = lookup(request.form.get("symbol"))["price"]
        symbol = lookup(request.form.get("symbol"))["symbol"]

        return render_template("quoted.html", name=name, price=price, symbol=symbol)

    return render_template("quote.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Account"""
    return render_template("account.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("old"):
            return apology("Missing old password", 403)

        # Ensure old password is correct
        old_hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]["hash"]
        if not check_password_hash(old_hash, request.form.get("old")):
            return apology("incorrect old password", 403)

        # Ensure there is a new password
        if not request.form.get("password"):
            return apology("must provide new password", 403)

        # Ensure there is a new password
        if not request.form.get("confirmation"):
            return apology("must confirm new password", 403)

        # Ensure new password was confirmed
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must be equal", 403)

        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Insert user
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])

        return redirect("/")

    return render_template("change_password.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username does not exist
        for user in db.execute("SELECT username FROM users"):
            if user["username"] == request.form.get("username"):
                return apology("username already exists", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was confirmed
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password confirmation is correct
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must be equal", 400)

        # Check if password contains number, capital letter, special characters and is longer than a specified length
        # if not is_password_correct(request.form.get("password")):
         #   return apology("password is not correct", 403)

        # Generate hash from password
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Insert user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash)

        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    shares_owned = {}
    for row in db.execute("SELECT symbol, shares FROM purchases WHERE user_id = ?", session["user_id"]):
        if not row["symbol"] in shares_owned:
            shares_owned[row["symbol"]] = row["shares"]
        else:
            shares_owned[row["symbol"]] += row["shares"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")

        if not symbol or symbol not in shares_owned:
            return apology("Invalid symbol", 400)

        if not request.form.get("shares"):
            return apology("Number of shares required", 400)

        shares = int(request.form.get("shares"))

        if shares > shares_owned[symbol]:
            return apology("Too many shares", 400)
        else:
            # Selling price of shares
            price = lookup(request.form.get("symbol"))["price"]

            # User's cash
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

            # Update cash of the seller
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + shares * price, session["user_id"])

            now = datetime.now()

            # Updating purchases database
            db.execute("INSERT INTO purchases (user_id, shares, symbol, dtime, price) VALUES(?, ?, ?, ?, ?)",
                       session["user_id"], -shares, symbol, now, price)

            return redirect("/")

    return render_template("sell.html", shares_owned=shares_owned)
