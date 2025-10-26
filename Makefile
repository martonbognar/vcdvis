.PHONY: help
help:
	@echo "Available commands:"
	@echo "    help          - Show this help message"
	@echo "    build         - Build the package"
	@echo "    clean         - Remove build artifacts"
	@echo "    test-install  - Test that package is installable"

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
