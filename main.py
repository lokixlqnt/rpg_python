from classes.game import Person, Bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

#Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
supotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
megaelixir = Item("Mega Elixir", "elixir", "Fully restores HP/MP of whole party", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 5},
                {"item": supotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 5}, {"item": grenade, "quantity": 5}]

player1 = Person("Loki", 460, 65, 60, 34, player_spells, player_items)
player2 = Person("Nyxo", 460, 65, 60, 34, player_spells, player_items)
player3 = Person("Blue", 460, 65, 60, 34, player_spells, player_items)

players = [player1, player2, player3]

enemy = Person("Grand Magus", 1200, 100, 100, 100, [], [])

running = True
i = 0

print(Bcolors.FAIL + Bcolors.BOLD + "AN ENEMY ATTACKS!" + Bcolors.ENDC)

while running:
    print("===================================")
    print(Bcolors.BOLD + "NAME                HP                                  MP" + Bcolors.ENDC)

    for player in players:
        player.get_stats()

    print("\n")

    enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print(Bcolors.BOLD + Bcolors.OKGREEN + player.name + Bcolors.ENDC + " attacked for", dmg, "points of damage.")
        elif index == 1:
            player.choose_spell()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(Bcolors.FAIL + "\n Not enough MP!" + Bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + Bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage." + Bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if player.items[item_choice]["quantity"] == 0:
                print(Bcolors.FAIL + "\n" + "None left.." + Bcolors.ENDC)

            if item.type == "potion":
                player.heal(item.prop)
                print(Bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + Bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                    else:
                        player.hp = player.max_hp
                        player.mp = player.max_mp
                print(Bcolors.OKGREEN + "\n" + item.name + " fully restores HP and MP" + Bcolors.ENDC)
            elif item.type =="attack":
                enemy.take_damage(item.prop)
                print(Bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "damage" + Bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemy.generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    print("-----------------------------")

    if enemy.get_hp() == 0:
        print(Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(Bcolors.FAIL + "Your enemy has defeated you!" + Bcolors.ENDC)
        running = False
