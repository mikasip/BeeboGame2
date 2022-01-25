import pickle

class GameState:
    def __init__(self):
        self.mapStates = []
    
    """
        Format:
        'map_name,type(player/mob),id,pos_x,pos_y,hp(if_player),max_hp,way_x,way_y,image_index,weapon(if player),body,feet,hands,eyes,hair'
        or
        'map_name,type=spell,player_id,id,pos_x,pos_y,way_x,way_y,hit,file'
        or
        'remove,map_name,player_id'
        or
        'dead,map_name,mob_id'
        or
        'remove_spell,map_name,player_id,id'
        or
        'damage,map_name,mob_id,damage_amount,slow'
    """
    def updateState(self, updateString):
        parts = updateString.split(",")
        if parts[0] == "remove":
            existingMap = list(filter(lambda map: map.name == parts[1], self.mapStates))
            if len(existingMap) > 0:
                existingPlayer = list(filter(lambda playerState: playerState.id == int(parts[2]), existingMap[0].playerStates))
                if len(existingPlayer) > 0:
                    existingMap[0].playerStates.remove(existingPlayer[0])
                    if len(existingMap[0].playerStates) == 0:
                        self.mapStates.remove(existingMap[0])
            return
        if parts[0] == "remove_spell":
            existingMap = list(filter(lambda map: map.name == parts[1], self.mapStates))
            if len(existingMap) > 0:
                existingSpell = list(filter(lambda spellState: spellState.id == int(parts[3]) and spellState.playerId == int(parts[2]), existingMap[0].spellStates))
                if len(existingSpell) > 0:
                    existingMap[0].spellStates.remove(existingSpell[0])
            return
        if parts[0] == "dead":
            existingMap = list(filter(lambda map: map.name == parts[1], self.mapStates))
            if len(existingMap) > 0:
                existingMob = list(filter(lambda mobState: mobState.id == int(parts[2]), existingMap[0].mobStates))
                if len(existingMob) > 0:
                    existingMob[0].dead = True
            return
        if parts[0] == "damage":
            existingMap = list(filter(lambda map: map.name == parts[1], self.mapStates))
            if len(existingMap) > 0:
                existingMob = list(filter(lambda mobState: mobState.id == int(parts[2]), existingMap[0].mobStates))
                if len(existingMob) > 0:
                    existingMob[0].hp -= int(float(parts[3]))
                    existingMob[0].slow *= float(parts[4])
                    if existingMob[0].hp <= 0:
                        existingMob[0].dead = True
            return
        existingMap = list(filter(lambda map: map.name == parts[0], self.mapStates))
        if len(existingMap) > 0:
            existingMap[0].updateState(parts[1], parts[2:])
        else:
            newMapState = MapState()
            newMapState.name = parts[0]
            newMapState.updateState(parts[1], parts[2:])
            self.mapStates.append(newMapState)

class MapState:
    def __init__(self):
        self.name = ""
        self.mobStates = []
        self.playerStates = []
        self.spellStates = []

    def updateState(self, type, properties):
        if type == "mob":
            existingMob = list(filter(lambda mob: mob.id == int(properties[0]), self.mobStates))
            if len(existingMob) > 0:
                existingMob[0].updateState(properties[2:])
            else:
                newMobState = MobState()
                newMobState.id = int(float(properties[0]))
                newMobState.hp = int(float(properties[1]))
                newMobState.updateState(properties[2:])
                self.mobStates.append(newMobState)
        elif type == "player":
            existingPlayer = list(filter(lambda player: player.id == int(properties[0]), self.playerStates))
            if len(existingPlayer) > 0:
                existingPlayer[0].updateState(properties[1:])
            else:
                newPlayerState = PlayerState()
                newPlayerState.id = int(properties[0])
                newPlayerState.updateState(properties[1:])
                self.playerStates.append(newPlayerState)
        elif type == "spell":
            existingSpell = list(filter(lambda spellState: spellState.id == int(properties[1]) and spellState.playerId == int(properties[0]), self.spellStates))
            if len(existingSpell) > 0:
                existingSpell[0].updateState(properties[2:])
            else:
                newSpellState = SpellState()
                newSpellState.id = int(properties[1])
                newSpellState.playerId = int(properties[0])
                newSpellState.spellFile = properties[7]
                newSpellState.updateState(properties[2:])
                self.spellStates.append(newSpellState)
                
class MobState:
    def __init__(self):
        self.id = 0
        self.hp = 20
        self.pos = (0,0)
        self.dead = False
        self.slow = 1

    def updateState(self, properties):
        self.pos = (round(float(properties[0])), round(float(properties[1])))
        self.way = (round(float(properties[2])), round(float(properties[3])))
        self.image_index = int(properties[4])

class PlayerState:
    def __init__(self):
        self.id = 0
        self.pos = (57 * 32, 10 * 32)
        self.hp = 60
        self.max_hp = 60
        self.way = (1,0)
        self.image_index = 0
        self.feet = ""
        self.body = ""
        self.eyes = ""
        self.hands = ""
        self.hair = ""
    
    def updateState(self, properties):
        self.pos = (round(float(properties[0])), round(float(properties[1])))
        self.hp = int(float(properties[2]))
        self.max_hp = int(float(properties[3]))
        self.way = (round(float(properties[4])), round(float(properties[5])))
        self.image_index = int(properties[6])
        if properties[7] != "none":
            self.weapon = properties[7]
        else:
            self.weapon = None
        self.body = properties[8]
        self.feet = properties[9]
        self.hands = properties[10]
        self.eyes = properties[11]
        self.hair = properties[12]

class SpellState:
    def __init__(self):
        self.id = 0
        self.pos = (0,0)
        self.way = (1,0)
        self.hit = False
        self.playerId = 0
        self.spellFile = ""

    def updateState(self, properties):
        self.pos = (round(float(properties[0])), round(float(properties[1])))
        self.hit = (properties[4] == "True")
        self.way = (round(float(properties[2])), round(float(properties[3])))