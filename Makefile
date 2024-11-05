# Makefile
VENV_DIR = .venv

# Target to set up environment
setup: $(VENV_DIR)/bin/activate

# Create the virtual environment
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt  # or `poetry install` if using pyproject.toml

# Shortcut to activate the environment
activate:
	@echo "Run 'source $(VENV_DIR)/bin/activate' to activate the virtual environment."

# Clean the environment
clean:
	rm -rf $(VENV_DIR)

# Run tests
test: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/python -m unittest discover -s tests