#!/usr/bin/env python
"""
DISCLAIMER: 
	1) Download files from trusted sources only
	2) If the server returns 3xx headers, "curl --location" will 
	redo the request to the location that the server forwards you to.
"""

import os
import json
import sys
from joblib import Parallel, delayed

# shared link provided by HPCAC
shared_link = "https://mellanox.box.com/s/tpxr8g34ueic90ye1r8rtbqxgaj47rtp"

# tmp'ly save json response containing files within targeted folder to text file
output_file = "file_list.txt"


def download_file(file_id, file_name):
    print(file_id + " --- " + file_name + " --- trying to download")
    download_file_by_id = (
            'curl --location --silent'
            ' --output ' + file_name +
            ' --header "BoxApi: shared_link=' + shared_link + '"'
            ' --header "Authorization: Bearer ' + developer_token + '"'
            ' https://api.box.com/2.0/files/' + file_id + '/content'
    )

    os.system(download_file_by_id)
    print(file_id + " --- " + file_name + " --- target processed")


if(2 == len(sys.argv) and 32 == len(sys.argv[1])):
	developer_token = sys.argv[1]
else:
	exit(
		"A valid access_token of length 32 characters must be provided as argument.\n"
		"Sign up at box.com as free user, create an application, get a developer_token.\n"
		"Developer_token expire after 60 min. You might want to look into OAuth for\n"
		"authentication.\n"
	)

get_files_by_folder = (
	'curl --location' 
	' --header "BoxApi: shared_link=' + shared_link + '"'
	' --header "Authorization: Bearer "' + developer_token +
	' https://api.box.com/2.0/folders/66454095235/items'
	' >> ' + output_file
)

os.system(get_files_by_folder)

# output_file doesn't/shouldn't contain spaces or line breaks
with open(output_file, 'r') as myfile:
	file_string = myfile.read()

j = json.loads(file_string)

# pretty print json
print(json.dumps(j, indent=4, sort_keys=True))

# download files in parallel with max number cpus available (n_jobs=-1)
# as token expires after 60 min
Parallel(n_jobs=-1)(delayed(download_file)(entry["id"], entry["name"]) for entry in j["entries"])
