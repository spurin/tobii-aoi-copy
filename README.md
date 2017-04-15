# Tobii-aoi-copy

Tobii Eye Tracker Area of Interest (AOI) Copy Utility

# Description

This is a script that can be used to copy the AOI (Areas of Interest) from one Tobii project to another.  It is useful if you have created Areas of Interest against a video in one project, and then need to replicate those Areas of Interest to another project, that uses exactly the same video.  This creates a pixel perfect copy of the areas of interest with exact frames.

# Why this was created

Despite a number of users seeking similar functionality on the Tobii related forums, Tobii studio at present does not provide a way of exporting AOI's so that they can be used in another project.  This project addresses this issue until a more suitable workaround is provided by the Tobii Studio software.

# How it works

Tobii projects use SQLite databases to store project information, these are the database.db3 files in the project directory.  The script uses Python to analyze both the source and destination project.  It scans the Media table, looking for media that is common between the source and destination project, in this case the filename will be shared across both projects but each will have their own unique MediaID within the project.

Upon finding a matching file, the script scans the MovingAOI table of the source project, in search of any Areas of Interest for the video in question, if there are Areas of Interest, it creates the equivalent entries in the destination database, using the correspondong MediaId of the video file for the destination project.

Then, for each matched MovingAOI entry found, it copies all of the corresponding data from the Keyframe table from the source to the destination project.

# Instructions for use

Firstly, create a copy of your project as a backup.

You will need to have a version of Python 3.x installed, if you are using a version installed from Python.org it should already include the requirements of sqlite.  Modify the source_db and dest_db so that they correlate to the full paths of your source and destination databases, then simply run the script in Python.  Running it multiple times should have no detrimental effect and as it only places the entries if they do not exist.

Review your project in Tobii Studio, the project should now contain the equivalent points of interest.

# Disclaimer

As per the Instructions for use, ensure that you backup your project prior to making any changes.  The project relies on the use of the same video file with the same filename, if you have a video file using the same name, but a different file, it will not work.

# Contribution

This project was done to assist in a problem that arose for my wife during her PhD studies, I personally am not an active user of any of the Tobii projects and built this project by examaning saved projects from Tobii Studio.  If this is of use to you in any way or you make any improvements to it, then please feel free to raise a merge request.
