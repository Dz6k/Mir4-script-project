from typing import Generator, Any


class Tuppsub(tuple):
    """Protects tuples internally from being flattened, same as ProtectedTuple"""

    pass


class ProtectedTuple(tuple):
    """Protects tuples from being flattened, same as Tuppsub"""

    pass


class ProtectedList(list):
    """Protects lists from being flattened"""

    pass


class ProtectedDict(dict):
    """Protects dicts from being flattened"""

    pass


class ProtectedSet(set):
    """Protects sets from being flattened"""

    pass


def flatt_dict(
    v,
    forbidden=(list, tuple, set, frozenset),
    allowed=(
        str,
        int,
        float,
        complex,
        bool,
        bytes,
        type(None),
        ProtectedTuple,
        ProtectedList,
        ProtectedDict,
        ProtectedSet,
    ),
) -> Any:
    """
    Flattens any dict, but should not be used directly, use fla_tu
    Use this function to flatten any iterable
        Parameters:
            v: dict
                Input dict
            forbidden: tuple
                Data dtype which cannot be returned
                (default=(list, tuple, set, frozenset))
            allowed: tuple
                Data dtype which can be returned
                default (
                str,
                int,
                float,
                complex,
                bool,
                bytes,
                type(None),
                ProtectedTuple,  # Inherits from tuple but is protected, this is how you protected iterables
                ProtectedList,  # same here
                ProtectedDict, # same here
                ProtectedSet, # same here
                Tuppsub  #Inherit from tuple and exclude it from being flattened -

                )
        Returns:
            Generator


    """

    if isinstance(v, dict):
        if isinstance(v, allowed):
            yield v
        else:
            for k, v2 in v.items():
                if isinstance(v2, allowed):
                    yield v2
                else:
                    yield from flatt_dict(v2, forbidden=forbidden, allowed=allowed)
    elif isinstance(v, forbidden):
        for v2 in v:
            if isinstance(v2, allowed):
                yield v2
            else:
                yield from flatten_everything(v2, forbidden=forbidden, allowed=allowed)
    elif isinstance(v, allowed):
        yield v
    else:
        try:
            for v2 in v:
                try:
                    if isinstance(v2, allowed):
                        yield v2
                    else:
                        yield from flatt_dict(v2, forbidden=forbidden, allowed=allowed)
                except Exception:
                    yield v2
        except Exception:

            yield v


def flatten_everything(
    item,
    forbidden=(list, tuple, set, frozenset),
    allowed=(
        str,
        int,
        float,
        complex,
        bool,
        bytes,
        type(None),
        ProtectedTuple,
        ProtectedList,
        ProtectedDict,
        ProtectedSet,
    ),
    dict_variation=(
        "collections.defaultdict",
        "collections.UserDict",
        "collections.OrderedDict",
    ),
) -> Generator:

    """

    Usage:

    Use any nested iterable
    data = [  # WORKS WITH ANY ITERABLE
    {
        "id": "001",
        "company": "XYZ pvt ltd",
        "location": "London",
        "info": {
            "president": "Rakesh Kapoor",
            "contacts": {"email": "contact@xyz.com", "tel": "9876543210"},
            "onemorefortesting": {
                "name": {"name": "John", "age": "27", "sex": "Male"},
                "Peter2": {"name": "Marie", "age": "22", "sex": "Female"},
                "sdfsdf": {"name": "Luna", "age": "24", "sex": "Female"},
                "another_nested_something": [
                    (2, 1),
                    (3, 2),
                    (1, 2),
                    (1, 3),
                    (1, 3),
                    (2, 3),
                    (1, 1),
                    (3, 3),
                    (2, 1),
                    (1, 1),
                    (1, 2),
                    (3, 1),
                    (3, 1),
                    (3, 2),
                    (1, 2),
                    (1, 1),
                    (3, 2),
                    (2, 1),
                    (1, 1),
                    (3, 1),
                ],
                "Peter": {"name": "Peter", "age": "29", "sex": "Male"},
            },
        },
    },
    {
        "id": "002",
        "company": "PQR Associates",
        "location": "Abu Dhabi",
        "info": {
            "president": "Neelam Subramaniyam",
            "contacts": {"email": "contact@pqr.com", "tel": "8876443210"},
        },
    },
]

        list(flatten_everything(data))

        Result:
        ['001', 'XYZ pvt ltd', 'London', 'Rakesh Kapoor', 'contact@xyz.com', '9876543210', 'John', '27', 'Male', 'Marie', '22', 'Female', 'Luna', '24', 'Female', 2, 1, 3, 2, 1, 2, 1, 3, 1, 3, 2, 3, 1, 1, 3, 3, 2, 1, 1, 1, 1, 2, 3, 1, 3, 1, 3, 2, 1, 2, 1, 1, 3, 2, 2, 1, 1, 1, 3, 1, 'Peter', '29', 'Male', '002', 'PQR Associates', 'Abu Dhabi', 'Neelam Subramaniyam', 'contact@pqr.com', '8876443210']


        If you want to protect iterables from being flattened, you can use:

            data = [
        {
            "id": "001",
            "company": "XYZ pvt ltd",'protect_test':ProtectedTuple((333,332,555)),
            "location": "London",
            "info": {
                "president": "Rakesh Kapoor",
                "contacts": {"email": "contact@xyz.com", "tel": "9876543210"}, 'onemorefortesting': {
                    "name": {"name": "John", "age": "27", "sex": "Male"},
                    "Peter2": {"name": "Marie", "age": "22", "sex": "Female"},
                    "sdfsdf": {"name": "Luna", "age": "24", "sex": "Female"}, 'another_nested_something': ProtectedList([(2, 1),
                                                                                                           (3, 2),
                                                                                                           (1, 2),
                                                                                                           (1, 3),
                                                                                                           (1, 3),
                                                                                                           (2, 3),
                                                                                                           (1, 1),
                                                                                                           (3, 3),
                                                                                                           (2, 1),
                                                                                                           (1, 1),
                                                                                                           (1, 2),
                                                                                                           (3, 1),
                                                                                                           (3, 1),
                                                                                                           (3, 2),
                                                                                                           (1, 2),
                                                                                                           (1, 1),
                                                                                                           (3, 2),
                                                                                                           (2, 1),
                                                                                                           (1, 1),
                                                                                                           (3, 1)]),
                    "Peter": ProtectedDict({"name": "Peter", "age": "29", "sex": "Male"}),
                },
            },
        },
        {
            "id": "002",
            "company": "PQR Associates",
            "location": "Abu Dhabi",
            "info": {
                "president": "Neelam Subramaniyam",
                "contacts": {"email": "contact@pqr.com", "tel": "8876443210"},
            },
        },
    ]
    print(list(flatten_everything(data)))
    ['001', 'XYZ pvt ltd', (333, 332, 555), 'London', 'Rakesh Kapoor', 'contact@xyz.com', '9876543210', 'John', '27', 'Male', 'Marie', '22', 'Female', 'Luna', '24', 'Female', [(2, 1), (3, 2), (1, 2), (1, 3), (1, 3), (2, 3), (1, 1), (3, 3), (2, 1), (1, 1), (1, 2), (3, 1), (3, 1), (3, 2), (1, 2), (1, 1), (3, 2), (2, 1), (1, 1), (3, 1)], {'name': 'Peter', 'age': '29', 'sex': 'Male'}, '002', 'PQR Associates', 'Abu Dhabi', 'Neelam Subramaniyam', 'contact@pqr.com', '8876443210']



        Parameters:
            item: Any
                Input iterable
                Most of the time you will be using only this parameter.
            forbidden: tuple
                Data dtype which cannot be returned
                (default=(list, tuple, set, frozenset))
            allowed: tuple
                Data dtype which can be returned
                default (
                str,
                int,
                float,
                complex,
                bool,
                bytes,
                type(None),
                ProtectedTuple,  # Inherits from tuple but is protected, this is how you protected iterables
                ProtectedList,  # same here
                ProtectedDict, # same here
                ProtectedSet, # same here
                Tuppsub  #Inherit from tuple and exclude it from being flattened -

                )
            dict_variation: tuple
                Due to recent changes, might not be necessary anymore, used to filter dict variations
                (default =
                (
                "collections.defaultdict",
                "collections.UserDict",
                "collections.OrderedDict",
                )
        Returns:
            Generator
    """

    if isinstance(item, allowed):
        yield item
    elif isinstance(item, forbidden) and not isinstance(item, allowed):
        for xaa in item:
            if isinstance(xaa, allowed):
                yield xaa
            else:
                try:
                    yield from flatten_everything(
                        xaa,
                        forbidden=forbidden,
                        allowed=allowed,
                        dict_variation=dict_variation,
                    )
                except Exception:

                    yield xaa
    elif isinstance(item, dict):
        if isinstance(item, allowed):
            yield item
        else:
            yield from flatt_dict(item, forbidden=forbidden, allowed=allowed)
    elif str(type(item)) in dict_variation:
        if isinstance(item, allowed):
            yield item
        else:
            yield from flatt_dict(dict(item), forbidden=forbidden, allowed=allowed)

    elif "DataFrame" in str(type(item)):

        yield from flatt_dict(item.to_dict(), forbidden=forbidden, allowed=allowed)

    else:
        try:
            for ini2, xaa in enumerate(item):
                try:
                    if isinstance(xaa, allowed):
                        yield xaa

                    elif isinstance(xaa, dict):

                        if isinstance(xaa, allowed):
                            yield xaa
                        else:
                            yield from flatt_dict(
                                item, forbidden=forbidden, allowed=allowed
                            )

                    else:
                        yield from flatten_everything(
                            xaa,
                            forbidden=forbidden,
                            allowed=allowed,
                            dict_variation=dict_variation,
                        )
                except Exception:

                    yield from flatten_everything(
                        xaa,
                        forbidden=forbidden,
                        allowed=allowed,
                        dict_variation=dict_variation,
                    )
        except Exception:

            yield item


