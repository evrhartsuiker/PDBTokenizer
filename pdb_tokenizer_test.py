"""This program is meant only as an automated test for the pdb_tokenizer.py program"""

import sys

from pathlib import Path

from pdb_tokenizer import Cipher, PDBTokenizer

def main():
    """Main"""
    input_dir = Path.joinpath(Path.cwd() / 'data/input')

    cipher = Cipher()

    tokenizer = PDBTokenizer(cipher=cipher,
                             min_len=5,
                             max_len=10)

    tokenizer.parse_pdbs(n_cores=1, input_dir=input_dir)

    tokenizer.prepare_train_valid(source_language='source_test',
                                  target_language='target_test')


if __name__ == '__main__':
    sys.exit(main())
