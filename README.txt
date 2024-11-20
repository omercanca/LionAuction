 i) context of your code:
    auction_details.html is a file used to see the list of auctions that a buyer can bid on. It is only accessible through the buyer login.
    buyer.html is the page we see when the logs in. It includes a welcome message, a search bar to search for auctions based on keywords, a logout button to log out, a categories dropdown to search for auctions, and a profile button to view info of the logged in buyer.
    edit_listing.html is the page we use to edit listings that are already posted. It is accessed by logging in as a seller, going to listings, and pressing edit on a listings. We can update each part of the listing and it will be reflected in the database. If we want to cancel, we simply press the goback button
    helpdesk.html is the page we see when logged in as a helpdesk member. On the page, we have a profile button where we can go see the profile of the logged in person. We have a requests button where we can see the requests for the specific helpdesk member logged in. And we have a logout button
    index.html is the homepage where we log in. It features a moving title, a lion and a login box. the login box has a form for email and password. there are also 3 buttons to login as you choose.
    the listings.html file is the file where we see a sellers listings. Here we see all the listings details from the auction_listings database. We can also see completed listings once they finish. We can also edit and delete listings.
    the profile.html file shows us the profile of the person logged in. Depending on the role they are, it shows different information form different tables in the database.
    the requests.html file is used to view the requests from the helpdesk member logged in.
    the seller.html page is the page we see when a seller logs in. It has buttons to view profile, sell an item, view listings, and logout
    the sellform.html is the file we use to sell an item. It asks for the different details of the item and has a submit buttonto put it live and into the database. It also has a go back button to cancel.
    the status0.html button is the error page we get when we try to edit an auction that has already been completed.
    The app.py file is the backend for our database. It features countless function that we will speak about in part 2.
 ii) index() takes us to to the homepage
     status0() takes us to status0.html
     requests() displays helpdesk requests assigned to the currently logged-in user by querying the database
     seller() takes us to seller.html
     completed_transactions() displays completed transactions for a seller from transactions table based on the email logged in
     listings() display auction listings and completed transactions
     edit_listing(listing_id) allows us to edit the listing and posts changes to the database
     update_listing(listing_id): allows us to update the listing
     delete_listing(listing_id): deletes listing and updates in database
     helpdesk() takes us to helpdesk page
     logout() logs us out and pops the session.
     login(): logs in and takes us to certain page based on who we log in as. it fails if we try to login as someone who doesnt have the correct role
     profile() shows us profile info for the person logged in. it chooses info from the table based on the login info.
     get_db(), close_connection(exception), and query_db(query, args=(), one=False): establish, query, and close a connection
     buyer(): takes us to the buyer page
     auctions(): displays  listings based on search queries or category
     place_bid(listing_id): ensures that a bid is allowed tobe placed and places it, making the database change. also closes and moves auction if its finished
     get_listings_by_title(search_query) and get_listings_by_category(category): show us the listings by title searchd or category queried.
     sellform(): helps filter subcategories for the sell form
     create_auction(): makes the listing update in the table
     All the HTML files are formatted the same way. They feature the styling, html code, then any javascript code if necessary to display the website.
iii) organization (i.e., how the files are organized);
     All the python functions are in app.py in the NittanyPath folder. The .html files are all in the templates folder. The CSV folder features are all the data used in the database.
iv) instructions: the file is loaded into pycharm by going to file--> open--> and then selecting NittanyPath folder. However, we must unzip the folder first. Then, we must make sure to run the app on a server that is not being used. Next, we configure to run on flask (app.py). when we run this file, we open the server that it is being ran on. After this, we can access the app.
