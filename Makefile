# PI Background IP
# Copyright (c) 2026, Planet Innovation Pty Ltd
# 436 Elgar Rd, Box Hill, 3128, VIC, Australia
# Phone: +61 3 9945 7510
#
# The copyright to the computer program(s) herein is the property of
# Planet Innovation, Australia.
# The program(s) may be used and/or copied only with the written permission
# of Planet Innovation or in accordance with the terms and conditions
# stipulated in the agreement/contract under which the program(s) have been
# supplied.

default: help

.PHONY : help
help:
	@echo "micropython_pca9635 Makefile"
	@echo "Please use 'make target' where target is one of:"
	@grep -h ':\s\+##' Makefile | column -t -s# | awk -F ":" '{ print "  \033[36m" $$1 "\033[0m" $$2 }'

# Run unit tests job
# This job will automatically be run inside a docker container (if not already) which includes the unittest library
# and its direct dependencies.
# Any additional project test dependencies should be added to the `export MICROPYPATH` line below instead/alongside the `lib` entry.
.PHONY: tests
tests:  ## Execute unit tests (inside the Unix port).
tests: submodules
	@echo "-----------------------------------"
	@echo "Execute unit tests..."
	@CMD="micropython -m unittest_junit discover -s test -p test_micropython_pca9635.py"; \
	export MICROPYPATH=test/mocks/micropython-mock-machine:lib/micropython-lib/python-stdlib/logging:lib:.frozen; \
	if [ -n "$${MICROPYTHON_UNIX_UNITTEST}" ]; then \
	  $${CMD}; \
	else \
	  docker run -t --rm -e MICROPYPATH="$${MICROPYPATH}" -v $$(pwd):/code -w /code \
	  gitlab.pi.planetinnovation.com.au:5004/degraves/ci/micropython-unix-unittest:latest \
	  $${CMD}; \
	fi

.PHONY: checks
checks:  ## Run static analysis
checks: submodules
	pre-commit run --all-files

.PHONY: init
init:  ## Initialise the repository and submodules
	git init
	git symbolic-ref HEAD refs/heads/main
	@if [ ! -d lib/micropython-lib/.git ]; then \
		git submodule add https://github.com/micropython/micropython-lib.git lib/micropython-lib; \
	else \
		echo "Submodule lib/micropython-lib already exists, skipping..."; \
	fi
	@if [ ! -d test/mocks/micropython-mock-machine/.git ]; then \
		git submodule add https://gitlab.pi.planetinnovation.com.au/degraves/library/micropython-mock-machine.git test/mocks/micropython-mock-machine; \
	else \
		echo "Submodule test/mocks/micropython-mock-machine already exists, skipping..."; \
	fi
	pip install -U micropython-stm32-stubs --no-user --target ./tools/typings
	pre-commit install
	pre-commit run --all-files
	git add --all

.PHONY: doc-autobuild
doc-autobuild: ## Autobuild the docs so a browser can monitor changes
	docker run --rm -v $$(pwd)/doc:/doc -w /doc -p 8000:8000 minidocks/sphinx-doc sphinx-autobuild --host 0.0.0.0 . _build/

# Use submodule README.md files as a proxy for submodule init
# By adding a stem rule that will match all submodule README.md files
%/README.md:
	git submodule update --init --recursive $*

# Add more dependencies here. As more submodules are added, add a dependency on their README.md
.PHONY: submodules
submodules: ## Initalise submodules
submodules: lib/micropython-lib/README.md test/mocks/micropython-mock-machine/README.md
