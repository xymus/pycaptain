#
# This file contains ids of images (mostly) shared between server and client.
# 

### version
revision = "$Revision: 101 $" # updated by subversion

revisionSplitted = revision.split()
if len(revisionSplitted) > 2:
    local_version = "ids%s"% revisionSplitted[1]
else:
    local_version = "idsNA"

### autogenerated ids
chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
# TODO alphanumericpart unused :( need to change comms first

def getId( p ):
    b=p
    id = []
    i = 1
    lChars = len(chars)

    pli = 1
    while p > 0:
        li = (lChars ** i)
        r = (p % li)
    #    print b,p,i,r,li
        id.append( chars[r / pli] )
        p -= r
        i += 1
        pli = li

    id.reverse()
    id = "".join(id)
    return id

idPos = 0
def getNextId():
    global idPos
    # id = getId( idPos ) # TODO ahplanum
    idPos += 1

    return idPos # id # TODO ahplanum


### asteroids ids
# there mainly for consistency
A_0		= getNextId()
A_1		= getNextId()
A_2		= getNextId()
A_3		= getNextId()
A_4		= getNextId()


### Ships
# human's
S_HUMAN_CARGO 	= getNextId()
S_HUMAN_PIRATE 	= getNextId()

S_HUMAN_FS_0 	= getNextId()
S_HUMAN_FS_1 	= getNextId()
S_HUMAN_FS_2 	= getNextId()
S_HUMAN_FIGHTER 	= getNextId()
S_HUMAN_BOMBER 	= getNextId()

S_HARVESTER 	= getNextId()
S_HUMAN_BUILDER = getNextId()
S_HUMAN_TRANSPORTER = getNextId()

S_CIVILIAN_0	= getNextId()

S_HUMAN_BASE 	= getNextId()
S_HUMAN_BASE_MINING 	= getNextId()
S_HUMAN_BASE_CARRIER    = getNextId()

S_MINE	 	= getNextId()

# ai's
S_AI_BASE_MILITARY 	= getNextId()
S_AI_FIGHTER 	= getNextId()
S_AI_FS_0 	= getNextId()
S_AI_FS_1 	= getNextId()
S_AI_FS_2 	= getNextId()
S_AI_BOMBER 	= getNextId()
S_AI_HARVESTER 	= getNextId()
S_AI_BASE_CARGO 	= getNextId()
S_AI_BUILDER = getNextId()
S_AI_TRANSPORTER = getNextId()

# nomad's
S_NOMAD_FS_0 	= getNextId()
S_NOMAD_FS_1 	= getNextId()
S_NOMAD_FS_2 	= getNextId()
S_NOMAD_BASE_MILITARY	= getNextId()
S_NOMAD_FIGHTER	= getNextId()
S_NOMAD_HARVESTER	= getNextId()
S_NOMAD_HARVESTER_1	= getNextId()
S_NOMAD_BASE_CARGO	= getNextId()
S_NOMAD_BUILDER = getNextId()
S_NOMAD_TRANSPORTER = getNextId()

# evolved's
S_EVOLVED_FS_0 	= getNextId()
S_EVOLVED_FS_1 	= getNextId()
S_EVOLVED_FS_2 	= getNextId()
S_EVOLVED_FIGHTER = getNextId()
S_EVOLVED_BOMBER = getNextId()
S_EVOLVED_HARVESTER 	= getNextId()
S_EVOLVED_BASE_MILITARY	= getNextId()
S_EVOLVED_BASE_CARGO	= getNextId()
S_EVOLVED_BUILDER = getNextId()
S_EVOLVED_BASE_HEAVY_MILITARY	= getNextId()
S_EVOLVED_TRANSPORTER = getNextId()

# extras's
S_EXTRA_BASE 	= getNextId()
S_EXTRA_FS_1 	= getNextId()
S_EXTRA_FS_2 	= getNextId()
S_EXTRA_FIGHTER = getNextId()
S_EXTRA_BOMBER 	= getNextId()
S_EXTRA_HARVESTER 	= getNextId()

### Weapons
# human's
W_LASER_SR 	= getNextId()
W_LASER_MR_0 	= getNextId()
W_LASER_MR_1 	= getNextId()

W_MASS_SR 	= getNextId()
W_MASS_MR 	= getNextId()
W_MASS_LR 	= getNextId()

W_MISSILE 	= getNextId()
W_NUKE	 	= getNextId()
W_PULSE 	= getNextId()
W_MINER 	= getNextId()
W_PROBE 	= getNextId()
W_COUNTER	= getNextId()
W_FRIGATE_BUILDER = getNextId()

W_BOMB_0 	= getNextId()

W_HARVESTER_T 	= getNextId()

# ai's
W_AI_MISSILE	= getNextId()
W_AI_MASS_EX    = getNextId()

# extra's
W_ROCK_THROWER_0	= getNextId()
W_ROCK_THROWER_1	= getNextId()
W_DRAGON_0		= getNextId()
W_LARVA_0		= getNextId()
W_EXTRA_FIGHTER		= getNextId()
W_EXTRA_BOMBER		= getNextId()

W_ESPHERE_0             = getNextId()
#W_ESPHERE_1             = getNextId()
#W_ESPHERE_2             = getNextId()
W_BURST_LASER_0         = getNextId()
#W_BURST_LASER_1         = getNextId()
#W_BURST_LASER_2         = getNextId()
W_OMNI_LASER_0          = getNextId()
W_OMNI_LASER_1          = getNextId()
W_OMNI_LASER_2          = getNextId()
W_SUBSPACE_WAVE_0       = getNextId()
W_SUBSPACE_WAVE_1       = getNextId()
W_EVOLVED_MISSILE       = getNextId()
W_EVOLVED_PULSE         = getNextId()
W_EVOLVED_COUNTER       = getNextId()

W_NOMAD_REPEATER        = getNextId()
W_NOMAD_CANNON           = getNextId()
W_DISCHARGER_0          = getNextId()
W_DISCHARGER_1          = getNextId()
W_NOMAD_MISSILE         = getNextId()

### bullets / projectiles
B_BULLET_0	= getNextId()
B_BOMB_0	= getNextId()
B_ROCK_0	= getNextId()
B_ROCK_1	= getNextId()
B_AI_0		= getNextId()
B_FIRE_0	= getNextId()
B_EGG_0		= getNextId()
B_ESPHERE       = getNextId()
B_WAVE_0        = getNextId()
B_WAVE_1        = getNextId()

### Turrets
# human's Ts (and basics)
T_LASER_SR_0 	= getNextId()
T_LASER_SR_1    = getNextId()
T_LASER_MR_0 	= getNextId()
T_LASER_MR_1 	= getNextId()

T_MASS_MR_0 	= getNextId()
T_MASS_SR_0 	= getNextId()
T_MASS_SR_1 	= getNextId()
T_MASS_SR_2 	= getNextId()
T_MASS_LR 	= getNextId()
T_MASS_MR_1     = getNextId()

T_MISSILES_0 	= getNextId()
T_MISSILES_1 	= getNextId()
T_MISSILES_2 	= getNextId()

T_HARVESTER 	= getNextId()
T_SPOTLIGHT 	= getNextId()
T_RED_SPOTLIGHT = getNextId()

T_INTERDICTOR 	= getNextId()
T_NUKE	 	= getNextId()
T_PULSE 	= getNextId()
T_RADAR 	= getNextId()
T_BUILDING 	= getNextId()
T_GENERATOR 	= getNextId()
T_SOLAR_0 	= getNextId()
T_HANGAR 	= getNextId()
T_REPAIR 	= getNextId()
T_SHIELD_RECHARGE 	= getNextId()
T_MAXSHIELD 	= getNextId()
T_MINER 	= getNextId()
T_COUNTER 	= getNextId()
T_BIOSPHERE	= getNextId()
T_SOLAR_1 	= getNextId()
T_SOLAR_2 	= getNextId()
T_SUCKER 	= getNextId()
T_EJUMP 	= getNextId()
T_INERTIA 	= getNextId()
T_BIOSPHERE_1	= getNextId()
T_SAIL_0	= getNextId()
T_JAMMER	= getNextId()
T_SCANNER	= getNextId()
T_SAIL_1        = getNextId()
T_SAIL_2        = getNextId()

T_GENERATOR_1 	= getNextId()
T_GENERATOR_2 	= getNextId()
T_RADAR_1 	    = getNextId()
T_RADAR_2 	    = getNextId()

# ai's Ts
T_AI_MISSILE_0	= getNextId()
T_AI_MISSILE_1	= getNextId()
T_AI_MISSILE_2	= getNextId()
T_AI_MISSILE_3	= getNextId()
T_AI_FLAK_0	    = getNextId()
T_AI_FLAK_1	    = getNextId()
T_AI_FLAK_2	    = getNextId()
T_AI_FLAK_3	    = getNextId()
T_AI_OMNI_LASER_0	= getNextId()
T_AI_OMNI_LASER_1	= getNextId()

T_AI_CRYPT_0    = getNextId()
T_AI_CRYPT_1    = getNextId()
T_AI_CRYPT_2    = getNextId()
T_AI_CRYPT_3    = getNextId()

T_AI_ACTIVE_DEFENSE_0 = getNextId()

# extra's Ts
T_ROCK_THROWER_0	= getNextId()
T_ROCK_THROWER_1	= getNextId()
T_DRAGON_0		= getNextId()
T_LARVA_0		= getNextId()

# evolved's Ts
T_ESPHERE_0             = getNextId()
T_ESPHERE_1             = getNextId()
T_ESPHERE_2             = getNextId()
T_BURST_LASER_0         = getNextId()
T_BURST_LASER_1         = getNextId()
T_BURST_LASER_2         = getNextId()
T_OMNI_LASER_0          = getNextId()
T_OMNI_LASER_1          = getNextId()
T_OMNI_LASER_2          = getNextId()
T_SUBSPACE_WAVE_0       = getNextId()
T_SUBSPACE_WAVE_1       = getNextId()

T_DARK_EXTRACTOR_0      = getNextId()
T_DARK_EXTRACTOR_1      = getNextId()
T_DARK_ENGINE_0         = getNextId()

T_EVOLVED_PULSE 	= getNextId()
T_EVOLVED_COUNTER 	= getNextId()
T_EVOLVED_MISSILE_0 	= getNextId()
T_EVOLVED_MISSILE_1 	= getNextId()

T_EVOLVED_PARTICLE_SHIELD_0 = getNextId()

# Nomad's
T_DISCHARGER_0          = getNextId()
T_DISCHARGER_1          = getNextId()
T_REPEATER_0          = getNextId()
T_REPEATER_1          = getNextId()
T_REPEATER_2          = getNextId()
T_REPEATER_3          = getNextId()
T_NOMAD_CANNON_0          = getNextId()
T_NOMAD_CANNON_1          = getNextId()
T_NOMAD_CANNON_2          = getNextId()
T_NOMAD_MISSILE_0          = getNextId()
T_NOMAD_MISSILE_1          = getNextId()
T_NOMAD_SUCKER_0          = getNextId()
T_NOMAD_SUCKER_1          = getNextId()
T_NOMAD_SUCKER_2          = getNextId()
T_NOMAD_HULL_ELECTRIFIER_0 = getNextId()

# Build related
T_FRIGATE_BUILDER = getNextId()
T_CIVILIAN_BUILDER = getNextId()
T_MILITARY_BUILDER = getNextId()

### Turret AI type
# ?why isn't it the class passed directly as argument of the stats? ...there must be a reason...
TA_COMBAT_STABLE 	= getNextId()
TA_COMBAT_ROTATING 	= getNextId()
TA_ROTATING 		= getNextId()
TA_SOLAR 		= getNextId()
TA_HARVESTER 		= getNextId()
TA_MISSILE_SPECIAL 	= getNextId()
TA_TARGET		= getNextId()

### Weapon Type
## Allows build of the correct inheritance of Weapon
WT_LASER		= getNextId()
WT_MASS			= getNextId()
WT_BOMB			= getNextId()
WT_MISSILE		= getNextId()
WT_MISSILE_SPECIAL 	= getNextId()
WT_OMNI_LASER		= getNextId()

### Orders
O_MOVE			= getNextId()
O_STOP_MOVE		= getNextId()
O_ATTACK		= getNextId()
O_ORBIT			= getNextId()
O_BUILD_TURRET		= getNextId()
O_BUILD_SHIP		= getNextId()
O_BUILD_MISSILE		= getNextId()
O_LAUNCH_MISSILE	= getNextId()
O_CHARGE		= getNextId()
O_REPAIR		= getNextId()

O_RECALL_SHIPS 	= getNextId()
O_LAUNCH_SHIPS 	= getNextId()

O_JUMP_NOW 	= getNextId()
O_JUMP		= getNextId()

O_TURRET_ACTIVATE	= getNextId()
O_RELATION		= getNextId()
O_SELF_DESTRUCT		= getNextId()

O_BROADCAST		= getNextId()
O_DIRECTED_CAST		= getNextId()


### Relations type with objects sent on the network
U_FLAGSHIP 	= getNextId()
#U_FLAGSHIP_TURRET	= getNextId()
U_OWN		= getNextId()
U_FRIENDLY	= getNextId()
U_ENNEMY	= getNextId()
U_RESOURCE	= getNextId()
U_ORBITABLE	= getNextId()
U_NEUTRAL	= getNextId()
U_DEADLY        = getNextId()

### Astres type
A_SUN		= getNextId()
A_PLANET	= getNextId()
A_NEBULA_UNDER	= getNextId()
A_NEBULA_OVER	= getNextId()
A_BLACK_HOLE	= getNextId()


### Planets
S_SOL		= getNextId()
P_MERCURY	= getNextId()
P_VENUS		= getNextId()
P_EARTH		= getNextId()
P_MARS		= getNextId()
P_JUPITER	= getNextId()
P_SATURN	= getNextId()
P_NEPTUNE	= getNextId()

P_MOON		= getNextId()
P_X		= getNextId()
P_MARS_1	= getNextId()
P_MARS_2	= getNextId()
P_JUPITER_1	= getNextId()
P_MERCURY_1	= getNextId()
P_X_1		= getNextId()
P_SATURN_1	= getNextId()

P_ALPHA_1	= getNextId()
P_ALPHA_2	= getNextId()

P_BETA_1	= getNextId()
P_BETA_2	= getNextId()

P_GAIA		= getNextId()

### Gfxs
G_LASER_SMALL	= getNextId()
G_EXPLOSION	= getNextId()
G_SHIELD	= getNextId()
G_FRAGMENT	= getNextId()
G_EXHAUST	= getNextId()
G_LIGHTNING     = getNextId()
G_JUMP     = getNextId()

## Frigate
# TODO reintegrade
S_HUMAN_FRIGATE_0   = getNextId()
S_AI_FRIGATE_0      = getNextId()
S_EVOLVED_FRIGATE_0 = getNextId()
S_NOMAD_FRIGATE_0   = getNextId()

## Scaffolding
# TODO reintegrade
S_HUMAN_SCAFFOLDING   = getNextId()
S_AI_SCAFFOLDING      = getNextId()
S_EVOLVED_SCAFFOLDING = getNextId()
S_NOMAD_SCAFFOLDING   = getNextId()

# race relations
R_NEUTRAL	= getNextId()
R_HOSTILE	= getNextId()
R_ALLIED	= getNextId()

F_LARGE_0	= getNextId()
F_LARGE_1	= getNextId()

F_HUMAN_FS_0	= getNextId()
F_HUMAN_FS_1	= getNextId()
F_HUMAN_FS_2	= getNextId()

F_FIGHTER_0	= getNextId()
F_FIGHTER_1	= getNextId()
F_FIGHTER_2	= getNextId()

F_AI_0		= getNextId()

F_BLOOD_0	= getNextId()

### Exhauts / trails
# temporary deactivated/uselesss
E_0		= getNextId()
E_1		= getNextId()
E_2		= getNextId()

### Missiles
M_NORMAL	    = getNextId()
M_NUKE		    = getNextId()
M_PULSE		    = getNextId()
M_MINER		    = getNextId()
M_PROBE		    = getNextId()
M_COUNTER	    = getNextId()
M_AI		    = getNextId()
M_LARVA		    = getNextId()
M_EVOLVED	    = getNextId()
M_EVOLVED_PULSE		= getNextId()
M_EVOLVED_COUNTER	= getNextId()
M_FRIGATE_BUILDER	= getNextId()
M_BUILDER_BASE_CARGO	= getNextId()
M_BUILDER_BASE_MILITARY	= getNextId()
M_BUILDER_BASE_HEAVY_MILITARY	= getNextId()
M_BUILDER_BASE_CARRIER	= getNextId()

### Special ability of turrets
S_INTERDICTOR	= getNextId()
S_NUKE		= getNextId()
S_PULSE		= getNextId()
S_MINE		= getNextId()
S_RADAR		= getNextId()
S_REACTOR	= getNextId()
# S_SOLAR		= getNextId()
S_HANGAR	= getNextId()
S_MINER		= getNextId()
S_CIVILIAN	= getNextId()
S_COUNTER	= getNextId()
S_SUCKER	= getNextId()
S_INERTIA	= getNextId()
S_SAIL		= getNextId()
S_JAMMER	= getNextId()
S_SCANNER	= getNextId()
S_BUILDER		= getNextId()
# S_TRACTOR_AGR   = getNextId()

### Sound fxs
## Explosions
S_EX_FIRE	= getNextId()
S_EX_JUMP	= getNextId()
S_EX_SHIP	= getNextId()
S_EX_NUKE	= getNextId()
S_EX_PULSE	= getNextId()

### Categories of turret
# TODO: to be removed?
C_WEAPON	= getNextId()
C_MISSILE	= getNextId()
C_OTHER		= getNextId()

### Races
R_HUMAN		= getNextId()
R_AI		= getNextId()
R_NOMAD		= getNextId()
R_EXTRA		= getNextId()
R_EVOLVED	= getNextId()

### build type
B_FRIGATE       = getNextId()
B_FRIGATE_SR    = getNextId()
B_FRIGATE_MR    = getNextId()
B_FRIGATE_ENERGY= getNextId()
B_BASE_CARGO    = getNextId()
B_BASE_MILITARY = getNextId()
B_BASE_HEAVY_MILITARY = getNextId()
B_BASE_CARRIER  = getNextId()

if __name__ == "__main__":
    duplicatedSet = []
    for x in xrange( 0, 10000 ):
        i = getNextId()
        print x, "->", i
        if i in duplicatedSet:
            raise Exception( "Duplicated id generated" )
        duplicatedSet.append( i )

