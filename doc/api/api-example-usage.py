import requests

class CKANClient:
    """
    A client for interacting with the CKAN API.
    Allows searching, retrieving, creating, and updating datasets.
    """
    def __init__(self, base_url, api_token=None):
        """
        Initializes the CKANClient.
        :param base_url: Base URL of the CKAN instance (site).
        :param api_token: API token for authentication (if required).
        """
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {'Authorization': self.api_token}
    
    def search_datasets(self, query, rows=10):
        """
        Searches datasets based on a query.
        :param query: Search keyword(s).
        :param rows: Number of results to return (default is 10).
        :return: JSON response with search results.
        """
        url = f"{self.base_url}/api/3/action/package_search"
        params = {"q": query, "rows": rows}
        response = requests.get(url, params=params)
        return response.json()
    
    def get_dataset(self, dataset_id):
        """
        Retrieves details of a specific dataset.
        :param dataset_id: ID of the dataset.
        :return: JSON response with dataset details.
        """
        url = f"{self.base_url}/api/3/action/package_show"
        params = {"id": dataset_id}
        response = requests.get(url, params=params)
        return response.json()
    
    def create_dataset(self, name, notes, owner_org):
        """
        Creates a new dataset.
        :param name: Unique name identifier for the dataset.
        :param notes: Description of the dataset.
        :param owner_org: Organization ID owning the dataset.
        :return: JSON response with created dataset details.
        """
        url = f"{self.base_url}/api/3/action/package_create"
        dataset_dict = {
            "name": name,
            "notes": notes,
            "owner_org": owner_org
        }

        response = requests.post(url, json=dataset_dict, headers=self.headers)
        return response.json()
    
    def update_dataset(self, dataset_id, updates):
        """
        Updates an existing dataset.
        :param dataset_id: ID of the dataset to update.
        :param updates: Dictionary containing updated fields.
        :return: JSON response with updated dataset details.
        """
        url = f"{self.base_url}/api/3/action/package_update"
        updates["id"] = dataset_id
        response = requests.post(url, json=updates, headers=self.headers)
        return response.json()

# Example usage
if __name__ == "__main__":
    BASE_URL = "http://localhost:5000/"
    API_TOKEN = "api_token"
    
    client = CKANClient(BASE_URL, API_TOKEN)
    
    # Search datasets
    search_results = client.search_datasets("climate")
    # print("Search Results:", search_results)
    
    # Get dataset details
    dataset_id = "climate-data-test"
    dataset_details = client.get_dataset(dataset_id)
    print("Dataset Details:", dataset_details)
    
    # Create a new dataset
    new_dataset = client.create_dataset(
        name="climate-data-test1",
        notes="A dataset containing climate records.",
        owner_org="test-organization"
    )
    print("New Dataset:", new_dataset)

