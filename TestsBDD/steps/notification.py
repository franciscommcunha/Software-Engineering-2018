class Notification(object):
	def submit_notification(self, type, date):
		if(type!="" and date!=""):
			notif="Submission successful"
			print(notif)
			return True
		else:
			notif="Submission failed"
			print(notif)
			return False