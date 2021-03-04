import subprocess
import sys

import lsb_release


def verificar_versao_sistema_operacional():
    """
    Verifica a versão do sistema operacional que está sendo executado. Caso o sistema operacional não seja compatível com este script, uma exceção é lançada
    """
    os_release = lsb_release.get_os_release()
    if os_release['RELEASE'] != '20.10' or os_release['ID'] != 'Ubuntu':
        raise OSError("Versão de sistema operacional incompatível")


def executar_comandos_shell(comandos_shell: [], numero_maximo_de_repeticoes: int = 5):
    """
    Executa uma sequencia de comandos shell
    :param comandos_shell: Lista de comandos shell a serem executados.
    :param numero_maximo_de_repeticoes: Numero maximo de repetições do comando antes que o programa aborte
    """
    for comando_shell in comandos_shell:
        executar_comando_shell_sem_erro(comando_shell, numero_maximo_de_repeticoes)


def executar_comando_shell_sem_erro(comando: str, numero_maximo_de_repeticoes: int = 5):
    """
    Executa um comando shell repetindo, caso ocorra algum erro
    :param comando: Comando shell que sera executado
    :param numero_maximo_de_repeticoes: Numero maximo de repetições do comando antes que o programa aborte
    """
    print(comando)
    repetir = True
    while repetir and numero_maximo_de_repeticoes >= 0:
        try:
            subprocess.run(comando, shell=True, check=True)
            repetir = False
        except subprocess.CalledProcessError as erro:
            print(erro)
            repetir = True
            numero_maximo_de_repeticoes -= 1

    if numero_maximo_de_repeticoes < 0:
        sys.exit(-1)


def instalar_prerequisitos():
    """
    Instala os programas pre-requisitos necessários para instalar os outros programas
    """
    comandos = \
        [
            "sudo apt-get update;",
            "sudo apt-get install curl apt-transport-https snapd apt -y;"
        ]
    executar_comandos_shell(comandos)


def atualizar():
    """
    Atualiza todos os programas do sistema
    """
    comandos = \
        [
            "sudo apt update;",
            "sudo apt full-upgrade -y;"
        ]
    executar_comandos_shell(comandos)


def adicionar_repositorios():
    """
    Adiciona os repositórios do apt
    """
    comandos = \
        [
            # Google Chrome
            "wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -;",
            "echo 'deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main' | sudo tee --append /etc/apt/sources.list.d/google-chrome.list;",

            # Google Earth
            "echo 'deb [arch=amd64] https://dl.google.com/linux/earth/deb/ stable main' | sudo tee --append /etc/apt/sources.list.d/google-earth-pro.list;",

            # Signal
            "curl -s https://updates.signal.org/desktop/apt/keys.asc | sudo apt-key add -",
            "echo \"deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main\" | sudo tee --append /etc/apt/sources.list.d/signal-xenial.list"
        ]
    executar_comandos_shell(comandos)



def instalar_dot_net_sdk():
    """
    Baixa e instala o .NET SDK
    """

    comandos = \
        [
            # Adicionando a chave de assinatura da Microsoft
            "wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb;",
            "sudo apt install ./packages-microsoft-prod.deb -y;",

            # Atualizando a lista de repositórios
            "sudo apt update;",

            # Instalando pre-requisito
            "sudo apt install apt-transport-https -y;",

            # Atualizando a lista de repositórios
            "sudo apt update;",

            # Instalando o .NET SDK
            "sudo apt install dotnet-sdk-5.0 aspnetcore-runtime-5.0 dotnet-runtime-5.0 -y;",

            # Movendo o packages-microsoft-prod.deb para a lixeira
            "gio trash ./packages-microsoft-prod.deb"
        ]

    executar_comandos_shell(comandos)


def instalar_drivers():
    """
    Instala os drivers do Ubuntu
    """
    comandos = \
        [
            "sudo ubuntu-drivers autoinstall;"
        ]
    executar_comandos_shell(comandos)


def instalar_programas_apt():
    """
    Instala os programas por meio do apt
    """

    programas_apt = [

        # Ferramentas do sistema
        "gufw",  # Firewall
        "nemo",  # Gerenciador de Arquivos

        # Ferramentas de desenvolvimento
        "python3",
        "python3-pip",
        "python3-setuptools",
        "make",
        "gcc",
        "g++",
        "git",
        "gcc-multilib",
        "manpages-dev",
        "autoconf",
        "automake",
        "libtool",
        "flex",
        "bison",
        "gdb",
        "gcc-doc",
        "gradle",
        "git-gui",
        "openjdk-11-jdk",
        "openjdk-8-jdk",
        "ca-certificates-java",
        "golang",
        "python",

        # Cinnamon Deskop
        "cinnamon-core",

        # VirtualBox
        "virtualbox",
        # "virtualbox-ext-pack",
        "virtualbox-guest-additions-iso",

        # Google Chrome
        "google-chrome-stable",
        "chrome-gnome-shell",

        # LibreOffice
        "libreoffice",
        "libreoffice-lightproof-pt-br",
        "libreoffice-lightproof-en",
        "libreoffice-l10n-pt-br",
        "libreoffice-l10n-en-gb",

        # Flatpak
        "flatpak",
        "gnome-software-plugin-flatpak",

        # Outros programas
        "evince",
        "alien",
        "audacity",
        "brasero",
        "asunder",
        "file-roller",
        "gnome-disk-utility",
        "usb-creator-gtk",
        "transmission-gtk",
        "steam",
        "signal-desktop",
        "kdenlive",
        "obs-studio",
        "gpa",
        "logisim",
        "stacer",

        # VPN
        "openvpn",
        "network-manager-openvpn-gnome",
        "resolvconf",

        # Suporte a KVM no Android Studio
        "qemu-kvm",
        "libvirt-daemon-system",
        "libvirt-clients",
        "bridge-utils",

        # Utilitários do sistema
        "blueman",
        "ubuntu-report",
        "exfat-utils",
        "samba",
        "linux-headers-$(uname -r)",
        "dkms",
        "unrar",
        "unrar-free",
        "p7zip-full",
        "ffmpeg",
        "unattended-upgrades"
        # Não serão instalados: bless, dialog, libcanberra-gtk-module ,libcanberra-gtk3-module
    ]

    comando = "sudo apt install "

    for i in programas_apt:
        comando += i
        comando += " "

    comando += "-y;"

    executar_comando_shell_sem_erro(comando)


def instalar_flathub():
    """
    Instala o flathub
    """
    comandos = \
        [
            "sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo;"
        ]
    executar_comandos_shell(comandos)


def instalar_programas_snap():
    """
    Instala os programas por meio do snap
    """
    comandos = \
        [
            "sudo snap install spotify;",
            "sudo snap install slack --classic;",
            "sudo snap install skype --classic;",
            "sudo snap install intellij-idea-community --classic;",
            "sudo snap install code --classic;",
            "sudo snap install --devmode keepassxc;",
            "sudo snap install --classic android-studio;",
            "sudo snap install pycharm-community --classic;",
            "sudo snap install clion --classic;"
        ]
    executar_comandos_shell(comandos)


def instalar_programas_pip():
    """
    Instala os programas por meio do pip
    """
    comandos = \
        [
            "sudo pip3 install protonvpn-cli;"
        ]
    executar_comandos_shell(comandos)


def instalar_rust_lang():
    """
    Instala o compilador da linguagem Rust
    """
    comandos = \
        [
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh;"
        ]
    executar_comandos_shell(comandos)


def instalar_logisim():
    """
    Instala o Logisim
    """
    comandos = \
        [
            "sudo mv /usr/share/logisim/logisim.jar /usr/share/logisim/logisim.jar.old;",
            "sudo wget https://raw.githubusercontent.com/LogisimIt/Logisim/master/Compiled/Logisim-ITA.jar# -O /usr/share/logisim/logisim.jar;",
            "sudo chmod a+x /usr/share/logisim/logisim.jar;"
        ]
    executar_comandos_shell(comandos)


def instalar_youtube_dl():
    """
    Instala o Youtube-dl
    """
    comandos = \
        [
            "sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl;",
            "sudo chmod a+rx /usr/local/bin/youtube-dl;",
            "sudo youtube-dl -U;"
        ]
    executar_comandos_shell(comandos)


def desinstalar_programas_inuteis():
    """
    Desinstala programas inúteis
    """

    programas_inuteis = [

        "aisleriot",
        "five-or-more",
        "hitori",
        "iagno",
        "gnome-klotski",
        "lightsoff",
        "gnome-mahjongg",
        "gnome-mines",
        "gnome-nibbles",
        "quadrapassel",
        "four-in-a-row",
        "gnome-robots",
        "gnome-sudoku",
        "swell-foop",
        "tali",
        "gnome-taquin",
        "gnome-tetravex",
        "gnome-chess"
    ]

    comando_remover_programas_inuteis = "sudo apt autoremove "
    for i in programas_inuteis:
        comando_remover_programas_inuteis += i + " "
    comando_remover_programas_inuteis += "-y;"

    comandos = \
        [
            comando_remover_programas_inuteis,
            "sudo apt autoclean -y;"
        ]
    executar_comandos_shell(comandos)


def configurar_visual_studio_code():
    """
    Configurar o Visual Studio Code
    """
    comandos = \
        [
            "echo 'fs.inotify.max_user_watches=524288' | sudo tee --append /etc/sysctl.conf;",
            "sudo sysctl -p;",
            "git config --global core.editor \"code --wait\";"
        ]
    executar_comandos_shell(comandos)


def instalar_extensoes_visual_studio_code():
    """
    Instala as extensões do Visual Studio Code
    """
    comandos = \
        [
            # Tradução do VS Code em Português
            "code --install-extension ms-ceintl.vscode-language-pack-pt-br;",

            # Linguagem C/C++
            "code --install-extension ms-vscode.cpptools;",
            "code --install-extension ms-vscode.cmake-tools;",
            "code --install-extension austin.code-gnu-global;",

            # Linguagem C#
            "code --install-extension ms-dotnettools.csharp;",

            # Linguagem Java
            "code --install-extension vscjava.vscode-java-debug;",
            "code --install-extension vscjava.vscode-maven;",
            "code --install-extension vscjava.vscode-java-dependency;",
            "code --install-extension vscjava.vscode-java-pack;",
            "code --install-extension vscjava.vscode-java-test;",
            "code --install-extension redhat.java;",

            # Linguagem Rust
            "code --install-extension matklad.rust-analyzer;",
            "code --install-extension vadimcn.vscode-lldb;",
            "code --install-extension rust-lang.rust;",

            # Linguagem Go
            "code --install-extension golang.Go;",

            # HTML, CSS e Javascript
            "code --install-extension ecmel.vscode-html-css;",
            "code --install-extension firefox-devtools.vscode-firefox-debug;",
            "code --install-extension msjsdiag.debugger-for-chrome;",
            "code --install-extension dbaeumer.vscode-eslint;",

            # Tema do VS Code
            "code --install-extension GitHub.github-vscode-theme;",

            # Markdown
            "code --install-extension DavidAnson.vscode-markdownlint;",

            # Powershell
            "code --install-extension ms-vscode.PowerShell;",

            # Indentação de código
            "code --install-extension NathanRidley.autotrim;",
            "code --install-extension esbenp.prettier-vscode;",

            # AI-assisted IntelliSense
            "code --install-extension VisualStudioExptTeam.vscodeintellicode;"
        ]
    executar_comandos_shell(comandos)


def configurar_alias():
    """
    Configura os alias
    """
    comandos = \
        [
            "echo \"alias update='sudo apt update && sudo apt full-upgrade -y && sudo snap refresh && flatpak update -y &&  sudo do-release-upgrade'\" | tee --append ~/.bashrc;",
            "echo \"alias reload-sound='sudo apt update;sudo apt full-upgrade -y;sudo apt install --reinstall alsa-base alsa-utils alsa-tools-gui alsa-topology-conf alsa-ucm-conf bluedevil gir1.2-cvc-1.0 gir1.2-rb-3.0 gstreamer1.0-libav gstreamer1.0-nice gstreamer1.0-packagekit gstreamer1.0-pulseaudio indicator-sound libao-common libao4 libasound2-plugins libbasicusageenvironment1 libcanberra-pulse libkf5pulseaudioqt2 libpulse-mainloop-glib0 libpulse0 libpulsedsp lightdm linux-image-`uname -r` linux-sound-base pavucontrol pulseaudio pulseaudio-equalizer pulseaudio-module-bluetooth pulseaudio-module-jack pulseaudio-module-lirc pulseaudio-module-raop pulseaudio-module-zeroconf pulseaudio-utils python3-libdiscid speech-dispatcher-audio-plugins ubuntu-desktop ubuntu-sounds -y;sudo bash ./Fix_Bluetooth.sh;killall pulseaudio;rm -r ~/.pulse*;ubuntu-support-status;sudo usermod -aG `cat /etc/group | grep -e '^pulse:' -e '^audio:' -e '^pulse-access:' -e '^pulse-rt:' -e '^video:' | awk -F: '{print $1}' | tr '\n' ',' | sed 's:,$::g'` `whoami`;sudo pulseaudio -k;sudo alsa force-reload;'\" | tee --append ~/.bashrc;",
            "echo \"alias java8='/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java'\" | tee --append ~/.bashrc;",
            "echo \"alias java11='/usr/lib/jvm/java-11-openjdk-amd64/bin/java'\" | tee --append ~/.bashrc;",
            "echo \"alias javac8='/usr/lib/jvm/java-8-openjdk-amd64/bin/javac'\" | tee --append ~/.bashrc;",
            "echo \"alias javac11='/usr/lib/jvm/java-11-openjdk-amd64/bin/javac'\" | tee --append ~/.bashrc;",
        ]
    executar_comandos_shell(comandos)


def main():
    """
    Função principal
    """
    parte = 0
    total = 16

    # Verificando versão do sistema operacional
    parte += 1
    print("(", parte, "/", total, ")", "Verificando versão do sistema operacional")
    verificar_versao_sistema_operacional()

    # Instalando pré-requisitos
    parte += 1
    print("(", parte, "/", total, ")", "Instalando os softwares pre-requisitos")
    instalar_prerequisitos()

    # Atualizando o sistema
    parte += 1
    print("(", parte, "/", total, ")", "Atualizando o sistema")
    atualizar()

    # Fazendo download dos repositórios necessário
    parte += 1
    print("(", parte, "/", total, ")", "Adicionando os repositórios")
    adicionar_repositorios()
    instalar_programas_deb()

    # Atualizando as listas de repositórios
    parte += 1
    print("(", parte, "/", total, ")", "Atualizando a lista de repositórios")
    atualizar()

    # Obtendo automaticamente os novos drivers
    parte += 1
    print("(", parte, "/", total, ")", "Instalando os drivers")
    instalar_drivers()

    # Baixando e Instalando os pacotes apt
    parte += 1
    print("(", parte, "/", total, ")", "Instalando os pacotes pelo gerenciador de pacotes APT")
    instalar_programas_apt()

    # Instalando o flathub
    parte += 1
    print("(", parte, "/", total, ")", "Instalando o repositório flathub")
    instalar_flathub()

    # Baixando e Instalando os pacotes snap
    parte += 1
    print("(", parte, "/", total, ")", "Instalando pacotes snap")
    instalar_programas_snap()

    # Baixando e Instalando os pacotes pip
    parte += 1
    print("(", parte, "/", total, ")", "Instalando pacotes pip")
    instalar_programas_pip()

    # Instalando o compilador de Rust Lang e Go Lang
    parte += 1
    print("(", parte, "/", total, ")", "Instalando o compilador de Rust Lang")
    instalar_rust_lang()

    # Instalando o .NET SDK
    parte += 1
    print("(", parte, "/", total, ")", "Instalando o .NET SDK")
    instalar_dot_net_sdk()

    # Instalando o logisim
    parte += 1
    print("(", parte, "/", total, ")", "Instalando o Logisim")
    instalar_logisim()

    # Instalando a ultima versão do Youtube-dl
    parte += 1
    print("(", parte, "/", total, ")", "Instalando a ultima versão do Youtube-dl")
    instalar_youtube_dl()

    # Removendo programas inúteis
    parte += 1
    print("(", parte, "/", total, ")", "Desinstalando programas inúteis")
    desinstalar_programas_inuteis()

    # Configurando o Visual Studio Code
    parte += 1
    print("(", parte, "/", total, ")", "Configurando o Visual Studio Code")
    configurar_visual_studio_code()
    instalar_extensoes_visual_studio_code()

    # Criando alias
    parte += 1
    print("(", parte, "/", total, ")", "Criando alias")
    configurar_alias()

    # Saindo do terminal
    print("Instalação concluída!")


if __name__ == "__main__":
    main()
