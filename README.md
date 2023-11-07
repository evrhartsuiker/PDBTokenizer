# Tokenizing PDB files for transformer model training

Created by Ruben Hartsuiker, Hanze University of Applied Sciences

## Usage
This repository contains the module pdb_tokenizer.py. A python script intented to process pdb files into a tokenized representation to be used for machine learning. The polypeptide of the PDB is parsed into sentences with amino acids pairs as words. The dihedral angles (phi- and psi- angles) are also parsed into sentences. Creating a new language that a transformer encoder decoder based translator can be trained on. 

## Deployment
Follow the installation guide that matches your OS.

[Linux](###Linux)
[MacOS](###MacOS)
[Windows](###Windows)

### Linux
These four commands quickly and quietly install the latest 64-bit version of the installer and then clean up after themselves. To install a different version or architecture of Miniconda for Linux, change the name of the .sh installer in the wget command.

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:

~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

### MacOS
These four commands quickly and quietly install the latest M1 macOS version of the installer and then clean up after themselves. To install a different version or architecture of Miniconda for macOS, change the name of the .sh installer in the curl command.

mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:

~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh

### Windows
These three commands quickly and quietly install the latest 64-bit version of the installer and then clean up after themselves. To install a different version or architecture of Miniconda for Windows, change the name of the .exe installer in the curl command.

curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
start /wait "" miniconda.exe /S
del miniconda.exe

After installing, open the “Anaconda Prompt (miniconda3)” program to use Miniconda3. For the Powershell version, use “Anaconda Powershell Prompt (miniconda3)”.





