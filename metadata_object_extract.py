"""
A script for collecting analytics JSON metadata for securty, traffic or retail enviroments
"""

from prettytable import PrettyTable
from requests.auth import HTTPDigestAuth
from sseclient import SSEClient
import csv
import json
import requests


def get_vca_object_class(vca_class):
    """
    Collects ID and date of the events alogside the class
    of the objects

     Args:
        vca_class: VCA JSON Event metadata. The structure can be a dictionary or
        a list contaning the dictionary.

    Returns:
        event_id: ID of the event
        event_date: Date of the event
        object_class: The ML classification of the object

    """
    if vca_class['typename'] == 'vca.meta.data.Event':
        event_id = vca_class['id']
        date = vca_class['start']
        new_date = date.split(".")
        event_date = new_date[0].split("T")
        for vca_events in vca_class['objects']:
            if vca_events['typename'] == 'vca.meta.data.Object':
                vca_object = vca_events['meta']
                for vca_meta in vca_object:
                    if vca_meta['typename'] == 'vca.meta.data.classification.Confidence':
                        object_class = vca_meta['class']
                        return [event_id, event_date[0], event_date[1], object_class]


def get_vca_channel_info(vca_channel):
    """
    Collects information about the camera configuration

     Args:
        vca_channel: VCA JSON Event metadata. The structure can be a
        dictionary or a list contaning the dictionary.

    Returns:
        channel_name: The name of the channel
        channe_id: ID of the channel
        rule_type: The type of the rule that triggered the
        event (e.g dwell, presence, fall, fight, tailgating)
    """
    if vca_channel['typename'] == 'vca.meta.data.Event':
        rule_type = vca_channel['type']
        for vca_objects in vca_channel['objects']:
            if vca_objects['typename'] == 'vca.meta.data.Channel':
                channel_name = vca_objects['name']
                channel_id = vca_objects['id']
                return [channel_name, channel_id, rule_type]


def get_zone_info(vca_zone):
    """
       Collects information about the Region of Interest (ROI)

        Args:
           vca_zone: VCA JSON Event metadata. The structure can be a
           dictionary or a list contaning the dictionary.

       Returns:
           zone_name: The custom name for the Region of Interest (ROI)
       """
    if vca_zone['typename'] == 'vca.meta.data.Event':
        for zones in vca_zone['objects']:
            if zones['typename'] == 'vca.meta.data.Zone':
                zone_name = zones['name']
                return zone_name


def get_vca_object_colour(vca_object_colour):
    """
       Collects information about the colour of an object

        Args:
           vca_object_colour: VCA JSON ColourSignature metadata.
           The structure can be a dictionary or a list contaning the
           dictionary

       Returns:
           colours_name: The name of the colour
       """
    if vca_object_colour['typename'] == 'vca.meta.data.ColourSignature':
        for colours in vca_object_colour['colours']:
            for colour_signature in colours:
                colours_name = colour_signature['colour_name']
                return colours_name


if __name__ == '__main__':
    SERVER_IP = 'SERVER_IP_ADDRESS'
    PORT = 'WEB_PORT'
    CHANNEL_ID = 2
    file_path = "./CSV_FILE_NAME.csv"


    # Create a PrettyTable object
    table_resul = PrettyTable()

    # Define the columns
    table_resul.field_names = ["ID", "Date", "Time", "Source", "Class", "Zone", "Type"]

    # Connection to the SSE Events
    messages = SSEClient('http://' + SERVER_IP + ':' + PORT + '/metadata/' + str(CHANNEL_ID) +
                         '?events=1&events.unique=1',
                         headers={"Accept": "text/event-stream","Accept-Encoding": "identity"},
                         auth=requests.auth.HTTPDigestAuth('admin', 'admin'))

    # Create a CSV file to store and save the metadata
    with open(file_path, mode='a', newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = csv.DictWriter(csv_file, fieldnames=["ID", "DATE", "TIME", "SOURCE", "CLASS", "ZONE", "RULE"])

        header.writeheader()

        for msg in messages:
            metadata = json.loads(msg.data)
            for values in metadata.values():
                for data in values:
                    writer.writerow([get_vca_object_class(data)[0], get_vca_object_class(data)[1],
                                     get_vca_object_class(data)[2], get_vca_channel_info(data)[0],
                                     get_vca_object_class(data)[3], get_zone_info(data), get_vca_channel_info(data)[2]])

                # Add the row
                table_resul.add_row([get_vca_object_class(data)[0],get_vca_object_class(data)[1],
                                      get_vca_object_class(data)[2],get_vca_channel_info(data)[0], get_vca_object_class(data)[3],
                                      get_zone_info(data), get_vca_channel_info(data)[2]])

                print(table_resul)

    csv_file.close()
