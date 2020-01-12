from arcgis.gis import GIS
import json
import os
import time

# This script will take a backup from ArcGIS Online.  This includes:
# - File Geodatabase exports of all Feature Service data
# - Json files for item Description and Item Data as shown by the ArcGIS Online Assistant (https://ago-assistant.esri.com/)
# It will backup all the items that the user has access to, that belong to the following types:
# Feature Service, Web Map, Web Mapping Application, Dashboard

# Limitations
# The script does not currently backup the following:
# - Users and Groups
# - Attachments
# - Metadata

# Prerequisites
# Need to have ArcGIS API for Python installed (note is installed with ArcGIS Pro)
# https://developers.arcgis.com/python/
#  
# Usage: set the variables below and run.

# Credits.
# Json dumps informed by:
# https://community.esri.com/thread/193624-save-items-as-json-with-arcgis-api-for-pyhton
# Download file geodatabase informed by:
# https://github.com/jjhi11/ArcGIS-Online-Backup-Python-Script/blob/master/AGOL_Backup.py

# Set up variables
agol_user = "Bob"
agol_password = "Bob"
output_dir = "C:\\Backups\\AGOL\\"

# Global variables
print("Connecting to AGOL...")
gis = GIS("https://www.arcgis.com", agol_user, agol_password)
backup_date = time.strftime("%Y%m%d")

def main():
    # Main routine

    # record time to run
    start_time = time.time()

    print("Getting hold of items...")
    all_items = gis.content.search("owner:*", max_items=1000)

    # Keep list of ignored items for reporting later
    ignored_items = []

    for item in all_items:
        #print(item.title + ": " + item.type)
        # Filter: We are only interested in sepecific item types
        if item.type in ("Feature Service", "Web Map", "Web Mapping Application", "Dashboard"):
            print("\nBacking up " + item.title + ": " + item.type + "...")
            # Download json files
            backup_json(item)

            # Backup data for Feature Services
            if item.type == "Feature Service":
                # Check for views - do not want to download their data
                if not "View Service" in item.typeKeywords:
                    #print("Backing up data...")
                    backup_data(item)
                else:
                    print("  ignoring view data")
        else:
            #print("  Ignoring " + item.title + ": " + item.type)
            # Add ignored item to list to report later
            ignored_items.append(item)

    # print list of ignored items
    print("\n\n### Items ignored and not backed up: ###")
    for ignored in ignored_items:
        print(ignored.title + " - " + ignored.type)

    print("\nDone.")
    print("%s seconds to complete" % (time.time() - start_time))

def backup_json(item):
    print("...Downloading Item Json")
    # Get elements of output file name
    item_name = item.title.replace(" ", "_")
    item_type = item.type.replace(" ", "_")

    # Want file name to be <date>-<item name>-<item type>-<json type>.json
    desc_file = os.path.join(output_dir, backup_date + "-" + item_name + "-" + item_type + "-desc.json")
    data_file = os.path.join(output_dir, backup_date + "-" + item_name + "-" + item_type + "-data.json")

    # Write out item Description json
    dict_my_item = dict(item) 
    with open (desc_file, "w") as file_handle:
        file_handle.write(json.dumps(dict_my_item))

    # Write out item Data json
    with open (data_file, "w") as file_handle:
        file_handle.write(json.dumps(item.get_data()))

def backup_data(item):
    print ("...Exporting Hosted Feature Layer...")
    AGOLitem = gis.content.get(item.id)
    GDBname = (backup_date + "-" + item.title.replace(" ", "_"))

    # Export the data to hosted file geodatabase
    AGOLitem.export(GDBname,'File Geodatabase', parameters=None, wait='True')
    time.sleep(60)#add 10 seconds delay to allow export to complete

    print ("...Downloading File Geodatabase...")
    #find the newly created file geodatabase in ArcGIS online
    search_fgb = gis.content.search(query = "title:{}*".format(GDBname)) 
    if len(search_fgb) > 0:
        fgb_item_id = search_fgb[0].id
        fgb = gis.content.get(fgb_item_id)

        #download file gdb from ArcGIS Online to your computer
        fgb.download(save_path=output_dir) 

        # Deleting hosted File Geodatabase
        # This will delete the temporary File Geodatabase in ArcGIS Online
        print("...Deleting temporary " + fgb.title + "(" + fgb.type + ")" + " from ArcGIS Online...")
        fgb.delete()
    else:
        print("...No backup File Geodatabase found.")


# Run the script
main()
