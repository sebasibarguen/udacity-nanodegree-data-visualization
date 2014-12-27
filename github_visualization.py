#
import json
import gzip
import urllib
from unlock import Places

base_url = "http://data.githubarchive.org/"
file_directory = "data/2014-11-01-0.json.gz"

filenames = ["2014-11-01-" + str(i) + ".json.gz" for i in range(0,24)]

accepted_event_types = ["PushEvent"]

def validate_input(day_of_year, event):
    pass

def get_github_files(day_of_year, event):
    pass


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

                    # if user has location data, use Unlock API to get lat,long
                    if 'actor_attributes' in event:
                        if 'location' in event['actor_attributes']:
                            place = event['actor_attributes']['location']
                            print "user has location: " + place

                            try:
                                unlock_response = places.nameAndFeatureSearch( place, 'Countries', 'json' )
                                unlock_json = json.loads(unlock_response)

                                features = unlock_json['features']
                                properties = features[0]['properties']
                                centroid = properties['centroid']
                                # print "got unlock lat-long: " + centroid

                                event['actor_attributes']['lat'] = float(centroid.split(", ")[0])
                                event['actor_attributes']['lon'] = float(centroid.split(", ")[-1])
                            except:
                                pass
                                # print "problems with converting lat-long."

                    f.write(json.dumps(event))
        print "Finished writing: " + filename
