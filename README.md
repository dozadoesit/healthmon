# healthmon
a simple application in python for tracking weightloss

![image](https://user-images.githubusercontent.com/66890080/161881257-d2068168-2a35-40a9-acea-ca76466d05d6.png)


The Goal of this application is to make it so that people can take charge of tracking their own food and weightloss privately. I am using the easyGUI library to keep the program simple and linear and as much as possible contain the whole project in one file. At this time the application is more a proof of concept than anything. 

How to install:
on Ubuntu or Ubuntu like Distros ( should work on any distro supporting python3 )

1) install dependencies:
$ sudo apt install python3-easygui python3-numpy
2) Clone repo
3) install itd: https://gitea.arsenm.dev/Arsen6331/itd
4) From a command prompt from within the healthmon directory run: $ python3 healthmon_test.py

Current features:
* Sync steps with pinetime ( you also need to have itd installed )
* the steps you sync count towards your calorie goal
* create a waitloss program
* log and track your calories
* log your weight 
* calculate BMI
* calculate calories burned every refresh

Upcoming features:
* charts to watch your progress
* better logging features 
* better file organization
