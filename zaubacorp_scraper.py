#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 19:45:04 2020

@author: sanjay sharma
"""

import requests
from bs4 import BeautifulSoup as bs
import re
import logging
from pymongo_get_database import get_database


def page_count_(response):
    """
        Extracts the total number of pages from the given HTTP response content.

        Parameters:
            response (HTTP response): An HTTP response object containing the content of a web page.

        Returns:
            int: The total number of pages as an integer. If the extraction fails or encounters an error,
            it returns the default value of 1, indicating a single page.
        """
    try:
        page_no=1
        number_of_page = re.search('>Page (.*?)<', response.content.decode()).group(1)
        page_no = int(number_of_page.split('of')[-1].strip().replace(',', ''))
    except Exception as e:
        logging.error("Issue in page_count_()",e)
    return page_no


def extract_data(soup):
    """
        Extracts data from a BeautifulSoup 'soup' object representing an HTML table and stores it in a list.
        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object containing the HTML table data.
        Returns:
            None
        here we are appending the dictionary company_data into company_information List.
        Raises:
            Exception: If there is an issue while extracting data from the HTML table.
        """

    try:
        table_data = soup.find('table', id='table')
        data = table_data.find_all('tr')
        for element in data[1:]:
            company_data = {}
            all_ = element.find_all('td')
            company_data['ID'] = all_[0].text
            company_data['Company']= all_[1].text
            company_data['RoC']= all_[2].text
            company_data['Status'] = all_[3].text

            company_information.append(company_data)
    except Exception as e:
        logging.error("Issue in extract_data()")


def get_url_response(url):
    """
        Fetches the HTML content of a given URL, parses it using BeautifulSoup, and extracts data from a specific table.

        Parameters:
            url (str): The URL from which to fetch the HTML content.

        Returns:
            tuple: A tuple containing the response object from the HTTP request (requests.Response)
            and the BeautifulSoup object representing the parsed HTML.

        Raises:
            Exception: If there is an issue while making the HTTP request, parsing the HTML,
            or extracting data from the table.
        """
    try:
        r = requests.get(url, headers=headers)
        soup = bs(r.content,'lxml')
        extract_data(soup)
    except Exception  as e:
        logging.error("Issue in get_url_response()")
    return r,soup



def extract_company(less_url_list):
    """
        Extracts data from multiple pages using a list of company links.
        Parameters:
            less_url_list (list): A list of URLs representing company profile pages.
        Returns:
            None
            Here we are calling get_url_response() that will get the data from each page using extract_data
        Raises:
            Exception: If there is an issue while processing any of the company links, making HTTP requests,
                       parsing the HTML, or extracting data from the tables on the pages.
        """
    for lurl in less_url_list:
        r,soup =get_url_response(lurl)
        page_count = page_count_(r)
        if page_count >1:
            for p_no in range(2, page_count + 1):
                pagination_url=lurl.split('-company.html')[0]+'/p-'+str(p_no)+'-company.html'
                r, soup = get_url_response(pagination_url)


def get_company_by_type(response, less_url_list, more_url_list,total_company_max_limit):
    """
        Filters company links based on their type and total company count.

        Parameters:
            response (requests.Response): The HTTP response containing the HTML content of a web page.
            less_url_list (list): A list to store URLs of companies with a total count below 'total_company_max_limit'.
            more_url_list (list): A list to store URLs of companies with a total count
            equal to or above 'total_company_max_limit'.
            total_company_max_limit (int): The maximum total count of companies considered as the threshold.

        Returns:
            None
            Here will store data in less_url_list & more_url_list (list)
        Raises:
            Exception: If there is an issue while filtering the company links based on their type and total count.
        """

    c_soup = bs(response.text, 'lxml')
    try:
        company_type = c_soup.find('h4', text='Company Type').find_next('ul').find_all('a', class_='secCode')

        # Create the key-value pairs
        for c_item in company_type:
            text = c_item.get_text()
            number = int(text.split('(')[-1].replace(',', '').split(')')[0])
            url = c_item['href']

            if number < total_company_max_limit:
                less_url_list.append(url)
            else:
                get_paid_up_type(url, less_url_list, more_url_list,total_company_max_limit)
    except:
        less_url_list = []
        logging.error("Issue in filtering: in get_company_by_type()")


def get_paid_up_type(more_count_url_company_by_type,less_url_list,more_url_list,total_company_max_limit):
    """
        Filters company links based on their paid-up capital count.

        Parameters:
            more_count_url_company_by_type (str): The URL representing a specific company type with more company count.
            less_url_list (list): A list to store URLs of companies with a paid-up capital count below 'total_company_max_limit'.
            more_url_list (list): A list to store URLs of companies with a paid-up capital count equal to or above 'total_company_max_limit'.
            total_company_max_limit (int): The maximum paid-up capital count considered as the threshold.

        Returns:
            None
            Here will store data in less_url_list & more_url_list (list)

        Raises:
            Exception: If there is an issue while filtering the company links based on their paid-up capital count.
        """

    g_response = requests.get(more_count_url_company_by_type, headers=headers)
    try:
        if g_response.status_code == 200:
            g_soup = bs(g_response.text, 'lxml')
            company_type = g_soup.find('h4', text='Paid Up Capital').find_next('ul').find_all('a', class_='secCode')

            # Create the key-value pairs
            for item in company_type:
                text = item.get_text()
                number = int(text.split('(')[-1].replace(',', '').split(')')[0])
                url = item['href']

                if number < total_company_max_limit:
                    less_url_list.append(url)
                else:
                    get_by_age_type(url, less_url_list, more_url_list,total_company_max_limit)
    except:
        logging.error("Issue in filtering: in get_paid_up_type() and using filtered urls from get_company_by_type()")

def get_by_age_type(more_url_paid_by_type,less_url_list,more_url_list,total_company_max_limit):
    """
        Filters company links based on their age category.
        Parameters:
            more_url_paid_by_type (str): The URL representing a specific company type with more paid-up capital count.
            less_url_list (list): A list to store URLs of companies with an age category below 'total_company_max_limit'.
            more_url_list (list): A list to store URLs of companies with an age category equal to or above 'total_company_max_limit'.
            total_company_max_limit (int): The maximum age category count considered as the threshold.
        Returns:
            None
            Here will store data in less_url_list & more_url_list (list)
        Raises:
            Exception: If there is an issue while filtering the company links based on their age category count.
        """

    age_response = requests.get(more_url_paid_by_type, headers=headers)
    try:
        if age_response.status_code == 200:
            age_soup = bs(age_response.text, 'lxml')
            company_type_by_age = age_soup.find('h4', text='Age Category').find_next('ul').find_all('a', class_='secCode')

            # Create the key-value pairs
            for item in company_type_by_age:
                text = item.get_text()
                number = int(text.split('(')[-1].replace(',', '').split(')')[0])
                url = item['href']

                if number < total_company_max_limit:
                    less_url_list.append(url)
                else:
                    get_by_section_code_type(url,less_url_list,more_url_list,total_company_max_limit)
    except:
        logging.error("Issue in filtering: in get_paid_up_type() and using filtered urls from get_paid_up_type()")


def get_by_section_code_type(more_url_paid_by_type,less_url_list,more_url_list,total_company_max_limit):
    """
        Filters company links based on their section code type.
        Parameters:
            more_url_paid_by_type (str): The URL representing a specific company type with more paid-up capital count.
            less_url_list (list): A list to store URLs of companies based on their section code type.
            more_url_list (list): Not used in this function. It's a placeholder to maintain consistency with other functions.
            total_company_max_limit (int): Not used in this function. It's a placeholder to maintain consistency with other functions.

        Returns:
            None
            here will store all the filtered urls in less_url_list.
        Raises:
            Exception: If there is an issue while filtering the company links based on their section code type.
        """
    response = requests.get(more_url_paid_by_type, headers=headers)
    try:
        if response.status_code == 200:
            soup = bs(response.text, 'lxml')
            company_type = soup.find('h4', text='Section Code').find_next('ul').find_all('a', class_='secCode')

            # Create the key-value pairs
            for item in company_type:
                text = item.get_text()
                number = int(text.split('(')[-1].replace(',', '').split(')')[0])
                url = item['href']
                less_url_list.append(url)
    except:
        logging.error("Issue in filtering: in get_paid_up_type()")

if __name__ == "__main__":

    # company_information will contain list of dictonary
    company_information = []
    headers = {
              "authority": "www.zaubacorp.com",
              "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
              "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
              "cache-control": "max-age=0",
              "referer": "https://www.zaubacorp.com/company-list-company.html",
              "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
              "sec-ch-ua-mobile": "?0",
              "sec-ch-ua-platform": "\"Linux\"",
              "sec-fetch-dest": "document",
              "sec-fetch-mode": "navigate",
              "sec-fetch-site": "same-origin",
              "sec-fetch-user": "?1",
              "upgrade-insecure-requests": "1",
              "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    # Sending the GET request with the defined headers
    response = requests.get('https://www.zaubacorp.com/company-list-company.html',  headers=headers)

    # Based on the Site Behaviour we defined the block size for company count per page and max page
    record_per_page = 30
    max_page_limit = 13333

    # Calculating the threshold for filters
    total_company_max_limit = record_per_page*max_page_limit

    # defining the list
    less_url_list = []
    more_url_list = []

    """calling get_company_by_type it will create filter based on 
    Company Type > Paid Up Capital > Age Category > Section Code
    """
    get_company_by_type(response, less_url_list, more_url_list,total_company_max_limit)

    # checking for the list with the urls else will execute on the base urls and it will extract data from the base url
    if less_url_list:
        extract_company(less_url_list)
    else:
        less_url_list = ['https://www.zaubacorp.com/company-list-company.html']
        extract_company(less_url_list)
        logging.error("Issue in filtering: The less_url_list is empty.")

    # Access of Mongo DB Atlas
    dbname = get_database()
    collection_name = dbname["company_info"]

    # storing the data in MongoDB collection from company_information
    for c_data in company_information:
        collection_name.insert_one(c_data)
