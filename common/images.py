import subprocess
import os


def combo_trim_split(img, output_path, image_vars, in_place=None):
    trim_borders(img, output_path, image_vars)
    img = os.path.join(output_path, os.path.basename(img))
    vertical_split(img, output_path, image_vars,True)


def trim_borders(img, output_path, image_vars, in_place=None):
    command = f'mogrify -fuzz {image_vars["fuzz"]}% -trim -path {output_path} {img}'
    subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True)
    return


def vertical_split(img, output_path, image_vars, in_place=False):
    in_place = '' if in_place else f'-path {output_path} '
    command = f'mogrify -crop {image_vars["split"]}%x100% +repage {in_place}{img}'
    subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True)
    return



