import random


class Character:
    def __init__(self, type, health, level, strength, defense, weapons, name='default'):
        self.type = type
        self.health = health
        self.level = level
        self.strength = strength
        self.defense = defense
        self.weapons = weapons
        self.name = name

    def attack_phrases(self, damage, enemy):
        player_phrases = {'cheers': ["Ну же, целься в голову!",
                                     "Не перживай, дажу у самых лучших бывают промахи.",
                                     "Ещё бы. Ты его вообще видел?", "Кажись, тебе *****."],
                          'failphrases': [
                              'Ты делаешь неудачный выпад, твоя нога подскальзывается на камне выворачиваясь'
                              ' под неестественным углом.',
                              'Замахиваясь, ты отвлёкся на пролетающую мимо '
                              'бабочку, и траектория удара сместилась в сторону твоего колена.',
                              'Ты вдруг вспомнил, что в школе тебя обызвали плюшкой и эта психологическая '
                              'травма бьёт сильнее любого меча.'],
                          'battle': [f"Ты получаешь {damage} урона.",
                                     f"У тебя осталось {self.health} здоровья.\n",
                                     f"\nТы наносишь врагу {enemy.name} {damage} урона!",
                                     f"У {enemy.name} осталось {enemy.health} здоровья.\n",
                                     f"\nТы промахиваешся по {enemy.name}!\n"]}
        enemy_phrases = {'cheers': ["Повезло-полвезло",
                                    "Над ухом просвистело",
                                    "Хаха, пни его в ответ",
                                    "Кажись, ему *****."],
                         'failphrases': [f"\n{self.name} раскручивается на месте для удара\nно не справляется с управл"
                                         f"eнием и падает в грязь.",
                                         f"\n{self.name} изменился в лице, кажется ему внезапоно приспичило\nи он "
                                         f"вынужден терпеть.",
                                         f"\nЗамахиваясь {self.name} бьёт себя по хребту. Ну что за кадр?"],
                         'battle': [f"{self.name} получает {damage} урона.",
                                    f"У {self.name} осталось {self.health} здоровья.\n",
                                    f"{self.name} наносит тебе {damage} урона!",
                                    f"У тебя осталось {enemy.health} здоровья.\n",
                                    f"{self.name} промахивается\n"]}

        if self.type == 'player':
            return player_phrases
        else:
            return enemy_phrases

    def attack(self, enemy, weapon):
        hit_throw = random.randint(1, 20)
        weapon_damage = random.randint(weapon["damage"][0], weapon["damage"][1])
        hit = hit_throw + self.strength
        damage = weapon_damage + self.level + self.strength
        if hit_throw == 1:
            print(random.choice(self.attack_phrases(damage, enemy)['failphrases']))
            self.health = self.health - weapon_damage
            print(self.attack_phrases(weapon_damage, enemy)['battle'][0])
            if self.health > 0:
                print(self.attack_phrases(damage, enemy)['battle'][1])
        elif hit > enemy.defense:
            enemy.health = enemy.health - damage
            print(self.attack_phrases(damage, enemy)['battle'][2])
            if enemy.health > 0:
                print(self.attack_phrases(damage, enemy)['battle'][3])
        else:
            print(self.attack_phrases(damage, enemy)['battle'][4] +
                  f"{random.choice(self.attack_phrases(damage, enemy)['cheers'])}\n")

    def block(self):
        block = self.defense / 2
        print("\nТы как можешь закрываешься и вертишься из стороны в сторону.\n"
              f"Твой показатель защиты повышен на +{block} на 3 хода.\n")
        return block