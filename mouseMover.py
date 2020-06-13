import win32api, win32con
import sys
import math, numpy
import time
import pickle
import threading
import subprocess

leftClickState=win32api.GetKeyState(0x01)
leftCickStatPrev=[]

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def call(command):
	try:
		subprocess.call(command,shell=True)
	except Exception as e:
		print(e)

def check(command):
	try:
		subprocess.check_output(command,shell=True)
	except Exception as e:
		print(e)

#print(sys.argv)
def get(arg,default=0):
	try:
		if arg in sys.argv:
			return sys.argv[sys.argv.index(arg)+1]
		else:
			return default
	except Exception as e:
		print(e)

tLimit = int(get('-t',-1))

print(' ')
print("Running for %d" % tLimit)
Hz=float(get('-h',100))
print("... at %s Hz" % Hz)
T=float(1.0/float(Hz));

#tLimit = 2
#Hz=100
#T=0.01

logDir=".\\logs"
logging=False
logStart=[]
logStop=[]

try:
	lastSessionIDFile=open("lastSessionID",'r')
	lastSessionID=lastSessionIDFile.read().rstrip('\n')
	if not lastSessionID:
		lastSessionID="%d" % numpy.random.randint(0,100)
	print("Session ID: %s" % lastSessionID)
	lastSessionIDFile.close()
	lastSessionIDFile=open("lastSessionID",'w')
	lastSessionIDFile.write("%s" % (int(lastSessionID)+1))
	lastSessionIDFile.close()
except Exception as e:
	print(e)

print('Checking user input')

pos=[]
set=[]

def move(x,y):
	print(x)
	print(y)
	try:
		d = math.sqrt((y[0]-x[0])+(y[1]-x[1]))
	except Exception as e:
		d = math.sqrt((x[0]-y[0])+(x[1]-y[1]))
	print(d)
	for i in range(0,int(d)):
		print(i)
		win32api.SetCursorPos((i*10,i*10))
		time.sleep(0.1)

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def startlog():
	logging=True

def stoplog():
	logging=False

def log():
	global set, pos, logStart, logStop, logging, logFile, T, tLimit, sessionID
	global leftClickState, lastSessionID
	rate=0
	i=1
	dtPrev=0
	dt=0
	dtAvg=0
	dtList=[]
	avg=0
	samples=1000
	try:
		#tempLog=check('mktemp')
		logFile.write("%s\n" % time.time())
		while(logging):
	# GET CURSOR & WRITE POSITION
			pos = win32api.GetCursorPos()
			set.append(pos)
#			print(pos)
			dtPrev=dt
			dt = time.clock() - logStart
			dtList.append(dt)
			if tLimit != -1 and dt > tLimit:
				logging = False
			leftClickStatePrev = leftClickState
			leftClickCheck=win32api.GetKeyState(0x01)
#			print(leftClickCheck)
			logFile.write("%s,%s,%s" % (dt,pos[0],pos[1]))
			logFile.flush()
			if leftClickState != leftClickCheck:
				leftClickState = leftClickCheck
				if leftClickCheck < 0:
					logFile.write(",mouse_down")
				else:
					logFile.write(",mouse_up")
	# COMPUTE AVG HZ
#			print(dtPrev - dt)
			#avg=float(dtAvg/i+1)+float(dt/i)
#			try:
#				avg=numpy.diff(numpy.array(dtList[i-samples:i-1])).mean()
#			except Exception as e:
#				dummy=0
#				print(e)

	# LOOP DT LIST
#			print(dtList)
	# AVG LOOP HZ
#			print(float(1.0/float(avg)))
	#DO LAST
			i+=1
			logFile.write('\n')
			time.sleep(T)
#			call('echo %s >> %s' % (pos,tempLog))
		#call("mv %s %s/%s" % (tempLog, logDIr, tempLog))
	except Exception as e:
		print(e)
#	logFile.flush()
	logFile.close()
	print("Closed log: %s" % (logFile.name))

#	logFile=open("%s" % tempLog,"r")
#	print(logFile.read())

value = 0
def val():
	global pos
	global value
	while(value < 2):
		time.sleep(1)

tempLog="%s\\%s.csv" % (logDir,lastSessionID)
print("Logging to %s" % tempLog)
logFile=open("%s" % tempLog,"a")

logging=True
logStart = time.clock()

tLog = StoppableThread(target=log,args=())
#tLog.daemon = True
try:
	tLog.start()
except Exception as e:
	cleanup_stop_thread()
	print(e)

#log()

#tCheck = Thread(target=log,args=())
#tCheck.start()

def printVal():
	global pos
	print(pos)

def changeVal():
	global value
	value+=1

#threading.start_new_thread(log,())

#click(0,0)
#move((0,0),(200,200))
