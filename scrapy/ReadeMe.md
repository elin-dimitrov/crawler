You need to have isntall the following products before start the API:
 Python version 3.8
 virtualenv==20.0.31

==========================INSTALLATION================================= 
Please execute the following steps:
	Enter at folder "scrapy open the terminal and execute the command: 
	"virtualenv ven" then type source ven/bin/activate and press enter.
	After the virtual environemnt is successfully runing we need to install
	all packagest andd framework's by typing "pip install -r requirements.txt"

=========================START SCRAPY==================================
Before we use our API we need to extract the data from the specif site
for the purpose execute "python data_pro/data_pro/spiders/start_fetch.py"
This command will start a script which will run the web crawler and produce
json file with the gathered content. After the procces is finished close the
sesion by using "ctrl + c"

========================START DJANGO===================================
To start the API please enter in the following directory "scrapy/data_pro_crawl"
and execeute the following command: 
	- "python manage.py migrate" - This will populate the database with the
	field need for the work of our API. Then run python manage.py createsuperuser"
	this will require some user data input for creating admin account. 
	Then run the command "python manage.py runserver"
	and paste the following adress in the browser "http://127.0.0.1:8000/admin/"
	
	Since this API required token authorization go to 
	http://127.0.0.1:8000/admin/authtoken/token/add/ and create token for the admin
	user that was created above.
	This is the admin page for our api and from here the user can work direclty with
	the databse!!!
	
=======================Working with the api============================
Due to absence of forntend please install the postman application
and can be downloaded from this link https://www.postman.com/.
How to use POSTMAN please check the provided documentation from the official site.
************************
То verfiy and import the json data please use GET method from the api and
add the followin url http://127.0.0.1:8000/ministers/data.
************************
To following url http://127.0.0.1:8000/ministers 
To filter the data please you can use the following key words:
minister_name ,party, date_of_birth, place_of_birth, languages, proffesion

========================Basic Generate Documentation===================
for Django api please visit http://127.0.0.1:8000/redoc/
for Spider api please open with the browser html file located in 
"scrapy/data_pro/data_pro/spiders/html"
