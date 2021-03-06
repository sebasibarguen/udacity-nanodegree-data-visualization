"""

To do's:
- fix unlock data insertion. there is a problem when trying to add new data.
- add flatten capabilities right here, so the saved file is csv.
"""
import json
import gzip
import urllib
import csvkit
from unlock import Places

base_url = "http://data.githubarchive.org/"
file_directory = "data/2014-11-01-0.json.gz"

filenames = ["2014-11-01-" + str(i) + ".json.gz" for i in range(0,24)]

accepted_event_types = ["PushEvent"]



# Write to file
with open('data/2014-11-01-PushEvent.json', 'wb') as f:
    places = Places()

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

                    event['actor_attributes']['lat'] = "NA"
                    event['actor_attributes']['lon'] = "NA"

                    event['actor_attributes']['country'] = "NA"



                    f.write(json.dumps(event))
        print "Finished writing: " + filename
        break

with open("data/") as f:
    # if user has location data, use Unlock API to get lat,long
    if 'actor_attributes' in event:
        if 'location' in event['actor_attributes']:
            if event['actor_attributes']['location']:

                place = event['actor_attributes']['location']
                print "user has location: " + place

                try:
                    # unlock_response = places.nameAndFeatureSearch( place, 'Countries', 'json' )
                    unlock_response = places.nameSearch( place, 'json' )
                    unlock_json = json.loads(unlock_response)

                    features = unlock_json['features']
                    properties = features[0]['properties']
                    centroid = properties['centroid']

                    country = properties['country']
                    # print "got unlock lat-long: " + centroid

                    event['actor_attributes']['lat'] = float(centroid.split(", ")[0])
                    event['actor_attributes']['lon'] = float(centroid.split(", ")[-1])

                    event['actor_attributes']['country'] = country
                except:
                    pass
                    # print "problems with converting lat-long."
