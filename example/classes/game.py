import np.random as random
import numpy as np

# This task was quite interesting since it sort of kicked off imagination right from the start and I would have really liked to sort of try to make a game out of it
# But also it would have been interesting to try to teach it some strategy with machine learning. Probably though I went too fast into it and started writing new code...
# Good experience though because you really have to sit down and think what is the structure and I so far ended up changing the structure because something somehow didnt anymore seem to work out.
# I must say I was every now and then dissapointed about how jupyter that we mainly used during our course does dirty hacks in the background and was quite impractical in many ways.
# This was sort of a welcome sideproject where you didnt have to all the time start some jupyter notebook server and write some scripts instead of being able to write something that is more universal.
# I really want to see how the sigmoid function and the learning properties I came up with would affect a game. 
# Idea was that you learn quickly and you learn more when you do either very badly or very well.
# And another idea I had was that the game was not like typically attack and defense rounds just that you can decide do you do twice attack , both or twice defence and also that you could defend somebody in your team
#
#  An attack is first counted in the next round, whereas defence is immideately affecting the round happening. By that one can still react on attacks (that were chosen against you last round) 
# Anyhow you cannot see anything else but who is attacking you but not if it was succesful
# Now I have to still move this to my forked branch I hope it will work to just rename the old directory and copy this file accross. Thx for your efford the task was very interesting. 
# Also it was quite clear what direction this should develop into and there was an example code

class Person:
    def __init__(self, name,ptypes,mhp,ba,bd,bdam,actions,items,**args):
        ### This is the basic class that all characters base on, there is hitpoints, but no magick for this base person class(yet)
        self.maxhp = mhp  # HP of character when it's full
        self.hp = mhp  # HP during the game will change, but the max HP should stay the same, yet mp is initiallised
        self.base_attack= ba # basic attack value, not sure maybe they will vanish into some actions
        self.base_defense=bd # basic defense value, same as ba
        self.base_damage=bdam#basic damage for attack
        self.actions=actions #basic actions
        #["Attack", "Defence","Item",'Fall','Raise','Group'] for example# 
        #can do action with item(item object contains actions what you can do with it) 
        #  Also, you can defend yourself or somebody else instead. 
        # These will be own objects 
        self.supply = items # items like sword etc. or also ring or wond, contain actions that you automatically learn
        self.state = []# state list that contains all the states  like on the floor etc
        self.inhand=[]# object(s?) in hand, normally one
        self.name = name
        self.ptypes = ptypes # Ptype is person type with this you can check if an action can be done
        # here later **args handling
    def istype(self,type)# Check if person is of certain type. E.g. warrior or Magician
        for ptype in self.ptypes:
            if ptype==type:
                return True
        return False
    

class Warrior(Person):
### for now a Hero has a second hand free for two items but no magick
### can defend with one hand attack with other or do twice item attack or twice item defense
### Typically is much better in attack   
    def __init__(self, name, mhp, ba,bd,action,experience,items,**args)
        self.inhand2=[]
        Person.__init__(self, name, mhp, ba,bd,action,experience,items,**args)

class Magician(Person):
### A Magician has magick energy and can cast spells. Spelling without an item in one hand is difficult 
### Oterwise he/she can attack/defend also with two hands, though not as efficiently
   def __init__(self, name, mhp, ba,bd,exp_a,exp_d,items,maxmagic,exp_m,**args)
        self.maxmagic=maxmagic # maximum magick energy
        self.magic= maxmagic # actual magick energy
        self.exp_m = exp_m # basic magick experience
        Person.__init__(self, name, mhp, ba,bd,exp_a,exp_d,items,**args)

class item:
    def __init__(self,name,type,mhp,actions,**args):
    ### basic item class idea is to attach actions that are objects with kind of functions that can be executed
    ### mhp is the hitpoints it can take until the item itself is destroyed
    ### idea is to attach it to persons or to ground
        self.mhp=mhp# maybe later you can attack the weapon and it will take hits
        self.hp=mhp# actual hitpoints
        self.bd=bd# basic defense against direct attack,very high (depending on size)such that it is difficult to hit
        # maybe also triggered with weapons when defense is succesfull 
        self.actions=actions# actions connected to the item. They are transferred to the person using the item
        self.name=name
        self.itype=type
    def is_item(self,name):# checking name of the item if action requires a specific item
        return (self.name==name)
    def is_type(self,type)#checking type of an item, if action requires a specific type
        return (self.itype==type)

class weapon(item):# weapon item has like the person a base attack and defense
    def __init__(self,name,type,mhp,actions,ba,bd,bdam,**args):
        self.base_attack=ba
        self.base_defense=bd
        self.base_damage=bdam
        item.__init__(self,name,type,mhp,actions,**args)
    pass
class magick_item(item):# later
    pass

class action:
## basic action class function defines mostly the type of action. It is attached first to an item and then passed on to the person using it
    def __init__(self,name,atype,required,base_experience,sfunction,ffunction,fcalc):
        self.name=name
        self.atype=atype# 'attack', 'defense' or 'other'
        self.required=required
        #dictionary of {items:[ list of required items or item type] applier_type:[list of person types], applied_to_type: [list of person types]} 
        #can be also empty, (n,) lists are meant to be concatenated by or to check
        self.experience=base_experience# experience that comes with the action when applied first time
    def check_requirements(self,appliers,applied_to):
        ok=True
        # check if any of the applier objs (Persons) have the required items
        for item in required[items]:
            found=False
            for person in appliers:
                if person.hasitem(item)|person.has_item_type(item):
                    found=True
                    break
            if not(found):
                ok=False
                break
        if not(ok):
            return False
        else:
            for ptype in required[appliertype]:
            found=False
            for person in appliers:
                if person.istype(ptype):
                    found=True
                    break
            if not(found):
                ok=False
                break
        if not(ok):
            return False
        else:
            for poitype in required[applied_to_type]:
            found=False
            for persoritem in applied_to:
                if persoritem.istype(poitype):
                    found=True
                    break
            if not(found):
                ok=False
                break
        if not(ok):
            return False
        else:
            return True


        # check if any of the applier has the required class
        pass
    def execute(self,modifier):
        # this is the central function to calculate if action was succesful. 
        # For that a random value is checked against the result of a sigmoid funciton
        def sigmoid(x):
            return (1 / (1 + np.exp(-x/20*6)))# sigmoid that is 1 at x=20 and 0 at x=-20
        value=self.experience.get_value()# read the experience as a basic value
        value=value+modifier# Modifier used to make it harder or easier. 
        #E.g. attack is easier if defence of opposite is low and vice versa
        value_to_exceed=sigmoid(value)
        rand=np.random.random()
        success=(rand>value_to_exceed)
        # learning: always learning but depending on how bad the fail or how splendig the success was
        if success:
            self.learn(rand)# The higher the random value the more you learn == splendid action
        else:
            self.learn(1-rand)# The lower the random value the more you learn == worst action
        return (success,rand-value_to_exceed)# return to caller to show success and how good or bad the action was
 
    def learn(self,increment=1)# learning when action was used
        self.experience.learn(increment)
##

class experience:
### experience object is attached to an action and the action stays with the person, even if requirements are not (anymore) fullfilled ,
# for example the item is lost or dropped or destroyed 
# experience is a counter that increases
    def__init__(self,value):
        self.value=value
    def learn(self,increment=1):
        self.value=self.value+increment
    def get_value(self)
        return self.value
### Class diagram use case diagram


class game:
    def __init__(persons):
        pass
    def __str__
    def next_turn():
        #run one turn and apply the results   
        pass
    def check_outcome():
        # check what happened, did people die
    def game_end():
        # game ends, determine who wins for exmample














# old code below keep it and later modify




class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


    # Generate the amount of damage randomly in range of highest attack and lowest attack
    def generate_atk_damage(self):
        return random.randrange(self.atkl, self.atkh)

    # When player takes damage, HP will be decreased

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_heal(self, dmg):
        self.hp += dmg
        if self.hp >= self.maxhp:
            self.hp = self.maxhp
        elif self.hp > 0 and self.hp < self.maxhp:
            return self.hp
        else:
            self.hp = 0
        return self.hp

    # MP will be decreased after casting spell
    def reduce_mp(self, cost):
        self.mp -= cost

    # Utility method to get properties
    def get_hp(self):
        if self.hp >= self.maxhp:
            self.hp = self.maxhp
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def choose_action(self):
        index = 1
        print(
            "\t   {} {} ACTIONS {}".format(Bcolors.OKBLUE, Bcolors.BOLD, Bcolors.ENDC)
        )
        for item in self.action:
            print(f"\t  {str(index)}: {item}")
            index += 1

    def choose_magic(self):
        index = 1
        print("\t   {} {} MAGIC {}".format(Bcolors.OKBLUE, Bcolors.BOLD, Bcolors.ENDC))
        for spell in self.magic:
            print("\t   {}: {} - Cost: {}".format(str(index), spell.name, spell.cost))
            index += 1

    def choose_item(self):
        index = 1
        print("\t   {} {} ITEMS {}".format(Bcolors.OKBLUE, Bcolors.BOLD, Bcolors.ENDC))
        for item in self.items:
            print(
                "\t   {}: {} (x{}) - {}".format(
                    str(index), item.name, item.quantity, item.description
                )
            )
            index += 1

    def get_stats(self, human):
        total_ticks = int((self.hp / self.maxhp) * 25)
        total_ticks_mp = int((self.mp / self.maxmp) * 25)
        white_space = int(25 - total_ticks)
        white_space_mp = int(25 - total_ticks_mp)
        stats_bar = "▓"
        space = " "
        mp_bar = "░"
        if human:
            print(f"{Bcolors.BOLD}{Bcolors.OKGREEN}{self.name}:{Bcolors.ENDC}")
            print("\t                 _________________________")
            print(
                f"\t{Bcolors.BOLD}HP   {self.hp}/{self.maxhp}\t|{Bcolors.OKGREEN}{stats_bar*total_ticks}{white_space*space}{Bcolors.ENDC}|"
            )
            print("\t                 _________________________")
            print(
                f"\t{Bcolors.BOLD}MP   {self.mp}/{self.maxmp}\t|{Bcolors.OKBLUE}{mp_bar*total_ticks_mp}{white_space_mp*space}{Bcolors.ENDC}|"
            )
        else:
            print(f"{Bcolors.BOLD}{Bcolors.FAIL}{self.name}:{Bcolors.ENDC}")
            print("\t                 _________________________")
            print(
                f"\t{Bcolors.BOLD}HP   {self.hp}/{self.maxhp}\t|{Bcolors.FAIL}{stats_bar*total_ticks}{white_space*space}{Bcolors.ENDC}|"
            )
            print("\t                 _________________________")
            print(
                f"\t{Bcolors.BOLD}MP   {self.mp}/{self.maxmp}\t|{Bcolors.OKBLUE}{mp_bar*total_ticks_mp}{white_space_mp*space}{Bcolors.ENDC}|"
            )


class Game:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def team_list(self, team):
        ind = 1
        for mem in team:
            print(f"\t{ind}: {mem.name}")
            ind += 1

    def get_choice(self, index):
        try:
            choice = int(index) - 1
            return choice
        except ValueError:
            print("Must be a number")

    def check_hp(self, team):
        for mem in team:
            if mem.hp == 0:
                team.remove(mem)
        return team

    def physical_attack(self, mem, enemy):
        dmg = mem.generate_atk_damage()
        enemy.take_damage(dmg)
        print("--------------------------------------------------")
        print(
            "\t{} attacked {} for {} points of damage".format(mem.name, enemy.name, dmg)
        )
        print("--------------------------------------------------")

    def magical_attack(self, mem, enemy, select):
        magic_choice = self.get_choice(select)
        spell = mem.magic[magic_choice]

        dmg = spell.generate_dmg()
        spellname = spell.name
        cost = spell.cost

        current_mp = mem.get_mp()

        if cost > current_mp:
            print("--------------------------------------------------")
            print("{} Not enough MP \n {}".format(Bcolors.FAIL, Bcolors.ENDC))
            self.physical_attack(mem, enemy)
            print("--------------------------------------------------")
        else:
            mem.reduce_mp(cost)

            if spell.type == "light":
                if mem.get_hp() == mem.get_maxhp():
                    print("--------------------------------------------------")
                    print(f"{mem.name} HP is full")
                    print("--------------------------------------------------")
                else:
                    mem.get_heal(dmg)
                    print("--------------------------------------------------")
                    print(
                        "{} {} heals {} for {} HP {}".format(
                            Bcolors.OKBLUE, spellname, mem.name, dmg, Bcolors.ENDC
                        )
                    )
                    print("--------------------------------------------------")
            else:
                enemy.take_damage(dmg)
                print("--------------------------------------------------")
                print(
                    "{} {} deals {} points of damage to {} {}".format(
                        Bcolors.OKBLUE, spellname, str(dmg), enemy.name, Bcolors.ENDC
                    )
                )
                print("--------------------------------------------------")

    def use_item(self, mem, enemy, select):
        item_choice = self.get_choice(select)
        item = mem.items[item_choice]
        if item.type == "potion":
            if item.quantity > 0:
                mem.get_heal(item.prop)
                item.quantity -= 1
                print("--------------------------------------------------")
                print(
                    "{}{} heals {} for {} HP - current amount: {} {}".format(
                        Bcolors.OKGREEN,
                        item.name,
                        mem.name,
                        str(item.prop),
                        str(item.quantity),
                        Bcolors.ENDC,
                    )
                )
                print("--------------------------------------------------")
            else:
                print("--------------------------------------------------")
                print("Insufficient amount of this item")
                self.physical_attack(mem, enemy)
                print("--------------------------------------------------")
        if item.type == "elixer":
            if item.quantity > 0:
                mem.hp = mem.maxhp
                mem.mp = mem.maxmp
                item.quantity -= 1
                print("--------------------------------------------------")
                print(
                    "{}{} fully restores HP & MP- current amount: {} {}".format(
                        Bcolors.OKGREEN, item.name, str(item.quantity), Bcolors.ENDC
                    )
                )
                print("--------------------------------------------------")
            else:
                print("--------------------------------------------------")
                print("Insufficient amount of this item")
                self.physical_attack(mem, enemy)

        if item.type == "attack":
            if item.quantity > 0:
                enemy.take_damage(item.prop)
                item.quantity -= 1
                print("--------------------------------------------------")
                print(
                    "{} {} deals {} points of damage to {}- current amount: {} {}".format(
                        Bcolors.OKBLUE,
                        item.name,
                        str(item.prop),
                        enemy.name,
                        str(item.quantity),
                        Bcolors.ENDC,
                    )
                )
                print("--------------------------------------------------")
            else:
                print("--------------------------------------------------")
                print("Insufficient amount of this item")
                self.physical_attack(mem, enemy)

    def turn(self, mem, enemy, select, human_turn):
        if human_turn:
            print("--------------------------------------------------")
            print("\t{}{}{}".format(Bcolors.BOLD, mem.name, Bcolors.ENDC))
            mem.choose_action()
            print("--------------------------------------------------")
        try:
            choice = self.get_choice(select)
            print("\t{} chose {}".format(mem.name, mem.action[choice]))
        except (IndexError, TypeError):
            print("Wrong number")

        # Physical Attack
        if choice == 0:
            self.physical_attack(mem, enemy)

        # Magical Attack
        elif choice == 1:
            if human_turn:
                # Print out options
                mem.choose_magic()

                # convert the choice to index number
                magic_choice = input("\tChoose your magic: ")
            else:
                magic_choice = random.randrange(1, len(mem.magic))

            self.magical_attack(mem, enemy, magic_choice)
        # USE ITEMS
        elif choice == 2:
            if human_turn:
                mem.choose_item()
                item_select = input("\tChoose item: ")
            else:
                item_select = random.randrange(1, len(mem.items))
            self.use_item(mem, enemy, item_select)
        else:
            print(
                "Wrong choice, there is no such option. You're forced to use physical attack !"
            )
            self.physical_attack(mem, enemy)
