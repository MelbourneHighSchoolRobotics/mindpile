let
  versionFile = builtins.readFile ./mindpile/__init__.py;
  # version = 
in
{
  description = "A transpiler for EV3 mindstorms to ev3dev2 Python";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/21.05";

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.mindpile = 
      with import nixpkgs { system = "x86_64-linux"; };
      pkgs.python39Packages.buildPythonPackage {
        pname = "mindpile";
        version = "0.0.2";
        src = builtins.path { path = ./.; name = "mindpile"; };
      };

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.mindpile;
    
    devShell.x86_64 = nixpkgs.mkShell {
      buildInputs = [ self.packages.x86_64-linux.mindpile ];
    };
  };
}
