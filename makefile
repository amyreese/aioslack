setup:
	python3 -m pip install -U black mypy pylint twine
	python3 -m pip install -Ur requirements.txt

release: lint test clean
	python3 setup.py sdist
	python3 -m twine upload dist/*

black:
	python3 -m black .

lint:
	python3 -m black --check aioslack tests
	python3 -m pylint --rcfile .pylint aioslack setup.py
	-python3 -m mypy --ignore-missing-imports --python-version 3.6 .

test:
	python3 -m unittest tests

clean:
	rm -rf build dist README MANIFEST aioslack.egg-info .mypy_cache
