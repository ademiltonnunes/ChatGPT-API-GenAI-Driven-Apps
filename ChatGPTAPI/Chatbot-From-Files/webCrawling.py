import re
import urllib.request
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import openai
from vector_and_embedding import LangChaing

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']

lc = LangChaing()

class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        # Create a list to store the hyperlinks
        self.hyperlinks = []

    # Override the HTMLParser's handle_starttag method to get the hyperlinks
    def handle_starttag(self, tag:str, attrs) -> None:
        attrs = dict(attrs)

        # If the tag is an anchor tag and it has an href attribute, add the href attribute to the list of hyperlinks
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])

class HyperLink():
    def __init__(self, http_url_pattern :str= r'^http[s]{0,1}://.+$') -> None:
        self.__HTTP_URL_PATTERN = http_url_pattern

    # Function to get the hyperlinks from a URL
    def get_hyperlinks(self, url):

        # Try to open the URL and read the HTML
        try:
            # Open the URL and read the HTML
            with urllib.request.urlopen(url) as response:

                # If the response is not HTML, return an empty list
                if not response.info().get('Content-Type').startswith("text/html"):
                    return []

                # Decode the HTML
                html = response.read().decode('utf-8')
        except Exception as e:
            print(e)
            return []

        # Create the HTML Parser and then Parse the HTML to get hyperlinks
        parser = HyperlinkParser()
        parser.feed(html)

        return parser.hyperlinks

    # Function to get the hyperlinks from a URL that are within the same domain
    def get_domain_hyperlinks(self, local_domain, url):
        clean_links = []
        for link in set(self.get_hyperlinks(url)):
            clean_link = None

            # If the link is a URL, check if it is within the same domain
            if re.search(self.__HTTP_URL_PATTERN, link):
                # Parse the URL and check if the domain is the same
                url_obj = urlparse(link)
                if url_obj.netloc == local_domain:
                    clean_link = link

            # If the link is not a URL, check if it is a relative link
            else:
                if link.startswith("/"):
                    link = link[1:]
                elif (
                    link.startswith("#")
                    or link.startswith("mailto:")
                    or link.startswith("tel:")
                ): 
                    continue
                clean_link = "https://" + local_domain + "/" + link

            if clean_link is not None:
                if clean_link.endswith("/"):
                    clean_link = clean_link[:-1]
                clean_links.append(clean_link)

        # Return the list of hyperlinks that are within the same domain
        return list(set(clean_links))

class Crawl():

    def crawling(self, url):
        # Parse the URL and get the domain
        local_domain = urlparse(url).netloc

        # Create a queue to store the URLs to crawl
        queue = deque([url])

        # Create a set to store the URLs that have already been seen (no duplicates)
        seen = set([url])      

        # While the queue is not empty, continue crawling
        while queue:

            # Get the next URL from the queue
            url = queue.pop()
            print(url) # for debugging and to see the progress

            try:
                #Load url and save it to vectorstore
                lc.upload_url(url, timer= True)            
            except Exception as e:
                print(f"Unable to parse page {url} {e}")

            # Get the hyperlinks from the URL and add them to the queue
            for link in HyperLink().get_domain_hyperlinks(local_domain, url):
                if link not in seen:
                    queue.append(link)
                    seen.add(link)       

# def main() -> None:
#     crawl = Crawl()    
#     crawl.crawling("https://www.sfbu.edu")

# if __name__== "__main__":
#     main()