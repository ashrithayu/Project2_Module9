# 3. Dataset scrape from any website using beautiful soup
# 4. analysis of the data from 2 or 3

import requests
import xml.etree.ElementTree as ET
import pandas as pd

class SitemapParser:
    """
    A class for parsing sitemaps from a given robots.txt file and extracting information from the sitemaps.

    Parameters:
    - robots_url (str): The URL of the robots.txt file containing information about sitemaps.

    Methods:
    - get_sitemap_urls(): Fetches the content of robots.txt and extracts the sitemap URLs.
    
    - parse_xml(sitemap_url): Parses the XML content of a sitemap URL and extracts information.

        Parameters:
        - sitemap_url (str): The URL of the sitemap to parse.

        Returns:
        A list of dictionaries containing information about each URL in the sitemap.

    - extract_page_sitemap(url): Extracts information, including images, from a page sitemap.

        Parameters:
        - url (str): The URL of the page sitemap to extract information from.

        Returns:
        A list of dictionaries containing information about each URL in the page sitemap.

    - parse(): Fetches sitemap URLs, parses the XML content of the first sitemap, and extracts detailed information.
      Returns the information in the form of a pandas DataFrame.
    """

    def __init__(self, robots_url):
        """
        Initializes the SitemapParser instance.

        Parameters:
        - robots_url (str): The URL of the robots.txt file containing information about sitemaps.
        """
        self.robots = robots_url
        self.sitemaps = []

    def get_sitemap_urls(self):
        """
        Fetches the content of robots.txt and extracts the sitemap URLs.
        """
        response = requests.get(self.robots)
        lines = response.text.split('\n')
        for line in lines:
            if line.startswith("Sitemap:"):
                self.sitemaps.append(line.split(": ")[1])

    def parse_xml(self, sitemap_url):
        """
        Parses the XML content of a sitemap URL and extracts information.

        Parameters:
        - sitemap_url (str): The URL of the sitemap to parse.

        Returns:
        A list of dictionaries containing information about each URL in the sitemap.
        """
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            sitemap_data = []
            for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                loc = sitemap_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                lastmod = sitemap_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text
                
                sitemap_data.append({
                    'loc': loc,
                    'lastmod': lastmod
                })
        return sitemap_data

    def extract_page_sitemap(self, url):
        """
        Extracts information, including images, from a page sitemap.

        Parameters:
        - url (str): The URL of the page sitemap to extract information from.

        Returns:
        A list of dictionaries containing information about each URL in the page sitemap.
        """
        xml_content = requests.get(url).text
        root = ET.fromstring(xml_content)
        data = []
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            lastmod = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text
            
            # Extract array of image URLs
            image_elems = url_elem.findall('.//{http://www.google.com/schemas/sitemap-image/1.1}image')
            image_urls = [image_elem.find('{http://www.google.com/schemas/sitemap-image/1.1}loc').text for image_elem in image_elems]
            
            data.append({'loc': loc, 'lastmod': lastmod, 'images': image_urls})
        return data

    def parse(self):
        """
        Fetches sitemap URLs, parses the XML content of the first sitemap, and extracts detailed information.
        Returns the information in the form of a pandas DataFrame.
        """
        self.get_sitemap_urls()
        data = self.parse_xml(self.sitemaps[0])
        for item in data:
            item['data'] = self.extract_page_sitemap(item['loc'])
        return pd.DataFrame(data)


if __name__ == "__main__":
    # Replace with your robots.txt URL
    robots_url = "https://befound.pt/robots.txt"

    crawler = SitemapParser(robots_url)
    df = crawler.parse()
    print(df)
