Sarah Lindsay
Professor Eddy
Cybersecurity Final Project 
May 2, 2025

* Testing Instructions:
1. Run werk.py. (The SQLite database storing credentials is created automatically)
2. Upon clicking the localhost link in the console, you will be able to test the functionality of registering and logging in. 
3. When testing the "locked out" feature for 3 failed logins, be aware that once you become locked 
out you will remain locked out even if you rerun the program because this feature uses cookies to determine
if a user is locked out. However, if you do get locked out you can work around this 
by using an incognito browser or clear your cache to continue testing the website functionality.

* Web Application Description
This file is a Flask web application for a secure bank website that
allows users to log in or register. When users are registering, the program does not 
allow users to use a username that is already in the database storing user information, 
and the password must meet all the requirements listed on the register page. When a user
creates a valid username and password, the user is redirected to the login page. Users are 
locked out after 3 failed login attempts. Other security features that maintain the 
authenticity, integrity, and confidentiality of the system include only storing salted 
and hashed passwords, preventing cross-site scripting via subresource integrity, and 
using parameterized queries to prevent SQL injection. Usernames, user type, and hashed 
and salted passwords are stored in a SQLite database called users_sql.

* Web Application Security Features
I used subresource integrity to mitigate the cross-site scripting attack because this security 
feature allows the browser to prevent the CDN from sending malicious code and verify that the 
JavaScript is being loaded from the correct file without being manipulated. This website relies 
on a content delivery network (CDN) to host resources, such as Bootstrap, therefore it does not 
self-host all of its resources. I applied SRI site wide by using a SRI hash generator to get 
cryptographic hashes for each website that is used in the layout, which includes Bootstrap, 
jQuery, and Popper.js CDNs that are used to style the website, add responsive components, and 
make sure these components work correctly. All code for SRI was implemented in the layout.html file. 

Before storing the user registration information in the users_list SQLite database, the program 
hashes & salts the passwords. The program does not store the plaintext passwords in any files. This 
is done to prevent dictionary attacks and an attacker from gaining full access to all user info, 
and ensure that each password is unique even if users choose the same password. I needed to 
modify the password_crack file to properly salt, hash, and authenticate the passwords to determine 
if the user entered valid login credentials. I did this by creating a secure random salt that is 
converted to a hex string, then using the salt_length object in the authenticate function to extract 
the salt from the salted and hashed password. The password entered by the user for the login is hashed 
and then compared to the stored hash.

Parameterized queries were used in bank.py to prevent SQL injection because this security feature
sanitizes the input to ensure that it is safe to use and does not take advantage of error messages. 
When attackers successfully complete SQL injection, they are able to manipulate queries that an 
application is sending to its database by inserting malicious SQL into the queries. The outcomes of 
this attack include the attacker gaining unauthorized access to view, modify and delete data, harm 
back-end infrastructure, and execute denial-of-service attacks.

* References (All sources used for this project are listed below. The sources below are also cited in comments in each of the files, 
next to or above the appropriate lines.)
Files from Professor Eddy's GitLab: https://gitlab.uvm.edu/James.Eddy/cs-2660-cross-site-scripting
https://docs.python.org/3.12/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
https://stackoverflow.com/questions/44608346/how-properly-i-refer-to-a-li-in-the-css-should-i-use-e-g-ul-li-or-just-ul-l 
https://stackoverflow.com/questions/41369105/django-bootstrap-alerts-not-working-as-expected 
https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
https://stackoverflow.com/questions/2906582/how-do-i-create-an-html-button-that-acts-like-a-link
https://tools.ietf.org/html/rfc3174
https://flask.palletsprojects.com/en/2.3.x/quickstart/
https://docs.python.org/3/library/hashlib.html
https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
https://getbootstrap.com/docs/5.0/components/alerts/
https://www.sqlite.org/index.html
https://www.w3schools.com/sql/
https://stackoverflow.com/questions/485827/css-100-height-with-padding-margin
https://stackoverflow.com/questions/33147303/flex-column-height100-inside-100vh-height-container
https://docs.python.org/3/library/string.html
https://www.w3schools.com/python/ref_random_shuffle.asp
https://runestone.academy/ns/books/published/webfundamentals/Flask/sessions.html
https://www.geeksforgeeks.org/python-sqlite-connecting-to-database/
https://stackoverflow.com/questions/13279399/how-to-obtain-values-of-request-variables-using-python-and-flask
https://www.geeksforgeeks.org/create-a-random-password-generator-using-python/