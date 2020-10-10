import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

#########################################################################
class SitesManager():
    def __init__(self):
        self.list_of_sites = []

    def add_site(self, site):
        self.list_of_sites.append(site)

    def update_site_info(self, site_id, structure_type, owner):
        for site in self.list_of_sites:
            if site_id == site.site_id:
                site.structure_type = structure_type
                site.owner = owner

    def get_free_sites(self):
        return [site for site in self.list_of_sites if site.structure_type == -1]

    def get_closest_free_site(self, queen):
        closest_site = min(self.get_free_sites(), key=lambda site: site.get_distance(queen))
        return closest_site

    def get_my_barracks_ids(self):
        return [site for site in self.list_of_sites if site.owner == 0]

    def sort_sites_by_distance(self, unit):
        return sorted(self.list_of_sites, key=lambda site: site.get_distance(unit))


NUM_OF_BARRACKS_TO_BUILT = 1


class Site():
    def __init__(self, site_id, x, y):
        self.site_id = site_id
        self.x = x
        self.y = y
        self.structure_type = None
        self.owner = None
        self.distance_from_queen = None

    def build_barracks(self, unit_type):
        print "BUILD %s BARRACKS-%s" % (self.site_id, unit_type)
        if self.structure_type == 2:
            return 1
        return 0

    def build_mine(self):
        print "BUILD %s MINE" % (self.site_id)
        if self.structure_type == 2:
            return 1
        return 0

    def get_distance(self, unit):
        self.distance_from_queen = math.sqrt((self.x - unit.x) ** 2 + (self.y - unit.y) ** 2)
        return self.distance_from_queen


class Unit():
    def __init__(self):
        self.x = None
        self.y = None
        self.owner = None
        self.unit_type = None
        self.health = None


sites_manager = SitesManager()
#########################################################################

num_sites = int(raw_input())
for i in xrange(num_sites):
    site_id, x, y, radius = [int(j) for j in raw_input().split()]
    sites_manager.add_site(Site(site_id, x, y))

my_queen = Unit()
my_barracks = []
set_of_my_barracks = set()
# game loop
j_ = 1
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in raw_input().split()]

    for i in xrange(num_sites):
        # ignore_1: used in future leagues
        # ignore_2: used in future leagues
        # structure_type: -1 = No structure, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in raw_input().split()]
        sites_manager.update_site_info(site_id, structure_type, owner)

    num_units = int(raw_input())
    for i in xrange(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        x, y, owner, unit_type, health = [int(j) for j in raw_input().split()]
        if unit_type == -1 and owner == 0:
            my_queen.x = x
            my_queen.y = y
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # First line: A valid queen action
    # Second line: A set of training instructions
    if j_ == 1:
        list_of_sites_ = sites_manager.sort_sites_by_distance(my_queen)
        j_ += 1
    print >> sys.stderr, "sorted sites: ", [site.site_id for site in list_of_sites_]

    print >> sys.stderr, len(my_barracks)
    # if len(set_of_my_barracks) < NUM_OF_BARRACKS_TO_BUILT:
    if len(my_barracks) < NUM_OF_BARRACKS_TO_BUILT:
        my_barracks = sites_manager.get_my_barracks_ids()
        print >> sys.stderr, "my_barracks: %s" % [site.site_id for site in my_barracks]

        if not my_barracks:
            # list_of_sites_ = sites_manager.sort_sites_by_distance()
            closest_site = list_of_sites_[len(list_of_sites_) / 2]

            # closest_site = sites_manager.get_closest_free_site(my_queen)
            print >> sys.stderr, "closest_site: %s" % closest_site.site_id

        build_status = closest_site.build_barracks("KNIGHT")
        print >> sys.stderr, "Build status: %s" % build_status
        if build_status:
            list_of_sites_.pop(len(list_of_sites_) / 2)

        # list_of_sites_ = sites_manager.sort_sites_by_distance()
        closest_site = list_of_sites_[len(list_of_sites_) / 2]
        # closest_site = sites_manager.get_closest_free_site(my_queen)
        print >> sys.stderr, "closest_site: %s" % closest_site.site_id

        # print "BUILD %s BARRACKS-KNIGHT" % closest_site.site_id
        if my_barracks:
            print "TRAIN %s" % ' '.join(str(site.site_id) for site in my_barracks)
        else:
            print "TRAIN"

        # print "TRAIN %s" % ' '.join(str(item) for item in [6,2,5])
    else:
        dist_to_0 = math.sqrt((my_queen.x) ** 2 + (my_queen.y) ** 2)
        dist_to_end = math.sqrt((1920 - my_queen.x) ** 2 + (1000 - my_queen.y) ** 2)
        # if dist_to_0 <= dist_to_end:
        # print "MOVE 0 0"
        status = list_of_sites_[0].build_mine()

        print >> sys.stderr, "mine status", status
        # print "BUILD %s MINE" % list_of_sites_[0].site_id

        # else:
        # print "MOVE 1920 1000"
        # print "BUILD %s MINE" % list_of_sites_[0].site_id
        # print "MOVE 0 0" #"BUILD %s BARRACKS-KNIGHT" % closest_site.site_id
        print "TRAIN %s" % " ".join(str(site.site_id) for site in my_barracks)

    # Dodac sortowanie site'ow od najblizszego do najdalszego. Nastepnie
    # trzeba wybrac cos po srodku i tam isc zbudowac ze 2 (lub moze nawet 1) baraki.baraki
    # w drodze powrotnej, na site ktory jest najblizej rogu z ktorego startujemy trzeba
    # zbudowac wieze i uciekac do rogu. Jezeli wieza zostanie zniszczona to trzeba
    # ja odbudowac. Podobnie z barakami ale to potem.potem
    # Mozna jeszcze pomyslec o jednym baraku na srodku mapy, jeden wiezy i jednego baraku
    # na lucznikow blisko rogu. Oczywiscie co zostanie zniszczone trzeba odbudowac.odbudowac

    # w metodach do budowania trzeba by dorobic jakis lock. zwykly bit ktory bylby ustawiany
    # gdy metoda zostanie wywolana, co bedzie oznaczalo, ze zadna inna metoda nie moze byc #
    # teraz wykonana. Na starcie kazdej metody byloby "if not lock: lock==1". Po wykonaniu
    # metody lock bylby sciagany i jakas kolejna mogla by sie wykonac.

