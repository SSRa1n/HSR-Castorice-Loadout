# 3.2v3

character_level = 80
enemy_level = 90

character_hp_substat = 0.432
character_cdmg = 2.00 # 200% CDMG for crit buffer

class Castorice:
    def __init__(self, maxhp, cr, cd):
        self.max_hp = maxhp
        self.crit_rate = cr
        self.crit_dmg = cd
        self.base_spd = 95
        self.dragon_max_hp = 36000
        self.dragon_base_spd = 165
        self.dragon_multiplier = 0.336 + 0.392 + 0.476 # Talent lvl 10
        self.dragon_kamikaze_multplier = 0.56 # Talent lvl 10
        self.dragon_kamikaze_instance = 6 # Each instance calculates CRIT seperately
        self.skill_hp_consume = 0.3
        self.enhanced_skill_hp_consume = 0.4

class Character:
    def __init__(self, basehp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn):
        self.base_hp = basehp
        self.max_hp = basehp
        self.buff_critrate = buffcr
        self.buff_critdmg = buffcd
        self.buff_tdmg = tdmg
        self.buff_truedmg = truedmg
        self.buff_respen = respen
        self.buff_defignore = defignore
        self.debuff_defreduct = defreduct
        self.debuff_vulnerability = vulne
        self.bonusturn = bonusturn

class Lightcone(Character):
    def __init__(self, superimpose, maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn, userbasehp, usercdmg):
        super().__init__(maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn)
        self.superimpose = superimpose
        self.user_base_hp = userbasehp
        self.user_crit_damage = usercdmg

def get_lightcone(name:str, superimpose:int, stack:int):
    if name == 'Dance Dance Dance': # DDD
        lc = Lightcone(superimpose,0,0,0,0,0,0,0,0,0,1,953,0)
    elif name == 'Planetary Rendezvous': # Asta LC
        lc = Lightcone(superimpose,0,0,0,0.09+(0.03*superimpose),0,0,0,0,0,0,1058,0)
    elif name == 'Past Self in Mirror': # Ruan Mei's LC
        lc = Lightcone(superimpose,0,0,0,0.2*(0.04*superimpose),0,0,0,0,0,0,1058,0)
    elif name == 'Earthly Escapade': # Sparkle's LC
        lc = Lightcone(superimpose,0,0.09+(0.01*superimpose),0.21+(0.07*superimpose),0,0,0,0,0,0,0,1164,0.25+(0.07*superimpose))
    elif name == 'Poised to Bloom': # March harmony LC
        lc = Lightcone(superimpose,0,0,0.12+(0.04*superimpose),0,0,0,0,0,0,0,953,0)
    elif name == 'Flowing Nightglow': # Robin's LC
        lc = Lightcone(superimpose,0,0,0,0.2+(0.04*superimpose),0,0,0,0,0,0,953,0)
    elif name == 'A Grounded Ascent': # Sunday's LC
        lc = Lightcone(superimpose,0,0,0,(0.1275+(0.0225*superimpose))*stack,0,0,0,0,0,0,1164,0)
    elif name == 'If Time Were a Flower': # Tribbie's LC
        lc = Lightcone(superimpose,0,0,0.36+(0.12*superimpose),0,0,0,0,0,0,0,1270,0.3+(0.06*superimpose))
    else:
        lc = Lightcone(superimpose,0,0,0,0,0,0,0,0,0,0,953,0)
    return lc

def get_character(name:str, eidolon:int, lightcone:Lightcone):
    if name == 'Ruan Mei':
        basehp = 1087 + lightcone.user_base_hp
        tdmg = 0.36 + (0.352 if eidolon >= 5 else 0.32) + lightcone.buff_tdmg
        respen = (0.27 if eidolon >= 3 else 0.25) + lightcone.buff_respen
        defignore = (0.2 if eidolon >= 1 else 0) + lightcone.buff_defignore
        character = Character(basehp,lightcone.buff_critrate,lightcone.buff_critdmg,tdmg,lightcone.buff_truedmg,respen,defignore,lightcone.debuff_defreduct,lightcone.debuff_vulnerability,lightcone.bonusturn)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
    elif name == 'Sparkle':
        basehp = 1397 + lightcone.user_base_hp
        buffcdmg = ((0.264 * character_cdmg) + 0.486 if eidolon >= 3 else (0.24 * character_cdmg) + 0.45) + lightcone.buff_critdmg
    return character

castorice = Castorice(10000, 70, 200)

# enemy_def_multiply = (character_level + 20) / (((enemy_level + 20) * (1 - total_def_reduction - total_def_ignore)) + character_level + 20)

team = []
total_hp_consume = sum(castorice.skill_hp_consume * member.max_hp for member in team)