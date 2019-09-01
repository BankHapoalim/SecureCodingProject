# Installation 

### Prerequisites
Python 3.7

7zip 

Make sure 7zip and python are added to your PATH

### Installation

Download or clone the Secure Coding app  
Open cmd and go to the project directory  
Install virtualenv and create a virtual environment  

```
pip install virtualenv
virtualenv venv
```
Activate the virtual environment
```
venv\Scripts\activate
```
install requirements
```
pip install -r requirements.txt 
```
Create application db: 
```
flask db upgrade 
```
Run the application
```
flask run
```
A web server should running. Browse to it in your browser. 
# Usage 

You can register a user. Then you can use upload check (vulnerable to command injection), and view check status (vulnerable to reflected and stored XSS, via check_id and message respectively) 


