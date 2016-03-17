from SECEdgar.crawler import SecCrawler

secCrawler = SecCrawler()
secCrawler.filing_8K('', '0001527166', '', '2000')
secCrawler.filing_8K('AAPL', '0000320193', '', '2000')
secCrawler.filing_10Q('AAPL', '0000320193', '20010101', '10')

secCrawler.filing_DEF14A('AAPL', '0000320193', '20010101', '10')
secCrawler.filing_DEF14A('', '0000320193', '', '')
secCrawler.filing_DEF14A('', '0001629210', '', '')
# http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=8-K&dateb=20010101&owner=exclude&output=xml&count=10

# https://www.sec.gov/Archives/edgar/data/320193/000091205700010000/0000912057-00-010000.txt
# https://www.sec.gov/Archives/edgar/data/320193/000091205700010000/0000912057-00-010000.txt


# https://www.sec.gov/Archives/edgar/data/320193/0000912057-00-010000-.txt

# www.sec.gov/Archives/edgar/data/320193/000104746999003858/0001047469-99-003858-.txt
# https://www.sec.gov/Archives/edgar/data/320193/0001047469-99-003858.txt

# http://www.sec.gov/Archives/edgar/data/320193/0001047469-99-003858-.txt

from tqdm import tqdm
import requests

url = "http://www.sec.gov/Archives/edgar/data/320193/000091205700053623/0000912057-00-053623.txt"
response = requests.get(url, stream=True)

with open("d:/SEC-Edgar-data/AAPL/0000320193/10-K/0000912057-00-053623.txt", 'w') as handle:
    for data in tqdm(response.iter_content()):
        handle.write(data)

import time
from SECEdgar.crawler import SecCrawler


def get_filings():
    t1 = time.time()

    # create object
    seccrawler = SecCrawler()

    companyCode = 'AAPL'  # company code for apple
    cik = '0000320193'  # cik code for apple
    date = '20010101'  # date from which filings should be downloaded
    count = '10'  # no of filings

    seccrawler.filing_10Q(str(companyCode), str(cik), str(date), str(count))
    seccrawler.filing_10K(str(companyCode), str(cik), str(date), str(count))
    seccrawler.filing_8K(str(companyCode), str(cik), str(date), str(count))
    seccrawler.filing_13F(str(companyCode), str(cik), str(date), str(count))

    t2 = time.time()
    print
    "Total Time taken: ",
    print(t2 - t1)


get_filings()
