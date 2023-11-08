"""This program is used for parsing PDB files into amino acid pairs and dihedral angle pairs
to be used as training data for transformer algoritms.
"""

import multiprocessing
import random
import sys
import warnings

from pathlib import Path
from typing import List, Generator

import yaml

from Bio.PDB import DSSP
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning


class Cipher():
    """A Cipher object is designed to encrypt the numerical values of phi- and psi-angles
    to a word representation.

    Attributes:
        encrypt_map: dictionary with original as keys and encryption as values
        decrypt_map: dictionary with encryption as keys and original as values
    """
    def __init__(self,
                 keys: str = '0123456789 ',
                 values: str = 'ABCDEFGHIJK'):
        """Inits Cipher

        Attributes (optional):
            keys: String with items for original representation
            values: String with items for encrypted representation
        """
        try:
            assert len(keys) == len(values)
            self.encrypt_map = dict(zip(list(keys), list(values)))
            self.decrypt_map = dict(zip(list(values), list(keys)))
        except AssertionError:
            error_msg = f'Length keys {len(keys)} is not equal to length values {len(values)}'
            raise IndexError(error_msg) from AssertionError

    def encrypt(self, original):
        """Encrypts elements using the encrypt map, if element is not present in map it is skipped
        Input: an iterable of elements
        Ouput: string of encrypted elements
        """
        try:
            iterable = iter(original)
        except TypeError:
            print(f'{original} is not iterable')
        return ''.join([self.encrypt_map[e] if e in self.encrypt_map else e for e in iterable])

    def decrypt(self, encrypted):
        """Decrypts elements using the decrypt map, if element is not present in map it is skipped
        Input: an iterable of elements
        Ouput: string of decrypted elements
        """
        try:
            iterable = iter(encrypted)
        except TypeError:
            print(f'{encrypted} is not iterable')
        return ''.join([self.decrypt_map[e] if e in self.decrypt_map else e for e in iterable])


class PDBTokenizer():
    """A PDBTokenizer object contains all the functions need to parse a pdb file
    into amino acids pair tokens and phi- psi-angle pair tokens to be used in a
    transformer algoritm

    Attributes:
        cipher: Cipher object for angle encryption

        min_len: Smallest length of amino acid/angle pair fragments
        max_len: = Greatest length of amino acid/angle pair fragments

        amino_acid_index: DSSP tuple index for the 1 letter representation of the amino acid
        phi_index: DSSP tuple index for the phi-angle
        psi_index: DSSP tuple index for the psi-angle

        split_lines: Dictionary for storing data split into train and validation data
    """
    def __init__(self,
                 cipher: Cipher,
                 min_len: int,
                 max_len: int,
                 ):
        """Inits PDBTokenizer

        Attributes:
            cipher: Cipher object
            min_len: Smallest length of amino acid/angle pair fragments
            max_len: = Greatest length of amino acid/angle pair fragments
        """
        try:
            assert min_len < max_len
            self.min_len = min_len
            self.max_len = max_len
        except AssertionError:
            error_msg = f'min_len: {min_len} must be smaller than max_len: {max_len}'
            raise TypeError(error_msg) from AssertionError

        self.cipher = cipher

        self.amino_acid_index = 1
        self.phi_index = 4
        self.psi_index = 5

        self.split_lines = {'train': [], 'valid': []}

    def get_residues(self, path: Path):
        """Extracts polypeptide residues of the first chain from a PDB file using DSSP
        Retuns list of DSSP tuples. Each tuple holds information about the residue on that
        position, see DSSP documentation for further information
        """
        parser = MMCIFParser()

        multiple_chains = False

        with warnings.catch_warnings():
            # Warnings become errors so except can catch them
            warnings.simplefilter('error')
            try:
                structure = parser.get_structure('_', path)
            except PDBConstructionWarning:
                multiple_chains = True
                warnings.simplefilter('ignore')
                structure = parser.get_structure('_', path)

        model = next(structure.get_models())
        dssp_model = DSSP(model, path)

        if multiple_chains:
            chain_a = dssp_model.keys()[0][0]
            subset_keys = [k for k in dssp_model.keys() if k[0] == chain_a]
            return [dssp_model[k] for k in subset_keys]

        return list(dssp_model)

    def yield_fragments(self, residues: List[tuple]):
        """Yields lists of DSSP residue tuples, length ranging from min_len to max_len"""
        n_residues = len(residues)

        for fragment_size in range(self.min_len, self.max_len):
            for i in range((n_residues + 1) - fragment_size):
                yield residues[i:i + fragment_size]

    def encrypt_angles(self, angles: int):
        """Transforms the phi- or psi-angle of a residue in a letter representation"""
        for angle in angles:
            angle_split = list(str(angle))
            while len(angle_split) < 3:
                angle_split = [' '] + angle_split
            yield self.cipher.encrypt(angle_split)

    def get_parsed_fragments(self, fragments: Generator):
        """Parses the lists of DSSP tuple residues to amino acid/angle pairs in
        string representation
        """
        parsed_fragments = []

        for frag in fragments:
            # for all residue tuples except the last
            # gets the 1 letter amino acid from the current and next residue tuples
            # joins them in a string seperated by a space
            # the end product can be seen as a sentence in which the aa pairs are words
            amino_acid_pairs = ' '.join([f'{frag[i][self.amino_acid_index]}' \
                                         f'{frag[i+1][self.amino_acid_index]}'
                                          for i in range(len(frag) - 1)])

            # +180 to get rid of negative values
            psi_angles = [round(frag[i][self.psi_index]) + 180 for i in range(len(frag) - 1)]
            phi_angles = [round(frag[i+1][self.phi_index]) + 180 for i in range(len(frag) - 1)]

            psi_words = self.encrypt_angles(psi_angles)
            phi_words = self.encrypt_angles(phi_angles)

            angle_words = ' '.join([a+' '+b for a, b in zip(psi_words, phi_words)])
            parsed_fragments.append(amino_acid_pairs + ',' + angle_words + '\n')

        return parsed_fragments

    def write_lines(self, lines: list, path: Path):
        """Writes all elements of a list to a file"""
        with open(path, 'w+', newline='\n', encoding='utf-8') as outfile:
            outfile.writelines(lines)

    def tokenize_pdb(self, pdb: Path):
        """Calls all functions to parse a pdb into amino acid/angle pairs and
        write the results to a file, main usage is for multiprocessing
        """
        residues = self.get_residues(pdb)

        tokenfile = Path.joinpath(Path.cwd() / 'data/output/tokens' /
                                  f'{self.min_len}_{self.max_len}_{pdb.stem}.csv')

        fragments = self.yield_fragments(residues)
        parsed_fragments = self.get_parsed_fragments(fragments)
        self.write_lines(parsed_fragments, tokenfile)

        evalfile = Path.joinpath(Path.cwd() / 'data/output/eval' / f'{pdb.stem}.csv')

        parsed_eval = self.get_parsed_fragments([residues])
        self.write_lines(parsed_eval, evalfile)

    def write_splitted_lines(self, source_language: str, target_language: str):
        """Writes the stored output of split_file to training/validation files"""
        for datatype, split_lines in self.split_lines.items():
            amino_acid_path = Path.joinpath(Path.cwd() / 'data/output' / datatype /
                                            f'{self.min_len}_{self.max_len}_{source_language}.txt')
            angles_path = Path.joinpath(Path.cwd() / 'data/output' / datatype /
                                        f'{self.min_len}_{self.max_len}_{target_language}.txt')

            random.shuffle(split_lines)

            with open(amino_acid_path, 'w+', encoding='utf-8') as amino_acidfile:
                with open(angles_path, 'w+', encoding='utf-8') as anglesfile:
                    for line in split_lines:
                        amino_acid_pairs, internal_angles = line.strip().split(',')
                        amino_acidfile.write(amino_acid_pairs + '\n')
                        anglesfile.write(internal_angles + '\n')

    def split_file(self, path: Path):
        """Takes a file and shuffles and splits the content for training/validation purposes"""
        with open(path, 'r', encoding='utf-8') as datafile:
            lines = datafile.readlines()
            n_lines = len(lines)

            split_point = round(n_lines / 100 * 80)

            random.shuffle(lines)

            self.split_lines['train'] += lines[0:split_point]
            self.split_lines['valid'] += lines[split_point:-1]

    def parse_pdbs(self, n_cores: int, input_dir: Path):
        """Calls tokenize_pdb() with multiprocessing, uses all pdb files with MMCIF format"""
        pdb_paths = Path.joinpath(Path.cwd() / input_dir).rglob('*.cif')
        try:
            n_cores = n_cores if n_cores else multiprocessing.cpu_count()
            with multiprocessing.Pool(n_cores) as pool:
                pool.map(self.tokenize_pdb, pdb_paths)
        finally:
            pool.close()
            pool.join()

    def prepare_train_valid(self, source_language: str, target_language: str):
        """Collects and reads all pdb token files, stores all the output of split_file() in a
        dictionary calls write_splitted_lines() which writes the combined tokes the
        train/valid files
        """
        tokenized_pdb_paths = Path.joinpath(Path.cwd() / 'data/output/tokens').rglob(
            f'{self.min_len}_{self.max_len}_*.csv')

        for tokenized_pdb in tokenized_pdb_paths:
            self.split_file(tokenized_pdb)

        self.write_splitted_lines(source_language, target_language)


def main():
    """Main"""
    configpath = Path.joinpath(Path.cwd() / 'config/config.yaml')
    with open(configpath, 'r', encoding='utf-8') as configfile:
        config = yaml.safe_load(configfile)

    input_dir = Path.joinpath(Path.cwd() / config['input_dir'])

    cipher = Cipher()

    tokenizer = PDBTokenizer(cipher=cipher,
                             min_len=config['min_fragment_len'],
                             max_len=config['max_fragment_len'])

    tokenizer.parse_pdbs(n_cores=config['n_cores'], input_dir=input_dir)

    tokenizer.prepare_train_valid(source_language=config['source_language'],
                                  target_language=config['target_language'])


if __name__ == '__main__':
    sys.exit(main())
