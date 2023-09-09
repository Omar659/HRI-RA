 
#!/bin/bash

# Detect the package manager and set the installation command accordingly
if command -v pacman >/dev/null 2>&1; then
    PACKAGE_MANAGER="pacman"
    INSTALL_CMD="sudo pacman -S"
elif command -v apt-get >/dev/null 2>&1; then
    PACKAGE_MANAGER="apt"
    INSTALL_CMD="sudo apt-get install -y"
else
    echo "Unsupported package manager. Exiting."
    exit 1
fi

# Function to check if a package is installed
check_package() {
    if pacman -Qs "$1" >/dev/null 2>&1 || dpkg -l | grep -q "ii  $1 "; then
        echo "$1 already installed."
        return 0
    else
        return 1
    fi
}

# Function to check if a file or directory exists
check_file() {
    if [ -e "$1" ]; then
        echo "$1 already present."
        return 0
    else
        return 1
    fi
}

if ! check_package "unified-planning"; then
    pip install --pre -U unified-planning
fi

if ! check_file "up-pyperplan"; then
    git clone https://github.com/aiplan4eu/up-pyperplan
    pip install up-pyperplan/
fi

if ! check_file "up-fast-downward"; then
    git clone https://github.com/aiplan4eu/up-fast-downward
    pip install up-fast-downward/
fi

if ! check_package "openjdk-17-jdk"; then
    $INSTALL_CMD openjdk-17-jdk
fi

if ! check_file "up-enhsp"; then
    git clone https://github.com/aiplan4eu/up-enhsp.git
    pip install up-enhsp/
fi

if ! check_file "up-tamer"; then
    git clone https://github.com/aiplan4eu/up-tamer
    pip install up-tamer/
fi
