from stackapi import StackAPI
import re

class ErrorParser:
    LANGUAGE_PATTERNS = {
        "python": [
            r"TypeError", r"ValueError", r"AttributeError", 
            r"IndexError", r"KeyError", r"ImportError",
            r"Traceback \(most recent call last\)"
        ],
        "javascript": [
            r"ReferenceError", r"TypeError.*JavaScript",
            r"Uncaught", r"Cannot read property"
        ],
        "java": [
            r"NullPointerException", r"ArrayIndexOutOfBoundsException",
            r"ClassNotFoundException"
        ]
    }
    
    @staticmethod
    def detect_language(error_msg):
        for lang, patterns in ErrorParser.LANGUAGE_PATTERNS.items():
            if any(re.search(pattern, error_msg, re.IGNORECASE) for pattern in patterns):
                return lang
        return None  # Unknown language
    
    @staticmethod
    def extract_error_type(error_msg):
        # Extract error type (e.g., "TypeError", "ValueError")
        match = re.search(r"(\w+Error|\w+Exception)", error_msg)
        return match.group(1) if match else None


class StackExchangeClient:
    def __init__(self, site="stackoverflow", api_key=None):
        self.site = site
        self.api_key = api_key
        self.stack_api = StackAPI(site, key=api_key)
        
    def get_accepted_answers(self, question_ids, pagesize=5):
        if not question_ids:
            return {"items": []}
        
        response = self.stack_api.fetch(
            "questions/{ids}/answers".format(ids=";".join(map(str, question_ids))),
            sort="votes",
            filter="withbody",
            pagesize=pagesize
        )
        
        # Filter to only accepted answers
        accepted_only = {
            "items": [
                answer for answer in response.get("items", [])
                if answer.get("is_accepted", False)
            ]
        }
        return accepted_only

    # Search questions related to a user's query or error message
    def search_similar(self, query, tagged=None, pagesize=15):
        # Request more than needed (15) to ensure we get at least 5 with accepted answers
        response = self.stack_api.fetch(
            "search/advanced",
            q=query,
            tagged=tagged,
            accepted=True,  # Only questions with accepted answers
            sort="relevance",
            pagesize=pagesize
        )
        
        # Double-check that questions have accepted_answer_id
        filtered_items = [
            q for q in response.get("items", [])
            if q.get("accepted_answer_id") is not None
        ]
        
        response["items"] = filtered_items[:5]  # Return top 5
        return response



if __name__ == "__main__":
    client = StackExchangeClient(site="stackoverflow")

    user_query = "Getting error when using stackexchange api"

    language = ErrorParser.detect_language(user_query)
    error_type = ErrorParser.extract_error_type(user_query)

    # Step 1. Search similar questions
    search_results = client.search_similar(user_query, tagged=language, pagesize=10)
    questions = search_results.get("items", [])

    print("--- Search Results ---")
    print(f"Found {len(questions)} questions similar to '{user_query}':\n")

    if not questions:
        print("No similar questions found.")
        exit()

    ids = [q["question_id"] for q in questions]

    # Step 2. Get answers
    answers_response = client.get_accepted_answers(ids)
    answers = answers_response.get("items", [])

    # Map accepted answers by question_id
    answer_map = {a["question_id"]: a for a in answers}

    dossier_items = []
    for q in questions:
        a = answer_map.get(q["question_id"])
        if not a:
            continue  # Skip if no accepted answer

        dossier_items.append({
                        "question": {
                            "id": q["question_id"],
                            "title": q["title"],
                            "score": q["score"],
                            "link": q["link"],
                            "tags": q.get("tags", [])
                        },
                        "accepted_answer": {
                            "id": a["answer_id"],
                            "body": a.get("body", ""),
                            "score": a["score"],
                            "created": a["creation_date"],
                            "link": a.get("link", q["link"])  # Fallback to question link
                        }
                    })
        
    print("\n--- Dossier Items ---")
    if not dossier_items:
        print("No dossier items found.")
    else:
        print(dossier_items[0])