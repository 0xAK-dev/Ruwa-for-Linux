# Ruwa Linux Installer

A simple **Linux installer** for [Ruwa](https://github.com/LuskusDeus/Ruwa).

The installer downloads the selected Ruwa version, builds the project, installs the required application files, and creates a desktop entry.

![Ruwa Linux Installer](assets/preview.png)

![Ruwa Linux Installer](assets/Installed_Ruwa.png)

## Quick Start

Download the latest pre-compiled **AppImage** directly from [Releases](../../releases):

```bash
chmod +x Ruwa-*.AppImage
./Ruwa-*.AppImage
```

## Manual Installation (Build from Source)

## Features

- Select the Ruwa version to install
- Select a custom installation directory
- Automatically clone the required Git tag
- Build Ruwa from source
- Install application binaries and resources
- Install shared libraries
- Install shaders, effects and plugins
- Create a `.desktop` launcher
- Configure environment variables
- Support for custom installation paths

## Requirements
Install the dependencies:

### Arch Linux

```bash
sudo pacman -S base-devel cmake ninja git qt6-base qt6-tools
```

### Ubuntu

```bash
sudo apt install python3-venv build-essential cmake ninja-build git qt6-base-dev qt6-tools-dev
```
### Fedora
```bash
sudo dnf install python3 python3-devel cmake ninja-build git gcc gcc-c++ qt6-qtbase-devel qt6-qttools-devel
```


## Installation Steps
### Source code
```bash
git clone https://github.com/0xAK-dev/Ruwa-Linux-Installer.git
cd Ruwa-Linux-Installer
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python installer_window.py
```