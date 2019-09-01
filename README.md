# Installation 

### Prerequisites
Python 3.7

7zip 

make sure 7zip and python are added to your PATH

### Installation

download or clone the Secure Coding app
open cmd and go to the project directory
install virtualenv and create a virtual environment

```
pip install virtualenv
virtualenv venv
```
activate the virtual environment
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
A web server should running. browse to it in your browser. 
# Usage 

You can register a user. Then you can use upload check (vulnerable to command injection), and view check status (vulnerable to reflected and stored XSS, via check_id and message respectively) 


