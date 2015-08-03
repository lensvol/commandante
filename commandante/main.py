# -*- coding: utf-8 -*-

import click

from functools import partial
from itertools import chain

from redbaron import RedBaron


def is_without_trailing_comma(fst):
    contents = fst['value']
    trailing_formatting = []

    for fmt_type in (
        'first_formatting',
        'second_formatting',
        'third_formatting',
        'fourth_formatting',
    ):
        trailing_formatting.extend(fst[fmt_type])

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
            bounds = node.value[-1].absolute_bounding_box
            line, column = bounds.bottom_right.to_tuple()
            yield line, column


@click.command()
@click.argument('filename', nargs=1)
def processor(filename):
    with open(filename, 'r') as fp:
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
            filename, line, column,
        )
    exit(positions and 1 or 0)


if __name__ == '__main__':
    processor()
