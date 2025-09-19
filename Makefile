.PHONY: help
help:
	@echo "Available commands:"
	@echo "    help   - Show this help message"
	@echo "    build  - Build the package"
	@echo "    clean  - Remove build artifacts"

.PHONY: build
build:
	python -m build

.PHONY: clean
clean:
	rm -rf dist/ build/ *.egg-info/
