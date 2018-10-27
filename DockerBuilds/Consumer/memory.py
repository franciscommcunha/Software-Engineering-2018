import threading, logging, abc, enum
from states import StateInterface, LightsState, BasicState

logger = logging.getLogger('consumerMain.memory')
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

class Mem(abc.ABC):

	@abc.abstractmethod
	def addState(self, type: str, room: str, state: StateInterface):
		pass

	@abc.abstractmethod
	def hasState(self, type: str, room: str) -> bool:
		pass

	@abc.abstractmethod
	def getEnumState(self, type: str, room: str) -> enum.Enum:
		pass

	@abc.abstractmethod
	def changeState(self, type: str, room: str, *newState):
		pass


class Memory(Mem):
	def __init__(self):
		self.mem = {}
		self.access = threading.Lock()

	def addState(self, type, room, state):
		if self.hasState(type, room):
			logger.error("State of type %s in room %s does exist in memory!!" % (type, room))
			raise Exception("State ALREADY exist in memory, check first!")
		self.access.acquire()
		if type not in self.mem:
			self.mem[type] = {room: state}
		else:
			if room not in self.mem[type]:
				self.mem[type][room] = state
		self.access.release()
		logger.info("Added a new state of type %s in room %s!" % (type, room))

	def hasState(self, type, room):
		self.access.acquire()
		if type in self.mem:
			if room in self.mem[type]:
				self.access.release()
				return True
		self.access.release()
		return False

	def getEnumState(self, type, room):
		if not self.hasState(type, room):
			logger.error("State of type %s in room %s does not exist in memory!!" % (type, room))
			raise Exception("State does not exist in memory, check first!")
		return self.mem[type][room].getState()

	def changeState(self, type, room, *newState):
		if not self.hasState(type, room):
			logger.error("State of type %s in room %s does not exist in memory!!" % (type, room))
			raise Exception("State does not exist in memory, check first!")
		self.mem[type][room].changeState(*newState)

