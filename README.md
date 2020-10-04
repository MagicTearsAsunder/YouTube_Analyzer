# Your YouTube Usage Analysis
A Django web application to upload, analyse, store and remove your Youtube data.
Take your data from https://takeout.google.com/. And authentication system with e-mail confirmation. 
<p>See the example: <a href="https://www.youtube.com/watch?v=I1K8ji-CSMY">Video Preview</a></p>


### Basic Data:
<img src="https://i.imgur.com/fPmJcyf.png?1" title="source: imgur.com"/>

### Wordcloud of searches:
<img src="https://i.imgur.com/m0nNTkQ.png" title="source: imgur.com" width="300" height="300"/></a>


### Overall year activity:
<img src="https://i.imgur.com/GqtHh5h.png?1" title="source: imgur.com" />


### Activity by hour and weekday:
<img src="https://i.imgur.com/Odiu1G2.png" title="source: imgur.com" />


### Top 5 watched videos and Top 5 viewed channels:
<img src="https://i.imgur.com/yE6M9PR.png" title="source: imgur.com" />


## Setup
### 1. Install Python3 interpreter
Additional information on https://www.python.org/downloads/

### 2. Clone this repository into your directory

    $ mkdir myproject && cd myproject
    $ git clone https://github.com/MagicTearsAsunder/YouTube_Analyzer.git
    $ cd TODO

### 3. Install requirements


    $ pip install -r requirements.txt

  
### 4. Set you Google account credentials for authentication system
In `shindeiru/settings.py` add your Google account credentials to `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`. If you don't have Google account - <a href="https://accounts.google.com/signup">create it</a>. Alternitavely, you can use other SMTP host.
Instructions, how to set Django SMTP described 
<a href="https://medium.com/@_christopher/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e">here</a>.

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    # TODO:
    EMAIL_HOST_USER = ""
    # TODO:
    EMAIL_HOST_PASSWORD = ""
    EMAIL_USE_TLS = True

### 5. Make migrations and run server
    python manage.py makemigrations 
    python manage.py migrate 
    python manage.py runserver
    

## Run it in Docker
    docker-compose up


## Register and upload your zip file

### 1. Download your YouTube data from https://takeout.google.com/. Deselect all, choose `Youtube`:
<img src="https://i.imgur.com/eD74Sn1.png" title="source: imgur.com" />

### 2. Press `Multiple formats` and choose `JSON`:
<img src="https://i.imgur.com/rEEVoJU.png?1" title="source: imgur.com" />

### 3. Select `.zip` file type:

<img src="https://i.imgur.com/ZGIytzU.png?1" title="source: imgur.com" />

### 4. Upload it to form.

### Enjoy it!
