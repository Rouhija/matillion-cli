import logging
import argparse

class Error(Exception):
    pass

class UtilError(Error):
    def __init__(self, message):
        self.message = message

def parse_command(s):
    ls = s.split(' ')
    return ls

def format_resp(raw_resp):
    try:
        ret = []
        raw_resp = raw_resp.replace('"', '').replace('[', '').replace(']', '')
        ls = raw_resp.split(',')
        for obj in ls:
            obj = obj.strip()
            ret.append(obj)
        return ret
    except Exception as e:
        raise UtilError(e)
        return None

def enumerate_list(ls, search=None):
    for i, obj in enumerate(ls):
        if search is not None:
            if search in obj:
                print(f'{i} - {obj}')
        else:
            print(f'{i} - {obj}')

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="log to console", action="store_true")
    parser.add_argument("-s", "--safe", help="ask for confirmation before executing any operations", action="store_true")
    parser.add_argument("-c", "--configuration", help="re-input configuration values", action="store_true")
    return parser.parse_args()

def logger_options(debug: int):
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(levelname)s:%(asctime)s ⁠— %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
    else:
        logging.basicConfig(
            level=logging.ERROR,
            format='%(levelname)s:%(asctime)s ⁠— %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
