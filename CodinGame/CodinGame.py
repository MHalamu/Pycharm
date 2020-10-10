import sys
import math
from abc import ABCMeta, abstractmethod

STRUCTURE_TYPE = {
    'Goldmine': 0,
    'TOWER': 1,
    'Barracks': 2
}


###### TO DO ######
#

# - Jezeli jaka kopalnia sie wywali, to wybrac jedna z wiez najbardziej po lewej i tam zrobic kopalnie, a wieze wybudowac na kolejnym site najblizszym krolowej
# - Dodac jakies specjalne zachowanie jezeli nie ma knightow przeciwnika. Wtedy mozna isc budowac kopalnie
# - Dodac mechanizm ktory nie pozwoli krolowej wejsc w zasieg wiez przeciwnika
# - Dodac mechanizm ucieczki krolowej w rog gdy przeciwnicy sa w malej odleglosci, zeby nie bylo sytuacji tak jak
#   teraz, ze krolowa leci do przodu robic upgrade wierzy i wpada w przeciwnika (i jeszcze jego wieze)
# - Dodac mozliwosc wyboru listy koment w zaleznosci od ilosci hp na starcie. Teraz to nie jest takie proste
#   bo jest sporo rzeczy zahardkodowanych, np. ilosc koszarow >1 zanim rozpocznie sie trening.
# - Jezeli idzie bardzo duza gruba przeciwnikow to dobrym pomyslem jest przeksztalcic jakies kopalnie lub koszary w wieze,
#   zeby odeprzec atak i potem przywrocic na nich kopalnie.
# - fajne byloby cos takiego, ze gdy mamy np 3 wieze, to gdy nie ma w poblizu przeciwnika krolowa idzie na najblizszego
#   wolnego site'u i buduje 4 wieze, a potem jedna najblizej jej strony zamienia na kopalnie. Wtedy ta kopalnia bylaby
#   bezpieczna i knight'y by jej nie niszczyly. To pozwoliloby przesuwac linie wiez blizej przeciwnika.przeciwnika
#


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

#####################################################
#################### SITES ##########################
#####################################################

class SitesUpdater(object):
    """Update attributes of all Sites for each loop step of a game."""

    def __init__(self, sites_finder):
        self.sites_finder = sites_finder

    def update_sites_attributes(self, site_id, structure_type, owner, param_1, max_mine_size, gold_remaining):
        # Find appropriate Site object
        site = self.sites_finder.find_site_by_id(site_id)

        site.structure_type = structure_type
        site.owner = owner
        site.param_1 = param_1
        site.max_mine_size = max_mine_size
        site.gold_remaining = gold_remaining
        if 10 > site.gold_remaining > 0:
            site.good_for_mine = False


class SitesFinderGlobal(object):
    """Find specific site or group of sites."""

    def __init__(self, sites_container):
        self.sites_container = sites_container

    def find_site_by_id(self, site_id):
        for site in self.sites_container.list_of_all_sites:
            if site_id == site.site_id:
                return site
        raise Exception("Cannot find site with give ID (%s)" % site_id)

    def _find_all_free_sites(self):
        return [site for site in self.sites_container.list_of_all_sites if site.structure_type == -1]

    def find_closest_free_site(self, queen):
        return min(self._find_all_free_sites(), key=lambda site: site.get_distance(queen))

    def find_most_to_my_side(self, queen_side):
        free_sites = self._find_all_free_sites()
        # print >> sys.stderr, "Queen side is %s" % queen_side
        if queen_side > 960:
            return max(free_sites, key=lambda site: site.x)
        else:
            return min(free_sites, key=lambda site: site.x)


class TowerFinder(SitesFinderGlobal):
    structure_type = STRUCTURE_TYPE['TOWER']

    def find_all_my_sides(self):
        """Find all my towers.

        :returns: list of all my towers.
        :rtype: list

        """
        return [site for site in self.sites_container.list_of_all_sites if
                site.owner == 0 and site.structure_type == self.structure_type]

    def find_most_damaged(self):
        """Find most damaged tower.

        :return: Site id of most damaged tower.
        :rtype: str
        """
        site = min(self.find_all_my_sides(), key=lambda site: site.param_1)
        return site.site_id


class MineFinder(SitesFinderGlobal):
    structure_type = STRUCTURE_TYPE['Goldmine']

    def _find_all_free_sites(self):
        """Find all free sites that are appropriate for gold mine.

        :returns: list of sites.
        :rtype: list

        """
        sites_with_gold = []
        # for site in self.sites_container.list_of_all_sites: # tu ma byc all free sites
        for site in super(MineFinder, self)._find_all_free_sites():
            if site.good_for_mine:
                sites_with_gold.append(site)
        return sites_with_gold

    def find_closest_free_site(self, queen):
        """Find closest free site with gold.

        :param queen:
        :return:
        """
        return min(self._find_all_free_sites(), key=lambda site: site.get_distance(queen))

    def find_all_my_sides(self):
        return [site for site in self.sites_container.list_of_all_sites if
                site.owner == 0 and site.structure_type == self.structure_type]

    def find_most_damaged(self):
        site = min(self.find_all_my_sides(), key=lambda site: site.param_1)
        return site.site_id


class BarrackFinder(SitesFinderGlobal):
    structure_type = STRUCTURE_TYPE['Barracks']

    def find_all_my_sides(self):
        return [site for site in self.sites_container.list_of_all_sites if
                site.owner == 0 and site.structure_type == self.structure_type]

    def find_most_damaged(self):
        site = min(self.find_all_my_sides(), key=lambda site: site.param_1)
        return site.site_id


class SitesContainer(object):
    def __init__(self):
        self.list_of_all_sites = []

    def add_site(self, site_obj):
        self.list_of_all_sites.append(site_obj)


class Site(object):
    def __init__(self, site_id, x, y):
        self.site_id = site_id
        self.x = x
        self.y = y
        self.structure_type = None
        self.owner = None
        self.distance_from_queen = None
        self.param_1 = None
        self.max_mine_size = None
        self.good_for_mine = True
        self.gold_remaining = None

    def get_distance(self, unit):
        self.distance_from_queen = math.sqrt((self.x - unit.x) ** 2 + (self.y - unit.y) ** 2)
        return self.distance_from_queen

    def is_bulding_done(self):
        if self.owner == 0:
            return True
        return False


#####################################################
#####################################################

class Unit(object):
    def __init__(self, x, y, owner, unit_type, health):
        self.x = x
        self.y = y
        self.owner = owner
        self.unit_type = unit_type
        self.health = health


class UnitsHolder(object):

    FRIENDLY_OWNER_CODE = 0
    ENEMY_OWNER_CODE = 1
    QUEEN_TYPE = -1
    KNIGH_TYPE = 0
    ARCHER_TYPE = 1

    def __init__(self):
        self.list_of_units = []

    def add_unit(self, unit):
        self.list_of_units.append(unit)
        # if unit.unit_type == self.QUEEN_TYPE:
        #     self.list_of_units.append(Queen(unit.x, unit.y, unit.owner, unit.unit_type, unit.health))
        # elif unit.unit_type == self.KNIGH_TYPE:
        #     self.list_of_units.append(Knight(unit.x, unit.y, unit.owner, unit.unit_type, unit.health))
        # elif unit.unit_type == self.ARCHER_TYPE:
        #     self.list_of_units.append(Archer(unit.x, unit.y, unit.owner, unit.unit_type, unit.health))

    @property
    def queen_unit(self):
        return next(unit for unit in self.list_of_units if unit.unit_type == self.QUEEN_TYPE)


class MyUnits(UnitsHolder):
    pass


class EnemyUnits(UnitsHolder):
    pass


##############################################
############# NEW COMMAND MANGER #############
##############################################

class Command(object):

    __metaclass__ = ABCMeta

    # Representation of command statuses
    NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2

    def __init__(self):
        self.command_status = self.NOT_STARTED

    @abstractmethod
    def update_command_status(self):
        pass

    @abstractmethod
    def execute(self):
        pass



class BuildCmd(Command):
    """
    Example:

    cmd = BuildCmd("Barracks", sites_finder_mine.find_closest_free_site(self.queen))
    while cmd.command_status != DONE:
        cmd.execute()
    """

    def __init__(self, building_type, site_obj):
        self.building_type = building_type
        self.site_obj = site_obj
        super(BuildCmd, self).__init__()

    def update_command_status(self):
        if self._building_finished:
            self.command_status = self.DONE

    def execute(self):
        print "BUILD {site_id} {building}".format(
            site_id=self.site_obj.site_id,
            building=self.building_type)
        self.update_command_status()

    def _building_finished(self):
        if self.site_obj.owner == 0 and self.site_obj.structure_type == self.building_type:
            return True

class TrainCmd(Command):
    def __init__(self, list_of_barracks):
        self.list_of_barracks = list_of_barracks
        super(TrainCmd, self).__init__()

    def update_command_status(self):
        #jak sprawdzic ze jednostki zostaly stworzone?
        pass

    def execute(self):
        print "TRAIN %s" % ' '.join([str(site.site_id) for site in self.list_of_barracks])
        self.update_command_status()



# command executora ktory bedzie odpowiednio te komenty laczyl w 2 printy
# zrobic planner'a ktory bedzie tworzyl finalne komenty tak jak w docstringu z BuildCmd





##############################################
##############################################
##############################################


class Command_Manager():
    def __init__(self, sites_finder, sites_finder_mine, sites_finder_barracks, sites_finder_tower):
        self.sites_finder = sites_finder
        self.queen = None
        # print >> sys.stderr, "Type of my queen %s" % type(self.queen)
        self.queen_side = None
        self.command_in_progress = False
        self.actual_command = None
        self.temp_var = 0
        self.site_id = ''
        self.site_obj = None
        self.gold = 0
        self.allow_train = False
        self.sites_finder_mine = sites_finder_mine
        self.sites_finder_barracks = sites_finder_barracks
        self.sites_finder_tower = sites_finder_tower

    def execute_command(self):
        # Translation of self.actual_command to 2 print lines

        if not self.command_in_progress:
            # resetting previous attributes
            self.site_id = ''

            if self.actual_command.action == Action.build:
                self.site_id = self.get_desired_site_id()
            command_manager.command_in_progress = True

        first_line_command = "{action} {site_id} {building}{additional_param}".format(
            action=self.actual_command.action,
            site_id=self.site_id,
            building=self.actual_command.what,
            additional_param=self.actual_command.unit_type
        )

        print first_line_command
        if self.gold > 160:
            self.allow_train = True

        if self.gold < 80:
            self.allow_train = False

        my_barracks = self.sites_finder_barracks.find_all_my_sides()
        # print >> sys.stderr, "gold: %s" % self.gold
        if len(my_barracks) > 1 and self.allow_train:
            print "TRAIN %s" % ' '.join([str(site.site_id) for site in my_barracks])
        else:
            print "TRAIN"

    def get_command(self):
        """Get a game command from list of commands.

        :return: Command as an object
        :rtype: Command
        """
        try:
            self.actual_command = commands_list.pop(0)
        except IndexError:
            # print >> sys.stderr, "Executing default command"

            my_mines = self.sites_finder_mine.find_all_my_sides()
            # print >> sys.stderr, "My mines: %s" % len(my_mines)

            if len(my_mines) < 2:
                # print >> sys.stderr, "Setting command to build closest mine"
                self.actual_command = Command_Object(action=Action.build,
                                                     where=Where.closest_gold,
                                                     what=Buildings.mine)
                return

            # if any(mine.param_1<mine.max_mine_size for mine in my_mines):
            for mine in my_mines:
                # print >> sys.stderr, "mine.param_1: %s, mine.max_mine_size:%s" % (mine.param_1, mine.max_mine_size)
                if mine.param_1 < mine.max_mine_size:
                    self.actual_command = Command_Object(action=Action.build,
                                                         where=mine.site_id,
                                                         what=Buildings.mine)
                    # print >> sys.stderr, "Setting command to build mine"
                    return

            # print >> sys.stderr, "Setting command to fix towers"
            self.actual_command = Command_Object(action=Action.build,
                                                 where=Where.most_damaged,
                                                 what=Buildings.tower)

    def update_status_of_command(self):

        self.site_obj = self.sites_finder.find_site_by_id(self.site_id)
        if self.actual_command.where == Where.most_damaged:
            if self.site_obj.param_1 > 700:
                self.actual_command.done_status = 1
        elif self.actual_command.what == Buildings.mine:
            # print >> sys.stderr, "mine.param_1: %s, mine.max_mine_size:%s" % (
            # self.site_obj.param_1, self.site_obj.max_mine_size)
            if self.site_obj.param_1 >= self.site_obj.max_mine_size:
                self.actual_command.done_status = 1
                # print >> sys.stderr, "mine done"
            else:
                # print >> sys.stderr, "mine not at max. Upgrading"
                pass
        else:
            if self.site_obj.is_bulding_done():
                # print >> sys.stderr, "Building done"
                # if self.site_manager.is_building_done(self.site_id):
                self.actual_command.done_status = 1

    def get_desired_site_id(self):
        if self.actual_command.where == Where.closest:
            site = self.sites_finder.find_closest_free_site(self.queen)
            # print >> sys.stderr, "closest free site: %s" % site.site_id
        elif self.actual_command.where == Where.closest_gold:
            # print >> sys.stderr, "searching closest site with gold"
            site = self.sites_finder_mine.find_closest_free_site(self.queen)

        elif self.actual_command.where == Where.most_damaged:

            # print >> sys.stderr, "mself.actual_command.what %s" % self.actual_command.what
            # print >> sys.stderr, "STRUCTURE_TYPE['Goldmine']: %s" % STRUCTURE_TYPE['Goldmine']

            if self.actual_command.what == 'Goldmine':
                return sites_finder_mine.find_most_damaged()

            elif self.actual_command.what == 'TOWER':
                # print >> sys.stderr, "Looking for most damaged tower"
                return sites_finder_tower.find_most_damaged()

            elif self.actual_command.what == 'Barracks':
                return sites_finder_barracks.find_most_damaged()

            # site = self.sites_finder.find_most_damaged_of_type(self.actual_command.what)

        elif self.actual_command.where == Where.most_to_queen_side:
            site = self.sites_finder.find_most_to_my_side(self.queen_side)
        else:
            return self.actual_command.where  # site id is in 'where'

        return site.site_id


class Command_Object:
    def __init__(self, action, where='', what='', unit_type=''):
        self.action = action
        self.where = where
        self.what = what
        self.unit_type = unit_type
        self.done_status = 0
        self.temp_var = 0


class Action(enumerate):
    build = 'BUILD'
    move = 'MOVE'
    wait = 'WAIT'


class Where(enumerate):
    closest = 'closest'
    closest_gold = "closest_gold"
    most_damaged = 'most_damaged'
    most_to_queen_side = 'most_to_queen_side'


class Buildings(enumerate):
    tower = 'TOWER'
    mine = 'MINE'
    barracks = 'BARRACKS'


class Units(enumerate):
    knight = '-KNIGHT'
    archer = '-ARCHER'
    giant = '-GIANT'


#############################################
sites_container = SitesContainer()

sites_finder_global = SitesFinderGlobal(sites_container)
sites_finder_mine = MineFinder(sites_container)
sites_finder_barracks = BarrackFinder(sites_container)
sites_finder_tower = TowerFinder(sites_container)

sites_updater = SitesUpdater(sites_finder_global)

command_manager = Command_Manager(sites_finder_global, sites_finder_mine, sites_finder_barracks,
                                  sites_finder_tower)

#############################################

num_sites = int(raw_input())
for i in xrange(num_sites):
    site_id, x, y, radius = [int(j) for j in raw_input().split()]
    sites_container.add_site(Site(site_id, x, y))

commands_list = [
    Command_Object(action=Action.build,
                   where=Where.closest,
                   what=Buildings.mine),

    Command_Object(action=Action.build,
                   where=Where.closest,
                   what=Buildings.mine),

    Command_Object(action=Action.build,
                   where=Where.closest,
                   what=Buildings.barracks,
                   unit_type=Units.knight),

    Command_Object(action=Action.build,
                   where=Where.closest,
                   what=Buildings.barracks,
                   unit_type=Units.knight),

    Command_Object(action=Action.build,
                   where=Where.most_to_queen_side,
                   what=Buildings.tower),

    Command_Object(action=Action.build,
                   where=Where.closest,
                   what=Buildings.tower),

    Command_Object(action=Action.build,
                   where=Where.closest,
                   what=Buildings.tower)

]

################# MAIN LOOP #################
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in raw_input().split()]
    for i in xrange(num_sites):
        # gold_remaining: -1 if unknown
        # max_mine_size: -1 if unknown
        # structure_type: -1 = No structure, 0 = Goldmine, 1 = Tower, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, gold_remaining, max_mine_size, structure_type, owner, param_1, param_2 = [int(j) for j in
                                                                                           raw_input().split()]
        sites_updater.update_sites_attributes(site_id, structure_type, owner, param_1, max_mine_size, gold_remaining)

    num_units = int(raw_input())

    my_units = MyUnits()
    enemy_units = EnemyUnits()
    for i in xrange(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER, 2 = GIANT
        x, y, owner, unit_type, health = [int(j) for j in raw_input().split()]
        unit = Unit(x, y, owner, unit_type, health)
        if unit.owner == 0:
            my_units.add_unit(unit)
        else:
            enemy_units.add_unit(unit)

    print >> sys.stderr, "My units (%s)" % len(my_units.list_of_units)
    for unit in my_units.list_of_units:
        print >> sys.stderr, "%s %s %s" % (unit.owner, unit.x, unit.y)

    print >> sys.stderr, "Enemy units (%s)" % len(enemy_units.list_of_units)
    for unit in enemy_units.list_of_units:
        print >> sys.stderr, "%s %s %s" % (unit.owner, unit.x, unit.y)

    print >> sys.stderr, "Enemy queen (%s.%s)" % (enemy_units.queen_unit.x, enemy_units.queen_unit.y)
    print >> sys.stderr, "My queen (%s.%s)" % (my_units.queen_unit.x, my_units.queen_unit.y)
    ###########################

    command_manager.queen_side = my_units.queen_unit.x

    # w command managerze trzeba aktualizaowac polozenie krolowej. bez tej linii ponizej
    # command manager mial tylko polozenie krolowerj z inicjalizacji obiektu command manager
    command_manager.queen = my_units.queen_unit
    command_manager.gold = gold

    # dodac blokade zeby nie budowal kopalni tam gdzie juz byla kopalnia.
    #######################################################

    if not command_manager.command_in_progress:
        # print >> sys.stderr, "Getting command"
        command_manager.get_command()

    command_manager.execute_command()
    command_manager.update_status_of_command()

    # print >> sys.stderr, "command status: %s" % command_manager.actual_command.done_status
    if command_manager.actual_command.done_status == 1:
        # print >> sys.stderr, "Done bit is set! Releasing command_in_progress"
        command_manager.command_in_progress = False

    #######################################################
