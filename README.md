# ArcGIS Online Python Scripts

Python scripts that I find useful in managing ArcGIS Online content.

### agol_BackupDataAndJson.py

A standalone Python3 script that will take a backup from ArcGIS Online.  
This includes:
- File Geodatabase exports of all Feature Service data
- Json files for item Description and Item Data as shown by the ArcGIS Online Assistant (https://ago-assistant.esri.com/)
It will backup all the items that the user has access to, that belong to the following types:
Feature Service, Web Map, Web Mapping Application, Dashboard

Limitations
The script does not currently backup the following:
- Users and Groups
- Attachments
- Metadata

Prerequisites
Need to have ArcGIS API for Python installed (note is installed with ArcGIS Pro)
https://developers.arcgis.com/python/
  
Usage: set the variables below and run.


## Author

* **Graham Morgan** 
* [Spatial Consultants Ltd](https://www.spatialconsultants.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Code that builds upon the work of others is acknowledged within the code files.
