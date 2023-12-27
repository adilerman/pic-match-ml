from common.images import trim_borders, vertical_split, prepare_stereo_image


FUNC_MAP = {
        'trim': trim_borders,
        'split': vertical_split,
        'prep': prepare_stereo_image
    }


def main():
    command, path = input('Enter command and file path\n').split(' ')
    FUNC_MAP[command](path)
    return


if __name__ == '__main__':
    main()
