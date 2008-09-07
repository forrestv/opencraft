import struct

def readitem((name, type, start)):
    dat.seek(start)
    type = '<228%s' % type
    return struct.unpack(type, dat.read(struct.calcsize(type)))

class UnitType(object):
    def __init__(self, number, attrs):
        #self.name = t[number]
        for (name, type, start), attr in zip(fields, attrs):
            setattr(self, name, attr)
        
        self.unit_hitpoints /= 256.
        if not self.unit_hasshields:
            self.unit_shields = None
        del self.unit_hasshields

fields = [
    ('sprite_general', 'B', 0),		# 228
    ('unit_subunit1', 'H', 228),	# 684
    ('unit_subunit2', 'H', 684),	# 912
    ('sprite_build', 'H', 912),		# 1140
    ('sprite_overlay', 'H', 1140),	# 1596
    
    ('unknown_1', 'B', 2244),		# 2472
    # 1 byte
    ('unit_hasshields', 'B', 2472), 	# 2700
    # -1 byte
    ('unit_shields', 'H', 2700), 	# 3156
    ('unit_hitpoints', 'I', 3156),	# 4068
    ('sprite_level', 'B', 4068),	# 4296
    ('unit_movement', 'B', 4296),	# 4524
    ('sublabel', 'B', 4524),		# 4752
    ('ai_computeridle', 'B', 4752),	# 4980
    ('ai_humanidle', 'B', 4980),	# 5208
    ('ai_unknown', 'B', 5208),		# 5436
    ('ai_attacktarget', 'B', 5436),	# 5664
    ('ai_attackmove', 'B', 5664),	# 5892
    ('weapon_ground', 'B', 5892),	# 6120
    ('weapon_groundc', 'B', 6120),	# 6348
    ('weapon_air', 'B', 6348),		# 6576
    ('weapon_airc', 'B', 6576),		# 6840
    ('unknown_2', 'B', 6804),		# 7032
    ('unit_ability', 'I', 7032),	# 7944
    ('unit_subunitrng', 'B', 7944),	# 8172
    ('unit_sight', 'B', 8172),		# 8400
    ('unit_armorup', 'B', 8400),	# 8628
    ('unit_size', 'B', 8628),		# 8856
    ('unit_armor', 'B', 8856),		# 9084
    ('unknown_3', 'B', 9084),		# 9312
    # 14.333
    ('unit_width', 'H', 12580),		# 13036
    ('unit_height', 'H', 13036),	# 13492
    ('sprite_selw', 'H', 13492),	# 13948
    ('sprite_selh', 'H', 13948),	# 14404
    ('sprite_portrait', 'H', 14404),	# 14860
    ('build_minerals', 'H', 14860),	# 15316
    ('build_gas', 'H', 15316),		# 15772
    ('build_time', 'H', 15772),		# 16228
    ('unit_restricts', 'H', 16228),	# 16684
    ('unit_team', 'B', 16684),		# 16912
    ('food_provided', 'B', 16912),	# 17140
    ('food_required', 'B', 17140),	# 17368
    ('space_required', 'B', 17368),	# 17596
    ('space_provided', 'B', 17596),	# 17824
    ('score_produce', 'H', 17824),	# 18280
    ('score_destroy', 'H', 18280),	# 19192
    ('unit_game', 'B', 19192),		# 19420
    ('unit_available', 'H', 19420),	# 19876
]

#import tbl
#t = tbl.read(open("stat_txt.tbl"))

dat = open('units.dat')
units = [UnitType(number, field) for number, field in enumerate(zip(*map(readitem, fields)))]

for i, x in enumerate(units):
    print i, x.unit_shields
