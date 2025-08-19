import argparse

parser = argparse.ArgumentParser(description='A simple calculator CLI.')
parser.add_argument("eval", type=str, help="Enter the statement to be evaluated")
args = parser.parse_args()
#if args.operation=="eval":
#    print(eval(args.eval))