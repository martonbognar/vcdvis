.PHONY: help
help:
	@echo "Available commands:"
	@echo "    help          - Show this help message"
	@echo "    setup         - Set up development environment (PYTHON_VERSION=$(PYTHON_VERSION))"
	@echo "    test          - Run tests"
	@echo "    build         - Build the package"
	@echo "    clean         - Remove build artifacts"
	@echo "    test-install  - Test that package is installable"

##############
# Develpment #
##############

PYTHON_VERSION ?= 3.9

.PHONY: setup
setup:
	uv python install python$(PYTHON_VERSION)
	uv sync --dev

.PHONY: test
test:
	uv run --python python$(PYTHON_VERSION) pytest -v

#############
# Packaging #
#############

.PHONY: build
build:
	python -m build

.PHONY: test-install
test-install:
	@test -f dist/vcdvis*.whl || (echo "Error: dist/vcdvis*.whl not found" && exit 1)
	@rm -rf test-venv
	@python -m venv test-venv
	@./test-venv/bin/python -m pip install dist/vcdvis*.whl
	@./test-venv/bin/vcdvis --help
	$(MAKE) clean
	@echo "Build ok."

.PHONY: clean
clean:
	rm -rf dist/ build/ *.egg-info/ test-venv
