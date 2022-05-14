from sphinx.transforms import SphinxTransform
import sphinx.addnodes as SphinxNodes
from docutils.nodes import Text, emphasis, inline


def patch_node(node, text=None, children=None, *, constructor=None):
    if constructor is None:
        constructor = node.__class__

    if text is None:
        text = node.text

    if children is None:
        children = node.children

    return constructor(
        node.source,
        text,
        *children,
        **node.attributes,
    )


def function_transformer():
    def xf(name_node, parameters_node):
        return (
            patch_node(name_node, name_node.astext().strip('_'), ()),
            patch_node(parameters_node, '', [
                SphinxNodes.desc_parameter('', 'self'),
                *parameters_node.children,
            ])
        )

    return xf


def unary_op_transformer(op):
    def xf(name_node, parameters_node):
        return (
            patch_node(name_node, op, ()),
            emphasis('', 'self'),
        )


def binary_op_transformer(op):
    def xf(name_node, parameters_node):
        return inline(
            '', '',
            emphasis('', 'self'),
            Text(' '),
            patch_node(name_node, op, ()),
            Text(' '),
            emphasis('', parameters_node.children[0].astext())
        )

    return xf


def brackets(parameters_node):
    return [
        emphasis('', 'self'),
        SphinxNodes.desc_name('', '', Text('[')),
        emphasis('', parameters_node.children[0].astext()),
        SphinxNodes.desc_name('', '', Text(']')),
    ]


SPECIAL_METHODS = {
    '__getitem__': lambda name_node, parameters_node: inline(
        '', '', *brackets(parameters_node)
    ),
    '__setitem__': lambda name_node, parameters_node: inline(
        '', '',
        *brackets(parameters_node),
        Text(' '),
        SphinxNodes.desc_name('', '', Text('=')),
        Text(' '),
        emphasis('', (
            (parameters_node.children[1].astext())
            if len(parameters_node.children) > 1 else ''
        )),
    ),
    '__delitem__': lambda name_node, parameters_node: inline(
        '', '',
        SphinxNodes.desc_name('', '', Text('del')),
        Text(' '),
        *brackets(parameters_node),
    ),
    '__contains__': lambda name_node, parameters_node: inline(
        '', '',
        emphasis('', parameters_node.children[0].astext()),
        Text(' '),
        SphinxNodes.desc_name('', '', Text('in')),
        Text(' '),
        emphasis('', 'self'),
    ),

    '__lt__': binary_op_transformer('<'),
    '__le__': binary_op_transformer('<='),
    '__eq__': binary_op_transformer('=='),
    '__ne__': binary_op_transformer('!='),
    '__gt__': binary_op_transformer('>'),
    '__ge__': binary_op_transformer('>='),

    '__hash__': function_transformer(),
    '__len__': function_transformer(),
    '__str__': function_transformer(),
    '__repr__': function_transformer(),

    '__add__': binary_op_transformer('+'),
    '__sub__': binary_op_transformer('-'),
    '__mul__': binary_op_transformer('*'),
    '__matmul__': binary_op_transformer('@'),
    '__truediv__': binary_op_transformer('/'),
    '__floordiv__': binary_op_transformer('//'),
    '__mod__': binary_op_transformer('%'),
    '__divmod__': function_transformer(),
    '__pow__': binary_op_transformer('**'),
    '__lshift__': binary_op_transformer('<<'),
    '__rshift__': binary_op_transformer('>>'),
    '__and__': binary_op_transformer('&'),
    '__xor__': binary_op_transformer('^'),
    '__or__': binary_op_transformer('|'),

    '__neg__': unary_op_transformer('-'),
    '__pos__': unary_op_transformer('+'),
    '__abs__': function_transformer(),
    '__invert__': unary_op_transformer('~'),
}


class PrettifySpecialMethods(SphinxTransform):
    default_priority = 800

    def apply(self):
        methods = (
            sig for sig in self.document.traverse(SphinxNodes.desc_signature)
            if 'class' in sig
        )

        for ref in methods:
            name_node = ref.next_node(SphinxNodes.desc_name)
            method_name = name_node.astext()

            if method_name in SPECIAL_METHODS:
                parameters_node = ref.next_node(SphinxNodes.desc_parameterlist)

                name_node.replace_self(SPECIAL_METHODS[method_name](name_node, parameters_node))
                parameters_node.replace_self(())


def show_special_methods(app, what, name, obj, skip, options):
    if what == 'class' and name in SPECIAL_METHODS and getattr(obj, '__doc__', None):
        return False
