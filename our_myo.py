import myo
from flask import Flask
import json
from multiprocessing import Process
from threading import Thread
app = Flask(__name__)

ori = 0

class Listener(myo.DeviceListener):
	
	def __init__(self):
		self.orientation = None
		self.status = 0

	def on_paired(self, event):
		print("Hello, {}!".format(event.device_name))
		event.device.vibrate(myo.VibrationType.short)

	def on_unpaired(self, event):
		return False  # Stop the hub

	def on_orientation(self, event):
		orientation = event.orientation
		self.orientation = orientation
		acceleration = event.acceleration
		gyroscope = event.gyroscope
		# ... do something with that

	def on_pose(self, event):
		#print(event.pose)
		if event.pose == myo.Pose.double_tap:
			print("Double Tap")
			self.status = 1
		else:
			self.status = 0
# global listener
listener = Listener()

@app.route('/output')
def hello_world():
	global listener
	data = {'x': listener.orientation.x, 'y': listener.orientation.y, 'status': listener.status}
	print(data)
	return json.dumps(data)

def run_myo(threadname):
	myo.init(sdk_path='./myo-sdk-win-0.9.0/')
	hub = myo.Hub()
	# listener = Listener()
	while hub.run(listener.on_event, 500):
		pass

def run_flask(threadname):
	global listener
	app.run()

if __name__ == '__main__':
	# Process(target=run_myo).start()
	# Process(target=run_flask).start()

	thread1 = Thread( target=run_flask, args=("Thread-1", ) )
	thread2 = Thread( target=run_myo, args=("Thread-2", ) )

	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()