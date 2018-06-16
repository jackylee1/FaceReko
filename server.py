from flask import Flask, render_template, request, Response, session, url_for
from gpiozero import LED
from signal import pause
import datetime, os, signal
import gevent
import gevent.monkey
import subprocess as sp
from gevent.pywsgi import WSGIServer

images = os.path.join('static', 'images')

app = Flask(__name__, template_folder='templates')
app.config['image_folder'] = images

ledRed = LED(21)
ledGreen = LED(20)


@app.route("/")
def chart():
	import mysql.connector
	u, pw,h,db = 'root', 'dmitiot', 'localhost', 'FaceReko'
	data = []
	con = mysql.connector.connect(user=u,password=pw,host=h,database=db)
	print("Database successfully connected")
	cur = con.cursor()
	query = "SELECT Time, Name, Similarity, Confidence, Image FROM AccessLog ORDER BY Time LIMIT 10"
	cur.execute(query)
	for (Time, Name, Similarity, Confidence, Image) in cur:
		d = []
		d.append("{:%d-%m-%Y %H:%M:%S}".format(Time))
		d.append(Name)
		d.append(Similarity)
		d.append(Confidence)
		d.append(Image)
		data.append(d)    
	#print(data)
	data_reversed = data[::-1]
	
	stat = session.get('status', 'Offline')
	templateData ={'status': stat}

	return render_template('index.html', data=data_reversed, **templateData)
	#print('Rendered')

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

@app.route("/<img>")
def display_image(img):
	full_filename = os.path.join(app.config['image_folder'], img)
	return render_template('image.html', img = full_filename)

if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #Hardcoded for simplicity sake
	app.run(debug=True,host='0.0.0.0')

