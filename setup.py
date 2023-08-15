import sys

from setuptools import setup, find_packages

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
    name='codenode',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/0xf0f/codenode',
    license='MIT',
    author='0xf0f',
    author_email='0x0meta@gmail.com',
    description='a simple framework for code generation',
    long_description=readme,
    long_description_content_type='text/markdown',
)
