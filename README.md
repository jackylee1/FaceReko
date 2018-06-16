# FaceReko
School IoT project. Simple Raspberry Pi face recognition security system for something like a door.
This project was created for a Raspberry Pi with default account pi (adjust install.sh if different) and a local mysql database.

FaceReko hardware consists of a Raspberry Pi(duh), PiCamera, MFRC522 RFID scanner, a red LED, a green LED and a buzzer. (Check frizting diagram/ image for how to connect hardware).

The WebApp supports a login system with accounts in a MySQL DB. The FaceReko system can be turned ON or OFF from the WebApp along with viewing of access history with images.

## Things to note: 
1. RFID tag id is hardcoded in rfid.py, change accordingly.
2. Account creation is manual by inserting into db.
3. MySQL login info in the codes has been hardcoded to my throwaway db, change/ setup accordingly.

## Pre-requisite setups:
  
###  Amazon Web Service(AWS) Rekognition
  1) Create AWS account (Free Tier allows 5k API calls per month)
  2) Login and create a new IAM user with "AmazonRekognitionFullAccess" and "AdministratorAccess" permissions (Refer to AWS doc for help: https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)
  3) Go to Security Credentials tab in IAM users page, generate and note down your aws_access_key_secret and aws_access_key_id

###  Local MySQL DB
  1) Install it, create accounts etc... Import given sql file or follow steps 2 - 4 to create database and tables.
  2) Create a database called "FaceReko" 
  3) Create table "AccessLog" with the following columns and data types(Column Name, Data Type): 
		```
		(ID, int(5), AutoIncrement)
		(Name, varchar(50))
		(Time, datetime)
		(Similarity, decimal(10,2))
		(Confidence, decimal(10,2))
		(Image, varchar(30))
		```
  4) Create table "Login" with the following columns and data types (Column Name, Data Type): 
		```
		(Username, varchar(30))
		(Password, varchar(30))
		```
  
##  Install:
You can simply just copy install.sh to /home/pi and `sudo chmod +x install.sh` then run it with `sudo ./install.sh` to install all        pre-requisite packages, configure AWS and setup FaceReko files.
    
Mid-run of install.sh you will be prompted with AWS config info (This is where your AWS credentials come in). When prompted **enter your AWS Key ID and Access Key**. The 3rd option will be for an **AWS server region which supports the Rekognition service** (eg. ap-northeast-1 which is tokyo). A full list can be found at https://docs.aws.amazon.com/general/latest/gr/rande.html (ctrl-F "Rekognition"). 
For the last option **just hit enter and leave default**.

## Usage:
Simply `cd` into the FaceReko folder and run `python server.py`

The webapp will be running on raspberryPi IP:5000
	
## TODO:
- Account creation front-end
- Secure passwords with hashing
- Save RFID card uid to DB
	- RFID card registration front-end
