#!/usr/bin/env python3
"""
iPhoenix - Detecção de Dispositivo
"""
import subprocess
import time
from .utils import get_device_info_dict, run_command

class DeviceDetector:
    def __init__(self):
        self.device = None
        self.connected = False
    
    def wait_for_device(self, timeout=30):
        """Aguarda dispositivo conectar via USB"""
        print(f"[*] Aguardando dispositivo conectar (timeout: {timeout}s)...")
        for i in range(timeout):
            code, out, _ = run_command("idevice_id -l 2>/dev/null")
            if code == 0 and out.strip():
                self.connected = True
                self.device = get_device_info_dict()
                return self.device
            time.sleep(1)
        return None
    
    def wait_for_dfu(self, timeout=60):
        """Aguarda dispositivo em DFU mode"""
        print("[*] Aguardando modo DFU...")
        for i in range(timeout):
            code, out, _ = run_command("irecovery -q 2>/dev/null | grep -i 'CPID'")
            if code == 0 and out.strip():
                return True
            time.sleep(1)
        return False
    
    def get_all_info(self):
        """Retorna todas as info do device conectado"""
        if not self.device:
            self.device = get_device_info_dict()
        return self.device
    
    def refresh(self):
        """Atualiza informações do dispositivo"""
        self.device = get_device_info_dict()
        return self.device
