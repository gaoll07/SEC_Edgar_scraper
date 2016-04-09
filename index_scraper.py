#!usr/bin/python

# This file download the SEC Edgar index files to the specified directory.
# The index files are used to scrape SEC filings from the Edgar database
# A typical line of an index file looks like:
# cik|Company name|filing type|filing date|filing url address
# 1000228|HENRY SCHEIN INC|4|20160104|edgar/data/1000228/0001209191-16-087797.txt


import sys, getopt, os, requests, edgar, ftplib, glob, time

def input_parser(argv):
    idx_path = ''
    file_path = ''
    start_year = 2014
    end_year = 2015
    try:
        opts, args = getopt.getopt(argv,"i:s:e:",["idx_path=","start_year=","end_year="])
    except getopt.GetoptError:
        print 'python index_scraper.py -i <idx_path> -s <start_year> -e <end_year>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--idx_path"):
            idx_path = arg
        elif opt in ("-s", "--start_year"):
            start_year = int(arg)
        elif opt in ("-e", "--end_year"):
            end_year = int(arg)+1
    print 'Index path is:', idx_path
    print 'Start year is:', start_year
    print 'End year is:', end_year
    return idx_path, start_year, end_year
    
def download_idx(idx_path, start_year, end_year):
    years = range(start_year, end_year)
    start_time = time.time()
    if not idx_path.endswith('/'):
        idx_path += '/'
    if not os.path.exists(idx_path):
        print 'The directory for saving index files does not exist, a new directory is created...'
        os.makedirs(idx_path)
    else:
        print 'You specified an existing directory!'
    ftp = ftplib.FTP(edgar.FTP_ADDR)
    ftp.login()
    try:
        edgar.download_all(ftp, idx_path)
    except Exception as e:
        print e
    finally:
        ftp.close()
    for y in years:
        if not os.path.exists(idx_path + str(y)):
            os.makedirs(idx_path + str(y))
        for f in glob.glob(idx_path + "*" + str(y) + "*.idx"):
            dst_f = idx_path + str(y) + f[len(idx_path)-1:]
            os.rename(f, dst_f)
    for item in os.listdir(idx_path):
        if os.path.isfile(idx_path + item):
            os.remove(idx_path + item)
    print('It takes %s seconds to download the index files' % (time.time() - start_time))

if __name__ == "__main__":
    idx_path, start_year, end_year = input_parser(sys.argv[1:])
    download_idx(idx_path, start_year, end_year)
    
