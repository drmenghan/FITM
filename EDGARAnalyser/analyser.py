# import re
import os
import pickle
import re
import sys
import time

import xlrd
# import string

import datetime
import requests
from tqdm import tqdm
from pytz import reference
from bs4 import BeautifulSoup
from time import localtime, strftime
import dateutil.parser as dparser

# from difflib import SequenceMatcher

__author__ = "Meng Han"
__copyright__ = "Copyright 2016, The FIANA Project"
__credits__ = ["Meng Han"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Meng Han"
__email__ = "code.mhan@gmail.com"
__status__ = "Working on"

"""
Thanks for the work of https://github.com/rahulrrixe and this code is working with Python 3.X
More features to analyze SEC EDGAR
"""


class Company(object):
    def __init__(self):
        self.name = ""
        self.cik = ""
        self.cid = ""
        self.num_def14A = 0
        self.def14a_list = []
        self.meeting_list = []
        self.number_of_period_filling_same_month = 0
        self.number_of_period_later_than_filling = 0
        self.total_number_meeting = 0
        self.number_of_meeting_changed = 0


class Tee(object):
    """
    For output both to log and std
    """

    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)


class AnnualMeeting(object):
    def __init__(self):
        self.filling_date = ""
        self.period_of_report = ""
        self.annual_meeting_date = ""
        self.def14a_file_link = ""


class EdgarAnalyser(object):
    def __init__(self):
        """
        Initialize the EdgarAnalyser
        :return: None
        """
        self.welcome = "EdgarAnalyser could help you analyze Edgar data automatically!" \
                       "EdgarAnalyser provides kinds of different way to collect and analyze the data from Edgar"

    # def make_directory(self, ticker, cik, date_b, count):
    def get_time(self):
        """
        Get the current whole format time
        :return: String format time
        """
        result = ""

        time = reference.LocalTimezone()

        result = strftime("%A, %d %B %Y %I:%M:%S %p ", localtime())

        result += time.tzname(datetime.datetime.now())
        return result

    def build_leader_company_list(self, XLSFile, logfile, sheetflag, num_rows=3300):
        """
        #Build questions buckets
        :param XLSFile:
        :return:List of questions in Excel
        """
        start_time = time.time()
        log = open(logfile, 'a')
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, log)
        print("\nGetting leaders list from Excel.\n---\t", self.get_time(), "\t---")
        sys.stdout = original

        company_list = []
        book = xlrd.open_workbook(XLSFile)

        sh = book.sheet_by_index(sheetflag)

        # num_cells = sh.ncols - 1
        curr_row = 1
        # flag = 1 #Old Company
        while curr_row < num_rows:
            company = Company()
            company.cid = str(sh.cell_value(curr_row, 0)).lower()
            company.name = str(sh.cell_value(curr_row, 1)).lower()
            company.cik = str(sh.cell_value(curr_row, 2)).lower()
            company_list.append(company)
            curr_row += 1

        sys.stdout = Tee(sys.stdout, log)
        print("---\tTotal", '{:.2f}'.format(time.time() - start_time), "seconds used.\t---")
        print("---\tThere are", len(company_list), "companies in the Excel.\t---")
        log.close()
        sys.stdout = original
        return company_list

    def get_size_of_file(self, filename, suffix='B'):
        num = os.stat(filename).st_size
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        result = TAG_RE.sub('', text)
        result = result.replace('\n', ' ')
        result = result.replace('&', ' ')
        result = result.replace('#', ' ')
        return result

    def save_object(self, obj, filename, logfile):
        """
        Save object to file
        :param obj:
        :param filename:
        :return:Success or not
        """
        start_time = time.time()
        original = sys.stdout
        log = open(logfile, 'a')
        sys.stdout = Tee(sys.stdout, log)
        with open(filename, 'wb') as output:
            print("\nSaving object to file", filename, "\n---\t", self.get_time(), "\t---")
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        print("---\tSize of the file", filename, "is", self.get_size_of_file(filename), "\t---")
        print("---\tTotal", '{:.2f}'.format(time.time() - start_time), "seconds used.\t---")
        sys.stdout = original
        log.close()

    def load_object(self, filename, logfile):
        """
        Load object from file
        :param filename:
        :param logfile:
        :return:Object saved to file previously
        """
        start_time = time.time()
        original = sys.stdout
        log = open(logfile, 'a')
        sys.stdout = Tee(sys.stdout, log)
        with open(filename, 'rb') as f:
            print("\nLoading object from file", filename, "\n---\t", self.get_time(), "\t---")
            pic = pickle.load(f)
            print("---\tSize of the file", filename, "is", self.get_size_of_file(filename), "\t---")
            print("---\tTotal", '{:.2f}'.format(time.time() - start_time), "seconds used.\t---")
        sys.stdout = original
        log.close()
        return pic

    def make_directory(self, ticker, cik, date_b, filing_type):
        """
        Initialize the file structure for later data download
        :param ticker: Results with the ticker
        :param cik: Results with the cik
        :param date_b: Results before the date
        :return: Message of file system creation
        """
        if not os.path.exists("Edgar-data/"):
            os.makedirs("Edgar-data/")
            print("Created Directory Edgar-data")
        if not os.path.exists("Edgar-data/" + str(ticker)):
            os.makedirs("Edgar-data/" + str(ticker))
            print("Created Directory Edgar-data/" + str(ticker))
        if not os.path.exists("Edgar-data/" + str(ticker) + "/" + str(cik)):
            os.makedirs("Edgar-data/" + str(ticker) + "/" + str(cik))
            print("Created Directory Edgar-data/" + str(ticker) + "/" + str(cik))
        if not os.path.exists("Edgar-data/" + str(ticker) + "/" + str(cik) + "/" + str(filing_type)):
            os.makedirs("Edgar-data/" + str(ticker) + "/" + str(cik) + "/" + str(filing_type))
            print("Created Directory Edgar-data/" + str(ticker) + "/" + str(cik) + "/" + str(filing_type))
        print("Build the file system for downloading data from Edgar DONE!")

        def save_data(self, ticker, cik, date_b, doc_list, doc_name_list, filing_type):
            for i in range(len(doc_list)):
                base_url = doc_list[i]
                r = requests.get(base_url, stream=True)
                # data = r.text
                path = "Edgar-data/" + str(ticker) + "/" + str(cik) + "/" + str(filing_type) + "/" + str(
                    doc_name_list[i])
                with open(path, 'wb') as handle:
                    for data in tqdm(r.iter_content()):
                        handle.write(data)
            print("Saved " + str(len(doc_list)) + "documents succefully!")

    def filing_AnnualMeetingDate(self, ticker="", cik="", date_b="", count=""):
        """
        Filling the date of annual meeting
        :return: Results regarding to annual meeting for each company
        """
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + str(
            cik) + "&type=DEF 14a&dateb=" + str(date_b) + "&owner=exclude&output=xml&count=" + str(count)
        # print(base_url)
        r = requests.get(base_url)
        data = r.text
        soup = BeautifulSoup(data)
        link_list = []
        annual_meeting_date_list = []
        number_of_period_filling_same_month = 0
        number_of_period_later_than_filling = 0
        number_of_meeting_changed = 0
        total_number_meeting = 0

        for link in soup.find_all('filinghref'):
            URL = link.string
            # URL = "http://www.sec.gov/Archives/edgar/data/320193/000119312516422528/0001193125-16-422528-index.htm"
            # URL = "http://www.sec.gov/Archives/edgar/data/320193/0000912057-00-010000-index.html"
            link_list.append(URL)
            # print(URL)
            info = requests.get(URL, stream=True)
            dd = info.text
            ss = BeautifulSoup(dd)

            annual_meeting = AnnualMeeting()
            try:
                annual_meeting.filling_date = ss.select(".info")[0].string
                annual_meeting.period_of_report = ss.select(".info")[3].string
                # print("Got two date")
                if annual_meeting.period_of_report[:7] == annual_meeting.filling_date[:7]:
                    # print("WARNING:Period of report and filling date are in same month!")
                    # print("filling_date: "+annual_meeting.filling_date)
                    # print("period_of_report: "+annual_meeting.period_of_report)
                    number_of_period_filling_same_month += 1

                    a_list = ss.find_all('a')
                    doc_url = "http://www.sec.gov"
                    temp_href = ""
                    for l in a_list:
                        if (l.get('href')[-4:] == ".txt"):
                            temp_href = l.get('href')
                            # print(doc_url)
                    doc_url += temp_href
                    r = requests.get(doc_url, stream=True)
                    data = self.remove_tags(r.text).upper()
                    begin = data.find("BE HELD")
                    conference_date = dparser.parse(data[begin:begin + 80], fuzzy=True)
                    annual_meeting.annual_meeting_date = conference_date.strftime("%Y-%m-%d")
                    # print(annual_meeting.annual_meeting_date)
                #
                elif annual_meeting.period_of_report > annual_meeting.filling_date:
                    annual_meeting.annual_meeting_date = annual_meeting.period_of_report
                    # print("annual_meeting.period_of_report>annual_meeting.filling_date")
                    # print(annual_meeting.annual_meeting_date)

                else:
                    # print("WARNING:Period of report is earlier than filling date!")
                    # print("filling_date: "+annual_meeting.filling_date)
                    # print("period_of_report: "+annual_meeting.period_of_report)
                    # print(URL)
                    number_of_period_later_than_filling += 1

                    a_list = ss.find_all('a')
                    doc_url = "http://www.sec.gov"
                    temp_href = ""
                    for l in a_list:
                        if (l.get('href')[-4:] == ".txt"):
                            temp_href = l.get('href')
                            # print(temp_href)
                    doc_url += temp_href
                    # print("Final:"+doc_url)
                    r = requests.get(doc_url, stream=True)
                    data = self.remove_tags(r.text).upper()
                    begin = data.find("BE HELD")
                    conference_date = dparser.parse(data[begin:begin + 80], fuzzy=True)
                    annual_meeting.annual_meeting_date = conference_date.strftime("%Y-%m-%d")
                annual_meeting_date_list.append(annual_meeting)
                print(annual_meeting.annual_meeting_date)
            except:
                number_of_meeting_changed += 1
                # print("Something wrong. Related URL is:")
                # print(ss.select(".info")[0].string)
                # print(ss.select(".info")[3].string)
                # print(URL)
                try:
                    # URL = "http://www.sec.gov/Archives/edgar/data/1501364/000150136415000057/0001501364-15-000057-index.htm"
                    a_list = ss.find_all('a')
                    doc_url = "http://www.sec.gov"
                    temp_href = ""
                    for l in a_list:
                        if (l.get('href')[-4:] == ".txt"):
                            temp_href = l.get('href')
                            # print(doc_url)
                    doc_url += temp_href
                    r = requests.get(doc_url, stream=True)
                    data = self.remove_tags(r.text).upper()
                    begin = data.find("BE HELD")
                    conference_date = dparser.parse(data[begin:begin + 80], fuzzy=True)
                    annual_meeting.annual_meeting_date = conference_date.strftime("%Y-%m-%d")
                    annual_meeting_date_list.append(annual_meeting)
                    print(annual_meeting.annual_meeting_date)
                    # print("Except Solved")
                except:
                    pass
                    # print("Something wrong. The second trial failed. :(")
                    # print(URL)

                    # print("filling_date: "+annual_meeting.filling_date)
                    # print("period_of_report: "+annual_meeting.period_of_report)

        total_number_meeting += len(annual_meeting_date_list)
        print("Number of Meetings: " + str(len(annual_meeting_date_list)))
        return annual_meeting_date_list, number_of_period_filling_same_month, number_of_period_later_than_filling, total_number_meeting, number_of_meeting_changed



        # edgar = EdgarAnalyser()

        # mylist = edgar.filing_AnnualMeetingDate(cik = "0000320193")

        # import xml.etree.ElementTree as ET
        # ET.f
        # def remove_tags(text):
        #     return ''.join(ET.fromstring(text).itertext())
        # text = "TO BE HELD ON MAY 22, 2014</font>"
        # remove_tags(text)
        #
        #
        #
        #
        #
        # dparser.parse('TO BE HELD ON MAY 22, 2014', fuzzy = True)
