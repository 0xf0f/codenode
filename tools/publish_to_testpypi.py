import shutil
import subprocess
import pathlib

cd = pathlib.Path(__file__).absolute().parent


def run():
    print('cd', cd)

    dist_folder = cd.parent / 'dist'
    build_folder = cd.parent / 'build'
    shutil.rmtree(dist_folder, ignore_errors=True)
    shutil.rmtree(build_folder, ignore_errors=True)

    for command in (
            'python setup.py sdist bdist_wheel',
            'twine upload --repository testpypi dist/* '
            '--skip-existing --config-file .pypirc',
    ):
        print('running', command)
        subprocess.run(command, cwd=cd.parent, shell=True)


if __name__ == '__main__':
    run()
