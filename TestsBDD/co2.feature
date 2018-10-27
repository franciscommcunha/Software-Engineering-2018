Feature: CO2 value
	As a End user
	It is defined a maximum level of CO2 for security reasons


	Scenario: High CO2 value

	Given A room CO2 level is 1500 ppm
	
	When The CO2 notifier acts

	Then Warn the user
