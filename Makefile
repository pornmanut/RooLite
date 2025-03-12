# Tic-tac-toe Game Makefile

.PHONY: run install clean

run:
	chmod +x run.sh
	./run.sh

install:
	cd backend && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
	cd frontend && npm install

clean:
	rm -rf backend/venv backend/__pycache__ backend/.pytest_cache
	rm -rf frontend/node_modules frontend/build frontend/dist

help:
	@echo "Available commands:"
	@echo "  make run       - Start both servers (recommended)"
	@echo "  make install   - Install all dependencies"
	@echo "  make clean     - Clean build artifacts"
