from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, JsonResponse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pprint
import re
import json

pp = pprint.PrettyPrinter(indent=4)

# Create your views here.

def login_with_credentials(driver, username, password):
	driver.get('https://services.spservices.sg/ssllogin/cs_mybills_login.asp')
	user_id_element = driver.find_element_by_name("UserID")
	password_element = driver.find_element_by_name("Password")
	user_id_element.send_keys(username)
	password_element.send_keys(password)
	password_element.submit()

def get_firefox_driver():
	caps = DesiredCapabilities.FIREFOX
	caps["marionette"] = True
	caps["binary"] = settings.PATH_BINARY_FIREFOX
	return webdriver.Firefox(capabilities=caps)

def does_string_end_with_at_least_one_number(s):
	m = re.search(r'\d+$', s)
	if m is not None:
	    return True
	return False

def get_first_floating_point_number_from_string(s):
	return re.findall(r"\d*\.\d+|\d+", s)[0]

def convert_bill_table_html_to_dict(html_table):
	table_data = [[cell.text.strip() for cell in row("td")] for row in BeautifulSoup(html_table)("tr")]
	json_dict = {}
	for row in table_data:
		if does_string_end_with_at_least_one_number(row[0]):
			json_dict[row[0]] = get_first_floating_point_number_from_string(row[1])
	return json_dict

def get_bills(driver):
	driver.get('https://services.spservices.sg/cs_mybills.asp')
	bills_table_element = driver.find_elements_by_tag_name('table')[4]
	bills_table_html = bills_table_element.get_attribute('innerHTML')
	driver.quit()
	return convert_bill_table_html_to_dict(bills_table_html)

def get_bill_with_credentials(username, password):
	driver = get_firefox_driver()
	login_with_credentials(driver, username, password)
	return get_bills(driver)

def add_error_and_data_keys(dict):
	new_dict = {}
	new_dict['error'] = False
	new_dict['data'] = dict
	return new_dict

@require_http_methods(["GET"])
def get_bill(request):
	username = request.GET.get('username', None)
	password = request.GET.get('password', None)
	if (not username) or (not password):
		return HttpResponseBadRequest()
	bill_amounts_dict = get_bill_with_credentials(username, password)
	json_response_dict = add_error_and_data_keys(bill_amounts_dict)
	return JsonResponse(json_response_dict)
	

