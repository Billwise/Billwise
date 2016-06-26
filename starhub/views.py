from django.shortcuts import render
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings
from selenium import webdriver
import pprint
from django.http import HttpResponseBadRequest, JsonResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
import random
import sys

pp = pprint.PrettyPrinter(indent=4)

# Create your views here.
def get_bill(request):
	username = request.GET.get('username', None)
	password = request.GET.get('password', None)
	if (not username) or (not password):
		return HttpResponseBadRequest()
	elif are_test_credentials_passed(username, password):
		return JsonResponse(get_random_bill_amount_dict())
	else:
		bill_amounts_dict = get_bill_with_credentials(username, password)
		return JsonResponse(bill_amounts_dict)

def are_test_credentials_passed(username, password):
	return (username == 'test') and (password == 'test')

def get_random_bill_amount():
	rounded_number = round(random.uniform(0, 101), 2)
	return rounded_number

def get_random_bill_amount_dict():
	return {
		'error': False,
		'data': get_random_bill_amount()
	}

def get_bill_with_credentials(username, password):
	driver = get_firefox_driver()
	login_with_credentials(driver, username, password)
	try:
		return add_error_and_data_keys(get_bills(driver))
	except:
		e = sys.exc_info()
		pp.pprint(e)
		driver.quit()
		return {
			'error': True,
			'data': None,
		}


def get_json_from_page_html(driver):
	pre_element = driver.find_element_by_tag_name("pre")
	json_text = json.loads(pre_element.text)
	pp.pprint(json_text)
	driver.quit()
	return json_text

def get_bills(driver):
	wait = WebDriverWait(driver, 10)
	wait.until(EC.presence_of_element_located((By.ID,'selectAccount')))
	driver.get('https://secure.starhub.com/paybill/getbillingaccounts')
	return get_json_from_page_html(driver)

def get_firefox_driver():
	caps = DesiredCapabilities.FIREFOX
	caps["marionette"] = True
	caps["binary"] = settings.PATH_BINARY_FIREFOX
	return webdriver.Firefox(capabilities=caps)

def login_with_credentials(driver, username, password):
	driver.get('https://secure.starhub.com/paybill/index')
	user_id_element = driver.find_element_by_name("fake_uid")
	password_element = driver.find_element_by_name("password")
	user_id_element.send_keys(username)
	password_element.send_keys(password)
	driver.find_element_by_class_name("login_button_extra_long").click()
	accept_security_warning(driver)

def accept_security_warning(driver):
	driver.switch_to_alert().accept()

def add_error_and_data_keys(dict):
	new_dict = {}
	new_dict['error'] = False
	new_dict['data'] = dict
	return new_dict