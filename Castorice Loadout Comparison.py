# 3.2v3

character_level = 80
enemy_level = 90

class Castorice:
    def __init__(self, maxhp, cr, cd):
        self.max_hp = maxhp
        self.crit_rate = cr
        self.crit_dmg = cd
        self.base_spd = 95
        self.dragon_max_hp = 36000
        self.dragon_base_spd = 165
        self.dragon_multiplier = 0.336 + 0.392 + 0.476 # Talent lvl 10
        self.dragon_kamikaze_multplier = 0.56 * 6 # Talent lvl 10 * 6 instance
        self.skill_hp_consume = 0.3
        self.enhanced_skill_hp_consume = 0.4

class Character:
    def __init__(self, maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne):
        self.max_hp = maxhp
        self.buff_critrate = buffcr
        self.buff_critdmg = buffcd
        self.buff_tdmg = tdmg
        self.buff_truedmg = truedmg
        self.buff_respen = respen
        self.buff_defignore = defignore
        self.debuff_defreduct = defreduct
        self.debuff_vulnerability = vulne

class Lightcone(Character):
    def __init__(self, maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne):
        super().__init__(maxhp, buffcr, buffcd, tdmg, truedmg, respen, defignore, defreduct, vulne)


def get_sunday(maxhp, eidolons, lc):
    pass

castorice = Castorice(10000, 70, 200)

# enemy_def_multiply = (character_level + 20) / (((enemy_level + 20) * (1 - total_def_reduction - total_def_ignore)) + character_level + 20)

team = []
