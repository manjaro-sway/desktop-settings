from sphinx.transforms import SphinxTransform
from sphinx.util.inspect import Signature

import inspect


__all__ = ['strip_annotations']


def strip_annotations(
    app,
    what: str,
    name: str,
    obj,
    options,
    signature,
    return_annotation
):
    if what not in { 'function', 'method', 'class' }:
        return

    new_signature = Signature(obj)
    new_signature.signature = new_signature.signature.replace(
        return_annotation=inspect.Signature.empty,
        parameters=[
            param.replace(annotation=inspect.Parameter.empty)
            for param in new_signature.signature.parameters.values()
            if param.name != 'self'
        ],
    )

    return new_signature.format_args(), None
