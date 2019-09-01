# Installation 

### Prerequisites
Python 3.7

7zip (make sure 7z.exe is in the PATH)

### Install packages: 
```
pip install -r requirements.txt 
```

### Create db: 
```
flask db migrate 

flask db upgrade 
```

### Run:
```
flask run
```
# Usage 

You can register a user. Then you can use upload check (vulnerable to command injection), and view check status (vulnerable to reflected and stored XSS, via check_id and message respectively) 


