# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pca9635** - MicroPython driver for PCA9635 16-channel I2C LED controller with PWM

This is a MicroPython library project generated from the [micropython_library_template](https://gitlab.pi.planetinnovation.com.au/degraves/template/micropython_library_template).

## Common Commands

### Primary Development Workflow
- `make tests` - Run unit tests via MicroPython Unix port (preferred method)
- `make checks` - Run all linting and static analysis checks (Black, Ruff, MyPy)
- `make help` - Show all available make targets

### Setup and Maintenance
- `make submodules` - Initialize git submodules (micropython-lib, mock-machine)
- `make doc-autobuild` - Start live documentation server on http://localhost:8000

### On-Demand Linting
Use `make checks` as the primary command for linting. This runs:
- Black code formatting
- Ruff linting with auto-fixes
- MyPy type checking
- Pre-commit hooks (trailing whitespace, EOF, YAML validation)

### Alternative Commands (use make targets instead)
- `pre-commit run --all-files` - Manual pre-commit execution (prefer `make checks`)
- `copier update --vcs-ref master --trust` - Update project from latest template

## Project Structure


### Single File Library
- `micropython_pca9635.py` - Main library implementation


### Supporting Files
- `test/test_micropython_pca9635.py` - Unit tests with MicroPython mocking
- `test/mocks/` - Mock implementations for MicroPython hardware interfaces
- `examples/` - Usage examples and demonstrations
- `doc/` - Sphinx documentation source
- `lib/` - Dependencies and submodules
- `manifest.py` - MicroPython package metadata for freezing/mip installation

## Testing Architecture

### Test Execution
Tests run in MicroPython Unix port environment with mocked hardware interfaces:
- **Docker**: Uses `gitlab.pi.planetinnovation.com.au:5004/degraves/ci/micropython-unix-unittest:latest`
- **Local**: Requires `MICROPYTHON_UNIX_UNITTEST` environment variable
- **Path**: `MICROPYPATH=test/mocks/micropython-mock-machine:lib/micropython-lib/python-stdlib/logging:lib:.frozen`

### Mocking
- Import `from mock_machine import register_as_machine` at test start
- Call `register_as_machine()` before importing library code
- Provides MicroPython `machine` module functionality for unit testing

## CI/CD Pipeline

### GitLab CI Stages
- **Quality**: Pre-commit checks, PI project compliance validation
- **Test**: Unit tests with JUnit XML reporting
- **Runner**: Uses `aws-525-degraves` tagged runners

### Required Setup
- Create `COMPLIANCE_CHECK` access token (Maintainer role, read_api scope)
- Add token to project CI/CD variables (masked, not protected)

## Code Style Configuration

### Tools
- **Black**: 99 character line length, fast mode
- **Ruff**: Python 3.10 target, MicroPython `const` builtin support
- **MyPy**: MicroPython stubs integration, library exclusions

### Standards
- PEP8 compliant module naming (enforced by template)
- 99 character line limit (matches MicroPython project standards)
- Type hints supported via micropython-stm32-stubs
- logging preferred over print

## Library Distribution

### MicroPython Package Manager (mip)
- `manifest.py` describes package metadata and dependencies
- Add runtime dependencies with `require("package_name")`

### Freezing
- Library can be frozen into MicroPython firmware builds
- Use manifest.py to specify which files to include
