import argparse
from mindpile import to_python

parser = argparse.ArgumentParser(description="Transpiles Mindstorms to ev3dev2 python.")

parser.add_argument("mindstorms_path", type=str, help="The path to your mindstorms program (file ending with .ev3)")
parser.add_argument("--output_path", "-o", type=str, default="code.py", dest="output_path", help="The file we output python code to.")

def main(passed_args=None):
    import os, sys
    import tempfile
    from zipfile import ZipFile
    args = parser.parse_args(passed_args or sys.argv[1:])
    # Some preliminary checks
    if not args.mindstorms_path.endswith(".ev3"):
        raise ValueError("The mindstorms file to extract should have the `.ev3` file ending.")
    # First -> Unzip the .ev3 file into a temporary location. Extract the ev3p file.
    with tempfile.TemporaryDirectory() as tmpdir:
        with ZipFile(args.mindstorms_path, "r") as zipObj:
            zipObj.extractall(tmpdir)
        # Second -> Generate the python code.
        python_source = to_python(os.path.join(tmpdir, "Program.ev3p"))
    # Third -> Save to the output_path.
    with open(args.output_path, "w") as f:
        f.write(python_source)
    print(f"Program written to {args.output_path}.")

if __name__ == "__main__":
    main()
