from codecs import lookup

__all__ = ['from_sublime', 'to_sublime']


def from_sublime(name: str) -> str:
    """Translate `name` from a Sublime encoding name to a standard Python encoding name.

    :raise ValueError: if `name` is not a Sublime encoding.

    .. code-block:: python

       >>> from_sublime("Western (Windows 1252)")
       "cp1252"

    .. versionchanged:: 1.3
        Raise :exc:`ValueError` if `name` is not a Sublime encoding.
    """

    try:
        return SUBLIME_TO_STANDARD[name]
    except KeyError:
        raise ValueError("Unknown Sublime encoding {!r}.".format(name)) from None


def to_sublime(name: str) -> str:
    """Translate `name` from a standard Python encoding name to a Sublime encoding name.

    :raise ValueError: if `name` is not a Python encoding.

    .. code-block:: python

       >>> to_sublime("cp1252")
       "Western (Windows 1252)"

    .. versionchanged:: 1.3
        Raise :exc:`ValueError` if `name` is not a Python encoding.
    """
    try:
        return STANDARD_TO_SUBLIME[lookup(name).name]
    except LookupError:
        raise ValueError("Unknown Python encoding {!r}.".format(name)) from None


SUBLIME_TO_STANDARD = {  # noqa: E121
    "UTF-8": "utf-8",
    "UTF-8 with BOM": "utf-8-sig",
    "UTF-16 LE": "utf-16-le",
    "UTF-16 LE with BOM": "utf-16",
    "UTF-16 BE": "utf-16-be",
    "UTF-16 BE with BOM": "utf-16",
    "Western (Windows 1252)": "cp1252",
    "Western (ISO 8859-1)": "iso8859-1",
    "Western (ISO 8859-3)": "iso8859-3",
    "Western (ISO 8859-15)": "iso8859-15",
    "Western (Mac Roman)": "mac-roman",
    "DOS (CP 437)": "cp437",
    "Arabic (Windows 1256)": "cp1256",
    "Arabic (ISO 8859-6)": "iso8859-6",
    "Baltic (Windows 1257)": "cp1257",
    "Baltic (ISO 8859-4)": "iso8859-4",
    "Celtic (ISO 8859-14)": "iso8859-14",
    "Central European (Windows 1250)": "cp1250",
    "Central European (ISO 8859-2)": "iso8859-2",
    "Cyrillic (Windows 1251)": "cp1251",
    "Cyrillic (Windows 866)": "cp866",
    "Cyrillic (ISO 8859-5)": "iso8859-5",
    "Cyrillic (KOI8-R)": "koi8-r",
    "Cyrillic (KOI8-U)": "koi8-u",
    "Estonian (ISO 8859-13)": "iso8859-13",
    "Greek (Windows 1253)": "cp1253",
    "Greek (ISO 8859-7)": "iso8859-7",
    "Hebrew (Windows 1255)": "cp1255",
    "Hebrew (ISO 8859-8)": "iso8859-8",
    "Nordic (ISO 8859-10)": "iso8859-10",
    "Romanian (ISO 8859-16)": "iso8859-16",
    "Turkish (Windows 1254)": "cp1254",
    "Turkish (ISO 8859-9)": "iso8859-9",
    "Vietnamese (Windows 1258)": "cp1258",
}


STANDARD_TO_SUBLIME = {  # noqa: E121
    standard_name: sublime_name
    for sublime_name, standard_name in SUBLIME_TO_STANDARD.items()
}
STANDARD_TO_SUBLIME['utf-16'] = 'UTF-16 LE with BOM'
