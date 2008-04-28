from rc import Rc

import os
import sys

import ids

class Image:
    def __init__( self, img ):
        self.image = img

class Animation:
    def __init__( self, images, tickPerFrame ):
        self.images = images
        self.tickPerFrame = tickPerFrame
        self.tick = 0

    def getImage( self ):
        return self.images[ self.tick/self.tickPerFrame ]

    def update( self ):
        self.tick = (self.tick+1)%(len(self.images)*self.tickPerFrame)

class Imgs( Rc ):
    def __init__( self, display ):
        Rc.__init__( self )
      #  self.wd = sys.path[0]
        self.display = display
        self.animations = []
        self.splashBack = self.loadImageWithDisplay( "splash/back.jpg" )

    def updateAnimations( self ):
        for animation in self.animations:
            animation.update()

    def __getitem__(self, i):
        item = self.__dict__[ i ]
        if isinstance( item, Animation ):
            return item.getImage()
        else:
            return item.image

    def loadImageWithDisplay( self, path ):
        return self.display.load( os.path.join( self.wd, "imgs", path ) )

    def loadImage( self, path ):
        return Image( self.loadImageWithDisplay( path ) )

    def loadAnimation( self, path, count, tickPerFrame=1 ):
        image = self.loadImageWithDisplay( path )
        dw = self.display.getWidth(image)/count
        images = [ self.display.getSubsurface( image, ( i*dw, 0, (i+1)*dw-1, self.display.getHeight(image) ) ) for i in xrange(count) ]
        animation = Animation( images, tickPerFrame )
        self.animations.append( animation )
        return animation

    def loadAll( self, display ):
        yield 0

        self[ ids.A_0 ] = self.loadImage( "asteroids/1.png" )
        self[ ids.A_1 ] = self.loadImage( "asteroids/2.png" )
        self[ ids.A_2 ] = self.loadImage( "asteroids/3.png" )
        self[ ids.A_3 ] = self.loadImage( "asteroids/4.png" )
        self[ ids.A_4 ] = self.loadImage( "asteroids/5.png" )

      #  self[ 0 ] = self.loadImage( "asteroids/gray10.png" )
      #  self[ 1 ] = self.loadImage( "asteroids/gray20.png" )
      #  self[ 2 ] = self.loadImage( "asteroids/gray30.png" ) 
      #  self[ 3 ] = self.loadImage( "asteroids/dark10.png" )
      #  self[ 4 ] = self.loadImage( "asteroids/dark20.png" )
      #  self[ 5 ] = self.loadImage( "asteroids/dark30.png" )
      #  self[ 6 ] = self.loadImage( "asteroids/beige10.png" )
      #  self[ 7 ] = self.loadImage( "asteroids/beige20.png" )
      #  self[ 8 ] = self.loadImage( "asteroids/beige30.png" )
        yield 5

        self[ ids.S_SOL ] = self.loadImage( "planets/sol.png" ) 
        yield 7
        self[ ids.P_MERCURY ] = self.loadImage( "planets/mercury.png" ) 
        yield 9
        self[ ids.P_MERCURY_1 ] = self.loadImage( "planets/mercury.1.png" ) 
        yield 11
        self[ ids.P_MARS ] = self.loadImage( "planets/mars.png" ) 
        yield 13
        self[ ids.P_MOON ] = self.loadImage( "planets/moon.png" ) 
        yield 15
        self[ ids.P_VENUS ] = self.loadImage( "planets/venus.png" ) 
        yield 17
        self[ ids.P_SATURN ] = self.loadImage( "planets/saturn.png" ) 
        yield 19
        self[ ids.P_SATURN_1 ] = self.loadImage( "planets/saturn.1.png" ) 
        yield 21
        self[ ids.P_NEPTUNE ] = self.loadImage( "planets/neptune.png" ) 
        yield 23
        self[ ids.P_GAIA ] = self.loadImage( "planets/gaia.png" ) 
        yield 25
        self[ ids.P_JUPITER ] = self.loadImage( "planets/jupiter.png" ) 
        yield 27
        self[ ids.P_JUPITER_1 ] = self.loadImage( "planets/jupiter.1.png" ) 
        yield 29
        self[ ids.P_EARTH ] = self.loadImage( "planets/earth.png" ) 
        yield 31
        self[ ids.P_X ] = self.loadImage( "planets/x.png" ) 
        yield 33
        self[ ids.P_X_1 ] = self.loadImage( "planets/x.1.png" ) 
        yield 35
        self[ ids.P_MARS_1 ] = self.loadImage( "planets/mars.1.png" )
        yield 37
        self[ ids.P_MARS_2 ] = self.loadImage( "planets/mars.2.png" )  
        yield 39

        self[ ids.S_AI_BASE ] 	= self.loadImage( "ships/ai-base.png" )
        self[ ids.S_AI_FIGHTER] = self.loadImage( "ships/ai-fighter.png" )
        self[ ids.S_AI_BOMBER] = self.loadImage( "ships/ai-bomber.png" )
        self[ ids.S_AI_FS_0] = self.loadImage( "ships/ai-fs-0.png" )
        self[ ids.S_AI_FS_1] = self.loadImage( "ships/ai-fs-1.png" )
        self[ ids.S_AI_FS_2] = self.loadImage( "ships/ai-fs-2.png" )
        self[ ids.S_AI_HARVESTER] = self.loadImage( "ships/ai-harvester.png" )

        self[ ids.S_NOMAD_FS_0 ] 	= self.loadImage( "ships/nomad-fs-0.png" )
        self[ ids.S_NOMAD_FIGHTER ] = self.loadImage( "ships/nomad-fighter.png" )
        self[ ids.S_NOMAD_FS_0 ] 	= self.loadImage( "ships/nomad-fs-0.png" )
        self[ ids.S_NOMAD_FS_1 ] 	= self.loadImage( "ships/nomad-fs-1.png" )
        self[ ids.S_NOMAD_FS_2 ] 	= self.loadImage( "ships/nomad-fs-2.png" )
        self[ ids.S_NOMAD_HARVESTER] = self.loadImage( "ships/nomad-harvester.png" )
        self[ ids.S_NOMAD_HARVESTER_1] = self.loadImage( "ships/nomad-harvester-1.png" )

        self[ ids.S_EVOLVED_FIGHTER ] = self.loadImage( "ships/evolved-fighter.png" )
        self[ ids.S_EVOLVED_BOMBER ] = self.loadImage( "ships/evolved-bomber.png" )
        self[ ids.S_EVOLVED_FS_0 ] 	= self.loadImage( "ships/evolved-fs-0.png" )
        self[ ids.S_EVOLVED_FS_1 ] 	= self.loadImage( "ships/evolved-fs-1.png" )
        self[ ids.S_EVOLVED_FS_2 ] 	= self.loadImage( "ships/evolved-fs-2.png" )
        self[ ids.S_EVOLVED_HARVESTER] = self.loadImage( "ships/evolved-harvester.png" )

        self[ ids.S_EXTRA_FS_0 ] 	= self.loadImage( "ships/extra-fs-0.png" )
        self[ ids.S_EXTRA_FS_1 ] 	= self.loadImage( "ships/extra-fs-1.png" )
        self[ ids.S_EXTRA_FS_2 ] 	= self.loadImage( "ships/extra-fs-2.png" )
        self[ ids.S_EXTRA_FIGHTER ] 	= self.loadImage( "ships/extra-fighter.png" )
        self[ ids.S_EXTRA_BOMBER ] 	= self.loadImage( "ships/extra-bomber.png" )
        self[ ids.S_EXTRA_HARVESTER] = self.loadImage( "ships/extra-harvester.png" )

        yield 41
        self[ ids.A_NEBULA ] = self.loadImage( "nebula.png" ) 
        self[ ids.A_BLACK_HOLE ] = self.loadImage( "planets/black-hole.png" )

       # self[ 9 ] = self.loadImage( "ship.png" ) 
        self[ ids.S_HARVESTER ] = self.loadImage( "ships/harvester.png" ) 
        self[ ids.S_FIGHTER ] = self.loadImage( "ships/human-fighter.png" ) 
        self[ ids.S_BOMBER ] = self.loadImage( "ships/human-bomber.png" ) 
        self[ ids.S_FLAGSHIP_0 ] = self.loadImage( "ships/human-fs-0.png" ) 
        self[ ids.S_FLAGSHIP_1 ] = self.loadImage( "ships/human-fs-1.png" ) 
        self[ ids.S_FLAGSHIP_2 ] = self.loadImage( "ships/human-fs-2.png" ) 
        self[ ids.S_CIVILIAN_0 ] = self.loadImage( "ships/civilian.png" )
        self[ ids.S_ORBITALBASE ] = self.loadImage( "ships/human-base.png" )

        self[ ids.S_MINE ] = self.loadImage( "mine.png" ) 

        self[ ids.T_LASER_SR ] = self.loadImage( "turrets/laser-sr.png" ) 
        self[ ids.T_LASER_MR_0 ] = self.loadImage( "turrets/laser-mr-0.png" ) 
        self[ ids.T_LASER_MR_1 ] = self.loadImage( "turrets/laser-mr-1.png" ) 

        self[ ids.T_MASS_SR_0 ] = self.loadImage( "turrets/mass-sr-0.png" ) 
        self[ ids.T_MASS_SR_1 ] = self.loadImage( "turrets/mass-sr-1.png" ) 
        self[ ids.T_MASS_SR_2 ] = self.loadImage( "turrets/mass-sr-2.png" ) 
        self[ ids.T_MASS_MR ] = self.loadImage( "turrets/mass-mr.png" ) 
        self[ ids.T_MASS_LR ] = self.loadImage( "turrets/mass-lr.png" ) 

        self[ ids.T_MISSILES_0 ] = self.loadImage( "turrets/missile-0.png" ) 
        self[ ids.T_MISSILES_1 ] = self.loadImage( "turrets/missile-1.png" ) 
        self[ ids.T_MISSILES_2 ] = self.loadImage( "turrets/missile-2.png" ) 
        yield 46

        self[ ids.T_HARVESTER ] = self.loadImage( "turrets/harvester-turret.png" ) 
        self[ ids.T_SPOTLIGHT ] = self.loadImage( "turrets/harvester-spotlight.png" ) 
        self[ ids.T_RED_SPOTLIGHT ] = self.loadImage( "turrets/harvester-red-spotlight.png" ) 

        self[ ids.M_NORMAL ] = self.loadImage( "missiles/missile.png" ) 
        self[ ids.M_NUKE ] = self.loadImage( "missiles/missile-nuke.png" ) 
        self[ ids.M_PULSE ] = self.loadImage( "missiles/missile-pulse.png" ) 
        self[ ids.M_MINER ] = self.loadImage( "missiles/missile-miner.png" ) 
        self[ ids.M_COUNTER ] = self.loadImage( "missiles/missile-counter.png" ) 
        self[ ids.M_AI ] = self.loadImage( "missiles/ai-missile.png" ) 
        self[ ids.M_LARVA ] = self.loadImage( "missiles/extras-missile.png" ) 
        yield 48

        self[ ids.T_INTERDICTOR ] = self.loadImage( "turrets/interdictor.png" ) 
        self[ ids.T_NUKE ] = self.loadImage( "turrets/nuke.png" ) 
        self[ ids.T_PULSE ] = self.loadImage( "turrets/pulse.png" ) 
        self[ ids.T_MINER ] = self.loadImage( "turrets/miner.png" ) 
        self[ ids.T_COUNTER ] = self.loadImage( "turrets/counter.png" ) 
        self[ ids.T_RADAR ] = self.loadImage( "turrets/radar.png" ) 
        self[ ids.T_BUILDING ] = self.loadImage( "turrets/building.png" ) 
        self[ ids.T_GENERATOR ] = self.loadImage( "turrets/generator.png" ) 
        self[ ids.T_HANGAR ] = self.loadImage( "turrets/hangar.png" ) 
        self[ ids.T_SOLAR_0 ] = self.loadImage( "turrets/solar-0.png" ) 
        self[ ids.T_SOLAR_1 ] = self.loadImage( "turrets/solar-1.png" ) 
        self[ ids.T_BIOSPHERE ] = self.loadImage( "turrets/biosphere-0.png" )

        self[ ids.T_SOLAR_2 ] = self.loadImage( "turrets/solar-2.png" )
        self[ ids.T_SUCKER ] = self.loadImage( "turrets/sucker.png" )
        self[ ids.T_EJUMP ] = self.loadImage( "turrets/ejump.png" )
        self[ ids.T_INERTIA ] = self.loadImage( "turrets/inertia.png" )
        self[ ids.T_BIOSPHERE_1 ] = self.loadImage( "turrets/biosphere-1.png" )
        self[ ids.T_SAIL ] = self.loadImage( "turrets/sail.png" )
        self[ ids.T_JAMMER ] = self.loadImage( "turrets/jammer.png" )


        yield 55
        self[ ids.T_ROCK_THROWER_0 ] = self.loadImage( "turrets/rock-thrower-0.png" ) 
        self[ ids.T_ROCK_THROWER_1 ] = self.loadImage( "turrets/rock-thrower-0.png" ) # TODO
        self[ ids.T_LARVA_0 ] = self.loadImage( "turrets/rock-thrower-0.png" ) # TODO
        self[ ids.T_DRAGON_0 ] = self.loadImage( "turrets/dragon-0.png" ) # TODO

        self[ ids.T_AI_MISSILE_0 ] = self.loadImage( "turrets/ai-missile-0.png" ) 

      #  self[ ids.MISSILE_0 ] = self.loadImage( "missiles/missile.png" ) 
        self[ ids.B_BULLET_0 ] = self.loadImage( "projectiles/bullet.png" )  
        self[ ids.B_BOMB_0 ] = self.loadImage( "projectiles/bomb.png" ) 
        self[ ids.B_ROCK_0 ] = self.loadImage( "projectiles/rock-0.png" )  
        self[ ids.B_ROCK_1 ] = self.loadImage( "projectiles/rock-1.png" )  
        self[ ids.B_FIRE_0 ] = self.loadImage( "projectiles/fire.png" )  
        self[ ids.B_AI_0 ] = self.loadImage( "projectiles/ai.png" )  

        yield 60
        self.background =  self.loadImageWithDisplay( "background0.jpg" ) 
        yield 70

      ## fragment
        self[ ids.F_LARGE_0 ] = self.loadImage( "fragments/large-0.png" )
        self[ ids.F_LARGE_1 ] = self.loadImage( "fragments/large-1.png" )

        self[ ids.F_FLAGSHIP_0 ] = self.loadImage( "fragments/flagship0-frag.png" )
        self[ ids.F_FLAGSHIP_1 ] = self.loadImage( "fragments/flagship1-frag.png" )
        self[ ids.F_FLAGSHIP_2 ] = self.loadImage( "fragments/flagship2-frag.png" )

        self[ ids.F_FIGHTER_0 ] = self.loadImage( "fragments/fighter-0.png" )
        self[ ids.F_FIGHTER_1 ] = self.loadImage( "fragments/fighter-1.png" )
        self[ ids.F_FIGHTER_2 ] = self.loadImage( "fragments/fighter-2.png" )

        self[ ids.F_AI_0 ] = self.loadImage( "fragments/ai-0.png" )

        yield 77
     #   self[ ids.E_0 ] = self.loadImage( "exhaust/particle0.png", True )
     #   self[ ids.E_1 ] = self.loadImage( "exhaust/particle1.png", True )
     #   self[ ids.E_2 ] = self.loadImage( "exhaust/particle2.png", True )
        self.exhausts = [  ids.E_0, ids.E_1, ids.E_2 ]

        # ui
        self.uiTopLeft0 =  self.loadImageWithDisplay( "ui/top-left-0.png" ) # 241 45
        self.uiTopLeft1 =  self.loadImageWithDisplay( "ui/top-left-1.png" ) 
        self.uiTopRight0 =  self.loadImageWithDisplay( "ui/top-right-0.png" )
        self.uiTopRight1 =  self.loadImageWithDisplay( "ui/top-right-1.png" )
        self.uiBottomRight0 =  self.loadImageWithDisplay( "ui/bottom-right-0.png" )
        self.uiBottomRight1 =  self.loadImageWithDisplay( "ui/bottom-right-1.png" )
        self.uiBottomLeft =  self.loadImageWithDisplay( "ui/bottom-left.png" )
        self.uiTop = self.loadImageWithDisplay( "ui/top.png" ) # 189 72

        yield 83
        # tubes
        self.uiTubeTop2 =  self.loadImageWithDisplay( "ui/top-2-tubes.png" ) 
        self.uiTubeTop1 =  self.loadImageWithDisplay( "ui/top-1-tube.png" ) 

        self.uiTubeRight2 =  self.loadImageWithDisplay( "ui/right-2-tubes.png" ) 
        self.uiTubeRightA =  self.loadImageWithDisplay( "ui/right-1-tube-a.png" ) 
        self.uiTubeRightB =  self.loadImageWithDisplay( "ui/right-1-tube-b.png" ) 
        self.uiTubeRightCurve =  self.loadImageWithDisplay( "ui/right-curve-tube.png" ) 
        self.uiTubeRightCurveFill =  self.loadImageWithDisplay( "ui/right-curve-tube-fill.png" ) 

        self.uiTubeBottom2 =  self.loadImageWithDisplay( "ui/bottom-2-tubes.png" ) 
        self.uiTubeBottom1 =  self.loadImageWithDisplay( "ui/bottom-1-tube.png" ) 

  #      self.uiTopRight =  self.loadImage( "ui/top-right.png" ) 
     #   self.uiButLaunch =  self.loadImage( "ui/launch.png" ) 
     #   self.uiButRecall =  self.loadImage( "ui/recall.png" ) 
        self.uiButJump =  self.loadImageWithDisplay( "ui/jump.png" ) 
     #   self.uiButJumpNow =  self.loadImage( "ui/jump-now.png" ) 
     #   self.uiRadar =  self.loadImage( "ui/radar.png" ) 
     #   self.uiRadarOver =  self.loadImage( "ui/radar-over.png" ) 
     #   self.uiDigitalBack =  self.loadImage( "ui/digital-back.png" ) 
      #  self.uiGlassEnergy =  self.loadImage( "ui/energy-glass.png" ) 
        self.uiButLaunch =  self.loadImageWithDisplay( "ui/launch.png" ) 
        self.uiButRecall =  self.loadImageWithDisplay( "ui/recall.png" ) 
        self.uiButAim =  self.loadImageWithDisplay( "ui/aim.png" ) 

        self.uiButRadar =  self.loadImageWithDisplay( "ui/radar.png" ) 
        self.uiButFullscreen =  self.loadImageWithDisplay( "ui/fullscreen.png" ) 
        self.uiButCharge =  self.loadImageWithDisplay( "ui/charge.png" ) 
        self.uiButRepair =  self.loadImageWithDisplay( "ui/repair.png" ) 
        yield 90

        self.uiEnergyFill =  self.loadImageWithDisplay( "ui/energy-fill.png" ) 
        self.uiShieldFill =  self.loadImageWithDisplay( "ui/shield-fill.png" ) 
        self.uiOreFill =  self.loadImageWithDisplay( "ui/ore-fill.png" ) 
        self.uiChargeFill0 =  self.loadImageWithDisplay( "ui/charge-fill-0.png" ) 
        self.uiChargeFill1 =  self.loadImageWithDisplay( "ui/charge-fill-1.png" ) 
        self.uiRepairFill0 =  self.loadImageWithDisplay( "ui/repair-fill-0.png" ) 
        self.uiRepairFill1 =  self.loadImageWithDisplay( "ui/repair-fill-1.png" ) 

        self.uiRelationFill0 =  self.loadImageWithDisplay( "ui/relation-fill-red.png" ) 
        self.uiRelationFill1 =  self.loadImageWithDisplay( "ui/relation-fill-green.png" ) 
        self.uiRelationFill2 =  self.loadImageWithDisplay( "ui/relation-fill-blue.png" ) 

        yield 93
        self.uiHullFill0 =  self.loadImageWithDisplay( "ui/hull-fill-green.png" ) 
        self.uiHullFill1 =  self.loadImageWithDisplay( "ui/hull-fill-yellow.png" ) 
        self.uiHullFill2 =  self.loadImageWithDisplay( "ui/hull-fill-red.png" ) 
 
        yield 96
        self.uiHangarLeft = self.loadImageWithDisplay( "ui/hangar/hangar-left.png" ) # 64 39
        self.uiHangarCenter = self.loadImageWithDisplay( "ui/hangar/hangar-center.png" ) # 25 39
        self.uiHangarSlot = self.loadImageWithDisplay( "ui/hangar/hangar-slot.png" ) # 25 39
        self.uiHangarRight = self.loadImageWithDisplay( "ui/hangar/hangar-right.png" )
        self.uiHangarOver = self.loadImageWithDisplay( "ui/hangar/hangar-over.png" )
        self.uiHangarShipsFill = self.loadImageWithDisplay( "ui/hangar/ships-fill.png" )
        self.uiHangarMissilesFill = self.loadImageWithDisplay( "ui/hangar/missiles-fill.png" )

        self.uiTurret = self.loadImageWithDisplay( "ui/turret.png" ) # 48 39
        self.uiTurretOn = self.loadImageWithDisplay( "ui/turret-on.png" )
        self.uiTurretOff = self.loadImageWithDisplay( "ui/turret-off.png" )

        self.uiBuildGlass = self.loadImageWithDisplay( "ui/build-glass.png" )
        self.uiBuildFill = self.loadImageWithDisplay( "ui/build-fill.png" )

        self.uiMsgBoxLeft = self.loadImageWithDisplay( "ui/msgbox-left.png" )
        self.uiMsgBoxCenter = self.loadImageWithDisplay( "ui/msgbox-center.png" )
        self.uiMsgBoxRight = self.loadImageWithDisplay( "ui/msgbox-right.png" )

      #  self.buildOptions = {}
        self.option = self.loadImageWithDisplay( "ui/option.png" )

        self.shipsIcons = { ids.S_FIGHTER: self.loadImageWithDisplay( "icons/ships/fighter.png" ),
                            ids.S_BOMBER: self.loadImageWithDisplay( "icons/ships/bomber.png" ),
                            ids.S_HARVESTER: self.loadImageWithDisplay( "icons/ships/harvester.png" ),

                            ids.S_EVOLVED_FIGHTER: self.loadImageWithDisplay( "icons/ships/evolved-fighter.png" ),
                            ids.S_EVOLVED_BOMBER: self.loadImageWithDisplay( "icons/ships/evolved-bomber.png" ),
                            ids.S_EVOLVED_HARVESTER: self.loadImageWithDisplay( "icons/ships/evolved-harvester.png" ),
                            
                            ids.S_AI_FIGHTER: self.loadImageWithDisplay( "icons/ships/ai-fighter.png" ),
                            ids.S_AI_BOMBER: self.loadImageWithDisplay( "icons/ships/ai-bomber.png" ),
                            ids.S_AI_HARVESTER: self.loadImageWithDisplay( "icons/ships/ai-harvester.png" ),
                            }

        self.missilesIcons = { ids.M_NORMAL: self.loadImageWithDisplay( "icons/missiles/missile.png" ),
                            ids.M_NUKE: self.loadImageWithDisplay( "icons/missiles/missile-nuke.png" ),
                            ids.M_PULSE: self.loadImageWithDisplay( "icons/missiles/missile-pulse.png" ),
                            ids.M_MINER: self.loadImageWithDisplay( "icons/missiles/missile-miner.png" ),
                            ids.M_COUNTER: self.loadImageWithDisplay( "icons/missiles/missile-counter.png" ),
                            ids.M_AI: self.loadImageWithDisplay( "icons/missiles/ai-missile.png" ),
        	            ids.M_LARVA: self.loadImageWithDisplay( "missiles/extras-missile.png" ) 
                            }

        yield 99
        self.notToRotate = [ ids.P_MARS, ids.P_MOON, ids.S_SOL ] # 59 33
        yield 100
        

 #   def notToRotate( self, id ):
   #     return self.notToRotate

