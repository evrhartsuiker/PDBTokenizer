# Tokenizing PDB files for transformer model training

Created by Ruben Hartsuiker, Hanze University of Applied Sciences

## Introduction
This repository contains the module pdb_tokenizer.py. A python script intented to process pdb files into a tokenized representation to be used for machine learning. The polypeptide of the PDB is parsed into sentences with amino acids pairs as words. The dihedral angles (phi- and psi- angles) are also parsed into sentences. Creating a new language that a transformer encoder decoder based translator can be trained on. 

## Deployment
Follow the installation guide.

### Step 1: Setting up your workspace
Either [clone][clone] or [download][download] the repository

### Step 2: Installing Python
This module was developed in the language Python (version 3.12.0). Please follow the instructions on how to install Python [here][python].

### Step 3: Conda Setup
These four commands quickly and quietly install the latest 64-bit version of the installer and then clean up after themselves. To install a different version or architecture of Miniconda for Linux, change the name of the .sh installer in the wget command.

```{bash}
$ mkdir -p ~/miniconda3
```
```{bash}
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
```
```{bash}
$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
```
```{bash}
$ rm -rf ~/miniconda3/miniconda.sh
```

After installing, initialize your newly-installed Miniconda.

```{bash}
$ ~/miniconda3/bin/conda init bash
```

Refresh the bashrc

```{bash}
$ source ~/.bashrc
```

### Virtual environment setup
Create and activate a new python virtual environment

```{bash}
$ conda create --name venv python=3.12.0
```
```{bash}
$ conda activate venv
```

### Step 4: Installing Dependencies

If all has gone corretly you should see a (venv) in front of you prompt. If not repeat the last steps.

```console
(venv) $
```

Install DSSP using conda

```{bash}
$ conda install -c salilab dssp
```

Install the dependencies using the supplied requirements file. See the file [requirements.txt](dependencies/requirements.txt) for package and version details.

```{bash}
$ pip install -r dependencies requirements.txt
```

## Running the module
To use this program, move the pdb files you want tokenized to the [data/input](data/input) folder.

Next adjust the parameters in the [config file](config/config.yaml)

Run the module:

```{bash}
$ python pdb_tokenizer.py
```

## Testing
If the module is not working it might have broken down thanks to updates in the dependencies. To test if the code is still functional run the supplied test script:

```{bash}
$ python pdb_tokenizer_test.py
```

## Contact
If any issue or question remains, don't hesitate to get in touch with us at [r.hartsuiker@st.hanze.nl](mailto:r.hartsuiker@st.hanze.nl)

[clone]: https://github.com/evrhartsuiker/pdb_parser_for_ml.git
[download]: https://github.com/evrhartsuiker/pdb_parser_for_ml/src/master/
[python]: https://www.python.org/
