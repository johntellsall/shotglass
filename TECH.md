A source tree is scanned for symbols, which are stored in SourceLine records; an index. One record is for one symbol, with name, file location, and line number information.

The Render code turns the index into a "skeleton." For all symbols, the position and x,y location of each symbol is calculated.  If a user decides to exclude e.g. the Examples and Tests directories, the skeleton would change.

Lastly, the Draw code colors in the skeleton based on specific needs. One drawing style puts colored boxes around each directory in the source tree. Another style draws each symbol in a different color, so the entire effect is like a rainbow.  Third-party information can also be rendered: draw each symbol with color based on complexity. Very complex code is seen as red, simple, clear code in blue.
