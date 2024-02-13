## Update:

**2022/09/30:** fixed ProtectedDict, ProtectedList, ProtectedTuple, ProtectedSet - Sometimes didn't protect!

**2022/09/30:** Added doc strings

## What does it do?

It flattens any iterable, it doesn't matter how deeply it is nested. If there are dicts in you iterable, it will only return the values. If you need the keys too, have a look at this package: [flatten-any-dict-iterable-or-whatsoever · PyPI](https://pypi.org/project/flatten-any-dict-iterable-or-whatsoever/)

## Install it:

```python
pip install flatten-everything
```

## Import it:

```python
from flatten_everything import flatten_everything, ProtectedDict,ProtectedList,ProtectedTuple,ProtectedSet
```

## Use it:

```python
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
            "another_nested_something": [(2, 1), (3, 2), (1, 2), (1, 3), (1, 3), (2, 3), (1, 1), (3, 3), (2, 1), (1, 1), (1, 2), (3, 1), (3, 1), (3, 2), (1, 2), (1, 1), (3, 2), (2, 1), (1, 1), (3, 1)],
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


    #If you want to protect iterables from being flattened, you can use:

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
        "sdfsdf": {"name": "Luna", "age": "24", "sex": "Female"}, 'another_nested_something': ProtectedList([(2, 1), (3, 2), (1, 2), (1, 3), (1, 3), (2, 3), (1, 1), (3, 3), (2, 1), (1, 1), (1, 2), (3, 1), (3, 1), (3, 2), (1, 2), (1, 1), (3, 2), (2, 1), (1, 1), (3, 1)]),
        "Peter": ProtectedDict({"name": "Peter", "age": "29", "sex": "Male"}),
    },},},{"id": "002",
"company": "PQR Associates",
"location": "Abu Dhabi",
"info": {    "president": "Neelam Subramaniyam",
    "contacts": {"email": "contact@pqr.com", "tel": "8876443210"},},},]
print(list(flatten_everything(data)))
['001', 'XYZ pvt ltd', (333, 332, 555), 'London', 'Rakesh Kapoor', 'contact@xyz.com', '9876543210', 'John', '27', 'Male', 'Marie', '22', 'Female', 'Luna', '24', 'Female', [(2, 1), (3, 2), (1, 2), (1, 3), (1, 3), (2, 3), (1, 1), (3, 3), (2, 1), (1, 1), (1, 2), (3, 1), (3, 1), (3, 2), (1, 2), (1, 1), (3, 2), (2, 1), (1, 1), (3, 1)], {'name': 'Peter', 'age': '29', 'sex': 'Male'}, '002', 'PQR Associates', 'Abu Dhabi', 'Neelam Subramaniyam', 'contact@pqr.com', '8876443210']

#Parameters:
#    item: Any
#        Input iterable
#        Most of the time you will be using only this parameter.
#    forbidden: tuple
#        Data dtype which cannot be returned
#        (default=(list, tuple, set, frozenset))
#    allowed: tuple
#        Data dtype which can be returned
#        default (
#        str,
#        int,
#        float,
#        complex,
#        bool,
#        bytes,
#        type(None),
#        ProtectedTuple,  # Inherits from tuple but is protected, this is how you protected iterables
#        ProtectedList,  # same here
#        ProtectedDict, # same here
#        ProtectedSet, # same here
#        Tuppsub  #Inherit from tuple and exclude it from being flattened -
#
#        )
#    dict_variation: tuple
#        Due to recent changes, might not be necessary anymore, used to filter dict variations
#        (default =
#        (
#        "collections.defaultdict",
#        "collections.UserDict",
#        "collections.OrderedDict",
#        )
#Returns:
#    Generator
```
