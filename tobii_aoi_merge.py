import sqlite3
import pprint
import uuid
ppsetup = pprint.PrettyPrinter(indent=4)
pp = ppsetup.pprint

source_db = "C:\\Users\\James\\Documents\\Tobii Studio Projects\\Test 1\\database.db3"
dest_db   = "C:\\Users\\James\\Documents\\Tobii Studio Projects\\Test 2\\database.db3"

# Create connections
source_conn = sqlite3.connect(source_db)
dest_conn   = sqlite3.connect(dest_db)

# Create a media lookup table
medialookup = { 'source' : {}, 'dest' : {} }

print('Examining source media...')
source_cursor_1 = source_conn.cursor()
for row in source_cursor_1.execute("SELECT MediaID, FileId, TestId, Name FROM Media"):
    if 'Name_to_MediaID' not in medialookup['source']:
        medialookup['source']['Name_to_MediaID'] = {}
    if 'MediaID_to_Name' not in medialookup['source']:
        medialookup['source']['MediaID_to_Name'] = {}
    if row[3] not in medialookup['source']['Name_to_MediaID']:
        medialookup['source']['Name_to_MediaID'][row[3]] = [row[0]]
    else:
        medialookup['source']['Name_to_MediaID'][row[3]].append(row[0])
    medialookup['source']['MediaID_to_Name'][row[0]] = row[3]

print('Examining dest media...')
dest_cursor_1 = dest_conn.cursor()
for row in dest_cursor_1.execute("SELECT MediaID, FileId, TestId, Name FROM Media"):
    if 'Name_to_MediaID' not in medialookup['dest']:
        medialookup['dest']['Name_to_MediaID'] = {}
    if 'MediaID_to_Name' not in medialookup['dest']:
        medialookup['dest']['MediaID_to_Name'] = {}
    if row[3] not in medialookup['dest']['Name_to_MediaID']:
        medialookup['dest']['Name_to_MediaID'][row[3]] = [row[0]]
    else:
        medialookup['dest']['Name_to_MediaID'][row[3]].append(row[0])
    medialookup['dest']['MediaID_to_Name'][row[0]] = row[3]

print('Built the following medialookup')
pp(medialookup)

print('Looking in source media for AOI')

# Create additional cursors (cannot be reused in sqlite/python when nesting in for loops)
source_cursor_2 = source_conn.cursor()

for row in source_cursor_2.execute("SELECT MovingAoiId, MediaId, TestId, Name, Color, ZOrder, TextExportOrder, VersionNo FROM MovingAoi"):

    # Store names for ease
    aoi_id = row[0]
    source_media_id = row[1]
    video_name = medialookup['source']['MediaID_to_Name'][row[1]]
    aoi_name = row[3]

    print("Found AOI {} against video - {}".format(aoi_id, video_name))

    # Check to see if the MediaID's name exists in the destination
    if video_name in medialookup['dest']['Name_to_MediaID']:

        print('Video {} exists in both source and destination'.format(video_name))

        for i, dest_media_id in enumerate(medialookup['dest']['Name_to_MediaID'][video_name]):
            print('- Processing Video {} of {} with media_id {}'.format(i+1, video_name, dest_media_id))

            new_aoi_id = uuid.uuid1()
            print('-- Creating unique AOI id to avoid duplication, Original AOI ID = {}, Media ID = {}, New AOI ID = {}'.format(aoi_id, dest_media_id, new_aoi_id))

            print('--- Checking to see if AOI {} exists for video {} in the destination'.format(new_aoi_id, video_name))

            # Check using the equivalent name from the destination
            dest_cursor_2 = dest_conn.cursor()
            dest_cursor_2.execute("SELECT MovingAoiId, MediaId FROM MovingAoi WHERE MovingAoiID = '{}' AND MediaId = '{}'".format(new_aoi_id, dest_media_id))

            # If we didn't find the area of interest, add it to the table
            if dest_cursor_2.fetchall() == []:

                print('---- AOI {} does not exist on Destination, adding'.format(aoi_name))
                print("----- DEBUG INSERT INTO MovingAoi VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(new_aoi_id, dest_media_id, row[2], aoi_name, row[4], row[5], row[6], row[7]))
                dest_cursor_2.execute("INSERT INTO MovingAoi VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(new_aoi_id, dest_media_id, row[2], aoi_name, row[4], row[5], row[6], row[7]))
                dest_conn.commit()

                # Find all of the Keyframes that relate to the MovingAoi
                print('------ Checking for Keyframes for AOI {}'.format(aoi_name))

                source_cursor_3 = source_conn.cursor()
                for keyframe_row in source_cursor_3.execute("SELECT KeyFrameId, MovingAoiId, PointInTime, IsCollectingData, VersionNo, Vertices FROM KeyFrame WHERE MovingAoiId = '{}'".format(aoi_id)).fetchall():

                    keyframe_id = keyframe_row[0]
                    print('------- Found Keyframe ID {}'.format(keyframe_id))

                    new_keyframe_id = uuid.uuid1()
                    print('-------- Creating unique KeyFrame ID to avoid duplication, Original KeyFrame ID = {}, Media ID = {}, New KeyFrame ID = {}'.format(keyframe_id, dest_media_id, new_keyframe_id))
                    print('--------- Checking to see if Keyframe ID {} exists on the destination'.format(new_keyframe_id))
                    dest_cursor_3 = dest_conn.cursor()
                    dest_cursor_3.execute("SELECT * FROM KeyFrame WHERE KeyFrameId = '{}'".format(new_keyframe_id))

                    if dest_cursor_3.fetchall() == []:
                        print("---------- KeyFrame {} does not exist on the destination, adding".format(keyframe_id))

                        # Recreate uuid's within verticies
                        keyframe_data_entries = keyframe_row[5].split('|')
                        entries = []
                        for entry in keyframe_data_entries[:-1]:
                            components = entry.split('*')
                            components[0] = 'id:{}'.format(uuid.uuid1())
                            s = '*'
                            entries.append(s.join(components))
                        verticies_data = "|".join(entries) + '|'
                        print('----------- Recreated Vertices with new UUID, OLD = {}, New = {}'.format(keyframe_row[5], verticies_data))

                        print("------------ DEBUG INSERT INTO KeyFrame VALUE('{}','{}','{}','{}','{}','{}')".format(new_keyframe_id, new_aoi_id, keyframe_row[2], keyframe_row[3], keyframe_row[4], verticies_data))
                        dest_cursor_3.execute("INSERT INTO KeyFrame VALUES('{}','{}','{}','{}','{}','{}')".format(new_keyframe_id, new_aoi_id, keyframe_row[2], keyframe_row[3], keyframe_row[4], verticies_data))
                        dest_conn.commit()

                    else:
                        print("----------- KeyFrame ID {} exists on the destination, ignoring".format(keyframe_id))

            else:
                print('---- AOI {} already exists on Destination, ignoring'.format(aoi_name))

    else:
        print('Found that video {} exist on source but not destination, ignoring'.format(video_name))

    print('Finished processing source media')

source_conn.close()
dest_conn.close()
print('Finished')
