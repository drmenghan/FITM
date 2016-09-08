# FITM

Public business information could increase the efficiency and fairness of the securities market for the benefit of investors, corporations, and the economy.
Since 1934, the U.S. \textbf{S}ecurities and \textbf{E}xchange \textbf{C}ommission (SEC)\footnote{\url{https://www.sec.gov/about.shtml}} has required disclosure in forms and documents.
SEC's EDGAR \footnote{Electronic Data Gathering, Analysis, and Retrieval system (EDGAR)\\\url{https://www.sec.gov/edgar/searchedgar/webusers.htm}}, which is a data management system of SEC, began to collect electronic documents to help investors get information since 1984.
However, although EDGAR provides free access to more than 20 million filings, limited by the function of EDGAR search tools, it is very hard for the end user to query data related to different companies conveniently, not to mention mining the internal knowledge of a large number of documents from the aspect of statistics.
Moreover, most of the particular knowledge discovery from documents is still very challenging due to the complexity of material and semantic inside the documents.
In this paper, from a case study aspect, we provide a general data extraction and analysis resolution for mining the business knowledge from EDGAR.
Our case study particular focuses on mining the annual meeting date of each company which mainly indicated in company's ``DEF 14A'' form.

We tested our resolution with a list of 10,417 companies, more than 98.65\% (10,276) companies have been analyzed through our Python scripts automatically, the error is result of the lack of documents standardization and web mistake.
546,451 documents have been scanned and 82,872 annual meeting date records for all 10,417 companies have been extracted and analyzed.
The knowledge we mining could be used for further research and analysis usage.
Furthermore, we also provide several general resolution for other researchers to download or analyze other documents such as 10-K, 10-Q \textit{et al.}

We encouraged you to cite our package or datasets if you have used them in your work. You can use the following BibTeX citation:

@inproceedings{Meng_FICODE,
  title={Finding Number of Clusters in a Gene Co-expression Network Using Independent Sets.},
  author={Meng Han, Harun},
  booktitle={SocialCom},
  year={2016}
}

@misc{Meng_FIDATA,
  author       = {Meng Han, Yi Liang, Zhuojun Duan, and Yingjie Wang},
  title        = {Mining Public Business Knowledge: A Case Study in SEC's EDGAR},
  howpublished = {\url{http://cs.gsu.edu/~mhan7}},
  month        = July
  year         = 2016
}
