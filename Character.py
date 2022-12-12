import random


class Character:
    def __init__(self, type, health, level, strength, defense, inventory, name='default'):
        self.type = type
        self.health = health
        self.level = level
        self.strength = strength
        self.defense = defense
        self.name = name
        self.inventory = inventory
        self.unknown_command = "\nНеопознанная команда"

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

    def weapon_attack(self, enemy, weapon):
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

    def filter_inventory(self, items_type: str) -> dict:
        filtered_items = {}
        for item in self.inventory:
            if self.inventory[item]["type"] == items_type:
                filtered_items.update({item: self.inventory[item]})
        return filtered_items

    def show_item_description(self, item):
        showing_description = True
        while showing_description:
            try:
                print(f"\n{self.inventory[item]['name']}\n"
                      f"{self.inventory[item]['description']}")
                if self.inventory[item]["hp"] > 0:
                    print(f"Восстанавливает {self.inventory[item]['hp']} здоровья")
                if self.inventory[item]["mp"] > 0:
                    print(f"Восстанавливает {self.inventory[item]['mp']} энергии")
                if self.inventory[item]["damage"] != "":
                    print(f"Наносит {self.inventory[item]['damage'][0]}-{self.inventory[item]['damage'][1]} урона")

                print("\n1. Использовать\n"
                      "0. Назад")
                use = int(input("Выбери вариант: "))
                if use == 1:
                    return self.inventory[item]
                elif use == 0:
                    showing_description = False
                    break
                else:
                    print(self.unknown_command)
                    continue
            except ValueError:
                print(self.unknown_command)
                continue

    def pick_item(self, items):
        picking = True
        while picking:
            try:
                print('')
                for item in list(items.keys()):
                    print(f"{list(items.keys()).index(item) + 1}. {item}")
                print(f"0. Назад")
                item_pick = int(input("Выбери вариант: "))
                picked_item = list(items.keys())[item_pick - 1]
                if item_pick > len(list(items.keys())) or item_pick < 0:
                    print(self.unknown_command)
                    continue
                elif item_pick == 0:
                    picking = False
                    break
                description_and_pick = self.show_item_description(picked_item)
                if description_and_pick is None:
                    continue
                else:
                    return description_and_pick
            except ValueError:
                print(self.unknown_command)






            # try:
            #     print("\n1. Использовать")
            #     print("0. Назад")
            #     pick = int(input("Выбери вариант:"))
            #     if pick > 2 or pick < 0:
            #         print(self.unknown_command)
            #         continue
            #     elif pick == 0:
            #         break
            #     return self.inventory[item]
            # except ValueError:
            #     print(self.unknown_command)

# dont forget to remove дубина and all other stuff
Player = Character('player', 40, 1, 3, 10,
                   inventory={"золото": {"type": "currency", "quantity": 0},
                              "Рука": {"type": "weapon",
                                       "name": "Рука",
                                       "damage": [1, 4],
                                       "hp": 0,
                                       "mp": 0,
                                       "description": "Ты не совсем боец, но на безрыбье и рак - рыба (твоя рука - рак,"
                                                      " смекаешь?)"},
                              "Яблоко": {"type": "consumables",
                                         "name": "Яблоко",
                                         "hp": 3,
                                         "mp": 0,
                                         "damage": "",
                                         "description": f"Восстанавливает здоровье"}
                              }
                   )
