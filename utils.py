#!/usr/bin/env python3
"""
iPhoenix - Utilitários
Pentest iOS Activation Lock via USB
"""
import subprocess
import platform
import os
import json
import sys

SYSTEM = platform.system()

def run_command(cmd, timeout=120):
    """Executa comando shell e retorna output"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)

def check_dependencies():
    """Verifica dependências instaladas"""
    deps = {
        "libimobiledevice": "ideviceinfo",
        "usbmuxd": "usbmuxd",
        "irecovery": "irecovery",
    }
    missing = []
    for name, cmd in deps.items():
        code, _, _ = run_command(f"which {cmd} 2>/dev/null || command -v {cmd} 2>/dev/null")
        if code != 0:
            missing.append(name)
    return missing

def install_dependencies():
    """Instala dependências no Linux"""
    sys_type = SYSTEM.lower()
    if "linux" in sys_type:
        print("[*] Instalando dependências Linux...")
        run_command("sudo apt-get update -y", 60)
        run_command(
            "sudo apt-get install -y libimobiledevice-dev libimobiledevice-utils "
            "usbmuxd libusb-1.0-0-dev python3-tk python3-pip git curl build-essential", 120
        )
        # libideviceactivation
        run_command(
            "cd /tmp && git clone https://github.com/libimobiledevice/libideviceactivation.git "
            "&& cd libideviceactivation && ./autogen.sh && make && sudo make install", 120
        )
    elif "darwin" in sys_type:
        print("[*] Instalando dependências macOS...")
        run_command("brew install libimobiledevice usbmuxd ideviceactivation", 120)
    elif "windows" in sys_type:
        print("[*] Windows: Instale libimobiledevice via MSYS2 ou baixe os binários")
        print("[*] https://github.com/libimobiledevice/libimobiledevice/releases")
    return check_dependencies()

def get_device_info():
    """Obtém informações do dispositivo via USB"""
    code, out, err = run_command("ideviceinfo 2>/dev/null")
    if code != 0:
        # Tenta com idevice_id primeiro
        code2, out2, _ = run_command("idevice_id -l 2>/dev/null")
        if code2 == 0 and out2.strip():
            code, out, err = run_command(f"ideviceinfo -u {out2.strip()} 2>/dev/null")
        else:
            return None
    
    info = {}
    for line in out.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

def get_device_info_dict():
    """Retorna dict estruturado com info do device"""
    raw = get_device_info()
    if not raw:
        return None
    return {
        "model": raw.get("ProductType", "Desconhecido"),
        "ios_version": raw.get("ProductVersion", "Desconhecido"),
        "udid": raw.get("UniqueDeviceID", raw.get("SerialNumber", "Desconhecido")),
        "activation_state": raw.get("ActivationState", "Desconhecido"),
        "name": raw.get("DeviceName", "iPhone"),
        "ecid": raw.get("Ecid", ""),
        "iboot_version": raw.get("iBootVersion", ""),
    }

def get_ios_major(version):
    """Extrai major version do iOS"""
    try:
        return int(version.split(".")[0])
    except:
        return 0

def is_checkm8_compatible(model):
    """Verifica se o modelo é compatível com checkm8 (A7-A11)"""
    a7_a11_models = [
        "iPhone6", "iPhone7", "iPhone8", "iPhone9", "iPhone10",
        "iPad4", "iPad5", "iPad6", "iPad7",
        "iPod7", "iPod9"
    ]
    for m in a7_a11_models:
        if model.startswith(m):
            return True
    return False
