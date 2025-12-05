# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

#.PHONY: help Makefile
.PHONY: docs docs-clean

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

docs:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"
	touch "$(BUILDDIR)/.nojekyll"

docs-clean:
# CNAME이나 추가 파일 보존하려면 제외 패턴 추가
	find $(BUILDDIR) -mindepth 1 ! -name 'CNAME' ! -name '.nojekyll' -exec rm -rf {} +

