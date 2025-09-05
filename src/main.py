import argparse
from lib.calc import ShuntingYard, evaluate_rpn

def main():
    parser = argparse.ArgumentParser(description='A simple calculator CLI.')
    parser.add_argument("expression", type=str, help="Enter the statement to be evaluated")
    args = parser.parse_args()

    try:
        rpn_tokens = ShuntingYard(args.expression)
        result = evaluate_rpn(rpn_tokens)
        print(result)
    except (ValueError, IndexError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()