#!/usr/bin/env python3
"""
iPhoenix - Bypass via checkm8/SSHRD (A7-A11)
"""
import os
import time
from .utils import run_command, SYSTEM

class Checkm8Bypass:
    def __init__(self, ios_version, model):
        self.ios_version = ios_version
        self.model = model
        self.ssh_rd_path = os.path.expanduser("~/.iphoenix/sshrd")
    
    def setup_sshrd(self):
        """Clona/configura SSHRD_Script"""
        print("[*] Configurando SSHRD_Script...")
        os.makedirs(self.ssh_rd_path, exist_ok=True)
        
        # Clone se não existir
        if not os.path.exists(f"{self.ssh_rd_path}/sshrd.sh"):
            run_command(
                f"cd {self.ssh_rd_path} && "
                f"git clone https://github.com/verygenericname/SSHRD_Script.git . --recursive",
                120
            )
        else:
            run_command(f"cd {self.ssh_rd_path} && git pull", 30)
        
        return os.path.exists(f"{self.ssh_rd_path}/sshrd.sh")
    
    def create_ramdisk(self):
        """Cria ramdisk para a versão do iOS"""
        print(f"[*] Criando ramdisk para iOS {self.ios_version}...")
        code, out, err = run_command(
            f"cd {self.ssh_rd_path} && "
            f"chmod +x sshrld.sh && "
            f"./sshrd.sh {self.ios_version}",
            300
        )
        return code == 0
    
    def boot_ramdisk(self):
        """Inicializa o ramdisk no dispositivo"""
        print("[*] Inicializando ramdisk...")
        code, out, err = run_command(
            f"cd {self.ssh_rd_path} && ./sshrd.sh boot",
            60
        )
        return code == 0
    
    def connect_ssh(self):
        """Conecta SSH ao dispositivo"""
        print("[*] Conectando SSH...")
        code, out, err = run_command(
            f"cd {self.ssh_rd_path} && ./sshrd.sh ssh",
            30
        )
        # Se funcionar, retorna True e podemos executar comandos
        return code == 0
    
    def mount_filesystems(self):
        """Monta sistema de arquivos iOS"""
        print("[*] Montando filesystems...")
        # Via SSH
        commands = """
        mount_filesystems
        cd /mnt2/containers/Shared/SystemGroup/systemgroup.com.apple.configurationprofiles/Library/ConfigurationProfiles
        """
        code, out, err = run_command(
            f"cd {self.ssh_rd_path} && "
            f"echo '{commands}' | ./sshrd.sh ssh 2>/dev/null",
            30
        )
        return code == 0
    
    def remove_activation_records(self):
        """Remove registros de ativação"""
        print("[*] Removendo registros de ativação...")
        commands = """
        mount_filesystems
        rm -f /mnt2/containers/Shared/SystemGroup/systemgroup.com.apple.configurationprofiles/Library/ConfigurationProfiles/CloudConfigurationDetails.plist
        rm -f /mnt2/mobile/Library/Preferences/com.apple.activation.plist
        rm -f /mnt2/mobile/Library/Preferences/com.apple.activationrecognition.plist
        rm -rf /mnt2/mobile/Library/ActivationRecords/
        
        # Forçar rebuild
        touch /mnt2/mobile/Library/Preferences/com.apple.activation.plist
        
        # Desativar passcode se existir
        rm -f /mnt2/mobile/Library/Preferences/com.apple.springboard.plist
        
        sync
        exit
        """
        code, out, err = run_command(
            f"cd {self.ssh_rd_path} && "
            f"echo '{commands}' | ./sshrd.sh ssh 2>&1",
            60
        )
        return code == 0
    
    def reboot_device(self):
        """Reinicia dispositivo"""
        print("[*] Reiniciando dispositivo...")
        code, out, err = run_command(
            f"cd {self.ssh_rd_path} && ./sshrd.sh clean",
            30
        )
        # Reboot via irecovery
        run_command("irecovery -c reboot", 10)
        return True
    
    def full_bypass(self, progress_callback=None):
        """Executa bypass completo"""
        steps = [
            ("Preparando SSHRD", self.setup_sshrd),
            ("Criando ramdisk", self.create_ramdisk),
            ("Coloque o dispositivo em DFU mode", None),
            ("Inicializando ramdisk", self.boot_ramdisk),
            ("Montando filesystems", self.mount_filesystems),
            ("Removendo ativação", self.remove_activation_records),
            ("Reiniciando", self.reboot_device),
        ]
        
        for i, (name, func) in enumerate(steps):
            if progress_callback:
                progress_callback(int((i / len(steps)) * 100), name)
            
            if func is None:
                # Aguarda DFU
                if progress_callback:
                    progress_callback(int((i / len(steps)) * 100), "Aguardando DFU mode...")
                # Espera o usuário colocar em DFU
                return {"status": "wait_dfu", "step": name, "progress": int((i / len(steps)) * 100)}
            
            success = func()
            if not success:
                return {"status": "error", "step": name, "error": f"Falha em: {name}"}
        
        return {"status": "success", "message": "Bypass concluído! Dispositivo reiniciando."}
