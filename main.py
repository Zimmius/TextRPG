from Character import Character, Player
from Encounter import Encounter

loot = {"золото": {"quantity": 15, "type": "currency"},
        "Дубина": {"type": "weapon",
                   "name": "Дубина",
                   "damage": [2, 6],
                   "hp": 0,
                   "mp": 0,
                   "description": "Если посильнее замахнуться, можно и убить!"},
        "Зелье лечения": {"type": "consumables",
                          "name": "Зелье лечения",
                          "hp": 6,
                          "mp": 0,
                          "damage": "",
                          "description": "Восстанавливает здоровье"},
        "яблоко": {"type": "consumables",
                   "name": "Яблоко",
                   "hp": 3,
                   "mp": 0,
                   "damage": "",
                   "description": "Восстанавливает здоровье"
                   }
        }
moves_list = ["Попытаться подойти не привлекая внимания", "Подойти обычным шагом", "Подбежать крича 'СПАСИТЕ ПАМАГИТЕ'"]
player_lines = ["Bla bla!!!", "Ble ble!", "Blu Blu!"]
tavern_guard_lines = ["Стражник: -Стой, кто идёт!\n"]
Encounter1 = Encounter(moves=moves_list,
                       dialogues={'player': player_lines, 'other': tavern_guard_lines},
                       acquirable_loot=loot)
Enemy = Character('npc', 40, 1, 3, 10,
                  inventory={"дубина": {"type": "weapon", "name": "Дубина", "damage": [2, 6]}},
                  name="Стражник таверны")

print("\nТы проснулся ночью в тёмном, сыром лесу. Через кроны густых виден тусклый свет луны, пробивающийся сквозь"
      " облака.\n"
      "Ты одет в простые одежды, кожанный жилет и потрёпанные старые сапоги. В голове пустота и ты не помнишь"
      " ни кто ты, ни как сюда попал.\n"
      "В далеке ты замечаешь еле различимый свет факелов. Ты решаешь:\n")

move = Encounter1.move(slice(0, 3))
if move == moves_list[0]:
    print("\nПриближаясь ты видишь небольшую древянную хижину. \n"
          "Судя по стоящим у упряжи коням, и звукам\n"
          "доносящимся изнутри - это придорожная таверна. \n"
          "У входа стоит стражник одетый в легкую кольчугу\n"
          "и что-то насвистывает себе под нос. Он тебя не заметил.")
elif move == moves_list[1]:
    print("\nПриближаясь ты видишь небольшую древянную хижину. \n"
          "Судя по стоящим у упряжи коням, и звукам\n"
          "доносящимся изнутри - это придорожная таверна. \n"
          "У входа стоит стражник одетый в легкую кольчугу\n"
          "При твоём приближении он поворачивается и обращается к тебе")
    dialogue = Encounter1.dialogue(slice(2, 3), 0)
    if dialogue == "Blu Blu!":
        print("\nПрахади")
        Encounter1.loot(slice(0, 4), Player)
        print(Player.inventory)
        print(Player.filter_inventory("consumables"))
elif move == moves_list[2]:
    print(f"\nТы несёшься на свет как ополумевший и орёшь: {move} \n"
          "Подбегая ты видишь небольшую древянную хижину. \n"
          "У хижины стоит стражник одетый в легкую кольчугу.\n"
          "Ты замечаешь, как он смотрит на тебя ошалевшими глазами и достаёт деревянную дубину\n"
          "но ты уже не успеваешь остановиться")
    Encounter1.battle(Player, Enemy)
