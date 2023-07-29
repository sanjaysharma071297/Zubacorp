
# ZaubaCorp Companies
### Introduction
This script is designed to extract the company information from ZaubaCorp.

To Increase the coverage we are using 4 different type of filter and categorize companies based on their count. It employs four different filtering functions to group companies by various criteria. Depending on the count of companies, the script applies different filtering methods and stores the resulting Less comapny count URLs in a list.

### Prerequisites
To execute the repository, we need to use the below libraries:

```bash
Python (version 3.6 or higher)
$ pip install beautifulsoup4==4.4.1
$ pip install requests==2.25.1
$ pip install pymongo==4.4.1
$ pip install re
$ pip install logging
```

# How the Script Works

This script is a Python program that performs data collection from a website called zaubacorp.com, which provide information about companies. The script collects data from zaubacorp.com and stores it in a MongoDB collection.

Here's a step-by-step explanation of how the script works:

### Importing necessary libraries:

The script starts by importing the required libraries, including requests, BeautifulSoup from bs4, re, logging, and a custom module named pymongo_get_database.
### Defining helper functions:

The script defines several helper functions to assist in the data extraction process. These functions include page_count_, extract_data, get_url_response, extract_company, get_company_by_type, get_paid_up_type, get_by_age_type, and get_by_section_code_type.

### HTTP GET request to the base URL of zaubacorp
The script starts the main part by sending an HTTP GET request to the base URL of zaubacorp.com to retrieve the first page of company information.

#### Site limit Obeservation :
```bash
record_per_page = 30
max_page_limit = 13333
```
#### Calculating the threshold for filters
```bash
total_company_max_limit = record_per_page*max_page_limit
```
From the less_url_list (list) python program will extract 4 data points from the table and if there are multiple pages are available it will go by the pagination too and extract the same data.

#### Execution of script 
python3 zaubacorp_scraper.py
