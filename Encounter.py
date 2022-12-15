import random


class Encounter:
    def __init__(self, moves=[], dialogues={'player': ['default'], 'other': ['default']}, acquirable_loot={}):
        self.moves = moves
        self.dialogues = dialogues
        self.acquirable_loot = acquirable_loot
        self.prebattle_actions = ["Сразиться!", "Бежать!"]
        self.battle_actions = ["Атаковать...", "Использовать...", "Принять защитную стойку"]

    unknown_command = "\nНеопознанная команда"

    def pick_action(self, action_list):
        encounter = True
        while encounter:
            try:
                print("")
                for action in action_list:
                    print(f"{action_list.index(action) + 1}. {action}")
                action_pick = int(input("Выбери вариант: "))
                if action_pick > len(action_list) or action_pick <= 0:
                    print(self.unknown_command)
                    continue
                picked_action = action_list[action_pick - 1]
                encounter = False
                return picked_action
            except ValueError:
                print(self.unknown_command)
                continue

    # need to refactor, looks ugly. works strange.
    def loot(self, loot_list_slice, player):
        loot_list = list(self.acquirable_loot.keys())[loot_list_slice]
        looting = True
        while looting:
            try:
                for item in loot_list:
                    print(f"{loot_list.index(item) + 1}. {item}")
                if len(loot_list) == 0:
                    print("\nПусто")
                else:
                    print(f"{len(loot_list) + 1}. Забрать всё")
                print(f"0. Выйти")
                loot_pick = int(input("\nВыбери вариант: "))
                if loot_pick > len(loot_list) + 1 or loot_pick < 0:
                    print(self.unknown_command)
                    continue
                elif loot_pick == len(loot_list) + 1:
                    for item in loot_list:
                        if item == "золото":
                            new_gold = player.inventory[item]["quantity"] + self.acquirable_loot[item][
                                "quantity"]
                            player.inventory[item]["quantity"] = new_gold
                        else:
                            player.inventory.update({item: self.acquirable_loot[item]})
                        self.acquirable_loot.pop(item)
                    loot_list.clear()
                    continue
                elif loot_pick == 0:
                    looting = False
                    break
                picked_loot = loot_list[loot_pick - 1]
                if picked_loot == "золото":
                    new_gold = player.inventory[picked_loot]["quantity"] + \
                               self.acquirable_loot[picked_loot]["quantity"]
                    player.inventory[picked_loot]["quantity"] = new_gold
                    self.acquirable_loot.pop(picked_loot)
                    loot_list.remove(picked_loot)
                else:
                    player.inventory.update({picked_loot: self.acquirable_loot[picked_loot]})
                    self.acquirable_loot.pop(picked_loot)
                    loot_list.remove(picked_loot)
            except ValueError:
                print(self.unknown_command)
                pass

    def dialogue(self, player_lines_numbers, other_lines_numbers):
        player_lines = self.dialogues['player'][player_lines_numbers]
        print(f"{self.dialogues['other'][other_lines_numbers]}")
        print("Вы отвечаете:")
        return self.pick_action(player_lines)

    def move(self, moves_list_slice):
        moves_list = self.moves[moves_list_slice]
        return self.pick_action(moves_list)

    def battle(self, player, enemy):
        weapons = player.filter_inventory("weapon")
        block = None
        block_duration = 3
        blocking = False
        encounter = True
        encounter_action = True
        # prebattle action pick
        while encounter_action:
            try:
                print(f"\nПеред тобой враг {enemy.name} {enemy.level} уровня!")
                prebattle_action = self.pick_action(self.prebattle_actions)
                # to battle
                if prebattle_action == self.prebattle_actions[0]:
                    break
                # run
                elif prebattle_action == self.prebattle_actions[1]:
                    print(f"Ты в страхе бежишь от {enemy.name}")
                    encounter = False
                    return prebattle_action
                    break
                else:
                    print(self.unknown_command)
                    continue
            except ValueError:
                print(self.unknown_command)
                continue

        while encounter:
            action = self.pick_action(self.battle_actions)
            # weapon attack
            if action == self.battle_actions[0]:
                item = player.pick_item(weapons)
                if item is None:
                    continue
                player.weapon_attack(enemy, item)
            # use consumables
            elif action == self.battle_actions[1]:
                item = player.pick_item(player.filter_inventory("consumables"))
                if item is None:
                    continue
                print(f"\nТы используешь {item['name']} и")
                if item['damage'] != "":
                    print(f"наносишь {enemy.name}, {random.choice(item['damage'])} урона")
                if item['hp'] > 0:
                    player.heal(item)
                    print(f"восстанавливаешь {item['hp']} здоровья")
                    print(f"{player.health}")
                if item['mp'] > 0:
                    print(f"восстанавливаешь {item['mp']} 'энергии'")
                if item['arm'] > 0:
                    print(f"повышаешь защиту на {item['arm']}")
                print("")
            # def stance
            elif action == self.battle_actions[2]:
                if not blocking:
                    block = player.block()
                    blocking = True
                else:
                    print("\nНельзя применить защитную стойку, когда ты уже в ней")
                    continue
            # blocking logic (maybe sometime make standalone function?)
            if blocking and block_duration == 3:
                player.defense = player.defense + block
            if block_duration > 0 and blocking:
                block_duration -= 1
            elif block_duration <= 0 and blocking:
                blocking = False
                player.defense = player.defense - block
                block_duration = 3
            # check if enemy is alive, if it is then attack. If not: + exp to player and win message
            if enemy.health > 0:
                enemy.weapon_attack(player, enemy.inventory["Дубина"])
                print("Хп игрока:", player.health)
                if player.health <= 0:
                    print("\nGame over, man")
                    encounter = False
                    return "Loose"
            else:
                player.level = player.level + 1
                print(f"\nТы одолел {enemy.name} {enemy.level}lvl! Твой уровень повышен. "
                      f"Текущий уровень {player.level}.")
                encounter = False

        # while encounter:
        #     for weapon in player.weapons:
        #         print(f"{weapon}. Использовать {player.weapons[weapon]['name']}")
        #     if not blocking:
        #         print(f"{len(player.weapons) + 1}. Сосредоточиться на защите")
        #     attack_choose = int(input("Выбери действие: "))
        #     if attack_choose == len(player.weapons) + 1 and not blocking:
        #         block = player.block()
        #         blocking = True
        #     else:
        #         player.attack(enemy, player.weapons[attack_choose])
        #         print("Хп врага:", enemy.health)
        #
        #     if blocking and block_duration == 3:
        #         player.defense = player.defense + block
        #
        #     if block_duration > 0 and blocking:
        #         block_duration -= 1
        #     elif block_duration <= 0 and blocking:
        #         blocking = False
        #         player.defense = player.defense - block
        #         block_duration = 3
        #
        #     if enemy.health > 0:
        #         enemy.attack(player, enemy.weapons[1])
        #         print("Хп игрока:", player.health)
        #         if player.health <= 0:
        #             print("Game over, man")
        #             encounter = False
        #     else:
        #         player.level = player.level + 1
        #         print(f"Ты одолел {enemy.name} {enemy.level}lvl! Твой уровень повышен. Текущий уровень {player.level}.")
        #         encounter = False
        #
        #     print(player.defense)
