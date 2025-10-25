import requests
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal

@dataclass
class SearchResult:
    """Data class for search results"""
    id: str
    title: str
    description: str
    stars: int
    trust_score: float
    versions: List[str]

@dataclass
class CodeSnippet:
    """Data class for code snippets in JSON response"""
    language: str
    code: str

@dataclass
class DocResult:
    """Data class for documentation results (JSON format)"""
    code_title: str
    code_description: str
    code_language: str
    code_id: str
    page_title: str
    code_list: List[CodeSnippet]
    relevance: float


class Context7Client:
    """Python client for Context7 API"""
    
    def __init__(self, api_key: str):
        """
        Initialize the Context7 API client
        
        Args:
            api_key: Your Context7 API key
        """
        self.api_key = api_key
        self.base_url = "https://context7.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def search(self, query: str) -> List[SearchResult]:
        """
        Search for libraries/documentation
        
        Args:
            query: Search term for finding libraries (e.g., "machine learning")
            
        Returns:
            List of SearchResult objects

        """
        url = f"{self.base_url}/search"
        params = {"query": query}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()

            # print(f"First search response entity: {data.get("results", [])[0]}")  # Debugging line
            """
            Example first search response entity:

            {'id': '/scikit-learn/scikit-learn', 'title': 'Scikit-learn', 
            'description': 'scikit-learn: machine learning in Python', 
            'branch': 'main', 'lastUpdateDate': '2025-09-24T00:42:32.328Z', 
            'state': 'finalized', 'totalTokens': 674531, 'totalSnippets': 4161, 
            'totalPages': 281, 'stars': 61913, 'trustScore': 8.5, 'benchmarkScore': 79.3, 
            'versions': ['1.7.1']}          
            """

            results = []
            
            for item in data.get("results", []):
                results.append(SearchResult(
                    id=item.get("id", ""),
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    stars=item.get("stars", 0),
                    trust_score=item.get("trustScore", 0.0),
                    versions=item.get("versions", [])
                ))
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Error during search: {e}")
            raise

    def get_docs(
        self,
        library_path: str,
        response_type: Literal["json", "txt"] = "json",
        topic: Optional[str] = None,
        tokens: Optional[int] = None
    ) -> Any:
        """
        Get documentation for a specific library
        
        Args:
            library_path: Path to the library (e.g., "vercel/next.js")
            response_type: Response format - "json" or "txt"
            topic: Optional search by topic (e.g., "ssr")
            tokens: Optional token limit
            
        Returns:
            For JSON: List of DocResult objects
            For TXT: Raw text string
        """
        url = f"{self.base_url}/{library_path}"
        params = {"type": response_type}
        
        if topic:
            params["topic"] = topic
        if tokens:
            params["tokens"] = tokens
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            if response_type == "json":
                try:
                    data = response.json()
                except ValueError:
                    print("Warning: Response is not valid JSON, returning as text")
                    return response.text
                
                # Check if data is a dict with 'snippets' key
                if isinstance(data, dict) and "snippets" in data:
                    data = data["snippets"]  # Extract the snippets list
                
                # Check if data is a list
                if not isinstance(data, list):
                    print(f"Warning: Expected list but got {type(data)}")
                    return response.text
                
                results = []
                
                for item in data:
                    # Add type check for each item
                    if not isinstance(item, dict):
                        print(f"Warning: Skipping non-dict item: {type(item)}")
                        continue
                    
                    # Parse code_list
                    code_list = []
                    for code_item in item.get("codeList", []):
                        code_list.append(CodeSnippet(
                            language=code_item.get("language", ""),
                            code=code_item.get("code", "")
                        ))
                    
                    results.append(DocResult(
                        code_title=item.get("codeTitle", ""),
                        code_description=item.get("codeDescription", ""),
                        code_language=item.get("codeLanguage", ""),
                        code_id=item.get("codeId", ""),
                        page_title=item.get("pageTitle", ""),
                        code_list=code_list,
                        relevance=item.get("relevance", 0.0)
                    ))
                
                return results

            else:  # txt format
                return response.text
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching documentation: {e}")
            raise


def main():
    """Example usage of the Context7API client"""
    
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("CONTEXT7_API_KEY")

    # Initialize the client
    client = Context7Client(api_key)
    
    # Example 1: Search for libraries
    print("=" * 50)
    search_topic = "scikit-learn"
    topic = "Linear Models" # Topic for documentation retrieval (not for search)

    print(f"Searching for '{search_topic}'...")
    print("=" * 50)
    
    search_results = client.search(search_topic)
    print(f"Found {len(search_results)} results.")
    # for result in search_results:
    #     print(f"\nTitle: {result.title}")
    #     print(f"Description: {result.description}")
    #     print(f"Trust Score: {result.trust_score}")
    #     print(f"Stars: {result.stars}")
    #     print("-" * 50)

    first_result_id = search_results[0].id if search_results else None
    if not first_result_id:
        print("No search results found, exiting.")
        return
    
    print("Frist result: ")
    print(f"\nTitle: {search_results[0]}")
    
    # Example 2: Get documentation in JSON format
    print("\n" + "=" * 50)
    print(f"Getting '{first_result_id}' documentation (JSON)...")
    print("=" * 50)

    docs_json = client.get_docs(
        first_result_id,
        response_type="json",
        topic=topic,
        tokens=5000
    )

    # Add this check
    if isinstance(docs_json, str):
        print("Received text response instead of JSON:")
        print(docs_json[:500])
        print("...")
    else:
        print(f"Found {len(docs_json)} documentation entries.")
        docs_json_sorted = sorted(docs_json, key=lambda x: x.relevance, reverse=True)
        for doc in docs_json_sorted[:5]:
            print(f"\nTitle: {doc.code_title}")
            print(f"Description: {doc.code_description[:100]}...")
            print(f"Language: {doc.code_language}")
            print(f"Relevance: {doc.relevance}")
            if doc.code_list:
                print(f"Code Preview:\n{doc.code_list[0].code[:200]}...")
            print("-" * 50)

        # print("First documentation entry:")
        # first_doc = docs_json[0]
        # print(first_doc)
        """
        Example first documentation entry:

        DocResult(code_title='Build Documentation with Example Gallery', 
        code_description='Builds the HTML documentation website including the execution of all examples, which can be time-consuming.', 
        code_language='bash', code_tokens=43, 
        code_id='https://github.com/scikit-learn/scikit-learn/blob/main/doc/developers/contributing.rst#_snippet_23', 
        page_title='Scikit-learn Contributing Guide', code_list=[CodeSnippet(language='bash', code='cd doc\nmake html')], 
        relevance=0.033333335)
        """

    
    # Example 3: Get documentation in TXT format
    print("\n" + "=" * 50)
    print(f"Getting '{first_result_id}' documentation (TXT)...")
    print("=" * 50)
    
    docs_txt = client.get_docs(
        first_result_id,
        response_type="txt",
        topic=topic,
        tokens=5000
    )
    
    # Print first 500 characters
    # print(docs_txt[:500])
    # print("...")

    print("Full text documentation received:")
    print(docs_txt)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")        