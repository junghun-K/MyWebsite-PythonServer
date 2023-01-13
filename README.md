# MyWebsite-PythonServer
* This Website is to practice creating HTTP server in python, which make HTTP requests/responses using socket.  
* Composed of HTML/CSS/Javascript to handle front-end

## How To Run
* pull the repository and the below code will run the with port 9001.  
If port 9001 is taken, change the port number.  
> python3 myServer.py

## Description
* All files images/files/audio in the repository can be gotten.  
For instance, below domain will give that html.  
e.g) http://localhost:9001/myContacts.html, http://localhost:9001/resources/images/amazon.png
* If unvalid files were requested, **404 NOT FOUND** will be responded.
* Only **Get, Post, Head** requests can be made.
