class CO2(object):
	def notify(self, current_co2):
		if(current_co2>=1500):
			notification=True
			return notification
		else:
			notification=False
			return notification	