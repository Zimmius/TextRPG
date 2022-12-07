class Encounter:
    def __init__(self, moves = {}, dialogues = {'player': ['default'], 'other': ['default']}):
        self.moves = moves
        self.dialogues = dialogues


    unknown_command = "Неопознанная команда"
    # def dialogue(self, player_lines, other_lines):
    #     encounter = True
    #     print(f"{other_lines[1]}")
    #     print("Вы отвечаете:")
    #     while encounter == True:
    #         try:
    #             for line in player_lines:
    #                 print(f"{line}. {player_lines[line]}")
    #             line_pick = int(input("Выберите вариант: "))
    #             if line_pick > len(player_lines) or line_pick <= 0:
    #                 print(self.unknown_command)
    #                 continue
    #             encounter = False
    #             return line_pick
    #         except ValueError:
    #             print(self.unknown_command)

    def dialogue(self, player_lines_numbers, other_lines_numbers):
        encounter = True
        player_lines = self.dialogues['player'][player_lines_numbers]
        print(f"{self.dialogues['other'][other_lines_numbers]}")
        print("Вы отвечаете:")
        while encounter == True:
            try:
                for line in player_lines:
                    print(f"{player_lines.index(line) + 1}. {line}")
                line_pick = int(input("Выберите вариант: "))
                if line_pick > len(player_lines) or line_pick <= 0:
                    print(self.unknown_command)
                    continue
                encounter = False
                return line_pick
            except ValueError:
                print(self.unknown_command)

#TODO: rebuild move() method to work with dict from Encounter object initialization
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
        block = None;
        block_duration = 3
        blocking = False
        encounter = True
        encounter_action = True
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
            for weapon in Player.weapons:
                print(f"{weapon}. Использовать {Player.weapons[weapon]['name']}")
            if blocking == False:
                print(f"{len(Player.weapons) + 1}. Сосредоточиться на защите")
            attack_choose = int(input("Выбери действие: "))
            if attack_choose == len(Player.weapons) + 1 and blocking == False:
                block = Player.block()
                blocking = True
            else:
                Player.attack(Enemy, Player.weapons[attack_choose])
                print("Хп врага:", Enemy.health)

            if blocking == True and block_duration == 3:
                Player.defense = Player.defense + block

            if block_duration > 0 and blocking == True:
                block_duration -= 1
            elif block_duration <= 0 and blocking == True:
                blocking = False
                Player.defense = Player.defense - block;
                block_duration = 3


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