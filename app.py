from flask import Flask, flash, redirect, url_for, render_template, g
import sqlite3
from flask_login import current_user
from flask import make_response

app = Flask(__name__)
if __name__ == "__main__":
    app.run(host='127.0.0.0', port=5001, debug=True)


@app.route('/')  # route for index page
def index():
    return render_template('index.html')


@app.route('/status0')  # route for status0 page. What happens when we edit already finished lsting
def status0():
    return render_template('status0.html')


@app.route('/requests')  # app route for helpdeks requests
def requests():
    # Retrieve the email of the currently logged in user from the cookie
    email = request.cookies.get('email')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # retrive data from requests table where helpdesk_staff_email matches the logged in user's email
    c.execute("SELECT * FROM requests WHERE helpdesk_staff_email=?", (email,))
    data = c.fetchall()
    print("data:", data)
    conn.close()

    # make the requests.html template with the data
    return render_template('requests.html', requests=data, current_user=current_user)


# app route for seller page
@app.route('/seller')
def seller():
    return render_template('seller.html')


# app route for completed transactions
@app.route('/completed_transactions')
def completed_transactions():
    email = request.cookies.get('email')  # get email with cookie
    if not email:  # if no email return to login
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # get completed transactions for seller from trans table
    c.execute("""
        SELECT *
        FROM transactions
        WHERE seller_email = ? AND Payment IS NOT NULL
    """, (email,))
    rows = c.fetchall()

    completed_transactions = []  # pute completed transaction in dic
    for row in rows:
        transaction = {
            'transaction_id': row[0],
            'seller_email': row[1],
            'listing_id': row[2],
            'bidder_email': row[3],
            'date': row[4],
            'payment': row[5]
        }
        completed_transactions.append(transaction)

    conn.close()

    return render_template('completed_transactions.html', completed_transactions=completed_transactions)


# app route for listings
@app.route('/listings')
def listings():
    email = request.cookies.get('email') # get email
    if not email:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # get listings from auction_listings
    c.execute("SELECT * FROM auction_listings WHERE seller_email = ?", (email,)) # get email where seller email is same as logged in
    rows = c.fetchall()

    listings = [] # put listings in dic
    for row in rows:
        listing = {
            'seller_email': row[0],
            'listing_id': row[1],
            'category': row[2],
            'auction_title': row[3],
            'product_name': row[4],
            'product_description': row[5],
            'quantity': row[6],
            'reserve_price': row[7],
            'max_bids': row[8],
            'status': row[9],
        }

        listings.append(listing)

    #get transactions for seller from tran table
    c.execute("""
        SELECT *
        FROM transactions
        WHERE seller_email = ? AND Payment IS NOT NULL AND seller_email IS NOT NULL
    """, (email,))
    rows = c.fetchall()

    completed_transactions = []
    for row in rows:
        transaction = {
            'transaction_id': row[0],
            'seller_email': row[1],
            'listing_id': row[2],
            'bidder_email': row[3],
            'date': row[4],
            'payment': row[5]
        }
        completed_transactions.append(transaction)

    conn.close()

    return render_template('listings.html', listings=listings, completed_transactions=completed_transactions)

#route for editing listings
@app.route('/edit_listing/<int:listing_id>')
def edit_listing(listing_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM auction_listings WHERE listing_id = ?", (listing_id,))
    row = c.fetchone()
# if its not there, say the listing isnt found
    if not row:
        conn.close()
        return "Listing not found", 404

    if row[9] != 1:  # see if status is 1. if it is, show the erroor page
        conn.close()
        return render_template("status0.html")

    listing = {
        'listing_id': row[1],
        'category': row[2],
        'auction_title': row[3],
        'product_name': row[4],
        'product_description': row[5],
        'quantity': row[6],
        'reserve_price': row[7],
        'max_bids': row[8],
        'status': row[9],
    }

    c.execute("SELECT DISTINCT parent_category FROM categories")
    categories = [{'parent_category': row[0]} for row in c.fetchall()]

    conn.close()

    return render_template('edit_listing.html', listing=listing, categories=categories)


@app.route('/update_listing/<int:listing_id>', methods=['POST']) #route for updating listing
def update_listing(listing_id):
    category = request.form['category'] #form request for updates
    auction_title = request.form['auction_title']
    product_name = request.form['product_name']
    product_description = request.form['product_description']
    quantity = int(request.form['quantity'])
    reserve_price = float(request.form['reserve_price'])
    max_bids = int(request.form['max_bids'])

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

#updating table with form
    c.execute('''UPDATE auction_listings
                 SET category = ?, auction_title = ?, product_name = ?, product_description = ?, quantity = ?, reserve_price = ?, max_bids = ?
                 WHERE listing_id = ?''', (
    category, auction_title, product_name, product_description, quantity, reserve_price, max_bids, listing_id))

    conn.commit()
    conn.close()

    return redirect(url_for('listings'))

#deleting listings route
@app.route('/delete_listing/<int:listing_id>', methods=['POST'])
def delete_listing(listing_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    #get listing where id is same as id
    c.execute("SELECT * FROM auction_listings WHERE listing_id = ?", (listing_id,))
    row = c.fetchone()

    if not row: #fail if not a row
        conn.close()
        return "Listing not found", 404

    seller_email = row[0]
    category = row[2]
    auction_title = row[3]
    product_name = row[4]
    product_description = row[5]
    quantity = row[6]
    reserve_price = row[7]
    max_bids = row[8]
    status = row[9]

    # remove the listing from the table
    c.execute("DELETE FROM auction_listings WHERE listing_id = ?", (listing_id,))

    # insert the listing into deleted listings table
    c.execute("""
        INSERT INTO deleted_listings (seller_email, listing_id, category, auction_title, product_name, product_description, quantity, reserve_price, max_bids, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (seller_email, listing_id, category, auction_title, product_name, product_description, quantity, reserve_price,
          max_bids, status))

    conn.commit()
    conn.close()

    return redirect(url_for('listings'))

#helpdesk route
@app.route('/helpdesk')
def helpdesk():
    return render_template('helpdesk.html')


DATABASE = 'database.db'

app.secret_key = "omer"

# logout route
@app.route('/logout')
def logout():
    session.pop('email', None) #kill session for this email
    session.pop('login_type', None)
    return redirect(url_for('login'))

#login function
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'] # get email and password from user
        password = request.form['password']
        login_type = request.form['login_type'] # login type from user

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        if login_type == 'buyer': # if they are a buyer, search in the users and make sure its there
            c.execute("SELECT * FROM Users WHERE email=? AND password=?", (email, password))
            if c.fetchone() is None:
                return 'Invalid email or password.'
            else: #check bidders and make sure its there
                c.execute("SELECT * FROM Bidders WHERE email=?", (email,))
                if c.fetchone() is not None:
                    response = make_response(redirect('/buyer')) # go to buyer.html
                    response.set_cookie('email', email) #remember email
                    response.set_cookie('login_type', login_type) #remember login type
                    return response
                else: #else return its not a buyer
                    return 'User is not a buyer.'
        #same process is repeated or seller and helpdesk
        elif login_type == 'seller':
            c.execute("SELECT * FROM Users WHERE email=? AND password=?", (email, password))
            user = c.fetchone()
            if user is None:
                return 'Invalid email or password.'
            else:
                c.execute("SELECT * FROM Sellers WHERE email=?", (email,))
                if c.fetchone() is not None:
                    response = make_response(redirect('/seller'))
                    response.set_cookie('email', email)
                    response.set_cookie('login_type', login_type)
                    return response
                else:
                    return 'User is not a seller.'

        elif login_type == 'helpdesk':
            c.execute("SELECT * FROM Users WHERE email=? AND password=?", (email, password))
            user = c.fetchone()
            if user is None:
                return 'Invalid email or password.'
            else:
                c.execute("SELECT * FROM Helpdesk WHERE email=?", (email,))
                if c.fetchone() is not None:
                    response = make_response(redirect('/helpdesk'))
                    response.set_cookie('email', email)
                    response.set_cookie('login_type', login_type)
                    return response
                else:
                    return 'User is not part of the helpdesk.'

        conn.close()

    return render_template('login.html')

#profile route
@app.route('/profile')
def profile():
    email = request.cookies.get('email') # get email
    login_type = request.cookies.get('login_type') #get login type
    if not email: #if none go login again
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if login_type == 'buyer': # if theyre a buyer, get buyer info
        c.execute(
            "SELECT email, first_name, last_name, gender, age, major, home_address_id FROM Bidders WHERE email=?",
            (email,))
        user_data = c.fetchone()
        address_id = user_data[6]
        c.execute("SELECT address_id, street_num, street_name, zipcode FROM Address WHERE address_id=?",
                  (address_id,))
        address_data = c.fetchone()
        zipcode = address_data[3]
        c.execute("SELECT city, state FROM Zipcode_Info WHERE zipcode=?", (zipcode,))
        city_state_data = c.fetchone()
        c.execute("SELECT credit_card_num FROM Credit_Cards WHERE owner_email=?", (email,))
        credit_card_data = c.fetchone()
        c.execute("SELECT rating, rating_desc FROM Rating WHERE bidder_email=?", (email,))
        rating_data = c.fetchone()

        # if any of the data is none just maek an empty tuple so it doesnt crash
        user_data = user_data if user_data else ()
        address_data = address_data if address_data else ()
        city_state_data = city_state_data if city_state_data else ()
        credit_card_data = credit_card_data if credit_card_data else ()
        rating_data = rating_data if rating_data else ()

        # last 4 of card
        last_4_digits = credit_card_data[0][-4:] if credit_card_data else ''

        user_data = user_data[:-1] + address_data[1:] + city_state_data + (last_4_digits,) + rating_data
        labels = ['Email', 'First Name', 'Last Name', 'Gender', 'Age', 'Major', 'Street Number', 'Street Name',
                  'Zipcode', 'City', 'State', 'Credit Card (Last 4)', 'Rating', 'Rating Description']
    #seller info, same thing as above
    elif login_type == 'seller':
        c.execute("SELECT email, bank_routing_number, bank_account_number, balance FROM Sellers WHERE email=?",
                  (email,))
        user_data = c.fetchone()
        seller_email = user_data[0]
        c.execute("SELECT rating, rating_desc FROM Rating WHERE seller_email=?", (seller_email,))
        rating_data = c.fetchone()
        if rating_data is None:
            rating_data = ()
        c.execute("SELECT business_name, email, customer_service_phone_number FROM Local_Vendors WHERE email=?",
                  (seller_email,))
        vendor_data = c.fetchone()
        if vendor_data:
            user_data = user_data + vendor_data + rating_data
            labels = ['Email', 'Bank Routing Number', 'Bank Account Number', 'Balance', 'Business Name', 'Email',
                      'Customer Service Phone Number', 'Rating', 'Rating Description']
        else:
            user_data = user_data + rating_data
            labels = ['Email', 'Bank Routing Number', 'Bank Account Number', 'Balance', 'Rating', 'Rating Description']
    elif login_type == 'helpdesk': #helpdesk info, same as above
        c.execute("SELECT email, position FROM Helpdesk WHERE email=?", (email,))
        user_data = c.fetchone()
        labels = ['Email', 'Position']
    else:
        conn.close()
        return "Invalid login type"

    conn.close()
    return render_template('profile.html', user_data=user_data, labels=labels)

#get teh database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#close database conn
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#query db
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# buyer route
@app.route("/buyer")
def buyer():
    parent_categories = query_db("SELECT DISTINCT parent_category FROM Categories") # categories dropdown
    categories = {} #make dic
    for parent in parent_categories:
        categories[parent[0]] = query_db("SELECT category_name FROM Categories WHERE parent_category=?", [parent[0]]) #put subcat under cat
    return render_template("buyer.html", categories=categories)

#auctions route
@app.route('/auctions', methods=['GET'])
def auctions():
    search_query = request.args.get('search') #search bar
    category = request.args.get('category')


    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # search the database to get keywords listings that match the search query or category
    if search_query:
        cursor.execute("""
            SELECT * FROM auction_listings WHERE auction_title LIKE ? OR category LIKE ?
        """, ('%' + search_query + '%', '%' + search_query + '%'))
    elif category:
        cursor.execute("""
            SELECT * FROM auction_listings WHERE category = ?
        """, (category,))
    else:
        cursor.execute("""
            SELECT * FROM auction_listings
        """)

    # get rows as tuples
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # make  rows into a list of dictionaries
    listings = []
    for row in rows:
        listing = {
            'seller_email': row[0],
            'listing_id': row[1],
            'category': row[2],
            'auction_title': row[3],
            'product_name': row[4],
            'product_description': row[5],
            'quantity': row[6],
            'reserve_price': row[7],
            'max_bids': row[8],
            'status': row[9],
            'current_bid': row[10],
            'bid_count': row[11]  # Add the bid_count key
        }

        listings.append(listing)

    # put  search query and cat vars in the template
    return render_template('auctions.html', listings=listings, search_query=search_query, category=category)

#place bid route
@app.route('/place_bid/<listing_id>', methods=['POST'])
def place_bid(listing_id):
    # get bid amount from the form
    bid_amount = int(request.form['bid_amount'])
    #get email from the cookies
    email = request.cookies.get('email')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ensure bid is 1 more than last bid
    cursor.execute("""
        SELECT current_bid, reserve_price, bid_count, max_bids, last_bidder_email FROM auction_listings WHERE listing_id = ?
    """, (listing_id,))
    row = cursor.fetchone()
    current_bid = row[0] if row else None
    reserve_price = row[1] if row else None
    bid_count = row[2] if row else None
    max_bids = row[3] if row else None
    last_bidder_email = row[4] if row else None
#if the last bidder email isnt the same as logged in email, then they can bid again
    if last_bidder_email != email:
        if bid_amount >= reserve_price and (current_bid is None or bid_amount > current_bid) and (bid_count < max_bids):
            # update listing with  new bid amount increment the bid count by1, set the last_bidder_email
            cursor.execute("""
                UPDATE auction_listings SET current_bid = ?, bid_count = bid_count + 1, last_bidder_email = ? WHERE listing_id = ?
            """, (bid_amount, email, listing_id))

            #see if bid amount is equal to the max bids
            if bid_amount >= reserve_price and (current_bid is None or bid_amount > current_bid) and (
                    bid_count == max_bids - 1):
                # find highest transactions_id from the trans table and increment it by 1
                cursor.execute("""
                    SELECT MAX(transaction_ID) FROM transactions
                """)
                highest_transactions_id = cursor.fetchone()[0]
                new_transactions_id = highest_transactions_id + 1

                #move it to trans table
                cursor.execute("""
                    INSERT INTO transactions (transaction_ID, Seller_Email, Listing_ID, buyer_email, date, Payment)
                    VALUES (?, (SELECT seller_email FROM auction_listings WHERE listing_id = ?), ?, ?, date('now'), ?)
                """, (new_transactions_id, listing_id, listing_id, email, bid_amount))

                # remove it from auctions table
                cursor.execute("""
                    DELETE FROM auction_listings WHERE listing_id = ?
                """, (listing_id,))


            conn.commit()

        else:
            #dollar more than last bid error message
            flash('Bid amount must be $1 higher than the current bid.', 'error')
    else:
        #conesecutive bides error message
        flash('You cannot place two consecutive bids.', 'error')

    cursor.close()
    conn.close()
    return redirect(request.referrer or url_for('auctions'))

#listings by title route
def get_listings_by_title(search_query):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # query for listings with matching auction titles
    cursor.execute("""
        SELECT * FROM auction_listings WHERE auction_title LIKE ?
    """, ('%' + search_query + '%',))
    #all rows as tuple list
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    #make rows into list of dictionaries
    listings = []
    for row in rows:
        listing = {
            'seller_email': row[0],
            'listing_id': row[1],
            'category': row[2],
            'auction_title': row[3],
            'product_name': row[4],
            'product_description': row[5],
            'quantity': row[6],
            'reserve_price': row[7],
            'max_bids': row[8],
            'status': row[9],
        }

        listings.append(listing)
    return listings

#category listings route
def get_listings_by_category(category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # query to get listings for specified category
    cursor.execute("""
        SELECT * FROM auction_listings WHERE category = ?
    """, (category,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    listings = []
    for row in rows:
        listing = {
            'seller_email': row[0],
            'listing_id': row[1],
            'category': row[2],
            'auction_title': row[3],
            'product_name': row[4],
            'product_description': row[5],
            'quantity': row[6],
            'reserve_price': row[7],
            'max_bids': row[8],
            'status': row[9],
        }

        listings.append(listing)
    return listings


from flask import request, session

# sell form route
@app.route('/sellform', methods=['GET'])
def sellform():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
#get parent category from categories for dropdown
    cursor.execute("SELECT DISTINCT parent_category FROM Categories")
    parent_categories = cursor.fetchall()

    cursor.execute("SELECT category_name FROM Categories")
    subcategories = cursor.fetchall()

    cursor.close()
    conn.close()

    categories = {}
    for parent in parent_categories:
        categories[parent[0]] = query_db("SELECT category_name FROM Categories WHERE parent_category=?", [parent[0]])

    return render_template('sellform.html', categories=categories, subcategories=subcategories)

# creating auctions
@app.route('/sellform', methods=['POST'])
def create_auction():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #get email of logged in
    seller_email = request.cookies.get('email')
#request form
    category = request.form['Category']
    auction_title = request.form['Auction_Title']
    product_name = request.form['Product_Name']
    product_description = request.form['Product_Description']
    quantity = request.form['Quantity']
    reserve_price = request.form['Reserve_Price']
    max_bids = request.form['Max_Bids']
    status = 1
#give listing id of one more than max
    cursor.execute("SELECT MAX(listing_id) FROM Auction_Listings")
    max_listing_id = cursor.fetchone()[0]
    if max_listing_id is None:
        max_listing_id = 0
    listing_id = max_listing_id + 1

    cursor.execute(
        "INSERT INTO Auction_Listings (listing_id, seller_email, category, auction_title, product_name, product_description, quantity, reserve_price, max_bids, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (listing_id, seller_email, category, auction_title, product_name, product_description, quantity, reserve_price,
         max_bids, status))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('sellform'))
