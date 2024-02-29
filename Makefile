build:
	python3 -m build

install:
	pip install dist/boto_formatter-*.tar.gz

test:
	python3 -m unittest discover -s tests/unittests -p "*.py"

clean:
	pip uninstall boto_formatter -y
	rm -r ./dist
