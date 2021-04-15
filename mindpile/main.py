import sys
import argparse
from mindpile import to_python

parser = argparse.ArgumentParser(description="Transpiles Mindstorms to ev3dev2 python.")

parser.add_argument("mindstorms_path", type=str, help="The path to your mindstorms program (file ending with .ev3)")
parser.add_argument("--output_path", "-o", type=str, default="code.py", dest="output_path", help="The file we output python code to.")

def main(passed_args=None):
    args = parser.parse_args(passed_args or sys.argv[1:])
    # Some preliminary checks
    if not args.mindstorms_path.endswith(".ev3"):
        raise ValueError("The mindstorms file to extract should have the `.ev3` file ending.")
    python_source = to_python(args.mindstorms_path)
    with open(args.output_path, "w") as f:
        f.write(python_source)
    print(f"Program written to {args.output_path}.")

if __name__ == "__main__":
    main()
