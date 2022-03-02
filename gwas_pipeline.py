import argparse

from src.command_main import command_main


def argument_collector():
    parser = argparse.ArgumentParser()
    search_term = parser.add_mutually_exclusive_group(required=True)
    search_term.add_argument('-id', help="Search based on trait ID code.", type=str, default=None)
    search_term.add_argument('-n', '--name', help="Searched based on trait name.", type=str, default=None)
    parser.add_argument('-o', '--output', help="Path for output file.", type=str, required=True)
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    # args = argument_collector()
    args = {'id': 'EFO_0000685', 'name': None, 'output': 'C:\\Users\\Martin\\OneDrive\\Documents\\Study\\rp1\\file.csv'}
    command_main(args['id'], args['name'], args['output'])
