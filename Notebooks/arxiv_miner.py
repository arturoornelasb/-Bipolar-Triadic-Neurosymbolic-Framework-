import sys
import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
from pypdf import PdfReader
from io import BytesIO

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from knowledge_miner import NeurosymbolicMiner

class ArxivMiner:
    """
    Connects to arXiv API, downloads papers, and feeds them to the Neurosymbolic Miner.
    """
    def __init__(self):
        self.miner = NeurosymbolicMiner()
        self.base_url = 'http://export.arxiv.org/api/query?'
        
    def search_arxiv(self, query, max_results=1):
        print(f"\n--- SEARCHING ARXIV: '{query}' ---")
        encoded_query = urllib.parse.quote(query)
        url = f"{self.base_url}search_query=all:{encoded_query}&start=0&max_results={max_results}"
        data = urllib.request.urlopen(url).read()
        
        root = ET.fromstring(data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            pdf_link = ''
            for link in entry.findall('atom:link', ns):
                if link.attrib.get('title') == 'pdf':
                    pdf_link = link.attrib['href']
            
            papers.append({'title': title, 'summary': summary, 'pdf': pdf_link})
            print(f"Found: {title}")
            
        return papers

    def download_and_extract_pdf(self, pdf_url):
        print(f"   Downloading PDF from {pdf_url}...")
        try:
            response = urllib.request.urlopen(pdf_url)
            pdf_file = BytesIO(response.read())
            
            print("   Extracting text...")
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            print(f"   ❌ Error downloading/parsing PDF: {e}")
            return ""

    def process_papers(self, query):
        papers = self.search_arxiv(query)
        
        print(f"\n--- MINING {len(papers)} PAPERS ---")
        for i, paper in enumerate(papers):
            print(f"\n[Paper {i+1}] {paper['title']}")
            
            full_text = ""
            if paper['pdf']:
                full_text = self.download_and_extract_pdf(paper['pdf'])
            
            if not full_text:
                print("   Using abstract only (PDF failed).")
                full_text = paper['summary']
            else:
                print(f"   Successfully extracted {len(full_text)} characters.")

            # Feed to miner
            self.miner.discover_law(full_text)

if __name__ == "__main__":
    arxiv = ArxivMiner()
    # Search for a specific topic likely to have formulas
    arxiv.process_papers("Newtonian Mechanics")
