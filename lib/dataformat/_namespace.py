# Namespace-specific rules for e.g. object name conversions

import re

from exceptions import ObjectError

def Dataset_format_software_version(value):
    if type(value) is str:
        formatted = eval(value)
    elif type(value) is not tuple:
        # some iterable
        formatted = tuple(value)
    else:
        formatted = value

    if type(formatted) is not tuple or len(formatted) != 4:
        raise ObjectError('Invalid software version %s' % repr(value))

    return formatted

def Block_to_internal_name(name_str):
    # block name format: [8]-[4]-[4]-[4]-[12] where [n] is an n-digit hex.
    return long(name_str.replace('-', ''), 16)

def Block_to_real_name(name):
    full_string = hex(name).replace('0x', '')[:-1] # last character is 'L'
    if len(full_string) < 32:
        full_string = '0' * (32 - len(full_string)) + full_string

    return full_string[:8] + '-' + full_string[8:12] + '-' + full_string[12:16] + '-' + full_string[16:20] + '-' + full_string[20:]        

def Block_to_full_name(dataset_name, block_real_name):
    return dataset_name + '#' + block_real_name

def Block_from_full_name(full_name):
    # return dataset name, block internal name

    delim = full_name.find('#')
    if delim == -1:
        raise ObjectError('Invalid block name %s' % full_name)

    return full_name[:delim], Block_to_internal_name(full_name[delim + 1:])

def Site_to_pfn(self, lfn, protocol):
    return self.backend + lfn

def Site_to_lfn(self, lfn, protocol):
    return pfn.replace(self.backend, '')

def customize_dataset(Dataset):
    # Enumerator for dataset type.
    # Starting from 1 to play better with MySQL
    Dataset._data_types = ['unknown', 'align', 'calib', 'cosmic', 'data', 'lumi', 'mc', 'raw', 'test']
    for name, val in zip(Dataset._data_types, range(1, len(_data_types) + 1)):
        # e.g. Dataset.TYPE_UNKNOWN = 1
        setattr(Dataset, 'TYPE_' + name.upper(), val)

    Dataset.SoftwareVersion.field_names = ('cycle', 'major', 'minor', 'suffix')

    Dataset.name_pattern = re.compile('/[^/]+/[^/]+/[^/]+')

def customize_block(Block):
    Block.to_internal_name = Block_to_internal_name
    Block.to_real_name = Block_to_real_name
    Block.to_full_name = Block_to_full_name
    Block.from_full_name = Block_from_full_name

    hex_chars = '[0-9a-fA-F]'
    Block.name_pattern = re.compile('{h}{{8}}-{h}{{4}}-{h}{{4}}-{h}{{4}}-{h}{{12}}'.format(h = hex_chars))

def customize_blockreplica(BlockReplica):
    BlockReplica._use_file_ids = False

def customize_site(Site):
    Site.to_pfn = Site_to_pfn
    Site.to_lfn = Site_to_lfn
