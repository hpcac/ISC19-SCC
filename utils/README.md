# What does the script do?

The script queries the folder in the shared link provided by HPCAC
and stores a temporal list of files as JSON to a .txt file.
It downloads the list of files in parallel using joblib.

# How to query box.com API to download files provided by HPCAC?

1) Get a free user account on https://app.box.com/developers/console
2) Log in, "Create New App"
3) Go the new app's page (some link like: https://app.box.com/developers/console/app/745451)
4) Go to "Configuration"
5) "Generate Developer Token" and copy it
6) This 32-character token expires after 60 min
7) Provide it as argument to the python script,
	e.g. "python path/to/file/download.py fuakwc2kihnr2kuplaninduar87oasso"
