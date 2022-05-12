def _MakeType(name):
    return _TypeMeta(name, (Type,), {})


class _TypeMeta(type):
    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (args,)

        name = '{}[{}]'.format(
            str(self),
            ', '.join(map(str, args))
        )
        return _MakeType(name)

    def __str__(self):
        return self.__name__


__all__ = [
    # Super-special typing primitives.
    'Any',
    'Callable',
    'ClassVar',
    'Generic',
    'Optional',
    'Tuple',
    'Type',
    'TypeVar',
    'Union',

    # ABCs (from collections.abc).
    'AbstractSet',  # collections.abc.Set.
    'GenericMeta',  # subclass of abc.ABCMeta and a metaclass
                    # for 'Generic' and ABCs below.
    'ByteString',
    'Container',
    'ContextManager',
    'Hashable',
    'ItemsView',
    'Iterable',
    'Iterator',
    'KeysView',
    'Mapping',
    'MappingView',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'Sequence',
    'Sized',
    'ValuesView',
    # The following are added depending on presence
    # of their non-generic counterparts in stdlib:
    'Awaitable',
    'AsyncIterator',
    'AsyncIterable',
    'Coroutine',
    'Collection',
    'AsyncGenerator',
    # AsyncContextManager

    # Structural checks, a.k.a. protocols.
    'Reversible',
    'SupportsAbs',
    'SupportsBytes',
    'SupportsComplex',
    'SupportsFloat',
    'SupportsInt',
    'SupportsRound',

    # Concrete collection types.
    'Counter',
    'Deque',
    'Dict',
    'DefaultDict',
    'List',
    'Set',
    'FrozenSet',
    'NamedTuple',  # Not really a type.
    'Generator',

    # One-off things.
    'AnyStr',
    'cast',
    'get_type_hints',
    'NewType',
    'no_type_check',
    'no_type_check_decorator',
    'overload',
    'Text',
    'TYPE_CHECKING',

    'ChainMap',
    'NoReturn',
]


def NewType(name, typ):
    return _MakeType(name)


def TypeVar(name, *types):
    return _MakeType(name)


def cast(typ, val):
    return val


def get_type_hints(obj, globals=None, locals=None):
    return {}


def overload(function):
    return function


def no_type_check(function):
    return function


def no_type_check_decorator(function):
    return function


TYPE_CHECKING = False


class Type(metaclass=_TypeMeta):
    pass


class Any(Type):
    pass


class Callable(Type):
    pass


class ClassVar(Type):
    pass


class Generic(Type):
    pass


class Optional(Type):
    pass


class Tuple(Type):
    pass


class Union(Type):
    pass


class AbstractSet(Type):
    pass


class GenericMeta(Type):
    pass


class ByteString(Type):
    pass


class Container(Type):
    pass


class ContextManager(Type):
    pass


class Hashable(Type):
    pass


class ItemsView(Type):
    pass


class Iterable(Type):
    pass


class Iterator(Type):
    pass


class KeysView(Type):
    pass


class Mapping(Type):
    pass


class MappingView(Type):
    pass


class MutableMapping(Type):
    pass


class MutableSequence(Type):
    pass


class MutableSet(Type):
    pass


class Sequence(Type):
    pass


class Sized(Type):
    pass


class ValuesView(Type):
    pass


class Awaitable(Type):
    pass


class AsyncIterator(Type):
    pass


class AsyncIterable(Type):
    pass


class Coroutine(Type):
    pass


class Collection(Type):
    pass


class AsyncGenerator(Type):
    pass


class AsyncContextManage(Type):
    pass


class Reversible(Type):
    pass


class SupportsAbs(Type):
    pass


class SupportsBytes(Type):
    pass


class SupportsComplex(Type):
    pass


class SupportsFloat(Type):
    pass


class SupportsInt(Type):
    pass


class SupportsRound(Type):
    pass


class Counter(Type):
    pass


class Deque(Type):
    pass


class Dict(Type):
    pass


class DefaultDict(Type):
    pass


class List(Type):
    pass


class Set(Type):
    pass


class FrozenSet(Type):
    pass


class NamedTuple(Type):
    pass


class Generator(Type):
    pass


class AnyStr(Type):
    pass


class Text(Type):
    pass


class ChainMap(Type):
    pass


class NoReturn(Type):
    pass
