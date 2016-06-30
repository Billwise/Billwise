from django.shortcuts import render
from common import utils
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
# Create your views here.

WAIT_TIME_MAX_IN_SECONDS = 10

def wait_for_element_with_id_to_load(driver, id):
	wait = WebDriverWait(driver, 10)
	wait.until(EC.presence_of_element_located((By.ID, id)))

def wait_for_start_of_url_load(driver, url, time_wait_left):
	if driver.current_url != url:
		if time_wait_left > 0:
			time.sleep(1)
			wait_for_start_of_url_load(driver, url, time_wait_left - 1)

def login_with_credentials(driver, username, password):
	driver.get('https://myaccount.singtel.com/login.aspx')
	driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
	wait_for_element_with_id_to_load(driver, 'loginid')
	user_id_element = driver.find_element_by_name("loginid")
	password_element = driver.find_element_by_name("pass")
	user_id_element.send_keys(username)
	password_element.send_keys(password)
	password_element.submit()
	wait_for_start_of_url_load(driver, 'https://myaccount.singtel.com/myaccount/account_summary.aspx', WAIT_TIME_MAX_IN_SECONDS)


def make_dictionary_from_billing_html_table(page_html):
	parser = BeautifulSoup(page_html)
	billing_information_dict = {}
	bills_list = []
	for element in parser.find('table', {'id': 'Table8'}).find_all('tr', {'class': 'FirstRow-white'}):
		td_elements = element.find_all('td')
		bill_information_dict = {}
		bill_information_dict['Bill ID'] = td_elements[0].get_text()
		bill_information_dict['Bill Date'] = td_elements[1].get_text()
		bill_information_dict['Due Date'] = td_elements[2].get_text()
		bill_information_dict['Current Charges'] = td_elements[3].get_text()
		bills_list.append(bill_information_dict)
	billing_information_dict['bills'] = bills_list
	billing_information_dict['account_number'] = re.findall(r'\d+', parser.find('table', {'id': 'Table9'}).find_all('td')[2].get_text())[0]
	billing_information_dict['amount_due'] = re.findall(r"[-+]?\d*\.\d+|\d+", parser.find('table', {'id': 'Table9'}).find_all('td')[1].get_text().strip())[0]
	return billing_information_dict

def get_bills(driver, username, password):
	login_with_credentials(driver, username, password)
	driver.get('https://mybill.singtel.com/ebill/mybill.asp')
	wait_for_element_with_id_to_load(driver, 'Table8')
	page_html = driver.page_source
	driver.quit()
	return make_dictionary_from_billing_html_table(page_html)

def get_bill_with_credentials(username, password):
	driver = utils.get_firefox_driver()
	try:
		return utils.add_error_and_data_keys(get_bills(driver, username, password))
	except:
		return utils.get_error_response(driver)

@require_http_methods(["GET"])
def get_bill(request):
	username = request.GET.get('username', None)
	password = request.GET.get('password', None)
	if (not username) or (not password):
		return HttpResponseBadRequest()
	elif utils.are_test_credentials_passed(username, password):
		return utils.get_response_for_test_credentials()
	else:
		bill_amounts_dict = get_bill_with_credentials(username, password)
		return JsonResponse(bill_amounts_dict)