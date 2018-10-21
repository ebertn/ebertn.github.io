from flask import Flask
import our_myo
import jsonify
app = Flask(__name__)

@app.route('/output')
def hello_world():
    return jsonify(our_myo.orientation)

if __name__ == '__main__':
	myo.init(sdk_path='./myo-sdk-win-0.9.0/')
	hub = myo.Hub()
	listener = Listener()

	hub.run_in_background(listener.on_event, 500)

	app.run()