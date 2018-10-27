Feature: Temperature Regulator
	As a End user
	I define a maximum and minimum temperature values so that the room temperature never surpasses this values.
	
	Scenario: High temperature

	Given A room temperature is 27

	And I have defined the maximum 25

	When The max regulator acts

	Then The room temperature is lowered to 25

	Scenario: Low temperature

	Given A room temperature is 10

	And I have defined the minimum 15

	When The min regulator acts

	Then Room temperature is raised to 15


	

