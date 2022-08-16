#!/usr/bin/env python3
# SPDX-License-Identifier: MIT OR Apache-2.0
# SPDX-FileCopyrightText: Critical Section GmbH

# Script that checks whether the glossary entry headers are in natural sorted order

from pathlib import Path

root = Path(__file__).parent.resolve()

glossary_lines = list(map(lambda line: line[:-1], open(f"{root}/src/glossary.rst", "r").readlines()))

followed_by_header_spec = lambda it: len(it[1]) > 0 and all(c == '^' for c in it[1])

lines_windows2 = zip(glossary_lines, glossary_lines[1:])

headers = list(map(lambda it: it[0], filter(followed_by_header_spec, lines_windows2)))

incorrect_headers = []
for (prev, next) in zip(headers, headers[1:]):
    import re
    # very simplistic natural ordering
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    if key(prev) > key(next):
        incorrect_headers.append((prev, next))

if len(incorrect_headers) != 0:
    print("Glossary headers are not sorted:")
    for (prev, next) in incorrect_headers:
        print(f"`{prev}` comes before `{next}` but it should come after")
    exit(1)
