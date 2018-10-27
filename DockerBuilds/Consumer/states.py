from enum import Enum, unique
import threading, logging, abc


logger = logging.getLogger('consumerMain.states')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('domoticsConsumer.log')
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

class StateInterface(abc.ABC):
	@abc.abstractmethod
	def changeState(self, *args):
		pass

	@abc.abstractmethod
	def hasChanged(self) -> bool:
		pass

	@abc.abstractmethod
	def getState(self) -> Enum:
		pass

################################################
######### BASE CLASSES FOR ACTUATORS############
################################################
class State(StateInterface):
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
	@abc.abstractmethod		
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
		self.author = None
		logger.debug("Lights State created")

	#Changes state
	#changeState(newState, author:("manual", "auto"))
	def changeState(self, *args):
		if len(args) != 2:
			logger.error("Wrong number of arguments! Need two arguments!")
			raise Exception("Wrong number of arguments", "need Two argument")
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
		toReturn = self.author.deepcopy()
		self.access.release()
		return toReturn


class MovementState(State):
	def __init__(self):
		State.__init__(self, allStates=[], defaultState=BasicState.OFF, killState=BasicState.KILL)
		logger.debug("Movement State created")

	#Changes state
	#changeState(newState, author:("manual", "auto"))
	def changeState(self, *args):
		if len(args) != 1:
			logger.error("Wrong number of arguments! Need one arguments!")
			raise Exception("Wrong number of arguments", "need one argument")
		if args[0] not in self.states:
			logger.error("That state is not valid. Need one valid argument (0,1)")
			raise Exception("Argument not possible", "need one valid argument")
		if args[0] == self.getState():
			return
		self.access.acquire()
		self.stateChanged = True
		self.currentState = args[0]
		self.access.release()