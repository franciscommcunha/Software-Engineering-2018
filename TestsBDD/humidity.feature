Feature: Humidity value
	As a End user
	It is defined a maximum percentage of humidity 

	Scenario: High humidity

	Given A room humidity is 45 %

	And I have defined the maximum to 35 %

	When The humidity regulator acts

	Then Lower the room temperature
