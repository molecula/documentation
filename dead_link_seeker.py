'''
The following was based on the repository found here: https://github.com/healeycodes/Broken-Link-Crawler
Small tweaks and additions were added to the code.

As per the license, the following is included:

MIT License

Copyright (c) 2019 Andrew Healey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

deadseeker.py
Seeking out your 404s in around 50 lines of vanilla Python.
'''

import sys
import urllib
from urllib import request, parse
from urllib.parse import urlparse, urljoin
from urllib.request import Request
from html.parser import HTMLParser
# Deque (Doubly Ended Queue) in Python is implemented using the module “collections“. 
# Deque is preferred over a list in the cases where we need quicker append and pop operations from both the ends of the container.
# Deque provides an O(1) time complexity for append and pop operations as compared to a list that provides O(n) time complexity.
from collections import deque

#parse all HTML tags on the given page looking for href and src attributes. including local pages
search_attrs = set(['href', 'src'])
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

# We extend the HTMLParser into LinkParser — the core of our program. We use super() to refer to the parent constructor that we're overriding.
class LinkParser(HTMLParser):
    def __init__(self, home, verbose):
        ''':home:    a homepage, e.g. 'https://docs.featurebase.com/ or http://127.0.0.1:4000/'
           :verbose: boolean for for verbose mode'''
        # The super() builtin returns a proxy object (temporary object of the superclass) that allows us to access methods of the base class.
        super().__init__()
        self.home = home
        self.verbose = verbose
        self.checked_links = set()
        self.pages_to_check = deque()
        self.pages_to_check.appendleft(home)
        self.scanner()

    def scanner(self):
        '''Loop through remaining pages, looking for HTML responses'''
        while self.pages_to_check:
            page = self.pages_to_check.pop()

            # set the current page for reporting
            self.page = page
            req = Request(page, headers={'User-Agent': agent})
            res = request.urlopen(req)
            if 'html' in res.headers['content-type']:
                with res as f:
                    body = f.read().decode('utf-8', errors='ignore')
                    # The feed method  return self. This means you can continue to call methods on the result of calling that method.
                    self.feed(body)
        print("All Done")

    #As feed parses the HTML, it will encounter tags and call handle_starttag, handle_endtag, and other methods. We've overridden handle_starttag with our own method that checks the attributes for the keys we're looking for.
    def handle_starttag(self, tag, attrs):
        '''Override parent method and check tag for our attributes'''
        for attr in attrs:
            # ('href', 'http://google.com')
            if attr[0] in search_attrs and attr[1] not in self.checked_links:
                self.checked_links.add(attr[1])
                self.handle_link(attr[1])

    def handle_link(self, link):
        '''Send a HEAD request to the link, catch any pesky errors'''
        if not bool(urlparse(link).netloc):  # relative link?
            link = urljoin(self.home, link)
        try:
            req = Request(link, headers={'User-Agent': agent}, method='HEAD')
            status = request.urlopen(req).getcode()
        except urllib.error.HTTPError as e:
            print(f'HTTPError: {e.code} - {link} in {self.page}')  # (e.g. 404, 501, etc)
        except urllib.error.URLError as e:
            print(f'URLError: {e.reason} - {link} in {self.page}')  # (e.g. conn. refused)
        except ValueError as e:
            print(f'ValueError {e} - {link} in {self.page}')  # (e.g. missing protocol http)
        else:
            if self.verbose:
                print(f'{status} - {link}')
        if self.home in link:
            self.pages_to_check.appendleft(link)


# check for verbose tag
verbose = len(sys.argv) > 2 and sys.argv[2] == 'v'
# enable this as a script, e.g., 'https://docs.featurebase.com/ v'
LinkParser(sys.argv[1], verbose)
#Add any false positives to this list to let users know to ignore these errors
false_positive = ['mailto*','https://roaringbitmap.org/', 'localhost*']
print("The following sites are flagged but do work: ")
for site in false_positive:
    print(site)
