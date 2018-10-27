class Humidity(object):
	def regulate(self, current, maximum):
		if(current>maximum):
			lower_temp=True
			return lower_temp
		else:
			lower_temp=False
			return lower_temp
				