# Makefile for Sphinx documentation

SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: clean doc

clean:
	rm -rf $(BUILDDIR)/*

doc: clean
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)

purge-server:
	fuser -k 8000/tcp >/dev/null 2>&1 || true

doc-serve: purge-server
	python -m http.server --directory $(BUILDDIR) > /tmp/training_ros.log 2>&1 & (sleep 2; python -m webbrowser "http://0.0.0.0:8000/")

doc-test: doc doc-serve
