#!/usr/bin/python2.7

import datetime
import os

# import matplotlib.pyplot as plt
import numpy as np
from easygui import *

runonce = 0
Base = 0
profile = 'me.txt'
Log = 'progress.txt'
foodjournal = datetime.datetime.now().strftime("%B%d%Y")+".csv"
version = 'alpha.3.30.2022'
# weight now updates live
# steps tracking need a lot more work
# add food should not crash if there are no results and it should display there are no results.
# you should be able to add a new food from the tool.
def weightloss(factor): # returns the calorie amount to subtract depending on difficulty.
	if factor == '1':
		return 250
	if factor == '2':
		return 500
	if factor == '3':
		return 750
	if factor == '4':
		return 1000

def BMR(weight,height,age): # calculates BMR and returns it as a float.
	BMR = 66.0 + ( 6.23 * weight ) + ( 12.7 * height ) - ( 6.8 * age )
	return BMR

def cls(): # clears the screen for CLI implementations *remove
	print("\n" * 100)

def new_day(): #determines if this a new day file needs to be created
	if os.path.exists(datetime.datetime.now().strftime("%B%d%Y")+".csv") == True:
		cls()
		main(4)
	try:
		day = open(datetime.datetime.now().strftime("%B%d%Y")+".csv", 'w')
	except:
		cls()
		main(5)

def graph( nomonths ):
	# a very simple function to graph the data in stats
	# take noofmonths and subtract it from the current month
	# then pull in any data with that month name
	# graph that month data on a graph
	monthstart = datetime.datetime.now()
	counter = 0
	err = 0
	if nomonths == '':
		offset = 24
	elif int(nomonths) > 12:
		offset = 48
		err = 1
	else:
		offset = int(nomonths) * 4
	months =[]
	monthnumbers=[]
	while counter <= offset:
		if counter == 0:
			month = datetime.datetime.now()
			counter = 4
		else:
			month = datetime.datetime.now() - datetime.timedelta(weeks=counter)
			counter += 4
		months.append(month.strftime("%B"))
		monthnumbers.append(month.strftime("%m"))
	deliveries = []
	worklist = []
	projects = []
	for item in months:
		if os.path.exists('Archive\\'+item+'\\'+'monthlystats.txt'):
			stats = open('Archive\\'+item+'\\'+'monthlystats.txt')
			for data in stats:
				data = data.split(',')
				delivery = data[0]
				wrklst = data[1]
				try:
					prjt = data[2]
				except:
					prjt = '0'
				deliveries.append(int(delivery))
				worklist.append(int(wrklst))
				projects.append(int(prjt))
		elif os.path.exists('Archive\\'+datetime.datetime.now().strftime("%Y")+'\\'+item+'\\'+'monthlystats.txt'):
			stats = open('Archive\\'+datetime.datetime.now().strftime("%Y")+'\\'+item+'\\'+'monthlystats.txt')
			for data in stats:
				data = data.split(',')
				delivery = data[0]
				wrklst = data[1]
				try:
					prjt = data[2]
				except:
					prjt = '0'
				deliveries.append(int(delivery))
				worklist.append(int(wrklst))
				projects.append(int(prjt))
		elif os.path.exists('Archive\\'+getprevyear()+'\\'+item+'\\'+'monthlystats.txt'):
			stats = open('Archive\\'+getprevyear()+'\\'+item+'\\'+'monthlystats.txt')
			for data in stats:
				data = data.split(',')
				delivery = data[0]
				wrklst = data[1]
				try:
					prjt = data[2]
				except:
					prjt = '0'
				deliveries.append(int(delivery))
				worklist.append(int(wrklst))
				projects.append(int(prjt))
		else:
			error = input(' could not find the'+item+'in Archive or in'+getprevyear()+'press any key to close')

			myday()
			main(0)
	plt.title('Work', fontdict=None)
	if err == 1:
		plt.text(0.5, 0.5, 'graph can only display a max of 12 months', fontdict=None)
	plt.plot(np.array(monthnumbers),np.array(deliveries))
	plt.plot(np.array(monthnumbers),np.array(worklist))
	plt.plot(np.array(monthnumbers),np.array(projects))
	plt.ylabel('values')
	plt.xlabel('months')
	plt.legend(('deliveries', 'worklist', 'projects'), loc='upper right', shadow=True)
	plt.axis([0, 12, 0, 300])
	plt.show()


def profilesetup(weight,height,age,activityLVL): #sets up a new profile and stores it in me.txt
	global Base
	output = open(profile, 'w')
	output.write('profile,'+weight+','+height+','+age+','+activityLVL+'\n')
	weight = float(weight)
	height = float(height) * 12.0
	age = float(age)
	if activityLVL == '1':
		Base = BMR(weight, height, age) * 1.2
		output.write('Base,'+ str(Base)+','+activityLVL+',')
	if activityLVL == '2':
		Base = BMR(weight, height, age) * 1.375
		output.write('Base,'+ str(Base)+','+activityLVL+',')
	if activityLVL == '3':
		Base = BMR(weight, height, age) * 1.55
		output.write('Base,'+ str(Base)+','+activityLVL+',')
	if activityLVL == '4':
		Base = BMR(weight, height, age) * 1.725
		output.write('Base,'+ str(Base)+','+activityLVL+',')
	if activityLVL == '5':
		Base = BMR(weight, height, age) * 1.9
		output.write('Base,'+ str(Base)+','+activityLVL+',')
	output.close()
	main(0)

def add_to_fooddict(food,amount):#take the food and amount passed from food dict get and give the user the option to add it to the dictionary
	data = multenterbox(msg='add new food', fields=['food','brand','amount'],values=[food,'',amount], title=version+' add food to the dicionary')
	main(0)

def food_dict_get(food,amount): #searches through food dictionary returns string of the item and calorie
	global food_Dict
	try:
		food_Dict = open('Food_Dictionary.csv', 'r')
	except:
		msgbox('no food dictionary found press ok to generate one')
		fooddictmake = open('Food_Dictionary.csv', 'w')
		fooddictmake.write('Food,Brand,calories,servings\n')
		msgbox('add some foods to the dictionary and try again')
		fooddictmake.close()
		main(0)
	foodarray = []
	for item in food_Dict:
		if 'Food' in item:
			continue
		else:
			item = item.split(',')
			foodarray.append(item[0])
	food_lookup = food
	if 's*' in amount:
		value = 'servings'
	if 'oz*' in amount:
		value = 'oz'
	if 'g*' in amount:
		value = 'grams'
	if '*' not in amount:
		cls()
		main(2)
	choices = []
	for item in foodarray:
		if food in item:
			choices.append(item)
	title='food picker %s' % (version)
	msg='pick a food from the list'
	command = choicebox(msg, title, choices)
	if command == 'Add more choices':
		add_to_fooddict(food,amount)
	else:
		food_Dict = open('Food_Dictionary.csv', 'r')
		for item in food_Dict:
			item = item.split(',')
			if 'Food' in item:
				continue
			if command == item[0] and int(item[3]) != 0:
				if value == 'servings':
					amount = float(item[3]) * float(amount.strip('s*'))
					calories = amount * int(item[2])
					food_Dict.close()
					return command+','+','+str(calories)
			elif int(item[3]) == 0:
				food_Dict.close()
				main(3)

def food_Journal_get_cals(): ##go through the food journal add up all the calories and return the total
	global foodjournal
	foodjournal = open(datetime.datetime.now().strftime("%B%d%Y")+".csv", 'r')
	total = 0
	for item in foodjournal:
		values = item.split(',')
		if 'Food' in values:
			next
		else:
			total = total + float(values[2])
	foodjournal.close()
	return total

def main(error): #main loop
	global foodjournal
	global runonce
	global Base
	global profile
	#Error handling#
	if error == 1:
		print("Sorry that food doesn't exist in the dictionary please add it")
		print("")
	if error == 2:
		print("It looks like you didn't specify a serving value")
	if error == 3:
		print("oops we don't have a value prefix")
	if error == 4:
		print("log for today already exists")
	if error == 5:
		print("couldn't create new log file")
	#Error handling#

	if os.path.isfile(profile) == False: #do we need a new profile?
		runonce = 1
	else:
		runonce = 2
	if runonce == 1:
		message = 'Fill in values for the fields.\n'\
				  +'1:sedintary\n2:lightly active\n3:moderately active\n4:very active\n5:extra active'
		values = multenterbox(msg=message, fields=['weight','height','age','activityLVL'], title=version+' profile setup')
		profilesetup(values[0],values[1],values[2],values[3])

	prof = open(profile, 'r')
	for item in prof:
		if 'Base' in item:
			item = item.split(',')
			Base = item[1]
			factor = item[2]
		else:
			continue
	#This is going to be moved into the log window
	prof.close()
	try:
		foodjournal = open(datetime.datetime.now().strftime("%B%d%Y")+".csv", 'r')
		for item in foodjournal:
				print(item)
	except:
			new_day()
	#This is going to be moved into the log window

	#building text for main window
	if os.path.exists('statsfile.csv') == True:
		stats = open('statsfile.csv', 'r')
		steps = 'no steps today'
		stepsval = 0
		exercise = False
		for item in stats:
			if datetime.datetime.now().strftime("%B%d%Y") in item and 'exercise' in item:
				value = item.split(',')
				exercise = value[2]
				lefttoday = 'left for today '+str(NewBase + float(exercise))+' kcal'
				exercisecals = "exercise calories " + exercise
			if datetime.datetime.now().strftime("%B%d%Y") in item and 'steps' in item:
				value = item.split(',')
				steps = 'steps for the day '+value[2].strip('\n')
				stepsval = int(value[2].strip('\n'))
		stats.close()
	else:
		stats = open('statsfile.csv', 'w')
		stats.close()
		exercise = False
	basecalsstr = 'base starting calories is '+str(Base)+ ' kcal'
	calories = food_Journal_get_cals()
	print(stepsval)
	NewBase = float(Base) - float(calories) - weightloss(factor) + (stepsval*0.01)
	calsconsumed = 'total calories consumed today '+str(calories)+' kcal'
	#print how many calories you have burned resting so far
	hour = float(int(datetime.datetime.strftime(datetime.datetime.now(),"%H")))
	calsperhr = float(Base)/24
	calssofar = 'calories burned so far '+ str(calsperhr * hour)
	if (calsperhr * hour) + 100 < calories:
		zone = 'high.png'
	elif (calsperhr * hour) - 300 > calories:
		zone='Low.png'
	else:
		zone='good.png'
	if exercise == False:
		modetext = 'left for today '+str(NewBase)+' kcal'
	if factor == '1':
		modetext = 'weightloss mode is: easy'
	if factor == '2':
		modetext = 'weightloss mode is: medium'
	if factor == '3':
		modetext = 'weightloss mode is: beast mode'
	if factor == '4':
		modetext = 'weightloss mode is: fucking scary ass spider mode'
	print("")

	#add to log window
	if os.path.exists('statsfile.csv') == True:
		stats = open('statsfile.csv', 'r')
		weight = "todays weight is: no weight loged "
		for item in stats:
			if datetime.datetime.now().strftime("%B%d%Y") in item and 'weight' in item:
				value = item.split(',')
				weight = value[2]
				weight = "weight: %s LBS" % (weight.strip('\n'))
	#add to log window

	#building text for main window


	#Main Window#
	message = weight+'\n'+basecalsstr+'\n'+calsconsumed+'\n'+calssofar+'\n'+'calories left today: %s' % (NewBase)+'\n'+steps+'\n'+modetext
	command = buttonbox(msg=message, title='healthmon Overview'+version, choices=('log', 'refresh', 'stats','exit'), image='images/'+zone,)
	#End Main Window#



	#button actions
	if command == 'refresh':
		cls()
		main(0)
	if command == 'stats':
		msgbox('I am so sad right now')
		cls()
		main(0)
	if command == 'exercise':
		value = input('enter exercise calories ')
		statsfile = open('statsfile.csv', 'a')
		statsfile.write('exercise,'+datetime.datetime.now().strftime("%B%d%Y")+','+value+'\n')
		statsfile.close()
		cls()
		main(0)
	if command == 'log': # show the food log so far as well as the current weigh and other useful information while logging.
		message = basecalsstr+'\n'+calsconsumed+'\n'+calssofar+'\n'+steps
		command = buttonbox(msg=message, title='healthmon Log '+version, choices=('add food', 'add exercise', 'add steps', 'complete log', 'add weight', 'stats', 'done'), image='images/notebook01.png')
		if command == 'done':
			main(0)
		if command == 'add steps':
			value = enterbox(msg='enter the amount of steps')
			statsfile = open('statsfile.csv', 'a')
			statsfile.write('steps,'+datetime.datetime.now().strftime("%B%d%Y")+','+value+'\n')
			statsfile.close()
			main(0)
		if command == 'add weight':
			## working on this
			weighin = multenterbox(msg='weigh in', title='weigh in', fields=['weight','body fat'])
			data = open(profile, 'r')
			for item in data:
				if 'profile' in item:
					item = item.split(',')
					height=item[2]
					age=item[3]
					activityLVL=item[4].strip('\n')
				else:
					continue
			data.close()
			statsfile = open('statsfile.csv', 'a')
			statsfile.write('weight,'+datetime.datetime.now().strftime("%B%d%Y")+','+weighin[0]+'\n')
			statsfile.write('body fat,'+datetime.datetime.now().strftime("%B%d%Y")+','+weighin[1]+'\n')
			statsfile.close()
			profilesetup(weighin[0],height,age,activityLVL)
			cls()
			main(0)
		if command.lower() == 'add food':
			foodjournal = open(datetime.datetime.now().strftime("%B%d%Y")+".csv", 'a')
			food = multenterbox(msg='add food', title=' ', fields=['food','amount'], values=['','s* oz* g*'])
			entry = food_dict_get(food[0],food[1])
		if command == 'exit':
			sys.exit()
		if entry == None:
			cls()
			main(1)
		else:
			foodjournal.write(entry+'\n')
			cls()
			main(0)
	else:
		quit
	#end button actions



main(0)
