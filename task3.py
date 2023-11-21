import requests
from bs4 import BeautifulSoup
import pandas as pd

class BeautifulSoupScraper:
    """
    A web scraper using BeautifulSoup to extract data from a specified URL.

    Attributes:
    - url (str): The URL of the website to be scraped.
    - scraped_data: The raw HTML content containing the scraped data.

    Methods:
    - scrape(): Fetches the HTML content from the specified URL and extracts the table using BeautifulSoup.
    - parse(): Parses the scraped HTML data and returns a pandas DataFrame.

    Example:
    scraper = BeautifulSoupScraper()
    data_frame = scraper.parse()
    """

    def __init__(self):
        """
        Initializes the BeautifulSoupScraper with a default URL and sets scraped_data to None.
        """
        self.url = "http://www.nationmaster.com/country-info/stats/Media/Internet-users"
        self.scraped_data = None

    def scrape(self):
        """
        Fetches the HTML content from the specified URL and extracts the table using BeautifulSoup.
        """
        res = requests.get(self.url, verify=False)
        soup = BeautifulSoup(res.content, 'lxml')
        table = soup.find_all('table')[0]
        self.scraped_data = table

    def parse(self):
        """
        Parses the scraped HTML data and returns a pandas DataFrame.

        Returns:
        - pandas.DataFrame: A DataFrame containing the parsed data.
        """
        self.scrape()
        df = pd.read_html(str(self.scraped_data))
        return df[0]

if __name__ == '__main__':
    bss = BeautifulSoupScraper()
    df = bss.parse()