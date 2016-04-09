#!usr/bin/python

import sys, getopt, os, requests

def input_parser(argv):
    idx_path = ''
    file_path = ''
    start_year = 2014
    end_year = 2015
    file_type = '10-K'
    try:
        opts, args = getopt.getopt(argv,"i:f:s:e:t:",["idx_path=","file_path=","start_year=","end_year=","file_type="])
    except getopt.GetoptError:
        print 'python index_scraper.py -i <idx_path> -f <file_path> -s <start_year> -e <end_year> -t <file_type>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--idx_path"):
            idx_path = arg
        elif opt in ("-f", "--file_path"):
            file_path = arg
        elif opt in ("-s", "--start_year"):
            start_year = int(arg)
        elif opt in ("-e", "--end_year"):
            end_year = int(arg)+1
        elif opt in ("-t", "--file_type"):
            file_type = arg
    print 'Index path is:', idx_path
    print 'File path is:', file_path
    print 'Start year is:', start_year
    print 'End year is:', end_year
    print 'File type is:', file_type
    return idx_path, file_path, start_year, end_year, file_type
    
def scraper(idx_path, file_path, start_year, end_year, file_type, bs = False):
    ftp_path = "http://ftp.sec.gov/Archives/"
    years = range(start_year, end_year)
    if not idx_path.endswith('/'):
        idx_path += '/'
    if not file_path.endswith('/'):
        file_path += '/'
    for y in years:
		meta = open(file_path + 'meta-' + str(y) + '.txt','w+') # generate meta data
		error = open(file_path + 'error-' + str(y) + '.txt','w+')
		if not os.path.exists(file_path + str(y)):
			os.makedirs(file_path + str(y))
		for root, dirs, files in os.walk(file_path + str(y)):
			existing_files = [f for f in files if f.endswith('html')]
		for root, dirs, files in os.walk(idx_path + str(y)):
			files = [f for f in files if f.endswith('idx')]
			for fi in files:
				f = open(idx_path + str(y) + '/' + fi,'r')
				for line in f:
					ls = line.split('|')
					txt_name = ls[0] + "-" + ls[2] + "-" + ls[3] + '.html'
					if ls[2] == file_type:
						if txt_name not in existing_files:
							print line
							# download files
							try:
								response = requests.get(ftp_path + ls[4].strip())
							except requests.exceptions.ConnectionError:
								error.write('cannot get:' + ftp_path + ls[4].strip());
							#response = requests.get(ftp_path + ls[4].strip())
							html = response.text
							txt = open(file_path + str(y) + "/" + txt_name,'w+')
							try:
								txt.write(html)
							except UnicodeEncodeError:
								txt.write(html.encode('utf-8'))
							txt.close()
							date = ls[3].replace('-','')
							meta.write(txt_name + " " + date + " " + ftp_path + ls[4].strip() + " " + ls[1] + " " + ls[0] + "\n")
						else:
							print 'skipping:', txt_name
				f.close()
		meta.close()
		error.close()


if __name__ == "__main__":
    idx_path, file_path, start_year, end_year, file_type = input_parser(sys.argv[1:])
    scraper(idx_path, file_path, start_year, end_year, file_type)
