import codenode
import pathlib
import string

from docs.generate_readme import reference, reference_contents

cd = pathlib.Path(__file__).absolute().parent
template_path = cd / 'readme_template.md'
# output_path = cd.parent / 'README_pypi.md'


def run():
    with open(template_path) as file:
        template = string.Template(file.read())

    output = template.safe_substitute(
        {
            'reference_contents': codenode.dumps(reference_contents(), debug=True),
            'reference': codenode.dumps(reference(), debug=True),
            'codenode_utilities_link': (
                'https://github.com/0xf0f/codenode/'
                'blob/main/codenode_utilities/README.md'
            )
        }
    )
    # with open(output_path, 'w') as file:
    #     file.write(output)

    return output


if __name__ == '__main__':
    run()
