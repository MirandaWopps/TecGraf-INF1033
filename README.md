# Project Name

This is a template repository for Python projects that use uv for their dependency management.


## Getting started with your project

### 1. Change the project name

 - Rename src/project_name file
 - rename [project].name in pyproject.toml

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run tests

```bash
make test
```

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
