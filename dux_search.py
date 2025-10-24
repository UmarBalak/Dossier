from ddgs import DDGS

class DuxSearchClient:
    def __init__(self):
        pass

    def search(self, query, region='us-en', safesearch='on', max_results=5, page=1, backend="auto"):
        with DDGS() as dux:
            results = dux.text(query, region=region, safesearch=safesearch, max_results=max_results, page=page)
            return results
        
if __name__ == "__main__":
    client = DuxSearchClient()
    query = "What is the capital of France?"
    results = client.search(query, max_results=3)

    for result in results:
        for key, value in result.items():
            print(f"{key}: {value}")
        print("---")