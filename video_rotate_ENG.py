import os
from os.path import exists

# was importing:
# import moviepy.editor as mp  # moviepy 1.0.3
# Below because of "module 'moviepy.audio.fx.all' has no attribute 'audio_fadein'" in "pyinstaller" (.py to .exe)
# Import below dependencies fixed an issue from above and .exe is working properly.
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.editor import concatenate_videoclips,concatenate_audioclips,TextClip,CompositeVideoClip
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex


welcome_info_txt = """
The script has to be located in the same localization as videos source folder. 
User will be asked to provide the name of the source folder. 
Next user has to provide information about rotation angle, for all the videos in the source folder.
Rotated videos will be saved as new video in the output folder.
Output folder "Result" will be created automatically (if it is not existing), in the same location as script.
"""


def user_input_folder_name():
    # User input folder name.
    folder_name = input("Please enter name of source folder file.\n")

    if not exists(folder_name):
        print(f'{folder_name} folder does not exist in script location.\nRun script again.\n')
    else:
        folder_name = folder_name + '/'

    return folder_name


def user_input_angle_value():
    # User input angle.
    value = input("\nPlease enter a rotation angle.\nOptions are: 90, 180, 270 and -90, -180, -270.\n")

    if int(value) in (90, 180, 270, -90, -180, -270):
        print(f'You entered {value} deg angle.')
    else:
        value = input(f'You entered {value}.\nWrong angle.\nTry again: \n')

    value = int(value)

    return value


def rotate_vid(folder_name, value):
    i = 1
    for file in os.listdir(folder_name):
        print(f'\nProcessing file number {i}.\n')

        # Split file name to name and file format.
        f_name, form = file.split('.')

        # Load the file and assign original fps rate to variable.
        clip = VideoFileClip(folder_name + file)
        fps = clip.fps

        # Check if video is in portrait mode.
        if clip.rotation == 90:
            # Switch dimensions from h, w to w, h.
            clip = clip.resize(clip.size[::-1])
            clip.rotation = 0

        # Rotate based on user input.
        if value == 90:
            rotated_clip = clip.rotate(90)
        elif value == 180:
            rotated_clip = clip.rotate(180)
        elif value == 270:
            rotated_clip = clip.rotate(270)
        elif value == -90:
            rotated_clip = clip.rotate(-90)
        elif value == -180:
            rotated_clip = clip.rotate(-180)
        elif value == -270:
            rotated_clip = clip.rotate(-270)
        else:
            print('Wrong angle again.')
            break

        # Format name for resulting file.
        if i < 10:
            name = 'Result/' + '0' + str(i) + '_' + f_name + '_' + str(value) + 'deg.' + form
        else:
            name = 'Result/' + str(i) + '_' + f_name + '_' + str(value) + 'deg.' + form

        # Write rotated file with new name and original fps and sound.
        rotated_clip.write_videofile(name, fps=fps, audio=True, verbose=False)

        # Increment loop variable.
        i += 1

    # Kill moviepy process.
    clip.close()

    return print('Process finished.')


if __name__ == '__main__':
    print(welcome_info_txt)

    folder_name = user_input_folder_name()
    value = user_input_angle_value()

    # Create new directory for resulting files if it is not already existing.
    try:
        os.mkdir('Result/')
    except FileExistsError:
        print('Existing directory for output files.')

    rotate_vid(folder_name, value)
