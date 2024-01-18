import subprocess
import os


def combo_trim_split(img, output_path, fuzz, in_place=None):
    trim_borders(img, output_path, fuzz)
    img = os.path.join(output_path, os.path.basename(img))
    vertical_split(img, output_path, fuzz, True)


def trim_borders(img, output_path, fuzz, in_place=None):
    command = f'mogrify -fuzz {fuzz}% -trim -path {output_path} {img}'
    subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True)
    return


def vertical_split(img, output_path, fuzz=None, in_place=False):
    in_place = '' if in_place else f'-path {output_path} '
    command = f'mogrify -crop 50%x100% +repage {in_place}{img}'
    subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True)
    return



