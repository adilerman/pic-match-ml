import subprocess


def prepare_stereo_image(img_path):
    trim_borders(img_path)
    vertical_split(img_path)


def vertical_split(img_path):  # TODO should I put these functions inside Image class?
    command = f'mogrify -crop 50%x100% +repage {img_path}'
    result = subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True)
    return result


def trim_borders(img_path):  # TODO should I put these functions inside Image class?
    command = f'mogrify -fuzz 20% -trim {img_path}'
    subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True)
    return
