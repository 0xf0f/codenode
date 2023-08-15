import shutil
import subprocess
import pathlib
import atexit

cd = pathlib.Path(__file__).absolute().parent


def prepare_readme():
    from docs import generate_pypi_readme
    old_readme_path = cd.parent / 'README.md'
    new_readme_path = cd.parent / 'README_original.md'
    old_readme_path.rename(new_readme_path)

    def cleanup():
        old_readme_path.unlink(missing_ok=True)
        new_readme_path.rename(old_readme_path)

    atexit.register(cleanup)

    with open(old_readme_path, 'w') as file:
        file.write(generate_pypi_readme.run())


def run():
    print('cd', cd)
    prepare_readme()

    dist_folder = cd.parent / 'dist'
    build_folder = cd.parent / 'build'
    shutil.rmtree(dist_folder, ignore_errors=True)
    shutil.rmtree(build_folder, ignore_errors=True)

    for command in (
            'python setup.py sdist bdist_wheel',
            'twine upload dist/* '
            '--skip-existing --config-file .pypirc',
    ):
        print('running', command)
        subprocess.run(command, cwd=cd.parent, shell=True)


if __name__ == '__main__':
    run()
