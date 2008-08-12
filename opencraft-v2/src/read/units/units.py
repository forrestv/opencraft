import struct

def readitem((name, type, start)):
    dat.seek(start)
    type = '<228%s' % type
    return struct.unpack(type, dat.read(struct.calcsize(type)))

class UnitType(object):
    def __init__(self, number, attrs):
        self.name = t[number]
        for (name, type, start), attr in zip(fields, attrs):
            setattr(self, name, attr)

fields = [
    ('sprite_general', 'B', 0),
    ('unit_subunit1', 'H', 228),
    ('unit_subunit2', 'H', 684),
    ('sprite_build', 'H', 912),
    ('sprite_overlay', 'H', 1140),
    ('unit_hitpoints', 'I', 3156),
    ('sprite_level', 'B', 4068),
    ('unit_movement', 'B', 4296),
    ('sublabel', 'B', 4524),
    ('ai_computeridle', 'B', 4752),
    ('ai_humanidle', 'B', 4980),
    ('ai_unknown', 'B', 5208),
    ('ai_attacktarget', 'B', 5436),
    ('ai_attackmove', 'B', 5664),
    ('weapon_ground', 'B', 5892),
    ('weapon_groundc', 'B', 6120),
    ('weapon_air', 'B', 6348),
    ('weapon_airc', 'B', 6576),
    ('unknown_2', 'B', 6804),
    ('unit_ability', 'I', 7032),
    ('unit_subunitrng', 'B', 7944),
    ('unit_sight', 'B', 8172),
    ('unit_armorup', 'B', 8400),
    ('unit_size', 'B', 8628),
    ('unit_armor', 'B', 8856),
    ('unit_width', 'H', 12580),
    ('unit_height', 'H', 13036),
    ('sprite_selw', 'H', 13492),
    ('sprite_selh', 'H', 13948),
    ('sprite_portrait', 'H', 14404),
    ('build_minerals', 'H', 14860),
    ('build_gas', 'H', 15316),
    ('build_time', 'H', 15772),
    ('unit_restricts', 'H', 16228),
    ('food_provided', 'B', 16912),
    ('food_required', 'B', 17140),
    ('space_required', 'B', 17368),
    ('space_provided', 'B', 17596),
    ('score_produce', 'H', 17824),
    ('score_destroy', 'H', 18280),
    ('unit_game', 'B', 19192),
    ('unit_available', 'H', 19420),
]

import tbl
t = tbl.read(open("stat_txt.tbl"))

dat = open('units.dat')
units = [UnitType(number, field) for number, field in enumerate(zip(*map(readitem, fields)))]
