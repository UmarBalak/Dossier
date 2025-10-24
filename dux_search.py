from ddgs import DDGS

class DuxSearchClient:
    def __init__(self):
        pass

    def search(self, query, region='us-en', safesearch='on', max_results=5, page=1, backend="auto"):
        """DDGS text metasearch.

        Args:
            query: text search query.
            region: us-en, uk-en, ru-ru, etc. Defaults to us-en.
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m, y. Defaults to None.
            max_results: maximum number of results. Defaults to 10.
            page: page of results. Defaults to 1.
            backend: A single or comma-delimited backends. Defaults to "auto".

        Returns:
            List of dictionaries with search results.
        """
        with DDGS() as dux:
            results = dux.text(query, region=region, safesearch=safesearch, max_results=max_results, page=page, backend=backend)
            return results
        
if __name__ == "__main__":
    client = DuxSearchClient()
    query = "What is the capital of France?"
    results = client.search(query, max_results=5)

    for result in results:
        for key, value in result.items():
            print(f"{key}: {value}")
        print("---")