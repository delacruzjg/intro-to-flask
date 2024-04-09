from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'


logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))

    return render_template('branchdetails.html', code=code, branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_successful, user = authentication.login(username, password)
        app.logger.info('%s', is_successful)
        if(is_successful):
            session["user"] = user
            return redirect('/')
        else:
            error = "Invalid username or password. Please try again."
    return render_template('login.html', error=error)

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a 
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/updatecart', methods=['POST'])
def updatecart():
    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    for code in cart:
        qty = request.form.get('qty_'+code)
        product = db.get_product(int(code))
        item=dict()

        item["qty"] = int(qty)
        item["name"] = product["name"]
        item["subtotal"] = product["price"]*item["qty"]

        cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/removefromcart', methods=['GET'])
def removefromcart():
    code = request.args.get('code', '')
    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    if code in cart:
        del cart[code]
    session["cart"]=cart
    return redirect('/cart')

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route('/pastorders', methods=['GET'])
def pastorders():
    pastorder_list = db.get_pastorders(session["user"])
    return render_template('past orders.html', page="Past Orders", pastorder_list=pastorder_list)

@app.route('/changepass')
def changepass():
    return render_template('changepass.html')

@app.route('/firstcpa', methods = ['GET', 'POST'])
def firstcpa():
    trypassword = request.form.get('password')

    is_successful, user = changepassauth.login(trypassword)
    app.logger.info('%s', is_successful)

    if(is_successful):
        session["user"] = user
        return redirect('/finalchangepass')
    else:
        return redirect('/login')
    
@app.route('/secondcpa', methods = ['GET', 'POST'])
def secondcpa():
    password1 = request.form.get('username')
    password2 = request.form.get('password')

    is_successful, user = changepassauth.login(password1, password2)
    app.logger.info('%s', is_successful)

    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/finalchangepass', methods=['GET', 'POST'])
def finalchangepass():
    return render_template('finalchangepass.html')




