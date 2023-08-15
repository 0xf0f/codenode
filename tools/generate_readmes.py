import subprocess

import pathlib

cd = pathlib.Path(__file__).absolute().parent.parent


def run():
    print('cd', cd)

    for command in (
        'python -m docs.generate_readme',
        'python -m docs.generate_codenode_utilities_readme',
    ):
        print('running', command)
        subprocess.run(command, cwd=cd, shell=True)


if __name__ == '__main__':
    run()
