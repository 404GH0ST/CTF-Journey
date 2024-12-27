#!/bin/bash

clear 
os=$(lsb_release -i  | cut -d':' -f2 | tr -d '[:space:]')
ver=$(lsb_release -d | cut -d':' -f2 | tr -d '[:space:]')

red="\e[1;32m"
green="\e[3;32m"
blue="\e[1;94m"
reset="\e[0m"

echo -ne "[!] This script will install${green} pwntools${reset},${green} gdb${reset}-${green}gef${reset} and ${green}python3-pip${reset} in your system, do you want to proceed? (Y/n): " 
read ans
echo -ne "${reset}"

if [[ "$ans" == "" || "$ans" == "y" || "$ans" == "Y" ]]; then
  # Install gdb - gef - python3-pip
  echo -e "\n${blue}[*] $os ver: ${green}${ver}${reset}"
  echo -e "\n${blue}[*] Installing${green} pwntools${blue}${reset}..\n"
  sudo apt update -y
  sudo apt install gdb python3-pip -y
  bash -c "$(curl -fsSL https://gef.blah.cat/sh)"

  # Install pwntools
  if [[ "$ver" == "24.0"* && "$os" == "Ububntu" ]]; then
    python3 -m pip install --upgrade pip --break-system-packages && python3 -m pip install --upgrade pwntools --break-system-packages
  else
    python3 -m pip install --upgrade pip && python3 -m pip install --upgrade pwntools
  fi
  echo -e "${green}[+] Done!${reset}"
fi