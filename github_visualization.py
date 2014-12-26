#
import json
import gzip
import urllib


base_url = "http://data.githubarchive.org/"
file_directory = "data/2014-11-01-0.json.gz"

filenames = ["2014-11-01-" + str(i) + ".json.gz" for i in range(1,24)]

accepted_event_types = ["PushEvent"]

def validate_input(day_of_year, event):
    pass

def get_github_files(day_of_year, event):
    pass

# Write to file
with open('data/2014-11-01-PushEvent.json', 'wb') as f:

    # Download files
    for filename in filenames:
        url = base_url + filename

        print "Starting to download: " + url
        f_name, f_headers = urllib.urlretrieve(url)
        print "Finished download."

        with gzip.open(f_name) as g:
            content = g.readlines()

            for line in content:
                event = json.loads(line)

                if event["type"] == "PushEvent":
                    f.write(line)
        print "Finished writing: " + filename
