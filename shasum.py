#https://www.quora.com/How-do-I-write-a-python-script-that-will-find-a-specific-string-in-a-txt-file-select-the-rest-of-string-surrounding-it-and-paste-in-another-txt
#https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

import urllib.request
import hashlib
import sys

sha256 = hashlib.sha256()
headers = {'User-Agent': 'curl/7.64.1'}
url = 'https://download.litecoin.org/litecoin-0.17.1/linux/litecoin-0.17.1-linux-signatures.asc'

def get_shasum(filename):
  with open(filename, 'rb') as f:
      while True:
          data = f.read()
          if not data:
              break
          sha256.update(data)
  return sha256.hexdigest()

request = urllib.request.Request(url,None,headers)
response = urllib.request.urlopen(request)
data = response.read().decode("utf-8")
file = open('/tmp/litecoin-signatures.asc','w')
file.write(data)
file.close()

with open('/tmp/litecoin-signatures.asc') as f:
  for line in f:
    if 'litecoin-0.17.1-x86_64-linux-gnu.tar.gz' in line:
        shasum = line.strip().split()[0]
        if shasum == get_shasum('/tmp/litecoin.tar.gz'):
          print("SHASUM check succeeded!")
          continue
        else:
          print("SHASUM did not match!")
          raise sys.exit(1) # https://stackoverflow.com/questions/73663/terminating-a-python-script