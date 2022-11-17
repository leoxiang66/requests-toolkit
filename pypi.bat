# remember to modify setup.py (version and requirement)

rmdir  dist/
python setup.py sdist bdist_wheel
twine upload dist/*

