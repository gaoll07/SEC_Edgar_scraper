# SEC_Edgar_scraper
Download all kinds of SEC filings.

This scraper contains two parts:
index_scraper.py: downloads SEC index files, which are used for search SEC filings.
file_scraper.py: downloads SEC filings with type specified by users.

## Third party module
You need to the module python-edgar to get the index_scraper.py to work.
Installation: <pre><code>pip install python-edgar</code></pre>

## Usage
For first time users, there are two steps, downloading the index files and the type of files you are interested in.
For users who have downloaded index files, check Step 2.

### Step 1: download index files.
In terminal, run the following command
<pre><code>
python index_scraper.py -i &lt idx_path&gt -s &lt start_year&gt -e &lt end_year&gt
</code></pre>
For example, the following command downloads all index files (quarterly updated) from year 2013 to 2015, and saves them in directory <code>/home/usr/index</code> by year.
<pre><code>
python index_scraper.py -i /home/usr/index/ -s 2013 -e 2015
</code></pre>

### Step 2: download user specified files
In terminal, run the following command
<pre><code>
python index_scraper.py -i &lt idx_path&gt -f &lt file_path&gt -s &lt start_year&gt -e &lt end_year&gt -t &lt file_type&gt
</code></pre>
For example, the following command downloads all 10-K files from year 2013 to 2015, and saves them in directory <code>/home/user/file</code> by year.
<pre><code>
python file_scraper.py -i /home/usr/index/ -f /home/usr/file/ -s 2013 -e 2015 -t 10-K
</code></pre>
