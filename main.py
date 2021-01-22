from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


#Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 700, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 18, 350, "black")


#Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 50, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


#Create some Items
potion = Item("Potion", "potion", "Heels 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heels 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heels 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega-Elixer", "elixer", "Fully restores HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity":5}]

#Instantiate People
player1 = Person("PLAYER 2 :", 3260, 140, 300, 34, player_spells, player_items)
player2 = Person("PLAYER 1 :", 4160, 190, 311, 34, player_spells, player_items)
player3 = Person("PLAYER 3 :", 3089, 180, 290, 34, player_spells, player_items)

enemy1 = Person("ENEMY 2 :", 5000, 150, 450, 300, enemy_spells, [])
enemy2 = Person("ENEMY 1 :", 10000, 700, 530, 25, enemy_spells, [])
enemy3 = Person("ENEMY 3 :", 5000, 150, 450, 300, enemy_spells, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks!" + bcolors.ENDC)

while running:
    print("=========================")

    print("\n\n")
    print("NAME                     HP                                   MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose Action : ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name, "has Died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic : ")) - 1
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            if magic_choice == -1:
                continue

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MP!\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heel(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "Heels for" + str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", ""), "has Died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose items : ")) - 1

            if item_choice == -1:
                continue
            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heel(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + "fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", ""), "has Died.")
                    del enemies[enemy]

    #Check if the battle is over
    defeated_enemies = 0
    player_defeated = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            player_defeated += 1

    #Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False

    #check if enemy won
    elif player_defeated == 2:
        print(bcolors.FAIL + "You Lost!" + bcolors.ENDC)
        running = False
    print("\n")
    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            #chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_dmg)
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heel(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " Heels " + enemy.name + " for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", ""), "has Died.")
                    del players[player]
            print("Enemy Choose ", spell, "damage is ", magic_dmg)
