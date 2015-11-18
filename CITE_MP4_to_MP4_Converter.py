# BS"D
# 11/18/2015
# Good Start
'''
TODO:
	1. error checking
	2. log error
'''
import os
import subprocess

SRC_DIR = '\\Users\\Ben\\Desktop\\CITE\\Testing'
OUT_DIR = '\\Users\\Ben\\Desktop\\CITE\\Testing-Output'

# Loop through the src_directory file
print(SRC_DIR)
for f in os.listdir(SRC_DIR):
	print(f)
	#todo: check if nothing
	mp3_file_name = f[:-3] + 'mp3'
	#print(type(f))
	print(mp3_file_name)
	ffmpeg_convert_to_mp3_cmd = 'ffmpeg -i ' + SRC_DIR + '\\' + f + ' ' + SRC_DIR + '\\' + mp3_file_name
	print(ffmpeg_convert_to_mp3_cmd)
	command_output = subprocess.check_output(ffmpeg_convert_to_mp3_cmd, shell=True)          # Run the command
	print(command_output)