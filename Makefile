VENV = .venv
ifeq ($(OS), Windows_NT)
    PYTHON = python
    BIN = $(VENV)/Scripts
    PIP_LOCAL = $(BIN)/python.exe -m pip
    RM = powershell -Command "Remove-Item -Recurse -Force"
else
    PYTHON = python3
    BIN = $(VENV)/bin
    PIP_LOCAL = $(BIN)/pip
    RM = rm -rf
endif
ACTIVATE = $(BIN)/activate

.PHONY: init setup install update clean

init: update setup

setup: $(ACTIVATE) install

$(ACTIVATE):
	$(PYTHON) -m venv $(VENV)
	$(PIP_LOCAL) install --upgrade pip

install: $(ACTIVATE)
	$(PIP_LOCAL) install -e ./colorization-engine
	$(PIP_LOCAL) install -r ./colorization-app/requirements.txt

update:
	git submodule update --init --recursive
	git submodule foreach "git checkout main && git pull origin main && git fetch --tags"
# 	git submodule foreach git pull origin main

clean:
	$(RM) $(VENV)