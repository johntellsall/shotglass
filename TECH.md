A source tree is scanned for symbols, which are stored in SourceLine records; an index. One record for one symbol, with name, file location, and line number information.

The Render code turns the index into a "skeleton." For all symbols, the index and x,y location of each symbol is calculated.  If a user decides to exclude e.g. the Examples and Tests directories, the skeleton would change. The skeleton maps symbols into x,y positions on a grid.

Lastly, the Draw code colors in the skeleton based on specific needs. One drawing style puts colored boxes around each directory in the source tree. Another style draws each symbol in a different color, so the entire effect is like a rainbow.  Third-party information can also be rendered: draw each symbol with color based on complexity. Complex code is seen as red; simple, clear code in blue.

Draw code is of two types: _what_ is being drawn, and _what color_ it is. If we're just drawing the folders, then we don't are about symbol details. The former is known as a "draw style", and the latter is a (color) "theme".
