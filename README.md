# **iPhoenix 🔓**

> Ferramenta de Pentest iOS - Bypass de Activation Lock e MDM via USB

**iPhoenix** é uma ferramenta profissional de penetração testing para dispositivos iOS, desenvolvida para ambientes autorizados de segurança ofensiva. Ela automatiza técnicas de bypass de Activation Lock e remoção de MDM em iPhones e iPads conectados via USB.

> ⚠️ **Aviso Legal**: Esta ferramenta é destinada **EXCLUSIVAMENTE** para profissionais de segurança cibernética realizando testes de penetração autorizados em dispositivos de sua propriedade ou com permissão explícita do proprietário. O uso não autorizado é ilegal e viola leis de direitos digitais (DMCA, CFAA, etc.).

<img width="902" height="682" alt="iphoenix" src="https://github.com/user-attachments/assets/1e2b43a3-0377-475a-ae25-7b6471ccce2d" />


## 📋 **Índice**

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Dispositivos Suportados](#dispositivos-suportados)
- [Técnicas Implementadas](#técnicas-implementadas)
- [Interface Gráfica](#interface-gráfica)
- [Build Executável](#build-executável)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [FAQ Técnico](#faq-técnico)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## **Requisitos**

### **Hardware**
- Computador com porta USB
- Cabo USB compatível com iPhone/iPad (original ou certificado MFI)
- iPhone/iPad para testes (modelos de 5s a 15)

### **Sistemas Operacionais**
| Sistema | Suporte | Status |
|---------|---------|--------|
| Linux (Ubuntu/Debian) | ✅ Completo | Recomendado |
| macOS | ✅ Completo | Testado |
| Windows | ⚠️ Parcial (via MSYS2) | Em desenvolvimento |

### **Dependências Obrigatórias**
- Python 3.8+
- libimobiledevice (≥ 1.3.0)
- usbmuxd
- libideviceactivation
- Tkinter

---

## **Instalação**

### **🔧 Linux (Ubuntu/Debian)**

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/iphoenix.git
cd iphoenix

# 2. Instale dependências do sistema
sudo apt update
sudo apt install -y \
    build-essential \
    pkg-config \
    checkinstall \
    git \
    autoconf \
    automake \
    libtool-bin \
    libplist-dev \
    libimobiledevice-dev \
    libimobiledevice-utils \
    libxml2-dev \
    libcurl4-openssl-dev \
    usbmuxd \
    libusb-1.0-0-dev \
    python3-tk \
    python3-pip \
    curl

# 3. libideviceactivation (necessário compilar)
cd /tmp
git clone https://github.com/libimobiledevice/libideviceactivation.git
cd libideviceactivation
./autogen.sh
make
sudo make install
sudo ldconfig

# 4. Dependências Python
cd ~/iphoenix
pip3 install -r requirements.txt

# 5. Pronto!
python3 iphoenix.py
```

### **🍎 macOS**

```bash
# 1. Instale Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Dependências
brew install libimobiledevice usbmuxd libideviceactivation python-tk

# 3. Clone e execute
git clone https://github.com/seu-usuario/iphoenix.git
cd iphoenix
pip3 install -r requirements.txt
python3 iphoenix.py
```

### **🪟 Windows**

```powershell
# 1. Instale MSYS2 (https://www.msys2.org/)
# 2. No terminal MSYS2 UCRT64:
pacman -S mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-python \
          mingw-w64-ucrt-x86_64-python-pip mingw-w64-ucrt-x86_64-libusb \
          git make

# 3. Baixe libimobiledevice para Windows:
#    https://github.com/libimobiledevice/libimobiledevice/releases

# 4. Clone e execute
git clone https://github.com/seu-usuario/iphoenix.git
cd iphoenix
pip install pillow pyusb
python iphoenix.py
```

### **⚡ Instalação Rápida (via interface)**

O próprio iPhoenix pode instalar as dependências automaticamente:
1. Abra o programa
2. Clique em **"📦 Instalar Dependências"**
3. Aguarde a instalação automática

---

## **Uso**

### **Execução Básica**

```bash
python3 iphoenix.py
```

### **Fluxo de Trabalho**

```
1. Conecte o iPhone via USB
   ↓
2. O iPhoenix detecta automaticamente
   ↓
3. Verifique as informações do dispositivo
   ↓
4. Escolha a ação:
   ├── 🔓 Bypass via checkm8 (iPhone 5s até X)
   ├── 📋 Remover MDM (corporativo/DEP)
   └── ⚡ Reativar Dispositivo
   ↓
5. Siga as instruções na tela
   ↓
6. Dispositivo reinicia com activation lock removido
```

### **Detalhamento por Ação**

#### **🔓 Bypass via checkm8 (A7-A11)**
1. Conecte o iPhone ao computador
2. Clique em **"🔓 Bypass via checkm8"**
3. Coloque o dispositivo em **modo DFU** quando solicitado
4. O script cria um ramdisk, monta o sistema de arquivos
5. Remove registros de ativação (CloudConfigurationDetails.plist, etc.)
6. Dispositivo reinicia com o Activation Lock removido

#### **📋 Remover MDM**
1. Conecte o iPhone supervisionado
2. Clique em **"📋 Remover MDM"**
3. Remove perfis DEP e arquivos de configuração
4. Pula a tela de setup na reinicialização

#### **⚡ Reativar Dispositivo**
1. Útil se o dispositivo já estava ativado mas perdeu o estado
2. Tenta reenviar ticket de ativação via Apple servers

---

## **Dispositivos Suportados**

### **✅ Bypass Completo (via checkm8/SSHRD)**

| Geração | Modelos | Chip | iOS Máx |
|---------|---------|------|---------|
| iPhone 5s | iPhone6,1 / iPhone6,2 | A7 | iOS 12 |
| iPhone 6 / 6 Plus | iPhone7,2 / iPhone7,1 | A8 | iOS 12 |
| iPhone 6s / 6s Plus | iPhone8,1 / iPhone8,2 | A9 | iOS 15 |
| iPhone SE (1ª gen) | iPhone8,4 | A9 | iOS 15 |
| iPhone 7 / 7 Plus | iPhone9,1 / iPhone9,3 / iPhone9,2 / iPhone9,4 | A10 | iOS 15 |
| iPhone 8 / 8 Plus | iPhone10,1 / iPhone10,4 / iPhone10,2 / iPhone10,5 | A11 | iOS 16 |
| iPhone X | iPhone10,3 / iPhone10,6 | A11 | iOS 16 |
| iPad (5ª gen+) | iPad6,11 - iPad7,11 | A9-A11 | iOS 16 |

### **⚠️ Parcial (Recovery Mode + libideviceactivation)**

| Geração | Modelos | Chip |
|---------|---------|------|
| iPhone XR / XS | iPhone11,2 - iPhone11,8 | A12 |
| iPhone 11 | iPhone12,1 - iPhone12,8 | A13 |
| iPhone 12 | iPhone13,1 - iPhone13,4 | A14 |
| iPhone 13 | iPhone14,2 - iPhone14,8 | A15 |
| iPhone 14 | iPhone14,2 - iPhone14,8 | A15/A16 |
| iPhone 15 | iPhone15,2 - iPhone15,5 | A16/A17 |

> **Nota**: Para dispositivos A12+ (XR até 15), o Activation Lock é validado no servidor Apple (server-side). Não existe bypass de software puro. O iPhoenix tenta técnicas de recovery mode e reativação.

---

## **Técnicas Implementadas**

| Técnica | Descrição | Alvo |
|---------|-----------|------|
| **checkm8 + SSHRD** | Exploit bootrom (não patcheável) + SSH Ramdisk | A7-A11 |
| **Remoção de CloudConfigurationDetails.plist** | Remove perfis DEP/MDM | Todos checkm8 |
| **Remoção de ActivationRecords** | Limpa registros locais de ativação | Todos checkm8 |
| **libideviceactivation** | Reativação via Apple servers | Todos (USB) |
| **Recovery Mode** | Manipulação via iRecovery | A12+ (limitado) |
| **MDM Profile Removal** | Remove configurações de gerenciamento corporativo | Supervisionados |

---

## **Interface Gráfica**

```
┌─────────────────────────────────────────────────────────────┐
│  iPhoenix 🔓  -  iOS Activation Pentest Tool    [🔄][📦][🆘]│
├─────────────────────────────────────────────────────────────┤
│  ┌─ Dispositivo ──────────────────────────────────────────┐ │
│  │ Modelo:      iPhone 8 (iPhone10,1)                    │ │
│  │ iOS:         16.6.1                                   │ │
│  │ Estado:      Activation Lock                          │ │
│  │ UDID:        00008110-XXXXXXXXXXXXXXXX                │ │
│  │ ECID:        8937298712345678                         │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─ Ações de Pentest ────────────────────────────────────┐ │
│  │ [🔓 Bypass checkm8] [📋 Remover MDM] [⚡ Reativar]   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─ Log de Operações ───────────────────────────────────┐ │
│  │ > Dispositivo encontrado: iPhone 8 - iOS 16.6.1     │ │
│  │ > Iniciando bypass checkm8...                        │ │
│  │ > [20%] Preparando SSHRD                             │ │
│  │ > [40%] Criando ramdisk                              │ │
│  │ > Coloque o dispositivo em DFU mode                  │ │
│  │ > [60%] Inicializando ramdisk                        │ │
│  │ > [80%] Removendo registros de ativação              │ │
│  │ > ✓ Bypass concluído com sucesso!                    │ │
│  └─────────────────────────────────────────────────────┘ │
│  ████████████████████░░░░░░░░░░░░  80%                   │
│  Pronto                          iPhone 8 | iOS 16.6.1    │
└─────────────────────────────────────────────────────────────┘
```

---

## **Build Executável**

### **Cross-Platform**

```bash
# Dependências
pip install pyinstaller pillow pyusb

# Linux
./build.sh

# Ou manualmente:
pyinstaller --onefile --windowed --name "iPhoenix" \
    --add-data "core:core" \
    --hidden-import tkinter \
    --hidden-import PIL \
    --hidden-import usb \
    iphoenix.py
```

### **Output**

| Sistema | Arquivo | Localização |
|---------|---------|-------------|
| Linux | `iPhoenix` | `dist/` |
| macOS | `iPhoenix.app` | `dist/` |
| Windows | `iPhoenix.exe` | `dist/` |

---

## **Estrutura do Projeto**

```
iPhoenix/
├── iphoenix.py                    # Interface gráfica principal (Tkinter)
├── build.sh                       # Script de build para executável
├── requirements.txt               # Dependências Python
├── README.md                      # Este arquivo
│
├── core/                          # Módulos principais
│   ├── __init__.py
│   ├── device_detect.py           # Detecção de modelo/iOS via USB
│   ├── checkm8_bypass.py          # Bypass via checkm8/SSHRD (A7-A11)
│   ├── recovery_bypass.py         # Técnicas de Recovery Mode (A12+)
│   ├── mdm_bypass.py              # Remoção de perfis MDM
│   └── utils.py                   # Utilitários (libimobiledevice wrapper)
│
├── assets/                        # Recursos visuais
│   ├── icon.ico
│   └── icon.png
│
└── dist/                          # Executáveis compilados (gitignored)
```

---

## **FAQ Técnico**

### **O programa funciona em iPhones com iOS 17?**
Para **A7-A11** (5s até X): Sim, via checkm8 (exploit no bootrom, não patcheável por software). Para **A12+** (XR até 15): O Activation Lock é validado server-side, não há bypass via software.

### **Preciso fazer jailbreak primeiro?**
Não. O iPhoenix usa o exploit **checkm8** (bootrom) que não requer jailbreak. Para A11+ (iPhone 8, X), o checkra1n pode ajudar a entrar em DFU.

### **O iPhone precisa estar desbloqueado?**
Não. O dispositivo pode estar na tela de "iPhone Desativado" ou "Activation Lock". Contanto que entre em modo DFU, o bypass funciona.

### **Vai funcionar em iPhone roubado?**
**NÃO.** Esta ferramenta é apenas para pentest autorizado. O Activation Lock existe para proteger dispositivos roubados. Se você não é o proprietário legítimo ou não tem autorização por escrito, não use.

### **O que acontece com a rede do iPhone após o bypass?**
Em dispositivos compatíveis com checkm8, o bypass remove apenas os registros **locais** de ativação. A conectividade de rede (Wi-Fi, celular) volta ao normal pois o dispositivo não está mais bloqueado.

---

## **Como Contribuir**

1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona suporte a iPad A12'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### **Guidelines**
- Código em Python 3.8+ com tipagem
- Documente funções com docstrings
- Teste em múltiplos dispositivos/iOS
- Sinta-se à vontade para contribuir com suporte a novos modelos

---

## **Stack Tecnológica**

- **Linguagem**: Python 3.8+ / Bash
- **Interface**: Tkinter (nativo)
- **Comunicação USB**: libimobiledevice, libusb, pyusb
- **Exploit**: checkm8 (bootrom), SSHRD (SSH Ramdisk)
- **Build**: PyInstaller
- **Suporte**: Linux >> macOS > Windows

---

## **Licença**

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

## **Aviso Legal Final**

```
ESTA FERRAMENTA É FORNECIDA APENAS PARA FINS EDUCACIONAIS E DE TESTE DE SEGURANÇA AUTORIZADO.

O uso não autorizado desta ferramenta para contornar mecanismos de proteção em dispositivos 
que não lhe pertencem pode constituir violação de:

- Digital Millennium Copyright Act (DMCA) 17 U.S.C. § 1201
- Computer Fraud and Abuse Act (CFAA) 18 U.S.C. § 1030
- Legislação local equivalente (Marco Civil da Internet, Lei de Crimes Cibernéticos, etc.)
- Termos de Serviço da Apple Inc.

O desenvolvedor não se responsabiliza por qualquer uso indevido desta ferramenta.
```

---

<div align="center">
  <b>iPhoenix</b> — Pentest iOS Automation Tool<br>
  <sub>Desenvolvido para profissionais de segurança cibernética</sub>
</div>
```
