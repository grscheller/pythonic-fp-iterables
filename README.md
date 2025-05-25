# Pythonic FP - Tools for iterables and iterators

Tools for iterables and iterators. This project is part of the
[Pythonic FP][1] **pythonic-fp** PyPI namespace projects.

- **Repositories**
  - [pythonic-fp.iterables][2] project on *PyPI*
  - [Source code][3] on *GitHub*
- Detailed documentation for pythonic-fp.fptools
  - [Detailed API documentation][4] on *GH-Pages*

## Overview

- Concatenating and merging iterables
- Dropping and taking values from iterables
- Reducing and accumulating iterables
- Assumptions
  - iterables are not necessarily iterators
  - at all times iterator protocol is assumed to be followed
    - all iterators are assumed to be iterable
    - for all iterators `foo` we assume `iter(foo) is foo`

______________________________________________________________________

[1]: https://github.com/grscheller/pythonic-fp/blob/main/README.md
[2]: https://pypi.org/project/pythonic-fp.iterables/
[3]: https://github.com/grscheller/pythonic-fp-iterables/
[4]: https://grscheller.github.io/pythonic-fp/maintained/iterables/
