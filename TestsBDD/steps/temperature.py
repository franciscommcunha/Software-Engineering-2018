class Temperature(object):
	def regulate_max(self, current_temp, mod_temp):
			if(current_temp>mod_temp):
				return mod_temp
			else:
				return current_temp	

	def regulate_min(self, current_temp, mod_temp):
			if(current_temp<mod_temp):
				return mod_temp
			else:
				return current_temp				