#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

class EProcurementScraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        # Send an HTTP GET request
        response = requests.get(self.url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the rows in the table that contain the data
            rows = soup.find_all('tr')

            # Initialize lists to store the scraped data
            data = {
                'Serial Number': [],
                'Organization Name': [],
                'Number of Tenders': []
            }

            # Loop through the rows and extract the data
            for row in rows:
                columns = row.find_all('td', align=['left', 'right'])
                if len(columns) == 3:
                    serial_number = columns[0].text.strip()
                    organization_name = columns[1].text.strip()
                    number_of_tenders = columns[2].text.strip()
                    data['Serial Number'].append(serial_number)
                    data['Organization Name'].append(organization_name)
                    data['Number of Tenders'].append(number_of_tenders)

            # Create a Pandas DataFrame from the scraped data
            df = pd.DataFrame(data)

            return df
        else:
            return None

    def save_to_csv(self, filename):
        # Scrape the data
        data = self.scrape_data()

        if data is not None:
            # Save the data to a CSV file
            data.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("Failed to retrieve the webpage.")

if __name__ == "__main__":
    # Define the URL of the website
    url = "https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page"

    # Create an instance of the scraper
    scraper = EProcurementScraper(url)

    # Specify the output CSV filename
    output_filename = "e_procurement_data.csv"

    # Save the scraped data to a CSV file
    scraper.save_to_csv(output_filename)


# In[2]:


df = pd.read_csv('e_procurement_data.csv')


# In[3]:


df


# In[ ]:




