"""
Order of user steps, not build steps

1) Open app from homescreen

2) Adjust speed range

3) Start recording pace button
 
4) Gather data from motion, location, and/or strava api

5) Convert from m/s to mile time

6) Speak warning when threshold triggered

7) Resume music playback
	spotify and youtube never stop

"""

import time, motion, location, speech, sound, ui


# 5) Conversion
def convert_speed_to_string(speed):

	if speed > 0:
		mile_time = 26.822403501933/speed
	else:
		mile_time = 0

	minutes = int(mile_time)
	seconds = round((mile_time*60) % 60)

	time = "%02d:%02d" % (minutes, seconds)
	return time

# 2) Set Pace


def slider_action(sender):
	# Get the root view:
	v = sender.superview
	
	# Get the sliders:
	raw_input = v['slider1'].value
	
	# Calculate pace from the slider value:
	inv_input = 1-raw_input # Flip slider to 1-0, or a smaller input should be a faste
	speed = inv_input*10 # slider values range from 0-1
	time = convert_speed_to_string(speed)
	
	#Display goal mile time
	v['label1'].text = 'Target Pace: ' + time

# 4) Data

def start_gps():
	location.start_updates()
	current_speed_ms = location.get_location()['speed']
	return current_speed_ms

def stop_gps():
	location.stop_updates()

# 6) Speak Commands

goal_range = [-1, 1, 2]

def not_running():
	stop_gps()

def running(pace):
	if pace < goal_range[1]:
		print('Faster.')
		speech.say('Faster', 'en_US')
		stop_gps()
	if pace > goal_range[0]:
		print('Slow Down.')
		speech.say('Slow Down', 'en_US')
		stop_gps()

	
def loop(state):
	print(state)
	#while state == True:
		#print(state)
		#running(start_gps())
		#time.sleep(7) #check pace every 7 seconds

# 3) Start/Stop

def button_action(sender):
	v = sender.superview
	global state
	state = not state
	if state == True:
		v['button1'].background_color = 'red'
		v['button1'].title = 'Stop'
		loop(state)
	if state == False:
		v['button1'].background_color = '0079ff'
		v['button1'].title = 'Start'
		stop_gps()

					
										
															
					
#Load screen
v = ui.load_view('marathon')

#Initial values
slider_action(v['slider1'])
state = False
v['button1'].value = False

if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('sheet')
else:
	# iPhone
	v.present()
	







