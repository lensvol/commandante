# -*- coding: utf-8 -*-

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


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print 'No arguments. :-('
        exit(-1)

    source_file_fn = sys.argv[1]
    with open(source_file_fn, 'r') as fp:
        source_code = fp.read()

    red = RedBaron(source_code)
    lists = red.find_all('list')

    for list_node in lists:
        if is_without_trailing_comma(list_node.fst()):
            line, column = list_node.absolute_bounding_box.bottom_right.to_tuple()
            print '{0}:{1}:{2}: Y001 trailing comma mising'.format(
                source_file_fn, line, column,
            )
