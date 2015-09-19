# -*- coding: utf-8 -*-

import click

from functools import partial
from itertools import chain

from baron.parser import ParsingError
from baron.utils import BaronError
from redbaron import (
    Node,
    RedBaron,
)


def is_without_trailing_comma(node):
    fst = node.fst()
    contents = fst['value']
    trailing_formatting = []

    for fmt_type in (
        'second_formatting',
        'third_formatting',
    ):
        trailing_formatting.extend(fst[fmt_type])

    # If collection has no elements, we have no work to do
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
        if is_without_trailing_comma(node):
            last_value = node.value[-1]
            bounds = last_value.absolute_bounding_box
            top_left = bounds.top_left.to_tuple()
            bottom_right = bounds.bottom_right.to_tuple()

            # Sometimes right boundary determined incorrectly
            line, column = top_left if bottom_right[1] == 0 else bottom_right
            yield last_value, line, column


@click.command()
@click.argument('filenames', nargs=-1)
@click.option('--autofix/--no-autofix', default=False, help='Attempt to insert missing commas upon detection.')
def processor(filenames, autofix):
    found = False
    comma_node = Node.from_fst({
        'first_formatting': [],
        'second_formatting': [],
        'type': 'comma',
    })

    for filename in filenames:
        with open(filename, 'r') as fp:
            source_code = fp.read()

        try:
            red = RedBaron(source_code)
        except BaronError:
            print '[ERROR] Failed to parse {0} :-('.format(filename)
            continue

        node_types = ('list', 'dict', 'tuple', 'set', 'call')
        positions = map(
            partial(find_missing_commas, red),
            node_types,
        )

        positions = sorted(chain(*positions))
        for node, line, column in positions:
            found = True
            position_str = '{0}:{1}:{2}'.format(
                filename, line, column,
            )

            if autofix:
                try:
                    node.parent.node_list.append(comma_node)
                    print '[INFO] Missing comma inserted ({0})'.format(position_str)
                except ParsingError:
                    print '[ERROR] Failed to fix missing comma ' \
                          'due to parsing error ({0})'.format(position_str)
            else:
                print '{0}: Y001 missing trailing comma'.format(position_str)

        if found and autofix:
            with open(filename, 'w') as fp:
                fp.write(red.dumps())

    exit(found and 1 or 0)


if __name__ == '__main__':
    processor()
