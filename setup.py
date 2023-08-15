from setuptools import setup

with open('README.md') as file:
    readme = file.read()

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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
