from bonzi.acsparse import *
import struct

def create_acs_string(s):
    acs_string = struct.pack("<I", len(s))
    if len(s) != 0:
        acs_string += s.encode('utf-16le') + b"\x00\x00"
    return acs_string


def replace_locator(old_acs, old_loc, data_offset, shift_size):
    # Data is inserted after where locator is pointing to
    # so no need to modify the ACSLocator data

    if data_offset >= old_loc.offset + old_loc.size:
        return old_acs
    
    if data_offset >= old_loc.offset:
        new_size = old_loc.size + shift_size
        new_offset = old_loc.offset
    else:
        new_offset = old_loc.offset + shift_size
        new_size = old_loc.size

    return old_acs[:old_loc.get_offset()] + struct.pack("<2I", new_offset, new_size) + old_acs[old_loc.get_offset()+old_loc.get_size():]
    

def modify_data(old_acs, modify_offset, modify_sz):
    if modify_sz == 0:
        return old_acs
    
    header = ACSHeader(old_acs, 0)
    character = ACSCharacterInfo(old_acs, header.loc_acscharacter.offset)
    animations = ACSList(old_acs, header.loc_acsanimation.offset, ACSAnimationInfo)
    images = ACSList(old_acs, header.loc_acsimage.offset, ACSImageInfo)
    audio = ACSList(old_acs, header.loc_acsaudio.offset, ACSAudioInfo)

    new_acs = old_acs
    new_acs = replace_locator(new_acs, header.loc_acscharacter, modify_offset, modify_sz)
    new_acs = replace_locator(new_acs, header.loc_acsanimation, modify_offset, modify_sz)
    new_acs = replace_locator(new_acs, header.loc_acsimage, modify_offset, modify_sz)
    new_acs = replace_locator(new_acs, header.loc_acsaudio, modify_offset, modify_sz)

    new_acs = replace_locator(new_acs, character.loc_localizedinfo, modify_offset, modify_sz)

    for a in animations:
        new_acs = replace_locator(new_acs, a.loc_animation, modify_offset, modify_sz)
    
    for i in images:
        new_acs = replace_locator(new_acs, i.loc_image, modify_offset, modify_sz)

    for a in audio:
        new_acs = replace_locator(new_acs, a.loc_audio, modify_offset, modify_sz)
    
    return new_acs


# Insert insert_data at insert_offset inside old_acs
def insert_data(old_acs, insert_data, insert_offset):
    new_acs = modify_data(old_acs, insert_offset, len(insert_data))
    new_acs = new_acs[:insert_offset] + insert_data + new_acs[insert_offset:]
    return new_acs

    
def replace_data(old_acs, replace_data, replace_offset, replace_sz):
    new_acs = modify_data(old_acs, replace_offset, len(replace_data)-replace_sz)
    new_acs = new_acs[:replace_offset] + replace_data + new_acs[replace_offset+replace_sz:]
    return new_acs


def replace_description(data, new_description):
    header = ACSHeader(data, 0)
    character = ACSCharacterInfo(data, header.loc_acscharacter.offset)

    localized_info = ACSList(data, character.loc_localizedinfo.offset, LocalizedInfo)
    to_replace = localized_info[0].desc
    new_acs = replace_data(data, create_acs_string(new_description), to_replace.get_offset(), to_replace.get_size())

    return new_acs