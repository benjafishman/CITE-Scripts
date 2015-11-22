__author__ = 'bfishman'

import csv
import os
import subprocess
import shutil
import dropbox
import Environment_Vars as ev
 
Error = (0, 'No Errors')
'''
CSV Processing
'''
with open(ev.CSV_FILE_NAME, newline='') as csvfile:
    s = csv.reader(csvfile)
    for row in s:
        # TODO: Add semester and check for each column var
        # TODO: check env vars are set
        mp4_file_name = row[0]
        start_time = row[1]
        end_time = row[2]
        DROPBOX_FILE_NAME = row[3]

        # Check if the file exists in the source directory
        if not os.path.exists(ev.SRC_DIR + mp4_file_name):
            Error = (1, 'File does not exist')
        # Check if the file has valid extension
        elif len(mp4_file_name) < 4 or mp4_file_name[-4:] != '.mp4':
            Error = (1, 'Invalid extension or no extension')
        else:
            mp3_file_name = mp4_file_name[:-3] + 'mp3'
            print(mp3_file_name)
            '''
            Convert mp4 to mp3 using ffmpeg command
            '''
            # Create the ffmpeg command string for mp4 to mp3 conversion
            ffmpeg_convert_to_mp3_cmd = 'ffmpeg -i ' + ev.SRC_DIR + mp4_file_name + ' ' + ev.SRC_DIR + mp3_file_name

            try:
                # Run the command
                command_output = subprocess.check_output(ffmpeg_convert_to_mp3_cmd, shell=True)
            except subprocess.CalledProcessError as e:
                print(e)  

            if not os.path.exists(ev.Processed_MP3_Dir):
                os.makedirs(ev.Processed_MP3_Dir)

            '''
            Trim File according to csv specs
            '''
            # Create the ffmpeg trim command string and moved processed MP3 file to 'Processed_MP3_Dir' directory
            trim_cmd = 'ffmpeg -ss ' + str(start_time) + ' -i ' + ev.SRC_DIR + mp3_file_name + ' -to ' + str(
                end_time) + ' ' + ev.Processed_MP3_Dir + mp3_file_name

            # Run the command
            try:
                trim_command_output = subprocess.check_output(trim_cmd, shell=True)
                # remove mp3 file from src directory
                os.remove(ev.SRC_DIR + mp3_file_name)
            except subprocess.CalledProcessError as e:
                print(e)

            '''
            Move MP4 file to the 'Processed_MP4' directory
            '''
            # check if process_mp4 directory exists, if not make it
            if not os.path.exists(ev.Processed_MP4_Dir):
                os.makedirs(ev.Processed_MP4_Dir)

            shutil.move(ev.SRC_DIR + mp4_file_name, ev.Processed_MP4_Dir + mp4_file_name)

            '''
            Time to upload da file to DB BABAY!!
            '''

            dbx = dropbox.Dropbox(ev.DB_AUTH_KEY)

            upload_file = ev.Processed_MP3_Dir + mp3_file_name

            f = open(upload_file,'rb')

            print(f)

            dbx.files_upload(f, "/" + DROPBOX_FILE_NAME + "/" + mp3_file_name)

            print('File upload complete?')

        print(Error)






