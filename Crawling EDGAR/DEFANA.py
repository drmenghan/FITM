import sys

import xlrd


class Company(object):
    def __init__(self):
        self.name = ""
        self.cik = ""
        self.cid = ""
        self.num_def14A = 0
        self.def14AList = []


class Tee(object):
    """
    For output both to log and std
    """

    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)


def get_time():
    """
    Get the current whole format time
    :return: String format time
    """
    result = ""
    from pytz import reference
    import datetime
    time = reference.LocalTimezone()

    from time import localtime, strftime
    result = strftime("%A, %d %B %Y %I:%M:%S %p ", localtime())

    result += time.tzname(datetime.datetime.now())
    return result


def build_leader_company_list(XLSFile, logfile, sheetflag):
    """
    #Build questions buckets
    :param XLSFile:
    :return:List of questions in Excel
    """
    start_time = time.time()
    log = open(logfile, 'a')
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, log)
    print("\nGetting leaders list from Excel.\n---\t", get_time(), "\t---")
    sys.stdout = original

    CompanyList = []
    book = xlrd.open_workbook(XLSFile)

    sh = book.sheet_by_index(sheetflag)
    num_rows = 3300
    # num_cells = sh.ncols - 1
    curr_row = 1
    # flag = 1 #Old Company
    while curr_row < num_rows:
        company = Company()
        company.cid = str(sh.cell_value(curr_row, 0)).lower()
        company.CompanyName = str(sh.cell_value(curr_row, 1)).lower()
        company.cik = str(sh.cell_value(curr_row, 2)).lower()
        CompanyList.append(company)
        curr_row += 1
    sys.stdout = Tee(sys.stdout, log)

    print("---\tTotal", '{:.2f}'.format(time.time() - start_time), "seconds used.\t---")
    print("---\tThere are", num_rows - 1, "company leaders in the Excel.\t---")
    print("---\tThere are", len(CompanyList), "companies in the Excel.\t---")
    log.close()
    sys.stdout = original
    return CompanyList


import time

logfile = time.strftime("%H%M_%d%m%Y" + ".log")
XLSFile = "Crawling EDGAR/companylist.xlsx"
CompanyList = build_leader_company_list(XLSFile, logfile, 0)

for i in range(3000):
    print("----------  " + str(i) + "  ----------")
    secCrawler.filing_DEF14A('', CompanyList[i].cik, '', '')
    i += 1

from SECEdgar.crawler import SecCrawler

secCrawler.filing_DEF14A('', CompanyList[1150].cik, '', '')

secCrawler = SecCrawler()
