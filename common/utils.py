from django.http import JsonResponse
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings
from selenium import webdriver
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

def get_firefox_driver():
	caps = DesiredCapabilities.FIREFOX
	caps["marionette"] = True
	caps["binary"] = settings.PATH_BINARY_FIREFOX
	return webdriver.Firefox(capabilities=caps)

def get_random_bill_amount():
	rounded_number = round(random.uniform(0, 101), 2)
	return rounded_number

def get_random_bill_amount_dict():
	return {
		'error': False,
		'data': get_random_bill_amount()
	}

def get_response_for_test_credentials():
	return JsonResponse(get_random_bill_amount_dict())

def are_test_credentials_passed(username, password):
	return (username == 'test') and (password == 'test')

def add_error_and_data_keys(dict):
	new_dict = {}
	new_dict['error'] = False
	new_dict['data'] = dict
	return new_dict

def get_error_response(driver):
	e = sys.exc_info()
	pp.pprint(e)
	driver.quit()
	return {
		'error': True,
		'data': None,
	}