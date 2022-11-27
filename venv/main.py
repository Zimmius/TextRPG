import random


class Character:
    def __init__(self, type, health, level, strength, defense, weapons, name = 'default'):
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
        enemy_phrases = {'cheers':["Повезло-полвезло",
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
            if Enemy.health > 0:
                print(self.attack_phrases(damage, enemy)['battle'][3])
        else:
            print(self.attack_phrases(damage, enemy)['battle'][4] +
                  f"{random.choice(self.attack_phrases(damage, enemy)['cheers'])}\n")




    def block(self):
        block = self.defense / 5
        print("\nТы как можешь закрываешься и вертишься из стороны в сторону.\n"
              f"Твой показатель защиты повышен на +{block}.\n")
        return block


class Encounter:
    unknown_command = "Неопознанная команда"
    def dialogue(self, player_lines, other_lines):
        encounter = True
        print(f"{other_lines[1]}")
        print("Вы отвечаете:")
        while encounter == True:
            try:
                for line in player_lines:
                    print(f"{line}. {player_lines[line]}")
                line_pick = int(input("Выберите вариант: "))
                if line_pick > len(player_lines) or line_pick <= 0:
                    print(self.unknown_command)
                    continue
                encounter = False
                return line_pick
            except ValueError:
                print(self.unknown_command)


    def move(self):
        encounter = True
        while encounter:
            try:
                move = int(input("\n1. Попытаться подойти не привлекая внимания\n"
                                 "2. Подойти обычным шагом\n"
                                 "3. Подбежать крича... \n"
                                 "Выбери действие: "))
                if move == 1:
                    return move
                    break
                elif move == 2:
                    return move
                    break
                elif move == 3:
                    phrase = input("Введи фразу которую хочешь выкрикнуть: ")
                    return phrase
                    break
                else:
                    print(self.unknown_command)
            except ValueError:
                print(self.unknown_command)

    def battle(self, Player, Enemy):
        encounter = True;
        encounter_action = True;
        print(f"\nПеред тобой враг {Enemy.name} {Enemy.level}lvl!")
        while encounter_action:
            try:
                action = int(input("\nВыбери действие:"
                                   "\n1. Атаковать..."
                                   "\n2. Бежать"
                                   "\nВведи 1 или 2 и нажми Enter:\n"))
                if action == 1:
                    encounter;
                    break
                elif action == 2:
                    print(f"Ты в страхе бежишь от {Enemy.name}")
                    encounter = False
                    break
                else:
                    print(self.unknown_command)
                    encounter = False
            except ValueError:
                print(self.unknown_command)
                encounter = False

        while encounter:
            blocking = False;
            for weapon in Player.weapons:
                print(f"{weapon}. Использовать {Player.weapons[weapon]['name']}")
            print(f"{len(Player.weapons) + 1}. Сосредоточиться на защите")
            attack_choose = int(input("Выбери действие: "))
            if attack_choose == len(Player.weapons) + 1 and blocking == False:
                block = Player.block()
                Player.defense = Player.defense + block
                blocking = True
            else:
                Player.attack(Enemy, Player.weapons[attack_choose])
                print("Хп врага:", Enemy.health)
            if Enemy.health > 0:
                Enemy.attack(Player, Enemy.weapons[1])
                print("Хп игрока:", Player.health)
                if Player.health <= 0:
                    print("Game over, man")
                    encounter = False
            else:
                Player.level = Player.level + 1
                print(f"Ты одолел {Enemy.name} {Enemy.level}lvl! Твой уровень повышен. Текущий уровень {Player.level}.")
                encounter = False
            print(Player.defense)
            if blocking == True:
                Player.defense = Player.defense - block


Encounter1 = Encounter()
player_lines = {1: "-Bla bla!", 2: "-Ble ble!", 3: "-Blu Blu!"}
tavern_guard_lines = {1: "Стражник: -Стой, кто идёт!\n"}
player_weapons = {1: {"name": "Рука", "damage": [1, 4]}, 2: {"name": "Something else", "damage": [10, 15]}}
enemy_weapons = {1: {"name": "Дубина", "damage": [1, 4]}}
Enemy = Character('npc', 40, 1, 3,  10, enemy_weapons, "Стражник таверны")
Player = Character('player', 40, 1, 3, 10, player_weapons)



print("\nТы проснулся ночью в тёмном, сыром лесу. Через кроны густых виден тусклый свет луны, пробивающийся сквозь"
      " облака.\n"
      "Ты одет в простые одежды, кожанный жилет и потрёпанные старые сапоги. В голове пустота и ты не помнишь"
      " ни кто ты, ни как сюда попал.\n"
      "В далеке ты замечаешь еле различимый свет факелов. Ты решаешь:")


move = Encounter1.move()
if move == 1:
    print("\nПриближаясь ты видишь небольшую древянную хижину. \n"
          "Судя по стоящим у упряжи коням, и звукам\n"
          "доносящимся изнутри - это придорожная таверна. \n"
          "У входа стоит стражник одетый в легкую кольчугу\n"
          "и что-то насвистывает себе под нос. Он тебя не заметил.")
elif move == 2:
    print("\nПриближаясь ты видишь небольшую древянную хижину. \n"
          "Судя по стоящим у упряжи коням, и звукам\n"
          "доносящимся изнутри - это придорожная таверна. \n"
          "У входа стоит стражник одетый в легкую кольчугу\n"
          "При твоём приближении он поворачивается и обращается к тебе")
    guard_dialogue = Encounter1.dialogue(player_lines, tavern_guard_lines)
    print(guard_dialogue)
elif move == move:
    print(f"\nТы несётешься на свет как ополумевший и орёшь: {move} \n"
          "Подбегая ты видишь небольшую древянную хижину. \n"
          "У хижины стоит стражник одетый в легкую кольчугу.\n"
          "Ты замечаешь, как он смотрит на тебя ошалевшими глазами и достаёт деревянную дубину\n"
          "но ты уже не успеваешь остановиться")
    Encounter1.battle(Player, Enemy)