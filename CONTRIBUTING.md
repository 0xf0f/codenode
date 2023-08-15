## Guidelines
- Create a new branch in a fork to implement changes then open 
a pull request to merge them.
- Keep code straightforward, clean and readable.
- Document everything public facing with docstrings.
- Provide comments for things that might not be clear.
- Add type annotations where applicable.
- Adjust tests and docs as necessary.
- PEP8 compliance is ideal.

## Running tests
- Run `python -m tools.run_tests` to run tests.

## Generating docs
- Run `python -m tools.generate_readmes` to create README files.

## Pushing to PyPI
- Create and activate a venv, then install `twine` inside it
- Create a .pypirc file in the root of the project
- Fill the .pypirc file below using appropriate PyPI API tokens:
  ```yaml
  [pypi]
  username = __token__
  password = ...
  
  [testpypi]
  username = __token__
  password = ...
  ```
- Run `python -m tools.publish_to_testpypi` to publish to TestPyPI
- Run `python -m tools.publish_to_pypi` to publish to PyPI
