#!/usr/bin/env python

from picamera import PiCamera
import time
import os, MySQLdb
import boto3 as b3
from argparse import ArgumentParser
from time import gmtime, strftime
from gpiozero import LED

def get_client():
    return b3.client('rekognition')
	
def check_face(client, file):
    face_detected = False
    with open(file, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()})
        if (not response['FaceDetails']):
            face_detected = False
        else: 
            face_detected = True

    return face_detected, response

def check_matches(client, file):
    collection = 'home'
    face_matches = False
    with open(file, 'rb') as image:
        response = client.search_faces_by_image(CollectionId=collection, Image={'Bytes': image.read()}, MaxFaces=1, FaceMatchThreshold=85)
        if (not response['FaceMatches']):
            face_matches = False
        else:
            face_matches = True

    return face_matches, response

count = 3
camera = PiCamera()

def main():
	try:
		db = MySQLdb.connect("localhost", "root", "dmitiot", "FaceReko")
		curs = db.cursor()
		print("Successfully connected to database!")
	except:
		print("Error connecting to mySQL database")
	
	#directory = '/home/pi/pi-detector/faces'

	#if not os.path.exists(directory):
	#	os.makedirs(directory)

	print '[+] A photo will be taken in 3 seconds...'

	for i in range(count):
		print (count - i)
		time.sleep(1)

	
	image = 'image_current.jpg'
	camera.capture(image)
	print 'Your image was saved to %s' % image
	
	client = get_client()
    
	print '[+] Running face checks against image...'
	result, resp = check_face(client, 'image_current.jpg')

	if (result):
		print '[+] Face(s) detected with %r confidence...' % (round(resp['FaceDetails'][0]['Confidence'], 2))
		print '[+] Checking for a face match...'
		resu, res = check_matches(client, 'image_current.jpg')
    
		if (resu):
			person = res['FaceMatches'][0]['Face']['ExternalImageId']
			similarity = round(res['FaceMatches'][0]['Similarity'], 2)
			confidence = round(res['FaceMatches'][0]['Face']['Confidence'], 2)
			print 'Identity matched %s with %r similarity and %r confidence...' % (person, similarity, confidence)
			
			sql = "INSERT into AccessLog (Name, Time, Similarity, Confidence) VALUES (%s, NOW(), %s, %s)"
			#print(sql)
			curs.execute(sql, (person, similarity, confidence))
			db.commit()
			curs.close()
			db.close()
			
			return True
			
		else:
			print 'No face matches detected...' 

	else :
		print "No faces detected..."
        
if __name__ == '__main__':
    main()