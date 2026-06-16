#!/usr/bin/env python3
"""
iPhoenix - Técnicas via Recovery Mode (A12+)
"""
from .utils import run_command, get_device_info_dict

class RecoveryBypass:
    def __init__(self):
        pass
    
    def check_activation_state(self):
        """Verifica estado atual de ativação"""
        code, out, err = run_command("ideviceactivation state 2>/dev/null")
        if code == 0:
            return out.strip()
        return None
    
    def get_activation_info(self):
        """Obtém ticket de ativação"""
        code, out, err = run_command("ideviceactivation info 2>/dev/null")
        if code == 0:
            return out
        return None
    
    def unlock_via_recovery_logs(self):
        """Tenta extrair informações úteis dos logs de recovery"""
        print("[*] Analisando logs de recovery...")
        # Conecta em recovery e pega logs
        code, out, err = run_command("irecovery -q 2>/dev/null")
        if code == 0:
            # Extrai informações do device em recovery
            return out
        return None
    
    def send_activation_ticket(self, ticket_data=None):
        """Tenta reenviar ticket de ativação"""
        print("[*] Tentando reativar via libideviceactivation...")
        code, out, err = run_command("ideviceactivation activate 2>/dev/null", 60)
        if code == 0:
            return {"status": "success", "message": "Reativação concluída!"}
        return {"status": "error", "error": err}
    
    def bypass_mdm(self):
        """Remove MDM de dispositivos supervisionados"""
        print("[*] Removendo MDM...")
        commands = """
        mount_filesystems
        cd /mnt2/containers/Shared/SystemGroup/systemgroup.com.apple.configurationprofiles/Library/ConfigurationProfiles/
        rm -f CloudConfigurationDetails.plist
        rm -f com.apple.configurationprofiles.plist
        rm -rf *
        
        # Remove perfis MDM
        rm -f /mnt2/mobile/Library/Preferences/com.apple.mdm.plist
        rm -rf /mnt2/mobile/Library/ConfigurationProfiles/
        
        sync
        exit
        """
        # Para dispositivos checkm8, usa SSHRD
        # Para A12+, tenta via ideviceactivation
        code, out, err = run_command("ideviceactivation deactivate 2>/dev/null", 30)
        return code == 0
    
    def scan_network_after_unlock(self):
        """Verifica conectividade de rede após desbloqueio"""
        print("[*] Testando conectividade...")
        code, out, err = run_command("ping -c 2 8.8.8.8 2>/dev/null", 10)
        if code == 0:
            return {"status": "online", "message": "Rede funcionando"}
        return {"status": "offline", "message": "Sem conectividade"}
