#!/bin/bash
# iPhoenix - Build Script
# Gera executável para Linux, Windows e macOS

echo "=== iPhoenix Build Script ==="
echo ""

# Verifica Python
if ! command -v python3 &>/dev/null; then
    echo "[!] Python3 não encontrado. Instale primeiro."
    exit 1
fi

# Instala pyinstaller
echo "[*] Instalando PyInstaller..."
pip3 install pyinstaller 2>/dev/null | tail -1

# Cria diretório de saída
mkdir -p dist

# Detecta SO
OS=$(uname -s)
case "$OS" in
    Linux*)   TARGET="Linux" ;;
    Darwin*)  TARGET="macOS" ;;
    CYGWIN*|MINGW*|MSYS*) TARGET="Windows" ;;
    *)        TARGET="Unknown" ;;
esac

echo "[*] Build para: $TARGET"

# Gera executável
echo "[*] Compilando iPhoenix..."
pyinstaller --onefile \
    --windowed \
    --name "iPhoenix" \
    --icon assets/icon.ico \
    --add-data "core:core" \
    --hidden-import tkinter \
    --hidden-import PIL \
    --hidden-import usb \
    iphoenix.py 2>&1 | tail -5

# Verifica resultado
if [ -f "dist/iPhoenix" ] || [ -f "dist/iPhoenix.exe" ]; then
    echo ""
    echo "[✓] Build concluído!"
    echo "    Executável: dist/iPhoenix$([ "$TARGET" = "Windows" ] && echo '.exe')"
else
    echo ""
    echo "[!] Build falhou. Verifique erros acima."
    exit 1
fi
