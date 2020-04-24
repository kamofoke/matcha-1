from flask import Flask, render_template, url_for, request, redirect , session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from email_validator import validate_email, EmailNotValidError
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import date
import os, re
import pymongo

UPLOAD_FOLDER = './static/profile_pictures'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER

cluster = MongoClient("mongodb+srv://matcha:password13@matcha-g1enx.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["Matcha"]
col = db["Users"]

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_username'] = 'matcha13.noreply@gmail.com'
app.config['MAIL_PASSWORD'] = 'matcha1313'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == "GET":
		return render_template('index.html')
	name = request.form['name']
	surname = request.form['surname']
	username = request.form['username']
	email = request.form['email']
	password = request.form['password']
	passrep = request.form['passwordrepeat']
	bday = request.form['bday']
	bday2 = re.search("([12]\\d{3}/(0[1-9]|1[0-2])/(0[1-9]|[12]\\d|3[01]))", bday) 
	if bday2:
		today = date.today()
		age = str(today.year - int(bday[0:4]) - ((today.month, today.day) < (int(bday[5:7]), int(bday[8:10]))))
		if int(age) > 17:
			result = col.find_one({"username": username})
			if result == None:
				result = col.find_one({"Email": email})
				if result == None:
					if (re.match("[^@]+@[^@]+\\.[^@]+", email)):
						matches = re.search("(?=^.{8,}$)((?=.*\\d)(?=.*\\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", password)
						if (matches):
							if password == passrep:
								query = {"Pref": "0", "Verify": "0", "Name": name, "Surname": surname, "Age": age, "Email": email, "username": username, "Password": hash(password)}
								col.insert_one(query)
								msg = Message("Matcha Verification", sender="noreply@matcha.com", recipients=[email])
								msg.body = 	"Hello {0}!\n\nYou have successfully signed up for Matcha!\nPlease click the link below to verify your account.\n\nhttp://127.0.0.1:5000/verify/{0}.\n\nThank you.\n".format(username)
								mail.send(msg)
							else:
								return render_template('index.html', error = 1)
						else:
							return render_template('index.html', error = 4)
					else:
						return render_template('index.html', error = 5)
				else:
					return render_template('index.html', error = 6)
			else:
				return render_template('index.html', error = 7)
		else:
			return render_template('index.html', error = 8)
	else:
		return render_template('index.html', error = 9)
	return render_template('index.html', error = -1)

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == "GET":
		return render_template('index.html')
	username = request.form['username']
	password = hash(request.form['password'])
	result = col.find_one({"username": username})
	if request.method == 'POST':
		if result != None:
			result = col.find_one({"Password": password})
			if result != None:
				for cursor in col.find({"username": username}):
					pref = cursor['Pref']
					verify = cursor['Verify']
				if verify == "1":
					if pref == "0":
						session['user'] = username
						return render_template('preferences.html', username = username)
					else:
						session['user'] = username 
						return redirect(url_for('home'))
				else:
					return render_template('index.html', error = 8)
			else:
				return render_template('index.html', error = 2)
		else:
			return render_template('index.html', error = 3)
	else:
		return render_template('index.html')

@app.route('/logout', methods=['GET'])
def logout():
	if request.method == "GET":
		return render_template('home.html')
	session.pop("user", None)
	return render_template('index.html')
		
@app.route('/home', methods=['GET'])
def home():
	if request.method == "GET":
		return render_template('home.html')
	try:
		username = session['user']
	except KeyError:
		return render_template('index.html')
	username = session['user']
	query = {"username": username}
	for cursor in col.find(query):
		Food = cursor['Food']
		Music = cursor['Music']
		Movies = cursor['Movies']
		Animals = cursor['Animals']
		Sports = cursor['Sports']
		Gender = cursor['Gender']
		Sexual_Orientation = cursor['Sexual Orientation']

	query = {"$and" : [
		{ "username" : {"$ne" : username}},
		{ "$or" : [ { "Sports" : Sports }, { "Food" : Food }, { "Music" : Music }, { "Movies" : Movies }, { "Animals" : Animals } ] }
	]}

	if Sexual_Orientation == 'homosexual' and Gender == 'male':
		query["$and"].append({"$or" : [
			{"$and" : [ {"Gender": "male"}, {"Sexual Orientation" : "homosexual"}]},
			{"$and" : [ {"Gender": "male"}, {"Sexual Orientation" : "bisexual"} ]}
			]
		})
	elif Sexual_Orientation == 'heterosexual' and Gender == 'male':
		query["$and"].append({"$or" : [
			{"$and" : [{"Gender": "female"}, {"Sexual Orientation" : "heterosexual"}]},
			{"$and" : [{"Gender": "female"}, {"Sexual Orientation" : "bisexual"}]}
			]
		})
	elif Sexual_Orientation == 'bisexual' and Gender == 'male':
		query["$and"].append({"$or" : [
			{ "$and" : [{"Gender": "male"}, {"Sexual Orientation" : "homosexual"}]},
			{ "$and" : [{"Gender": "female"}, {"Sexual Orientation" : "heterosexual"}]},
			{"Sexual Orientation" : "bisexual"}
			]
		})
	elif Sexual_Orientation == 'homosexual' and Gender == 'female':
		query["$and"].append({"$or" : [
			{"$and" : [{"Gender": "female"}, {"Sexual Orientation" : "homosexual"}]},
			{"$and" : [{"Gender": "female"}, {"Sexual Orientation" : "bisexual"}]}
		]
		})
	elif Sexual_Orientation == 'heterosexual' and Gender == 'female':
		query["$and"].append({"$or" : [
			{"$and" : [{"Gender": "male"}, {"Sexual Orientation" : "heterosexual"}]},
			{"$and" : [{"Gender": "male"}, {"Sexual Orientation" : "bisexual"}]}
			]
		})
	elif Sexual_Orientation == 'bisexual' and Gender == 'female':
		query["$and"].append({"$or" : [
			{ "$and" : [{"Gender": "female"}, {"Sexual Orientation" : "homosexual"}]},
			{ "$and" : [{"Gender": "male"}, {"Sexual Orientation" : "heterosexual"}]},
			{"Sexual Orientation" : "bisexual"}
		]
		})
	x = col.find_one(query)
	if x:
		query = {"username": x['username']}
		for cursor1 in col.find(query):
			Name1 = cursor1['Name']
			Surname1 = cursor1['Surname']
			Food1 = cursor1['Food']
			Music1 = cursor1['Music']
			Movies1 = cursor1['Movies']
			Animals1 = cursor1['Animals']
			Sports1 = cursor1['Sports']
			Bio1 = cursor1['Bio']
			Suburb1 = cursor1['Suburb']
			Gender1 = cursor1['Gender']
			Sexual_Orientation1 = cursor1['Sexual Orientation']
		return render_template('home.html', name=Name1, surname=Surname1, food=Food1, music=Music1, movies=Movies1, animals=Animals1, sports=Sports1, bio=Bio1, suburb=Suburb1, gender=Gender1, sexual_orientation=Sexual_Orientation1, pro_img=Pro_Img, img1=Img1, img2=Img2, img3=Img3, img4=Img4)
	else:
		return "You have no matches"
			

def checkuser(fun):
	try:
		username = session['user']
	except KeyError:
		return render_template('index.html')
	return fun()

@app.route('/like')
def like():
	return render_template('index.html')

@app.route('/dislike')
def dislike():
		return redirect(url_for('profile'))

@app.route('/preferences/', methods=['POST'])
def preferences_handler():
	username = session['user'] #this comment
	gender = request.form['gender']
	suburb = request.form['suburb']
	postal_code = request.form['postal code']
	sexual = request.form['sexual']
	bio = request.form['bio']
	animals = request.form['animals']
	music = request.form['music']
	movies = request.form['movies']
	sports = request.form['sports']
	food = request.form['food']
	myquery = { "username": username }
	newvalues = { "$set": {"Pref": "1", "Name": name, "Surname": surname, "Gender": gender, "Suburb": suburb, "Postal Code": postal_code, "Sexual Orientation": sexual, "Bio": bio, "Animals": animals, "Music": music, "Sports": sports, "Food": food, "Movies": movies} }
	col.update_one(myquery, newvalues)
	img = request.files['img']
	query = {"Name": name}
	for cursor in col.find(query):
		user_id = str(cursor['_id'])
	img.save(os.path.join(app.config['IMAGE_UPLOADS'], user_id))
	return redirect(url_for('home'))
Pro_Img = "pexels-photo-937481.jpeg"
Img1 = "pexels-photo-1236701.jpeg"
Img2 = "pexels-photo-260367.jpeg"
Img3 = "pexels-photo-3497181.jpeg"
Img4 = "pexels-photo-3497182.jpeg"

@app.route('/profile')
def profile():
	username = session['user']
	query = {"username": username}
	for cursor in col.find(query):
		Name = cursor['Name']
		Surname = cursor['Surname']
		Food = cursor['Food']
		Music = cursor['Music']
		Movies = cursor['Movies']
		Animals = cursor['Animals']
		Sports = cursor['Sports']
		Bio = cursor['Bio']
		Suburb = cursor['Suburb']
		Gender = cursor['Gender']
		Postal_Code = cursor['Postal Code']
		Sexual_Orientation = cursor['Sexual Orientation']
	return render_template('profile.html', name=Name, surname=Surname, food=Food, music=Music, movies=Movies, animals=Animals, sports=Sports, bio=Bio, suburb=Suburb, gender=Gender, postal_code=Postal_Code, sexual_orientation=Sexual_Orientation, pro_img=Pro_Img, img1=Img1, img2=Img2, img3=Img3, img4=Img4)
 
@app.route('/verify/<username>', methods=['POST', 'GET'])
def verify(username):
	if request.method == 'GET':
		return "GET %s" %username
	elif request.method == 'POST':
		return "POST %s" %username
	# myquery = { "username": username }
	# newvalues = { "$set": {"Verify": "1"} }
	# col.update_one(myquery, newvalues)
	# return render_template('index.html', verified=1)
	
if (__name__ == "__main__"):
    app.run(debug = True)

#npm install -g @vue/cli
#vue init webpack Frontend
