import pandas as pd
from task3 import BeautifulSoupScraper
class InternetUsersAnalyzer:
    """
    A class to analyze internet users data.

    Attributes:
    - data_frame (pd.DataFrame): The DataFrame containing internet users data.

    Methods:
    - __init__(data_frame): Initializes the analyzer with the provided DataFrame.
    - analyse(): Performs basic analyses on the internet users data.
    """

    def __init__(self, data_frame):
        """
        Initializes the InternetUsersAnalyzer with the provided DataFrame.

        Parameters:
        - data_frame (pd.DataFrame): The DataFrame containing internet users data.
        """
        self.data_frame = data_frame

    def analyse(self):
        """
        Performs basic analyses on the internet users data.

        Analyses:
        1. Top 5 countries with the highest internet users in millions.
        2. Average internet users across all countries.
        3. Number of countries with internet users above the average.

        Returns:
        - dict: A dictionary containing the results of the analyses.
        """
        # Convert the 'AMOUNT' column to numeric by extracting the number and converting to millions
        self.data_frame['AMOUNT'] = self.data_frame['AMOUNT'].str.extract('([\d.]+)').astype(float)

        # Analysis 1: Top 5 countries with the highest internet users in millions
        top_countries = self.data_frame.sort_values(by='AMOUNT', ascending=False).head(5)

        # Analysis 2: Average internet users across all countries
        average_users = self.data_frame['AMOUNT'].mean()

        # Analysis 3: Number of countries with internet users above the average
        above_average_countries = self.data_frame[self.data_frame['AMOUNT'] > average_users]
        num_above_average = above_average_countries.shape[0]

        # Create a dictionary to store the results
        results = {
            'Top Countries': top_countries[['COUNTRY', 'AMOUNT']].to_dict(orient='records'),
            'Average Users': average_users,
            'Num Above Average Countries': num_above_average
        }

        return results

if __name__ == '__main__':
    bss = BeautifulSoupScraper()
    df = bss.parse()
    analyzer = InternetUsersAnalyzer(df)
    results = analyzer.analyse()
    print(results)
