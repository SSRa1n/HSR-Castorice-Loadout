import itertools

# 3.2v3

character_level = 80
enemy_level = 90

character_hp_substat = 0.432
character_cdmg = 2.00 # 200% CDMG for crit 

max_castorice_eidolon = 6
max_castorice_superimpose = 1
max_eidolon = 6
max_superimpose = 1

class Castorice:
    def __init__(self, eidolon, cr, cd, lightcone):
        self.eidolon = eidolon
        self.base_spd = 95
        self.dragon_max_hp = 36000
        self.dragon_base_spd = 165
        self.dragon_multiplier = 0.336 + 0.392 + 0.476 # Talent lvl 10
        self.dragon_kamikaze_multplier = 0.56 # Talent lvl 10
        self.dragon_kamikaze_instance = 6 # Each instance calculates CRIT seperately
        self.skill_hp_consume = 0.3
        self.enhanced_skill_hp_consume = 0.4

        basehp = 1630
        self.base_hp = basehp + lightcone.base_hp
        self.max_hp = basehp * (1 + lightcone.max_hp + character_hp_substat)
        self.crit_rate = cr + lightcone.buff_critrate
        self.crit_dmg = cd + lightcone.buff_critdmg
        self.tdmg = ((0.22 if eidolon >= 5 else 0.2) * 3) + lightcone.buff_tdmg
        self.truedmg = 0 + lightcone.buff_truedmg
        self.respen = (0.22 if eidolon >= 3 else 0.2) + lightcone.buff_respen
        self.defignore = 0 + lightcone.buff_defignore
        self.defreduct = 0 + lightcone.debuff_defreduct
        self.vulnerability = 0 + lightcone.debuff_vulnerability
        self.turn = 3 + lightcone.bonusturn

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
        self.lightcone = None

class Lightcone(Character):
    def __init__(self, name, superimpose, maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn, userbasehp, usercdmg):
        super().__init__(name, maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne, bonusturn)
        self.superimpose = superimpose
        self.user_base_hp = userbasehp
        self.user_crit_damage = usercdmg

def get_lightcone(name:str, superimpose:int, stack:int):
    if name == 'Make Farewells More Beautiful':
        lc = Lightcone(name, superimpose,0.225+(0.075*superimpose),0,0,0,0,0,0.225+(0.015*superimpose),0,0,0,1270,0)
    elif name == 'Sweat Now, Cry Less':
        lc = Lightcone(name, superimpose,0,0.1+(0.02*superimpose),0,0.21+(0.03*superimpose),0,0,0,0,0,0,1058,0)
    elif name == 'Reminiscence':
        lc = Lightcone(name, superimpose,0,0,0,(0.07+(0.01*superimpose))*stack,0,0,0,0,0,0,0,0)
    # --------------------------------------------------------------------------------------------------------------#
    elif name == 'Dance Dance Dance': # DDD
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
    else: # Memory of the past / Meshing Cogs
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
        character.lightcone = lightcone
    elif name == 'Sparkle':
        basehp = 1397 + lightcone.user_base_hp
        sparkle_cdmg = character_cdmg + lightcone.user_crit_damage
        buffcdmg = ((0.264 * sparkle_cdmg) + 0.486 if eidolon >= 3 else (0.24 * sparkle_cdmg) + 0.45) + ((0.3 * sparkle_cdmg) if eidolon >= 6 else 0) + lightcone.buff_critdmg
        tdmg = (0.066 + 0.108 if eidolon >= 5 else 0.06 + 0.1) * 3
        defignore = ((0.08 if eidolon >= 2 else 0) * 3) + lightcone.buff_defignore
        character = Character(name, basehp, lightcone.buff_critrate, buffcdmg, tdmg, lightcone.buff_truedmg, lightcone.buff_respen, defignore, lightcone.debuff_defreduct, lightcone.debuff_vulnerability, 2 + lightcone.bonusturn)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
        character.lightcone = lightcone
    elif name == 'Robin':
        basehp = 1281 + lightcone.user_base_hp
        buffcdmg = (0.23 if eidolon >= 5 else 0.2) + lightcone.buff_critdmg
        tdmg = (0.55 if eidolon >= 2 else 0.5) + lightcone.buff_tdmg
        respen = (0.24 if eidolon >= 1 else 0) + lightcone.buff_respen
        character = Character(name, basehp, lightcone.buff_critrate, buffcdmg, tdmg, lightcone.buff_tdmg, respen, lightcone.buff_defignore, lightcone.debuff_defreduct, lightcone.debuff_vulnerability, 1)
        character.lightcone = lightcone
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
        character.lightcone = lightcone
    elif name == 'Tribbie':
        basehp = 1048 + lightcone.user_base_hp
        respen = (0.264 if eidolon >= 5 else 0.24) + lightcone.buff_respen
        vuln = (0.33 if eidolon >= 3 else 0.3) + lightcone.debuff_vulnerability
        defignore = (0.18 if eidolon >= 4 else 0) + lightcone.buff_defignore
        truedmg = 0.24 + lightcone.buff_truedmg
        character = Character(name, basehp, lightcone.buff_critrate, lightcone.buff_critdmg, lightcone.buff_tdmg, truedmg, respen, defignore, lightcone.debuff_defreduct, vuln, lightcone.bonusturn)
        # Trace's HP bonus will be added later as it calculates teammates' HP
        character.lightcone = lightcone
    elif name == 'RMC':
        lightcone = Lightcone(5,0,0,0,0.16*3,0,0,0,0,0,0,1058,0,0) # Memory's Curtain Never Falls
        basehp = 1048 + lightcone.user_base_hp
        buffcr = 0.1 + lightcone.buff_critrate
        buffcd = (0.132 * character_cdmg) + 0.264 + lightcone.buff_critdmg
        truedmg = 0.3 + lightcone.buff_truedmg
        character = Character(name, basehp, buffcr, buffcd, 0, truedmg, 0, 0, 0, 0, 1)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
        character.lightcone = lightcone
    elif name == 'Pela':
        lightcone = Lightcone('Resolution Shines As Pearls of Sweat',5,0,0,0,0,0,0,0,0.16,0,0,953,0)
        basehp = 988 + lightcone.user_base_hp
        defreduct = 0.42 + lightcone.debuff_defreduct
        character = Character(name, basehp, 0, 0, 0, 0, 0, 0, defreduct, 0, 0)
        character.max_hp = character.base_hp * (1 + character_hp_substat)
        character.lightcone = lightcone
    return character

# enemy_def_multiply = (character_level + 20) / (((enemy_level + 20) * (1 - total_def_reduction - total_def_ignore)) + character_level + 20)

# TODO: Check Sunday E6 excess CR buff
# TODO: Check Tribbie HP trace

available_char = ['Ruan Mei', 'Sparkle', 'Robin', 'Sunday', 'Tribbie', 'RMC', 'Pela']
available_lc = ['Dance Dance Dance', 'Planetary Rendezvous', 'Past Self in Mirror', 'Earthly Escapade', 
                'Poised to Bloom', 'Flowing Nightglow', 'A Grounded Ascent', 'If Time Were a Flower']

available_castorice_lc = ['Make Farewells More Beautiful', 'Sweat Now, Cry Less'] 
# Change 'Sweat Now, Cry Less' to 'Reminiscence' for F2P option #

# team = []
# newbud_regen = sum(castorice.skill_hp_consume * member.max_hp for member in team) 

team_combinations = list(itertools.combinations(available_char, 2))
print(f'team combinations : {team_combinations}')
eidolon_levels = list(range(max_eidolon + 1))

lightcones = available_lc
superimpose_levels = list(range(max_superimpose + 1))

all_possible_teams = []

for team in team_combinations:
    for eidolons in itertools.product(eidolon_levels, repeat=2):  # Eidolon levels for both characters
        for lightcone_choices in itertools.product(lightcones, repeat=2):  # Lightcones for both characters
            for superimposes in itertools.product(superimpose_levels, repeat=2):  # Superimpose levels for both characters
                for eidolon in range(max_castorice_eidolon+1):
                    for cas_lc in available_castorice_lc:
                        for cas_si in range(1, max_castorice_superimpose+1):
                            castorice_lc = get_lightcone(cas_lc, cas_si, 2)
                            castorice = Castorice(0, 70, 200, castorice_lc)
                            characters = []
                            for i in range(2):
                                lc_name = lightcone_choices[i]
                                superimpose = superimposes[i]

                                if superimpose == 0:
                                    lightcone = get_lightcone("Memories of the past", 5, 0)
                                else:
                                    lightcone = get_lightcone(lc_name, superimpose, stack=3)

                                character = get_character(team[i], eidolons[i], lightcone)
                                characters.append(character)

                            # Append the full team (Castorice + 2 other characters)
                            all_possible_teams.append((castorice, characters[0], characters[1]))

# Print out the total number of combinations
print(f"Total simulation compositions: {len(all_possible_teams)}")