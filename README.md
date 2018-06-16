# FaceReko
School IoT project. Simple Raspberry Pi face recognition security system for something like a door.
This project was created for a Raspberry Pi with default account pi (adjust install.sh if different) and a local mysql database.

FaceReko hardware consists of a Raspberry Pi(duh), PiCamera, MFRC522 RFID scanner, a red LED, a green LED and a buzzer. (Check frizting diagram/ image for how to connect hardware) 

Things to note: 1. RFID tag id is hardcoded in rfid.py, change accordingly.
                2. Account creation is manual by inserting into db.
                3. MySQL login info in the codes has been hardcoded to my throwaway db, change/ setup accordingly.

Prerequisites:
  
  Amazon Web Service(AWS) Rekognition -
  1) Create AWS account (Free Tier allows 5k API calls per month)
  2) Login and create a new IAM user with "AmazonRekognitionFullAccess" and "AdministratorAccess" permissions (Refer to AWS doc for help:   https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html)
  3) Go to Security Credentials tab in IAM users page, generate and note down your aws_access_key_secret and aws_access_key_id

  Local MySQL DB -
  1) Install it, create accounts etc... Import given sql file or follow steps 2 - 4 to create database and tables.
  2) Create a database called "FaceReko" 
  3) Create table "AccessLog" with the following columns and data types(Column Name, Data Type): (ID, int(5), AutoIncrement),                  (Name, varchar(50)), (Time, datetime), (Similarity, decimal(10,2)), (Confidence, decimal(10,2)), (Image, varchar(30))
  4) Create table "Login" with the following columns and data types (Column Name, Data Type): (Username, varchar(30)), (Password,              varchar(30))
