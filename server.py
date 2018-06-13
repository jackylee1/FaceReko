from flask import Flask, render_template, request, Response, session
from gpiozero import LED
from signal import pause
import datetime, os, signal
import gevent
import gevent.monkey
import subprocess as sp
from gevent.pywsgi import WSGIServer

app = Flask(__name__, template_folder='templates')

ledRed = LED(21)
ledGreen = LED(20)

#session['status']= "Offline"

@app.route("/")
def chart():
	import mysql.connector
	u, pw,h,db = 'root', 'dmitiot', 'localhost', 'FaceReko'
	data = []
	con = mysql.connector.connect(user=u,password=pw,host=h,database=db)
	print("Database successfully connected")
	cur = con.cursor()
	query = "SELECT Time, Name, Similarity, Confidence FROM AccessLog ORDER BY Time DESC LIMIT 10"
	cur.execute(query)
	for (Time, Name, Similarity, Confidence) in cur:
		d = []
		d.append("{:%d-%m-%Y %H:%M:%S}".format(Time))
		d.append(Name)
		d.append(Similarity)
		d.append(Confidence)
		data.append(d)    
	print(data)
	data_reversed = data[::-1]
	
	stat = session.get('status', 'Offline')
	templateData ={'status': stat}

	return render_template('index.html', data=data_reversed, **templateData)
	print('Rendered')

@app.route("/activate/")
def activate():
	extProc = sp.Popen(['python', 'rfid.py'])
	pid = extProc.pid
	session['proc'] = pid
	session['status'] = 'Active'
	templateData = {
	      		'title' : 'FaceReko',
	      		'response' : 'Facial Recognition active'
   			}
	return render_template('trigger.html', **templateData)

@app.route("/deactivate/")
def deactivate():
	pid = session.get('proc', None)
	session['status'] = 'Offline'
	os.kill(pid, signal.SIGKILL)
	ledRed.off()
	ledGreen.off()
	templateData = {
	      		'title' : 'FaceReko',
	      		'response' : 'Facial Recognition deactivated'
   			}
	return render_template('trigger.html', **templateData)

if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #Hardcoded for simplicity sake
	app.run(debug=True,host='0.0.0.0')
