# FaceReko
School IoT project. Simple Raspberry Pi face recognition security system for something like a door.
This project was created for a Raspberry Pi with default account pi (adjust *install.sh* if different), a local mysql database and runs a simple WebApp.

The WebApp supports a login system with accounts in a MySQL DB. The FaceReko system can be turned ON or OFF from the WebApp along with viewing of access history with images.

## Hardware requirements:
Check frizting diagram/ image in repo for how to connect up the hardware.

- Raspberry Pi (Duh)
- PiCamera
- MFRC522 RFID reader and RFID card
- Red & Green LED diodes
- Buzzer

## Things to note: 
1. Default Pi account is used in *install.sh*, change accordingly if needed.
2. RFID tag ID is hardcoded in *rfid.py* under variable `hid`, change accordingly.
3. Account creation is manual by inserting into db.
4. MySQL login info in the codes has been hardcoded to my throwaway db, change/ setup accordingly.
5. There is a collection variable in *FaceReko.py* which needs to be changed to whatever collection name you set to later in install.

## Pre-requisite setups:
  
###  Amazon Web Service(AWS) Rekognition
  1) Create AWS account (Free Tier allows 5k API calls per month)
  2) Login and create a new IAM user with "AmazonRekognitionFullAccess" and "AdministratorAccess" permissions (Refer to AWS doc for help: https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)
  3) Go to Security Credentials tab in IAM users page, generate and note down your aws_access_key_secret and aws_access_key_id

###  Local MySQL DB
  1) Install it, create accounts etc...(If needed) Import given sql file or follow steps 2 - 4 to create database and tables.
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
You can simply just copy *install.sh* to */home/pi/* and `sudo chmod +x install.sh` then run it with `sudo ./install.sh` to install all  pre-requisite packages, configure AWS and setup FaceReko files.
    
Mid-run of *install.sh* you will be prompted for AWS config info (This is where your AWS credentials you noted down earlier come in). For the first 2 prompts **enter your AWS Key ID then Access Key**. The 3rd option will be for an **AWS server region which supports the Rekognition service** (eg. "ap-northeast-1" which is tokyo). A full list of which servers support the service and their shorthands can be found at https://docs.aws.amazon.com/general/latest/gr/rande.html (ctrl-F "Rekognition"). 

For the last option **just hit enter and leave default**.

Once complete, there should be a folder named *FaceReko* in */home/pi/* and permissions for it setup. (If there are any permission issues with the program later on just manually `sudo` run the last couple `chmod & chown` commands in *install.sh*).

From here `cd` into the FaceReko folder.

### AWS Rekognition setup
Run `python add_collection.py -n 'home'` (Replace 'home' with whatever you want to call your collection, remember to change the collection variable accordingly in *FaceReko.py*)

Run `python take_selfie.py` to take a photo of you or the person you want recognised. It will be saved in the same folder as *selfie.jpg*.

Run `python add_image.py -i 'selfie.jpg' -c 'home' -l 'Name'` (Replace 'home' with your collection name from earlier and 'Name' with the name of the person in *selfie.jpg*.

## Usage:
Simply `cd` into the FaceReko folder and run `python server.py`

The webapp will be running on raspberryPi IP:5000
	
## TODO:
- Account creation front-end
- Secure passwords with hashing
- Merge AWS Rekognition setup into front-end
- Save RFID card uid to DB
	- RFID card registration front-end
