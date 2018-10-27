from behave import given, when, then
from temperature import Temperature
from humidity import Humidity
from co2 import CO2
from notification import Notification


@given('A room temperature is {current:d}')
def given_current_input(context, current):
	context.current=current

@given('I have defined the maximum {maximum:d}')
def given_maximum_input(context, maximum):
	context.maximum=maximum

@when('The max regulator acts')
def regulator_max_act(context):
	context.temperature=Temperature()
	context.result_max=context.temperature.regulate_max(context.current,context.maximum)


@then('The room temperature is lowered to {result_max:d}')	
def check_result_max(context, result_max):
	assert context.result_max==result_max


@given('I have defined the minimum {minimum:d}')
def given_minimum_input(context, minimum):
	context.minimum=minimum

@when('The min regulator acts')
def regulator_min_act(context):
	context.temperature=Temperature()
	context.result_min=context.temperature.regulate_min(context.current,context.minimum)

@then('Room temperature is raised to {result_min:d}')	
def check_result_min(context, result_min):
	assert context.result_min==result_min

@given('A room humidity is {current_h:d} %')
def given_current_humidity(context, current_h):
	context.current_h=current_h


@given('I have defined the maximum to {maximum_h:d} %')
def given_maximum_humidity(context, maximum_h):
	context.maximum_h=maximum_h

@when('The humidity regulator acts') 	
def humidity_regulator_act(context):
	context.humidity=Humidity()
	context.result_h=context.humidity.regulate(context.current_h, context.maximum_h)

@then('Lower the room temperature')	
def check_result_h(context):
	assert context.result_h==True

@given('A room CO2 level is {co2_level:d} ppm')
def given_co2_level(context, co2_level):
	context.co2_level=co2_level

@when('The CO2 notifier acts') 	
def co2_notifier_act(context):
	context.co2=CO2()
	context.result_co2=context.co2.notify(context.co2_level)	

@then('Warn the user')	
def check_result_co2(context):
	assert context.result_co2==True	


@given('An alarm for a {type} is submited')
def given_type(context, type):
	context.type=type

@given('It is for {date}')
def given_date(context, date):
	context.date=date


@when('The user submits the alarm') 	
def submit_notification(context):
	context.notification=Notification()
	context.result_submission=context.notification.submit_notification(context.type,context.date)		

@then('It is given a success message')	
def check_result_notification(context):
	assert context.result_submission==True	
