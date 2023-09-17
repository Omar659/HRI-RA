#!/bin/bash

# pip install --pre -U unified-planning
pip install unified-planning
pip install unified-planning[fast-downward]

rm -rf up-pyperplan
git clone https://github.com/aiplan4eu/up-pyperplan
pip install up-pyperplan/

rm -rf up-fast-downward
git clone https://github.com/aiplan4eu/up-fast-downward
pip install up-fast-downward/

# apt-get install openjdk-17-jdk      # Ubuntu
sudo pacman -S jdk17-openjdk        # Arch-linux
rm -rf up-enhsp
git clone https://github.com/aiplan4eu/up-enhsp.git
pip install up-enhsp/

rm -rf up-tamer
git clone https://github.com/aiplan4eu/up-tamer
pip install up-tamer/

pip install flask
pip install flask_restful
pip install flask_cors
pip install inputimeout