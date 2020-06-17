# Tobii-aoi-copy

Tobii Eye Tracker Area of Interest (AOI) Copy Utility

# Description

This is a script that can be used to copy the AOI (Areas of Interest) from one Tobii project to another.  It is useful if you have created Areas of Interest against a video in one project, and then need to replicate those Areas of Interest to another project, that uses exactly the same video.  This creates a pixel perfect copy of the areas of interest with exact frames.

# Latest Update

I was suprised to see that this utility has had some popularity in China, based on the received Stars.  I'm not too sure why but I wish you the best :)
The most recent update also acopies the AOI grouping that exists in a project, if you do not wish to use this, see the previous commits.

# Why this was created

Despite a number of users seeking similar functionality on the Tobii related forums, Tobii studio at present provides a way of exporting AOI's, but does not provide an import facility allowing them to be used in another project.  This project addresses this issue until a more suitable workaround is provided by the Tobii Studio software.

# How it works

Tobii projects use SQLite databases to store project information, these are the database.db3 files in the project directory.  The script uses Python to analyze both the source and destination project.  It scans the Media table, looking for media that is common between the source and destination project, in this case the filename will be shared across both projects but each will have their own unique MediaID within the project.

Upon finding a matching file, the script scans the MovingAOI table of the source project, in search of any Areas of Interest for the video in question, if there are Areas of Interest, it creates the equivalent entries in the destination database, using the corresponding MediaId of the video file for the destination project.

Then, for each matched MovingAOI entry found, it copies all of the corresponding data from the Keyframe table from the source to the destination project.

It uses uuid.uuid1() to recreate the UUID's used as unique references for the data points

# Instructions for use

Firstly, create a copy of your target project as a backup.  Although this is done automatically in the script, we are working with a best efforts approach here so I always encourage due dilligence before use.

You will need to have a version of Python 3.x installed, if you are using a version installed from Python.org it should already include the requirements of sqlite and uuid.  Modify the source_db and dest_db entries at the top so that they correlate to the full paths of your source and destination tobii project databases, then simply run the script in Python.  Running it multiple times should have no detrimental effect and as it only places the entries if they do not exist.

Within the script, there is an optional boolean flag that can be set called 'CLEAR_DESTINATION' that defaults to false.  As the name implies, this will remove all AOI data, from the target.

The script will copy all corresponding source video AOI's to all destination AOI's if the filename matches, therefore, depending on your use setup, the tool can be used in a variety of ways, as a copy, or a merge tool.  In the examples the character after the video name signifies the same video, i.e. Video A in both Project A and Project X are the same video -

## Example 1 (One to one copy of AOI data):

```
Source: 
   Project A (Video A with AOI)
Destination: 
   Project X (Video A without AOI)
```

### Result:

```
Destination:
   Project X (Video A with AOI)
```

## Example 2 (One to one copy of multiple AOI data):

```
Source: 
   Project A (Video A with AOI) (Video B with AOI) 
Destination: 
   Project X (Video A without AOI) (Video B without AOI)
```

### Result:

```
Destination: 
   Project X (Video A with AOI) (Video B with AOI)
```

## Example 3 (One to one copy of AOI data where source contains multiple sets of AOI):

```
Source: 
   Project A (Video A with AOI) (Video B with AOI) (Video C with AOI)
Destination: 
   Project X (Video B with AOI)
```

### Result:

```
Destination: 
   Project X (Video B with AOI)
```

## Example 4 (Merge of AOI data from multiple sources to destination without AOI):

```
Source: 
   Project A (Video A with AOI)
   Project B (Video A with AOI)
Destination: 
   Project X (Video A without AOI)
```

### Result:

```
Destination: 
   Project X (Video A with AOI (from both Project A and Project B))
```

## Example 5 (Merge of AOI data from multiple sources to destination with AOI)::

```
Source: 
   Project A (Video A with AOI)
   Project B (Video A with AOI)
Destination: 
   Project X (Video A with AOI)
```

### Result:

```
Destination: 
   Project X (Video A with AOI (from Project X, Project A and Project B))
```

In most cases, example 1 is the simplest and with this in mind, it may be easier, to take a copy of a working project and to manipulate it so it acts as a clean copy source for others.  

With some modifications to the source code, it should also be possible to create a pipeline using the script so that you have one dedicated source, that allows you to copy from the source to all target projects.  If this is desired, I recommend implementing a SQL execute to clear the MovingAOI entries prior to insertion.

After running the script, review your project in Tobii Studio, the project should now contain the equivalent points of interest.

# Disclaimer

As per the Instructions for use, ensure that you backup your project prior to making any changes.  The project relies on the use of the same video file with the same filename, if you have a video file using the same name, but a different file, it will not work.

# Contribution

This project was done to assist in a problem that arose for my wife during her PhD studies, I personally am not an active user of any of the Tobii software and built this project by examining saved output projects from Tobii Studio.  If this is of use to you in any way or you make any improvements to it, then please feel free to raise a merge request.  If this is reviewed by a member of the Tobii Studio software team, I urge you to add this functionality to what is an excellent piece of software.

Should changes be made in the future, please let me know and I will update the repository to advise users of the appropriate version with said export/import functionality.
