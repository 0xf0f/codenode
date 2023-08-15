import codenode
import pathlib
import string

from docs.generation_utilities import functions, ClassDocumentation

cd = pathlib.Path(__file__).absolute().parent
template_path = cd / 'codenode_utilities_readme_template.md'
output_path = cd.parent / 'codenode_utilities' / 'README.md'

contents = (
    ClassDocumentation('codenode_utilities.PartitionedNode'),

    *functions(
        (
            'codenode_utilities.joined',
            'codenode_utilities.node_transformer',
            'codenode_utilities.prefixer',
            'codenode_utilities.suffixer',
            'codenode_utilities.auto_coerce_patch',
        )
    )
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
                }
            )
        )
