from crossref.restful import Works
class CrossRefDatasetAPI:
    """
    A class for interacting with the CrossRef Metadata API to retrieve information about scholarly works.

    Parameters:
    - return_df (bool): If True, methods will return data in the form of pandas DataFrame.

    Methods:
    - get_sample(num_samples): Retrieves a sample of scholarly works from the CrossRef API.

        Parameters:
        - num_samples (int): The number of samples to retrieve.

        Returns:
        If return_df is True, returns a pandas DataFrame containing the sampled works; otherwise, returns a list of dictionaries.

    - query(**args): Queries the CrossRef API with specified parameters to retrieve scholarly works.

        Parameters:
        - **args: Additional parameters to be passed to the query.

        Returns:
        If return_df is True, returns a pandas DataFrame containing the queried works; otherwise, returns a list of dictionaries.
    """

    def __init__(self, return_df=False):
        """
        Initializes the CrossRefDatasetAPI instance.

        Parameters:
        - return_df (bool): If True, methods will return data in the form of pandas DataFrame.
        """
        self.works = Works()
        self.return_df = return_df

    def get_sample(self, num_samples=10):
        """
        Retrieves a sample of scholarly works from the CrossRef API.

        Parameters:
        - num_samples (int): The number of samples to retrieve.

        Returns:
        If return_df is True, returns a pandas DataFrame containing the sampled works; otherwise, returns a list of dictionaries.
        """
        result = [item for item in self.works.sample(num_samples)]
        if self.return_df:
            return pd.DataFrame(result)
        else:
            return result

    def query(self, **args):
        """
        Queries the CrossRef API with specified parameters to retrieve scholarly works.

        Parameters:
        - **args: Additional parameters to be passed to the query.

        Returns:
        If return_df is True, returns a pandas DataFrame containing the queried works; otherwise, returns a list of dictionaries.
        """
        result = works.query(**args)
        result = [item for item in result]
        if self.return_df:
            return pd.DataFrame(result)
        else:
            return result

    
if __name__ == '__main__':
    dataset = CrossRefDatasetAPI(return_df=True)
    df = dataset.query(bibliographic='zika', author='johannes', publisher_name='Wiley-Blackwell')
    print (df)

