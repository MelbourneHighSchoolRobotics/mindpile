import argparse
from mindpile import from_ev3

parser = argparse.ArgumentParser(description="Transpiles Mindstorms to ev3dev2 python.")

parser.add_argument("mindstorms_path", type=str, help="The path to your mindstorms program (file ending with .ev3)")
parser.add_argument("--output_path", "-o", type=str, default="code.py", dest="output_path", help="The file we output python code to.")
parser.add_argument("--ev3sim", "-e", action="store_true", dest="ev3sim_support", help="Enable ev3sim support")

def main(passed_args=None):
    import sys
    args = parser.parse_args(passed_args or sys.argv[1:])
    python_source = from_ev3(args.mindstorms_path, ev3sim_support=args.ev3sim_support)
    # Third -> Save to the output_path.
    with open(args.output_path, "w") as f:
        f.write(python_source)
    print(f"Program written to {args.output_path}.")

if __name__ == "__main__":
    main()
