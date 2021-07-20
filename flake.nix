{
  description = "A transpiler for EV3 mindstorms to ev3dev2 Python";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/21.05";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.simpleFlake {
      inherit self nixpkgs;
      name = "mindpile";
      systems = flake-utils.lib.defaultSystems;
      overlay = (final: prev:
        let
          lib = prev.lib;
          versionFile = builtins.readFile ./mindpile/__init__.py;
          versionLine = lib.findFirst (lib.hasPrefix "__version__") "" (lib.splitString "\n" versionFile);
          version = lib.removePrefix "__version__ = \"" (lib.removeSuffix "\"" versionLine);
          package = prev.python39Packages.buildPythonPackage {
            pname = "mindpile";
            inherit version;
            src = builtins.path { path = ./.; name = "mindpile"; };
          };
        in {
          mindpile = {
            mindpile = package;
            defaultPackage = package;
          };
        });
    };
}
