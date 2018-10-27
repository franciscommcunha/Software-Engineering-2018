import threading, time
from sender_kafka import keydeserializer, send
from enum import Enum, unique
from kafka import KafkaConsumer
from kafka import KafkaProducer
from random import randint
import logging


logger = logging.getLogger('actuatorMain.actuator')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('domoticsActuators.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)



@unique
class BasicState(Enum):
	ON = 0
	OFF = 1
	KILL = 666

	def __int__(self):
		return self.value


################################################
######### BASE CLASSES FOR ACTUATORS############
################################################
class State:
	def __init__(self, allStates=[] , defaultState=None, killState=None ):

		self.states = allStates if allStates != [] else [BasicState.OFF, BasicState.ON, BasicState.KILL]
		self.currentState = defaultState if defaultState else self.states[0]
		self.killState = killState if killState else BasicState.KILL
		self.stateChanged = False
		self.access = threading.Lock()	

		if self.currentState not in self.states:
			self.states.append(self.defaultState)
		if self.killState not in self.states:
			self.states.append(self.killState)

	#Change state to a new state		
	def changeState(self, *args):
		pass

	#Returns true if the state has changed
	def hasChanged(self):
		self.access.acquire()
		toReturn = self.stateChanged
		self.access.release()
		return toReturn

	#Returns the current state of the actuator
	def getState(self):
		self.access.acquire()
		toReturn = self.currentState
		self.access.release()
		return toReturn


class LightsState(State):
	def __init__(self):
		State.__init__(self, allStates=[], defaultState=BasicState.OFF, killState=BasicState.KILL)
		self.author = "auto"
		logger.debug("Lights State created")

	#Changes state
	#changeState(newState, author:("manual", "auto"))
	def changeState(self, *args):
		if len(args) != 2:
			logger.error("Wrong number of arguments! Need two arguments!")
			raise Exception("Wrong number of arguments", "need one argument")
		if args[0] not in self.states:
			logger.error("That state is not valid. Need one valid argument (0,1)")
			raise Exception("Argument not possible", "need one valid argument")
		if args[0] == self.getState():
			return
		self.access.acquire()
		self.stateChanged = True
		self.currentState = args[0]
		self.author = "manual" if args[1] == "manual" else "auto"
		self.access.release()

	def getAuthor(self):
		self.access.acquire()
		toReturn = self.author.encode().decode()
		self.access.release()
		return toReturn


class Controller(threading.Thread):
	def __init__(self, mytype, room, action, state):
		threading.Thread.__init__(self)
		self.type = mytype
		self.room = room
		self.action = action
		self.state = state
		self.kill = False

	def run(self):
		pass
	def getRoom(self):
		return self.room
	def getType(self):
		return self.type
	def kill(self):
		self.kill = True
	def timeToDie(self):
		return self.kill;


## Manual Controllers
class ManualController(Controller):
	def __init__(self, type, room , action, state):
		Controller.__init__(self, type, room , action, state)
	def run(self):
		while not self.timeToDie():
			self.action.execute(self, self.state)


#######################################
#######  Online Controler #############
#######################################
class DomoticsController(Controller):
	def __init__(self, type, room, action, state):
		Controller.__init__(self, type, room , action, state)
	def run(self):
		while not self.timeToDie():
			self.action.execute(self, self.state)


class Action():
	def execute(self, controller, state):
		pass

# Lights consumer (topic: ConsumerOrders key: lights, msg={room|state})
# Message send (topic: ActuatorValues key:lights, msg={room|state})
class LightsConsumer(Action):
	def __init__(self, topic, room, servers):
		Action.__init__(self)
		logger.debug("Creating kafka-producer of Lights actuator for room %s" % room)
		self.consumer = KafkaConsumer(topic,
							bootstrap_servers=[servers],
							auto_offset_reset='latest',                
							enable_auto_commit=False,
							key_deserializer=keydeserializer)
		self.room = room
		logger.debug("Action consumer created")

	def execute(self, controller, state):
		for msg in self.consumer:
			if msg.key == "lights" and msg.offset > controller.offset:
				controller.offset = msg.offset
				m = message.value.decode().split('|')
				if m[0] == controller.getRoom():
					state.changeState(m[1], "auto" if len(m) < 3 else m[2])
					break


class LightsManual(Action):
	def __init__(self):
		Action.__init__(self)
		logger.debug("Manual Lights Action created")

	def execute(self, controller, state):
		rand = randint(0, 100)
		if rand == 100:
			nextState = BasicState.OFF if state.getState() == BasicState.ON else BasicState.ON
			state.changeState(nextState, "manual")
		time.sleep(2)



## The actuator for the lights, works with the consumer of movement sensor.
# Lights consumer (topic: ConsumerOrders key: lights, msg={room|state})
# Message send (topic: SensorsValues key:lights, msg={room|state})
class LightsActuator(threading.Thread):
	def __init__(self, topicReceiver, topicSender, room, servers):
		threading.Thread.__init__(self)
		self.state = LightsState()
		self.topicReceiver = topicReceiver
		self.topicSender = topicSender
		self.room = room
		self.servers = servers
		self.manController = ManualController("lights", self.room, LightsManual(), self.state)
		logger.debug("Manual Controler of Lights created for rom %s" % self.room)
		self.autoController = DomoticsController("lights", self.room, LightsConsumer(self.topicReceiver, self.room, self.servers), self.state)
		self.kill = False
		logger.debug("Lights actuator for room %s created!" % self.room)

	def run(self):
		logger.info("Actuator of lights in room %s has started!" % self.room)
		self.manController.start()
		logger.debug("Manual Controller of lights in room %s has started!" % self.room)
		self.autoController.start()
		logger.debug("Domotics Controller of lights in room %s has started!" % self.room)
		while not self._timeToDie():
			msg = "%s|%d|%s" % (self.room, int(self.state.getState()), self.state.getAuthor())
			send(msg, "lights", self.topicSender, self.servers)
			logger.debug("Domotics Actuator message sent. Message: %s ; from lights in room %s." % (msg, self.room))
			time.sleep(2)

		logger.info("Killing manual and domotics controllers of lights in room %s." % self.room)
		self.manController.kill()
		self.autoController.kill()
		logger.debug("Waiting for  manual and domotics controllers of lights in room %s to end" % self.room)
		self.manController.join()
		self.autoController.join()
		logger.info("Ending life cyle of Actuator of lights in room %s." % self.room)


	def orderToKill(self):
		self.kill = True

	def _timeToDie(self):
		return self.kill
