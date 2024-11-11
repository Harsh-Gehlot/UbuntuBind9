from Dns import BindSetup
from RecordUtils import createRecords
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--domain', type=str, nargs='+', help="Domain")
parser.add_argument('-ip', '--ipaddress', type=str, nargs='+', help="IP Address")
parser.add_argument('-ns', '--ns', type=str, nargs='*', help="IP Address")

args = parser.parse_args()

if __name__ == "__main__":
    bind = BindSetup(record=createRecords(args))
    bind.init()