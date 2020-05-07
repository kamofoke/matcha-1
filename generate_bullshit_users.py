from pymongo import MongoClient
from faker import Faker
import hashlib, os, binascii
import random

fake = Faker()

# cluster = MongoClient('mongodb+srv://matcha:password13@matcha-g1enx.mongodb.net/test?retryWrites=true&w=majority')
# db = cluster['Matcha']
# col = db['Users']

cluster = MongoClient('localhost', 27017)
db = cluster.matcha
col = db.users

# Pref:'1'
# Verify:'1'
# Matches:''
# Likes:''
# Dislikes:''
# Name:'Tanya'
# Surname:'Loft'
# Age:22
# Email:'tanya@gmail.com'
# username:'tanyaloft'
# Password:'876ee9c5bcdd53892dd18cb268d4b93c42ca9ee0eb3f47ef8fe2c823c1883056f6d0f1...'
# Gender:'female'
# Images:'trtvyoxhwtnwcxw1, vxrscllmrvqimvu2, ggzdavmalijyoun3, temeocunmfgvgtx4...'
# Popularity:1
# Blocked:'jerry, tc, hs, sm, thelani'
# ProfileViews:'hs, sm'
# ProfileLikes:'thelani, sm'
# Suburb:'Suburb'
# Postal Code:'1989'
# Sexual Orientation:'heterosexual'
# Bio:'I am Tanya'
# Animals:'yes'
# Food:'yes'
# Movies:'yes'
# Music:'yes'
# Sports:'yes'
def hash_password(password):
	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
	pwdhash = binascii.hexlify(pwdhash)
	return (salt + pwdhash).decode('ascii')

def createUsers():
	i = 0
	while (i < 10):
		# sexual orientation
		randSO = random.randint(0, 2)
		if (randSO == 0):
			SO = 'heterosexual'
		elif (randSO == 1):
			SO = 'homosexual'
		elif (randSO == 2):
			SO = 'bisexual'
		# gender, name, surname
		randGen = random.randint(0, 1)
		if (randGen == 0): # male
			gender = 'male'
			name = fake.first_name_male()
			while (len(name) < 5):
				name = fake.first_name_male()
			surname = fake.last_name_male()
			while (len(surname) < 6):
				surname = fake.last_name_male()
		elif (randGen == 1): #female
			gender = 'female'
			name = fake.first_name_female()
			surname = fake.last_name_female()
			while (len(name) < 5):
				name = fake.first_name_female()
			surname = fake.last_name_female()
			while (len(surname) < 6):
				surname = fake.last_name_female()
		nameLen = len(name)
		surLen = len(surname)
		first_letter = name[0]
		second_letter = name[random.randint(1, nameLen - 1)]
		third_letter = name[random.randint(1, nameLen - 1)]
		fourth_letter = name[nameLen - 1]
		fifth_letter = surname[0]
		sixth_letter = surname[random.randint(1, surLen - 1)]
		seventh_letter = surname[random.randint(1, surLen - 1)]
		eighth_letter = surname[surLen - 1]
		username = first_letter + second_letter + third_letter + fourth_letter + fifth_letter + sixth_letter + seventh_letter + eighth_letter
		originalRefPrefArr = ['Animals', 'Food', 'Movies', 'Music', 'Sports']
		refPrefArr = originalRefPrefArr
		randLoop = random.randint(1, 5)
		loop = 0
		leloop = 0
		perPrefArr = [{} for i in range(randLoop)]
		while (loop < randLoop):
			listLen = len(refPrefArr)
			perPrefArr[leloop] = refPrefArr[random.randint(0, listLen - 1)]
			refPrefArr.remove(perPrefArr[leloop])
			leloop += 1
			loop += 1
		age = random.randint(18, 80)
		birthYear = 2020 - age
		randServ = ['gmail', 'hotmail', 'yahoo', 'outlook']
		randThing = ['.co.za', '.com', '.org', '.gov.za', '.net']
		email = name + username + '@' + randServ[random.randint(0, 3)] + randThing[random.randint(0, 4)]
		locationArr = [
			'Albertville, Gauteng',
			'Albertskroon',
			'Aldara Park',
			'Amalgam, Gauteng',
			'Auckland Park',
			'Berario',
			'Beverley Gardens',
			'Blackheath, Gauteng',
			'Blairgowrie, Gauteng',
			'Bordeaux, Gauteng',
			'Bosmont',
			'Brixton, Gauteng',
			'Bryanbrink',
			'Bryanston West, Gauteng',
			'Clynton',
			'Coronationville, Gauteng',
			'Country Life Park',
			'Cowdray Park, Gauteng',
			'Craighall',
			'Craighall Park',
			'Cramerview',
			'Cresta, Gauteng',
			'Crown, Gauteng',
			'Daniel Brink Park',
			'Darrenwood',
			'Dunkeld West',
			'Dunkeld, Gauteng',
			'Emmarentia',
			'Ferndale, Gauteng',
			'Florida Glen',
			'Fontainebleau, Gauteng',
			'Forest Town, Gauteng',
			'Glenadrienne',
			'Gleniffer',
			'Greenside, Gauteng',
			'Greymont',
			'Hurlingham Gardens',
			'Hurlingham, Gauteng',
			'Hyde Park, Gauteng',
			'Jan Hofmeyer, Gauteng',
			'Kensington B',
			'Linden, Gauteng',
			'Lindfield House',
			'Lyme Park, Gauteng',
			'Malanshof',
			'Melville, Gauteng',
			'Mill Hill, Gauteng',
			'Newlands, Johannesburg',
			'Northcliff',
			'Oerder Park',
			'Osummit',
			'Parkhurst, Gauteng',
			'Parkmore',
			'Parktown North',
			'Parkview, Gauteng',
			'Praegville',
			'President Ridge',
			'Randburg',
			'Randpark',
			'Randpark Ridge',
			'Riverbend, Gauteng',
			'Rosebank, Gauteng',
			'Ruiterhof',
			'Sandhurst, Gauteng',
			'Solridge',
			'Sophiatown',
			'Strijdompark',
			'Total South Africa',
			'Vandia Grove',
			'Vrededorp, Gauteng',
			'Waterval Estate, Randburg',
			'Westbury, Gauteng',
			'Westcliff, Gauteng',
			'Westdene, Gauteng',
			'Willowild'
			]
		location = locationArr[random.randint(0, 74)]
		animals = 0
		food = 0
		movies = 0
		music = 0
		sports = 0
		dud = 0
		while (dud < len(perPrefArr)):
			if (perPrefArr[dud] == 'Animals'):
				animals = 1
			if (perPrefArr[dud] == 'Food'):
				food = 1
			if (perPrefArr[dud] == 'Movies'):
				movies = 1
			if (perPrefArr[dud] == 'Music'):
				music = 1
			if (perPrefArr[dud] == 'Sports'):
				sports = 1
			dud += 1
		animalsQuery = 'yes' if animals == 1 else 'no'
		foodQuery = 'yes' if food == 1 else 'no'
		moviesQuery = 'yes' if movies == 1 else 'no'
		musicQuery = 'yes' if music == 1 else 'no'
		sportsQuery = 'yes' if sports == 1 else 'no'
		query = {'Pref': '1', 'Verify': '1', 'Matches': '', 'Likes': '', 'Dislikes': '', 'Name': name, 'Surname': surname, 'Age': age, 'Email': email, 'username': username, 'Password': hash_password('Password123!'), 
				'Gender': gender, 'Popularity': 0, 'Blocked': '', 'ProfileViews': '', 'ProfileLikes': '', 'Suburb': location, 'Postal Code': random.randint(1000, 2999), 'Sexual Orientation': SO, 
				'Bio': 'I am ' + name , 'Animals': animalsQuery, 'Music': musicQuery, 'Sports': sportsQuery, 'Food': foodQuery, 'Movies': moviesQuery, 'Noti': '1', 
				'Images': 'trtvyoxhwtnwcxw1, vxrscllmrvqimvu2, ggzdavmalijyoun3, temeocunmfgvgtx4, nemgggxqfkphbkh5'}
		col.insert_one(query)
		print(query)
		i += 1

createUsers()