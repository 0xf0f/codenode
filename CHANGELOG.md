1.0 (August 16, 2023)

- A near total rewrite, featuring a change to how nodes are 
approached. Any tree of iterables can now be used as a node.
- Strings no longer represent full lines. Instead, lines are represented
using an indentation node, some strings, and a newline node.
- Removed language specific modules.
- Added some general helpful classes/functions in codenode_utilities
- Rewrote readme.
- Added documentation.
- Added extra debugging help using the debug paramter
in dump/dumps.
- Fleshed out the project in general:
  - Added some tool scripts for development.
  - Added some basic tests.
- Published on PyPI.