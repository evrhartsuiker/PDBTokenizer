# Tokenizing PDB files for transformer model training

Created by Ruben Hartsuiker, Hanze University of Applied Sciences

## Usage
This repository contains the module pdb_tokenizer.py. A python script intented to process pdb files into a tokenized representation to be used for machine learning. The polypeptide of the PDB is parsed into sentences with amino acids pairs as words. The dihedral angles (phi- and psi- angles) are also parsed into sentences. Creating a new language that a transformer encoder decoder based translator can be trained on. 

## Deployment
Follow the installation guide.

### Conda Setup
These four commands quickly and quietly install the latest 64-bit version of the installer and then clean up after themselves. To install a different version or architecture of Miniconda for Linux, change the name of the .sh installer in the wget command.

```console
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:

```console
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

Refresh the bashrc

```console
source ~/.bashrc
```

Create and activate a new python virtual environment

```console
conda create --name venv python=3.12.0
conda activate venv
```

### Installing Dependencies

If all has gone corretly you should see a (venv) in front of you prompt. If not repeat the last steps.

Install the dependencies using the supplied requirements file. See the file dependencies/requirements.txt for package and version details.

```console
pip install -r dependencies requirements.txt
```





