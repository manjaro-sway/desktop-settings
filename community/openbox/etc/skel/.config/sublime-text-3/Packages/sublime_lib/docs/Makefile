# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SOURCEDIR     = source
BUILDDIR      = .

.PHONY: clean

html:
	sphinx-build -M html "$(SOURCEDIR)" "$(BUILDDIR)"

clean:
	rm -rf doctrees html
