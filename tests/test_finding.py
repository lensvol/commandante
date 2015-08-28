# -*- coding: utf-8 -*-

from redbaron import RedBaron
from commandante.main import find_missing_commas


DICT_SAMPLES = (
    (
        '''
        d = {
            'a': 42,
            'b': 'hello, world'
        }
        ''',
        [(5, 8)],
    ),
    (
        '''
        d = {
            'a': 42,
        }
        ''',
        [],
    )
)


TUPLE_SAMPLES = (
    (
        '''
        (
            42,
            12345
        )
        ''',
        [(4, 17)],
    ),
    (
        '''
        (
            42,
            98,
        )
        ''',
        [],
    ),
    (
        # Multiline string case
        '''
        (
            "Hello"
            "World"
        )
        ''',
        [],
    ),
)


LIST_SAMPLES = (
    (
        '''
        [
            42,
            12345
        ]
        ''',
        [(4, 17)],
    ),
    (
        '''
        [
            42,
            12345,
        ]
        ''',
        [],
    )
)

CALL_ARGS_SAMPLES = (
    (
        '''
        f(
            123,
            'Hello, world!'
        )
        ''',
        [(5, 8)],
    ),
)

SET_SAMPLES = (
    (
        '''
        {
            123,
            'Hello, world!'
        }
        ''',
        [(5, 8)],
    ),
)

SAMPLES = {
    'dict': DICT_SAMPLES,
    'tuple': TUPLE_SAMPLES,
    'list': LIST_SAMPLES,
    'call': CALL_ARGS_SAMPLES,
    'set': SET_SAMPLES,
}


def test_finding_commas():
    for collection_type, samples in SAMPLES.iteritems():
        for sample, positions in samples:
            red = RedBaron(sample)
            results = list(find_missing_commas(red, collection_type))

            positions = sorted(positions)
            results = sorted(results, key=lambda c: (c[1], c[2]))
            results = [(c[1], c[2]) for c in results]
            assert positions == results
