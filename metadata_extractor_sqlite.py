"""
A script for collecting analytics JSON metadata for securty, traffic or retail enviroments
"""

from requests.auth import HTTPDigestAuth
from sseclient import SSEClient
import json
import requests
import sqlite3


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


if __name__ == '__main__':
    SERVER_IP = 'SERVER_IP'
    PORT = 'WEB_PORT'
    CHANNEL_ID = 1
    #file_path = "./vca_web_scraping.csv"

    print(f"ID:       Date:                            Source:                        Class:                           "
          f"Zone:                      Type:")

    # Connection to the SSE Events
    messages = SSEClient('http://' + SERVER_IP + ':' + PORT + '/metadata/' + str(CHANNEL_ID) +
                         '?events=1&events.unique=1',
                         headers={"Accept": "text/event-stream", "Accept-Encoding": "identity"},
                         auth=requests.auth.HTTPDigestAuth('admin', 'admin'))

   # Create a table to store the events
    create_table = """ 
    CREATE TABLE Events(
    id INT, 
    date TEXT,
    time TEXT,
    source TEXT,
    class TEXT,
    zone TEXT,
    rule TEXT
    );
    """

    # Create the connection to the database
    with sqlite3.connect("test_database.db") as connection:
        cursor = connection.cursor()
        # cursor.execute(create_table)
        # connection.commit()
        # connection.close()

        for msg in messages:
            metadata = json.loads(msg.data)
            for values in metadata.values():
                for data in values:
                    vca_metadata = [(get_vca_object_class(data)[0], str(get_vca_object_class(data)[1]),
                                     str(get_vca_object_class(data)[2]), str(get_vca_channel_info(data)[0]),
                                     str(get_vca_object_class(data)[3]), str(get_zone_info(data)),
                                     str(get_vca_channel_info(data)[2]))]
                    cursor.executemany("INSERT INTO Events VALUES(?, ?, ?, ?, ?, ?, ?)", vca_metadata)

                    connection.commit()
                    print(f"{get_vca_object_class(data)[0]}     {get_vca_object_class(data)[1]} {get_vca_object_class(data)[2]}           {get_vca_channel_info(data)[0]}          {get_vca_object_class(data)[3]}"
                    f"                       {get_zone_info(data)}                 {get_vca_channel_info(data)[2]}")
