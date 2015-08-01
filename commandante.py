# -*- coding: utf-8 -*-

from functools import partial
from itertools import chain
import sys

from baron.path import node_to_bounding_box
from redbaron import RedBaron


def is_without_trailing_comma(fst):
    contents = fst['value']
    trailing_formatting = fst['third_formatting']

    return (
        trailing_formatting
        and trailing_formatting[-1]['type'] == 'endl'
        and contents[-1]['type'] != 'comma'
    )


def find_missing_commas(red, collection_type):
    nodes = red.find_all(collection_type)
    positions = []

    for node in nodes:
        if is_without_trailing_comma(node.fst()):
            bounds = node.absolute_bounding_box
            line, column = bounds .bottom_right.to_tuple()
            yield line, column


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print 'No arguments. :-('
        exit(-1)

    source_file_fn = sys.argv[1]
    with open(source_file_fn, 'r') as fp:
        source_code = fp.read()

    red = RedBaron(source_code)

    collections = ('list', 'dict', 'tuple', 'set')
    positions = map(
        partial(find_missing_commas, red),
        collections,
    )

    positions = sorted(chain(*positions))
    for line, column in positions:
        print '{0}:{1}:{2}: Y001 missing trailing comma'.format(
            source_file_fn, line, column,
        )
    exit(positions and 1 or 0)
