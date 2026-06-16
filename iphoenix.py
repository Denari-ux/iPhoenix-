#!/usr/bin/env python3
"""
iPhoenix v1.0 - iOS Activation Pentest Tool
Interface Gráfica - Tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
import sys
import time

# Adiciona path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.utils import (
    check_dependencies, install_dependencies, get_device_info_dict,
    is_checkm8_compatible, get_ios_major, SYSTEM
)
from core.device_detect import DeviceDetector
from core.checkm8_bypass import Checkm8Bypass
from core.recovery_bypass import RecoveryBypass
from core.mdm_bypass import MDMBypass

class IPhoenixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iPhoenix - iOS Activation Pentest Tool v1.0")
        self.root.geometry("900x650")
        self.root.configure(bg="#1a1a2e")
        
        # Tenta ícone
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        self.device = None
        self.detector = DeviceDetector()
        self.running = False
        
        self.setup_ui()
        
        # Auto-detect na inicialização
        self.after_id = self.root.after(1000, self.auto_detect)
    
    def setup_ui(self):
        """Configura a interface"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1a1a2e")
        style.configure("TLabel", background="#1a1a2e", foreground="#e0e0e0", font=("Segoe UI", 10))
        style.configure("TButton", background="#16213e", foreground="#e0e0e0", borderwidth=0, 
                       font=("Segoe UI", 9, "bold"))
        style.map("TButton", background=[("active", "#0f3460")])
        style.configure("Accent.TButton", background="#0f3460", foreground="#ffffff")
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#00d4ff")
        style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#a0a0a0")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, text="iPhoenix", style="Header.TLabel")
        header.pack(anchor=tk.W)
        
        subtitle = ttk.Label(main_frame, text="iOS Activation Lock Penetration Testing Tool", 
                           font=("Segoe UI", 9), foreground="#888")
        subtitle.pack(anchor=tk.W)
        
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=10)
        
        # Frame de informações do dispositivo
        device_frame = ttk.LabelFrame(main_frame, text=" Dispositivo ", padding="10")
        device_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.device_info_text = tk.Text(device_frame, height=5, bg="#16213e", fg="#e0e0e0",
                                       font=("Courier", 9), relief=tk.FLAT, bd=0)
        self.device_info_text.pack(fill=tk.X)
        self.device_info_text.insert(tk.END, "Aguardando dispositivo...\n")
        self.device_info_text.config(state=tk.DISABLED)
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        self.refresh_btn = ttk.Button(action_frame, text="🔄 Atualizar", command=self.refresh_device)
        self.refresh_btn.pack(side=tk.LEFT, padx=2)
        
        self.deps_btn = ttk.Button(action_frame, text="📦 Instalar Dependências", command=self.install_deps)
        self.deps_btn.pack(side=tk.LEFT, padx=2)
        
        self.dfu_btn = ttk.Button(action_frame, text="🔄 DFU Mode Guide", command=self.show_dfu_guide)
        self.dfu_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame de ações de bypass
        bypass_frame = ttk.LabelFrame(main_frame, text=" Ações de Pentest ", padding="10")
        bypass_frame.pack(fill=tk.X, pady=5)
        
        btn_frame = ttk.Frame(bypass_frame)
        btn_frame.pack(fill=tk.X)
        
        self.bypass_checkm8_btn = ttk.Button(btn_frame, text="🔓 Bypass via checkm8 (A7-A11)", 
                                            command=lambda: self.start_bypass("checkm8"),
                                            style="Accent.TButton", width=30)
        self.bypass_checkm8_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        self.bypass_mdm_btn = ttk.Button(btn_frame, text="📋 Remover MDM", 
                                        command=lambda: self.start_bypass("mdm"),
                                        width=20)
        self.bypass_mdm_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        self.reactivate_btn = ttk.Button(btn_frame, text="⚡ Reativar Dispositivo", 
                                        command=self.reattempt_activation,
                                        width=20)
        self.reactivate_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # Frame de log
        log_frame = ttk.LabelFrame(main_frame, text=" Log de Operações ", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, bg="#0d0d1a", fg="#00ff88",
                                                 font=("Courier", 9), height=12, relief=tk.FLAT, bd=0)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode="determinate", style="TProgressbar")
        self.progress.pack(fill=tk.X, pady=5)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X)
        self.status_label = ttk.Label(status_frame, text="Pronto", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT)
        
        self.device_label = ttk.Label(status_frame, text="Nenhum dispositivo", style="Status.TLabel")
        self.device_label.pack(side=tk.RIGHT)
    
    def log(self, message, level="info"):
        """Adiciona mensagem ao log"""
        colors = {
            "info": "#00ff88",
            "warn": "#ffaa00",
            "error": "#ff4444",
            "success": "#00ff44",
            "step": "#00ccff",
        }
        color = colors.get(level, "#ffffff")
        tag = f"tag_{level}_{time.time()}"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"> {message}\n", tag)
        self.log_text.tag_config(tag, foreground=color)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def update_device_info(self, info=None):
        """Atualiza display de informações do dispositivo"""
        if info:
            self.device = info
        elif self.device:
            info = self.device
        
        if info:
            text = (
                f"Modelo:      {info.get('model', '?')}\n"
                f"iOS:         {info.get('ios_version', '?')}\n"
                f"Estado:      {info.get('activation_state', '?')}\n"
                f"UDID:        {info.get('udid', '?')[:20]}...\n"
                f"ECID:        {info.get('ecid', '?')}"
            )
            self.device_info_text.config(state=tk.NORMAL)
            self.device_info_text.delete("1.0", tk.END)
            self.device_info_text.insert(tk.END, text)
            self.device_info_text.config(state=tk.DISABLED)
            
            self.device_label.config(text=f"{info.get('model', '?')} | iOS {info.get('ios_version', '?')}")
            self.status_label.config(text="Conectado")
        else:
            self.device_info_text.config(state=tk.NORMAL)
            self.device_info_text.delete("1.0", tk.END)
            self.device_info_text.insert(tk.END, "Nenhum dispositivo detectado.\nConecte um iPhone via USB.")
            self.device_info_text.config(state=tk.DISABLED)
            self.device_label.config(text="Desconectado")
    
    def auto_detect(self):
        """Auto-detecção de dispositivo"""
        self.log("Procurando dispositivos iOS via USB...", "info")
        info = get_device_info_dict()
        if info:
            self.log(f"Dispositivo encontrado: {info.get('model')} - iOS {info.get('ios_version')}", "success")
            self.update_device_info(info)
        else:
            self.log("Nenhum dispositivo conectado.", "warn")
            self.update_device_info(None)
    
    def refresh_device(self):
        """Atualiza informações do dispositivo"""
        self.log("Atualizando informações do dispositivo...", "info")
        info = get_device_info_dict()
        self.update_device_info(info)
        if info:
            self.log(f"Atualizado: {info.get('model')} - iOS {info.get('ios_version')}", "success")
        else:
            self.log("Dispositivo não encontrado.", "error")
    
    def install_deps(self):
        """Instala dependências"""
        self.log("Verificando dependências...", "step")
        missing = check_dependencies()
        if not missing:
            self.log("Todas as dependências estão instaladas!", "success")
            return
        
        self.log(f"Dependências faltando: {', '.join(missing)}", "warn")
        self.log("Instalando dependências...", "step")
        
        def install_thread():
            self.running = True
            self.deps_btn.config(state=tk.DISABLED)
            try:
                result = install_dependencies()
                if not result:
                    self.log("Dependências instaladas com sucesso!", "success")
                else:
                    self.log(f"Ainda faltando: {', '.join(result)}", "error")
            except Exception as e:
                self.log(f"Erro na instalação: {e}", "error")
            finally:
                self.running = False
                self.deps_btn.config(state=tk.NORMAL)
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def show_dfu_guide(self):
        """Mostra guia de modo DFU"""
        guide = """COMO ENTRAR EM MODO DFU:

iPhone 8/X ou mais novo (A11+):
1. Conecte ao PC
2. Aperte e solte rápido: Volume +
3. Aperte e solte rápido: Volume -
4. Segure o botão Power por 10 segundos
5. Sem soltar Power, segure também Volume -
6. Segure ambos por 5 segundos
7. Solte Power MAS CONTINUE segurando Volume -
8. Tela preta = DFU mode!

iPhone 7/7 Plus:
1. Segure Power + Volume - por 10 segundos
2. Solte Power, continue segurando Volume - por 5s
3. Tela preta = DFU

iPhone 5s/6/SE (A7-A9):
1. Segure Power + Home por 10 segundos
2. Solte Power, continue Home por 5s
3. Tela preta = DFU"""
        
        messagebox.showinfo("Modo DFU - Guia Rápido", guide)
    
    def start_bypass(self, method):
        """Inicia bypass em thread separada"""
        if self.running:
            messagebox.showwarning("Aviso", "Já existe uma operação em andamento!")
            return
        
        if not self.device:
            messagebox.showwarning("Aviso", "Nenhum dispositivo detectado!")
            return
        
        self.running = True
        threading.Thread(target=self._bypass_worker, args=(method,), daemon=True).start()
    
    def _bypass_worker(self, method):
        """Worker de bypass"""
        try:
            if method == "checkm8":
                self.run_checkm8_bypass()
            elif method == "mdm":
                self.run_mdm_bypass()
        finally:
            self.running = False
    
    def run_checkm8_bypass(self):
        """Executa bypass via checkm8"""
        model = self.device.get("model", "")
        ios_ver = self.device.get("ios_version", "")
        
        if not is_checkm8_compatible(model):
            self.log(f"Modelo {model} não é compatível com checkm8 (A7-A11 apenas)", "error")
            return
        
        self.log(f"Iniciando bypass checkm8 para {model} (iOS {ios_ver})", "step")
        
        bypass = Checkm8Bypass(ios_ver, model)
        
        # Progress callback
        def update_progress(val, msg):
            self.progress["value"] = val
            self.log(f"[{val}%] {msg}", "step")
            self.status_label.config(text=msg)
        
        result = bypass.full_bypass(progress_callback=update_progress)
        
        if result.get("status") == "wait_dfu":
            self.log("Coloque o dispositivo em modo DFU!", "warn")
            messagebox.showinfo("DFU Mode", "Coloque o dispositivo em modo DFU agora.\n\nGuia: Clique em 'DFU Mode Guide'")
            
            # Aguarda DFU
            if self.detector.wait_for_dfu():
                self.log("DFU detectado! Continuando...", "success")
                result = bypass.full_bypass(progress_callback=update_progress)
            else:
                self.log("Timeout aguardando DFU.", "error")
                return
        
        if result.get("status") == "success":
            self.log("✓ Bypass concluído com sucesso!", "success")
            self.log("O dispositivo está reiniciando...", "info")
            self.log("Após reiniciar, o Activation Lock deve estar removido.", "success")
            messagebox.showinfo("Sucesso", "Bypass concluído!\n\nO iPhone está reiniciando.\nA tela de ativação deve ser pulada.")
        else:
            self.log(f"✗ Bypass falhou: {result.get('error', 'Erro desconhecido')}", "error")
    
    def run_mdm_bypass(self):
        """Executa bypass MDM"""
        self.log("Iniciando bypass MDM...", "step")
        mdm = MDMBypass(self.device)
        
        self.progress["value"] = 20
        self.log("[20%] Removendo perfis DEP...", "step")
        if mdm.remove_dep_profile():
            self.log("✓ Perfis DEP removidos", "success")
        else:
            self.log("⚠ Falha ao remover perfis DEP", "warn")
        
        self.progress["value"] = 60
        self.log("[60%] Pulando tela de setup...", "step")
        if mdm.skip_setup_screen():
            self.log("✓ Tela de setup removida", "success")
        else:
            self.log("⚠ Falha ao remover setup", "warn")
        
        self.progress["value"] = 100
        self.log("[100%] Bypass MDM concluído!", "success")
        self.log("Reinicie o dispositivo para aplicar as alterações.", "info")
        messagebox.showinfo("MDM Bypass", "Bypass MDM concluído!\n\nReinicie o iPhone para aplicar.")
    
    def reattempt_activation(self):
        """Tenta reativar o dispositivo"""
        if self.running:
            return
        
        self.running = True
        self.log("Tentando reativar dispositivo...", "step")
        
        def worker():
            try:
                bypass = RecoveryBypass()
                result = bypass.send_activation_ticket()
                if result.get("status") == "success":
                    self.log("✓ Dispositivo reativado com sucesso!", "success")
                else:
                    self.log(f"✗ Falha na reativação: {result.get('error', 'Erro')}", "error")
            finally:
                self.running = False
        
        threading.Thread(target=worker, daemon=True).start()

def main():
    root = tk.Tk()
    app = IPhoenixApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
