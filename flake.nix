{
  description = "A transpiler for EV3 mindstorms to ev3dev2 Python";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/21.05";

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.mindpile = 
      with import nixpkgs { system = "x86_64-linux"; };
      pkgs.python39Packages.buildPythonPackage (let
        versionFile = builtins.readFile ./mindpile/__init__.py;
        versionLine = lib.findFirst (lib.hasPrefix "__version__") "" (lib.splitString "\n" versionFile);
        version = lib.removePrefix "__version__ = \"" (lib.removeSuffix "\"" versionLine);
      in {
        pname = "mindpile";
        version = version;
        src = builtins.path { path = ./.; name = "mindpile"; };
      });

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.mindpile;
    
    devShell.x86_64 = nixpkgs.mkShell {
      buildInputs = [ self.packages.x86_64-linux.mindpile ];
    };
  };
}
