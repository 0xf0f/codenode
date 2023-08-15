import sys

from setuptools import setup

if sys.version_info[1] < 9:
    # readme generation uses some ast features only available in 3.9+
    readme = (
        "A simple framework for code generation. "
        "View project info at https://github.com/0xf0f/codenode"
    )
else:
    from docs import generate_pypi_readme
    readme = generate_pypi_readme.run()

setup(
    name='0xf0f-codenode',
    version='1.0',
    packages=[
        'codenode',
        'codenode.nodes',
        'codenode_utilities',
    ],
    url='https://github.com/0xf0f/codenode',
    license='MIT',
    author='0xf0f',
    author_email='0xf0f.dev@gmail.com',
    description='a simple framework for code generation',
    long_description=readme,
    long_description_content_type='text/markdown',
)
