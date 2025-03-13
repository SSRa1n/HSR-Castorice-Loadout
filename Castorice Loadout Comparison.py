# 3.2v3

character_level = 80
enemy_level = 90

character_hp_substat = 0.432
character_cdmg = 2.00 # 200% CDMG for crit 

max_castorice_eidolon = 6
max_castorice_superimpose = 6
max_eidolon = 6
max_superimpose = 5

class Castorice:
    def __init__(self, eidolon, maxhp, cr, cd):
        self.eidolon = eidolon
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

        self.tdmg = (0.22 if eidolon >= 5 else 0.2) * 3
        self.truedmg = 0
        self.respen = (0.22 if eidolon >= 3 else 0.2)
        self.defignore = 0
        self.defreduct = 0
        self.vulnerability = 0
        self.turn = 3

class Character:
    def __init__(self, name, basehp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn):
        self.name = name
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
    def __init__(self, name, superimpose, maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn, userbasehp, usercdmg):
        super().__init__(name, maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn)
        self.superimpose = superimpose
        self.user_base_hp = userbasehp
        self.user_crit_damage = usercdmg

def get_lightcone(name:str, superimpose:int, stack:int):
    if name == 'Dance Dance Dance': # DDD
        lc = Lightcone(name, superimpose,0,0,0,0,0,0,0,0,0,1,953,0)
    elif name == 'Planetary Rendezvous': # Asta LC
        lc = Lightcone(name, superimpose,0,0,0,0.09+(0.03*superimpose),0,0,0,0,0,0,1058,0)
    elif name == 'Past Self in Mirror': # Ruan Mei's LC
        lc = Lightcone(name, superimpose,0,0,0,0.2*(0.04*superimpose),0,0,0,0,0,0,1058,0)
    elif name == 'Earthly Escapade': # Sparkle's LC
        lc = Lightcone(name, superimpose,0,0.09+(0.01*superimpose),0.21+(0.07*superimpose),0,0,0,0,0,0,0,1164,0.25+(0.07*superimpose))
    elif name == 'Poised to Bloom': # March harmony LC
        lc = Lightcone(name, superimpose,0,0,0.12+(0.04*superimpose),0,0,0,0,0,0,0,953,0)
    elif name == 'Flowing Nightglow': # Robin's LC
        lc = Lightcone(name, superimpose,0,0,0,0.2+(0.04*superimpose),0,0,0,0,0,0,953,0)
    elif name == 'A Grounded Ascent': # Sunday's LC
        lc = Lightcone(name, superimpose,0,0,0,(0.1275+(0.0225*superimpose))*stack,0,0,0,0,0,0,1164,0)
    elif name == 'If Time Were a Flower': # Tribbie's LC
        lc = Lightcone(name, superimpose,0,0,0.36+(0.12*superimpose),0,0,0,0,0,0,0,1270,0.3+(0.06*superimpose))
    else:
        lc = Lightcone(name, superimpose,0,0,0,0,0,0,0,0,0,0,953,0)
    return lc

def get_character(name:str, eidolon:int, lightcone:Lightcone):
    if name == 'Ruan Mei':
        basehp = 1087 + lightcone.user_base_hp
        tdmg = 0.36 + (0.352 if eidolon >= 5 else 0.32) + lightcone.buff_tdmg
        respen = (0.27 if eidolon >= 3 else 0.25) + lightcone.buff_respen
        defignore = (0.2 if eidolon >= 1 else 0) + lightcone.buff_defignore
        character = Character(name, basehp,lightcone.buff_critrate,lightcone.buff_critdmg,tdmg,lightcone.buff_truedmg,respen,defignore,lightcone.debuff_defreduct,lightcone.debuff_vulnerability,lightcone.bonusturn)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
    elif name == 'Sparkle':
        basehp = 1397 + lightcone.user_base_hp
        sparkle_cdmg = character_cdmg + lightcone.user_crit_damage
        buffcdmg = ((0.264 * sparkle_cdmg) + 0.486 if eidolon >= 3 else (0.24 * sparkle_cdmg) + 0.45) + ((0.3 * sparkle_cdmg) if eidolon >= 6 else 0) + lightcone.buff_critdmg
        tdmg = (0.066 + 0.108 if eidolon >= 5 else 0.06 + 0.1) * 3
        defignore = ((0.08 if eidolon >= 2 else 0) * 3) + lightcone.buff_defignore
        character = Character(name, basehp, lightcone.buff_critrate, buffcdmg, tdmg, lightcone.buff_truedmg, lightcone.buff_respen, defignore, lightcone.debuff_defreduct, lightcone.debuff_vulnerability, 2 + lightcone.bonusturn)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
    elif name == 'Robin':
        basehp = 1281 + lightcone.user_base_hp
        buffcdmg = (0.23 if eidolon >= 5 else 0.2) + buffcdmg
        tdmg = (0.55 if eidolon >= 2 else 0.5) + lightcone.buff_tdmg
        respen = (0.24 if eidolon >= 1 else 0) + lightcone.buff_respen
        character = Character(name, basehp, lightcone.buff_critrate, buffcdmg, tdmg, lightcone.buff_tdmg, respen, lightcone.buff_defignore, lightcone.debuff_defreduct, lightcone.debuff_vulnerability, 1)
        # No HP substat as robin prioritizes ATK
    elif name == 'Sunday':
        basehp = 1242 + lightcone.user_base_hp
        sunday_cdmg = character_cdmg + lightcone.user_crit_damage
        buffcr = (0.22 if eidolon >= 5 else 0.2) * (3 if eidolon >= 6 else 1) + lightcone.buff_critrate
        buffcdmg = ((0.336 * sunday_cdmg) + 0.128 if eidolon >= 3 else (0.3 * sunday_cdmg) + 0.12) + lightcone.buff_critdmg
        tdmg = ((0.33 + 0.55) if eidolon > 5 else (0.3 + 0.5)) + (0.3 if eidolon >= 2 else 0) + lightcone.buff_tdmg
        defignore = (0.4 if eidolon >= 1 else 0) + lightcone.buff_defignore
        character = Character(name, basehp, buffcr, buffcdmg, tdmg, lightcone.buff_truedmg, lightcone.buff_respen, defignore, lightcone.debuff_defreduct, lightcone.debuff_vulnerability, 2 + lightcone.bonusturn)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
    elif name == 'Tribbie':
        basehp = 1048 + lightcone.user_base_hp
        respen = (0.264 if eidolon >= 5 else 0.24) + lightcone.buff_respen
        vuln = (0.33 if eidolon >= 3 else 0.3) + lightcone.debuff_vulnerability
        defignore = (0.18 if eidolon >= 4 else 0) + lightcone.buff_defignore
        truedmg = 0.24 + lightcone.buff_truedmg
        character = Character(name, basehp, lightcone.buff_critrate, lightcone.buff_critdmg, lightcone.buff_tdmg, truedmg, respen, defignore, lightcone.debuff_defreduct, vuln, lightcone.bonusturn)
    elif name == 'RMC':
        lightcone = Lightcone(5,0,0,0,0.16*3,0,0,0,0,0,0,1058,0) # Memory's Curtain Never Falls
        basehp = 1048 + lightcone.user_base_hp
        buffcr = 0.1 + lightcone.buff_critrate
        buffcd = (0.132 * character_cdmg) + 0.264 + lightcone.buff_critdmg
        truedmg = 0.3 + lightcone.buff_truedmg
        character = Character(name, basehp, buffcr, buffcd, 0, truedmg, 0, 0, 0, 0, 1)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
    elif name == 'Pela':
        lightcone = Lightcone('Resolution Shines As Pearls of Sweat',5,0,0,0,0,0,0,0,0.16,0,0,953,0)
        basehp = 988 + lightcone.user_base_hp
        defreduct = 0.42 + lightcone.debuff_defreduct
        character = Character(name, basehp, 0, 0, 0, 0, 0, 0, defreduct, 0, 0)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
    return character

castorice = Castorice(0, 9500, 70, 200, 0)

# enemy_def_multiply = (character_level + 20) / (((enemy_level + 20) * (1 - total_def_reduction - total_def_ignore)) + character_level + 20)

# TODO: Check Sunday E6 excess CR buff
# TODO: Check Tribbie HP trace

team = []
newbud_regen = sum(castorice.skill_hp_consume * member.max_hp for member in team) 