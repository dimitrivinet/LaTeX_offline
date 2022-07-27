INSTALL_DIR?=${HOME}/.local/bin

.PHONY: all dry-run install

all: dry-run

dry-run:
	@echo "Would install to: ${INSTALL_DIR}"

install:
	@echo "Installing to ${INSTALL_DIR}"
	cp dist/latex_offline.py ${INSTALL_DIR}/latex_offline
	chmod +x ${INSTALL_DIR}/latex_offline
