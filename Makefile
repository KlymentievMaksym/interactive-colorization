# Змінні
PYTHON = python
VENV = .venv
BIN = $(VENV)/bin

.PHONY: setup update clean

# 1. Повне налаштування проєкту
setup: $(VENV)/bin/activate

$(VENV)/bin/activate:
	@echo "--- Створення Virtual Environment ---"
	$(PYTHON) -m venv $(VENV)
	
	@echo "--- Оновлення pip та встановлення залежностей ---"
	$(BIN)/pip install --upgrade pip
	
	@echo "--- Встановлення Engine у режимі редагування ---"
	$(BIN)/pip install -e ./colorization-engine
	
	@echo "--- Встановлення залежностей UI ---"
	$(BIN)/pip install -r ./colorization-app/requirements.txt
	
	@echo "\nSETUP COMPLETE. Тепер виконай: source $(VENV)/bin/activate"

# 2. Оновлення сабмодулів
update:
	git submodule update --init --recursive
	git submodule foreach git pull origin main

# 3. Очищення тимчасових файлів
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +