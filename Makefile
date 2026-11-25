SHELL := /bin/bash

.PHONY: setup lint validate manifest

setup:
	python -m pip install --upgrade pip
	pip install pre-commit
	pre-commit install

lint:
	pre-commit run --all-files

validate:
	python scripts/validate_skills.py

manifest:
	python scripts/generate_skill_manifest.py
