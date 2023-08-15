import codenode
import pathlib
import string

from docs.generation_utilities import (
    functions, classes, variables, AttributeDocumentation
)

cd = pathlib.Path(__file__).absolute().parent
template_path = cd / 'readme_template.md'
output_path = cd.parent / 'README.md'

contents = (
    *functions(
        (
            'codenode.dump',
            'codenode.dumps',
            'codenode.line',
        )
    ),

    *variables(
        (
            'codenode.indent',
            'codenode.dedent',
            'codenode.newline',
            'codenode.indentation',
        )
    ),

    *functions(
        (
            'codenode.lines',
            'codenode.empty_lines',
            'codenode.indented',
        )
    ),

    AttributeDocumentation('codenode.default_writer_type'),

    *classes(
        (
            'codenode.writer.Writer',
            'codenode.writer.WriterStack',

            'codenode.nodes.newline.Newline',

            'codenode.nodes.depth_change.DepthChange',
            'codenode.nodes.depth_change.RelativeDepthChange',
            'codenode.nodes.depth_change.AbsoluteDepthChange',

            'codenode.nodes.indentation.Indentation',
            'codenode.nodes.indentation.RelativeIndentation',
            'codenode.nodes.indentation.AbsoluteIndentation',
            'codenode.nodes.indentation.CurrentIndentation',

            # 'codenode.debug.DebugIterator',
        )
    ),

    *functions(
        (
            # 'codenode.debug.print_writer_stack',
            'codenode.debug.debug_patch',
        )
    ),
)


def reference_contents():
    for item in contents:
        yield codenode.line(f'- [{item.path}](#{item.get_link()})')


def reference():
    for item in contents:
        yield codenode.line('---')
        yield item


if __name__ == '__main__':
    with open(template_path) as file:
        template = string.Template(file.read())

    with open(output_path, 'w') as file:
        file.write(
            template.safe_substitute(
                {
                    'reference_contents': codenode.dumps(reference_contents(), debug=True),
                    'reference': codenode.dumps(reference(), debug=True),
                    'codenode_utilities_link': 'codenode_utilities/README.md'
                }
            )
        )
