#!/usr/bin/env python3
"""
iPhoenix - MDM Bypass específico
"""
from .utils import run_command

class MDMBypass:
    def __init__(self, device_info):
        self.info = device_info
    
    def remove_dep_profile(self):
        """Remove perfil DEP"""
        print("[*] Removendo perfil DEP...")
        commands = """
        mount_filesystems
        
        # Remove perfis de configuração
        rm -f /mnt2/containers/Shared/SystemGroup/systemgroup.com.apple.configurationprofiles/Library/ConfigurationProfiles/*
        
        # Limpa dados de MDM
        rm -rf /mnt2/mobile/Library/ConfigurationProfiles/
        rm -f /mnt2/mobile/Library/Preferences/com.apple.mdm.plist
        
        # Remove cache de ativação
        rm -f /mnt2/mobile/Library/Preferences/com.apple.activation.plist
        
        sync
        exit
        """
        code, out, err = run_command(commands, 30)
        return code == 0
    
    def skip_setup_screen(self):
        """Pula tela de configuração"""
        print("[*] Pulando tela de setup...")
        commands = """
        mount_filesystems
        
        # Modifica plist de setup
        plist_path="/mnt2/mobile/Library/Preferences/com.apple.purplebuddy.plist"
        if [ -f "$plist_path" ]; then
            rm "$plist_path"
        fi
        
        # Remove restart plist que força setup
        rm -f /mnt2/mobile/Library/Preferences/com.apple.springboard.plist
        
        sync
        exit
        """
        code, out, err = run_command(commands, 30)
        return code == 0
