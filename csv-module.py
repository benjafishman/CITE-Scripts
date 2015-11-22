__author__ = 'bfishman'

import csv
import os
import subprocess
import shutil
import dropbox

SRC_DIR = '\\Users\\Ben\\Desktop\\CITE\\Testing\\'
Processed_MP4_Dir = '\\Users\\Ben\\Desktop\\CITE\\Processed_MP4\\'
Processed_MP3_Dir = '\\Users\\Ben\\Desktop\\CITE\\Processed_MP3\\'

DropBoxFile = '/Test-Uploads/'

csv_file_name = 'testcsv.csv'
Error = (0, 'No Errors')
'''
CSV Processing
'''
with open(csv_file_name, newline='') as csvfile:
    s = csv.reader(csvfile)
    for row in s:
        # TODO: Add semester
        mp4_file_name = row[0]
        start_time = row[1]
        end_time = row[2]

        # Check if the file exists in the source directory
        if not os.path.exists(SRC_DIR + mp4_file_name):
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
            ffmpeg_convert_to_mp3_cmd = 'ffmpeg -i ' + SRC_DIR + mp4_file_name + ' ' + SRC_DIR + mp3_file_name

            # Run the command
            command_output = subprocess.check_output(ffmpeg_convert_to_mp3_cmd, shell=True)

            if not os.path.exists(Processed_MP3_Dir):
                os.makedirs(Processed_MP3_Dir)
            '''
            Trim File according to csv specs
            '''
            # Create the ffmpeg trim command string and moved processed MP3 file to 'Processed_MP3_Dir' directory
            trim_cmd = 'ffmpeg -ss ' + str(start_time) + ' -i ' + SRC_DIR + mp3_file_name + ' -to ' + str(
                end_time) + ' ' + Processed_MP3_Dir + mp3_file_name

            # Run the command
            trim_command_output = subprocess.check_output(trim_cmd, shell=True)

            '''
            Move MP4 file to the 'Processed_MP4' directory
            '''
            # check if process_mp4 directory exists, if not make it
            if not os.path.exists(Processed_MP4_Dir):
                os.makedirs(Processed_MP4_Dir)

            shutil.move(SRC_DIR + mp4_file_name, Processed_MP4_Dir + mp4_file_name)

            '''
            Time to upload da file to DB BABAY!!
            '''

            dbx = dropbox.Dropbox('')

            upload_file = Processed_MP3_Dir + mp3_file_name

            f = open(upload_file,'rb')

            print(f)

            dbx.files_upload(f,DropBoxFile + mp3_file_name)

            print('File upload complete?')

        print(Error)






