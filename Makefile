VENV = .venv
ifeq ($(OS), Windows_NT)
    PYTHON = python
    BIN = $(VENV)/Scripts
    PIP_LOCAL = $(BIN)/python.exe -m pip
    PYTHON_LOCAL = $(BIN)/python.exe
    RM = powershell -Command "Remove-Item -Recurse -Force"
else
    PYTHON = python3
    BIN = $(VENV)/bin
    PIP_LOCAL = $(BIN)/pip
    PYTHON_LOCAL = $(BIN)/python3
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
    # My code
	$(PIP_LOCAL) install -e ./colorization-engine
	$(PIP_LOCAL) install -e ./colorization-app
	$(PIP_LOCAL) install -r ./data/requirements.txt

    # DDcolor code
# 	$(PIP_LOCAL) install -r ./colorization-engine/src/colorization_engine/models/util_models/DDColor/requirements.txt
# 	$(PIP_LOCAL) install -r ./colorization-engine/src/colorization_engine/models/util_models/DDColor/requirements.train.txt
# 	$(PYTHON_LOCAL) ./colorization-engine/src/colorization_engine/models/util_models/DDColor/setup.py develop
	$(PIP_LOCAL) install --no-deps --no-build-isolation -e ./colorization-engine/src/colorization_engine/models/util_models/DDColor
update:
	git submodule update --init --recursive --remote --merge

clean:
	$(RM) $(VENV)