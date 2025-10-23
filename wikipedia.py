import wikipediaapi

class WikipediaClient:
    def __init__(self, language='en', user_agent='Dossier/1.0', extract_format="plain"): # plain, html
        if extract_format == "html":
            self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=language, extract_format=extract_format)
        else:
            self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=language)

    def get_page(self, title):
        return self.wiki.page(title)
    
    def get_page_summary(self, title):
        page = self.get_page(title)
        return page.summary if page.exists() else None

    def get_page_sections(self, title):
        page = self.get_page(title)
        return page.sections if page.exists() else None
    
    def get_page_url(self, title):
        page = self.get_page(title)
        return page.fullurl if page.exists() else None

mywiki = WikipediaClient()
page_title = "Python (programming language)"
wiki_page = mywiki.get_page(page_title)
print("Title:", wiki_page.title)
print("Full text:", wiki_page.text)
print("Summary:", mywiki.get_page_summary(page_title))
print("URL:", mywiki.get_page_url(page_title))

# sections = mywiki.get_page_sections(page_title)
# if sections:
#     for section in sections:
#         print(section.text)
#         print("---"*30)