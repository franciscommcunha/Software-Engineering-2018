Feature: Notification
	As a End user
	It is defined an alarm for a specific event


	Scenario: Alarm submission

	Given An alarm for a medical appointement is submited
	
	And It is for 23/12/2034
	
	When The user submits the alarm

	Then It is given a success message
