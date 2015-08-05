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

    # If call has no arguments, we have no work to do
    if not contents:
        return False

    last_token = contents[-1]
    if last_token['type'] == 'dict_argument':
        # Python 2 syntax forbids putting trailing comma after
        # unpacking dict argument (like **d)
        return False

    return (
        trailing_formatting
        and trailing_formatting[-1]['type'] == 'endl'
        and last_token['type'] != 'comma'
    )


def find_missing_commas(red, collection_type):
    nodes = red.find_all(collection_type)

    for node in nodes:
        if is_without_trailing_comma(node.fst()):
            bounds = node.value[-1].absolute_bounding_box
            line, column = bounds.bottom_right.to_tuple()
            yield line, column


@click.command()
@click.argument('filenames', nargs=-1)
def processor(filenames):
    found = False

    for filename in filenames:
        with open(filename, 'r') as fp:
            source_code = fp.read()

        red = RedBaron(source_code)

        node_types = ('list', 'dict', 'tuple', 'set', 'call')
        positions = map(
            partial(find_missing_commas, red),
            node_types,
        )

        positions = sorted(chain(*positions))
        for line, column in positions:
            found = True
            print '{0}:{1}:{2}: Y001 missing trailing comma'.format(
                filename, line, column,
            )

    exit(found and 1 or 0)


if __name__ == '__main__':
    processor()
