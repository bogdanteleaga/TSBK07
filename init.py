from planet import Planet, Sun
from spaceship import Spaceship
from asteroids import Asteroids
from skybox import Skybox
from pyrr import Vector3 as vec3

def initObjects(classicProgram, normalMapProgram, skyboxProgram, asteroidProgram):
    planets = initPlanets(classicProgram, normalMapProgram, highDef=False)
    spaceship = initSpaceship(classicProgram)
    #skybox = initSkybox(skyboxProgram)
    belt = initBelt(asteroidProgram)
    return planets, spaceship, belt

def initBelt(program):
    belt = Asteroids(filename='asteroid_model.obj',
			  texImg='textures/asteroid_texture.png',
                          shininess=30,
                          ka=0.5,
                          kd=0.9,
                          ks=0.6,
                          program=program,
                          radius=270,
                          offset=25,
                          amount=1000000
                          )
    return belt
  
def initSkybox(program):
    skybox = Skybox(filenames=[
                        #"textures/galaxy/stars_xPos.png",
                        #"textures/galaxy/stars_xNeg.png",
                        #"textures/galaxy/stars_yPos.png",
                        #"textures/galaxy/stars_yNeg.png",
                        "textures/galaxy/stars_zPos.png",
                        "textures/galaxy/stars_zPos.png",
                        "textures/galaxy/stars_zPos.png",
                        "textures/galaxy/stars_zPos.png",
                        "textures/galaxy/stars_zPos.png",
                        "textures/galaxy/stars_zPos.png",
                        #"textures/galaxy/stars_zNeg.png"
                        ],
                    program=program)

    return skybox

def initSpaceship(program):
    spaceship = Spaceship(filename='asteroid_model.obj',
			  texImg='textures/metalic2.jpg',
                          shininess=30,
                          ka=0.5,
                          kd=0.9,
                          ks=0.6,
                          program=program)

    return spaceship

def initPlanets(classicProgram, normalMapProgram, highDef=None):
    p = normalMapProgram if highDef else classicProgram
    sun = Sun(name="Sun",
              position=vec3([0, 0, 0]),
              texImg="textures/sun.jpg",
              radius=17.25,
              mass=1.988435e30,
              spin=24.2,
              shininess=30,
              ka=1.0,
              kd=0.9,
              ks=0.6,
              program=classicProgram)

    mercury = Planet(name="Mercury",
                     parent=sun,
                     texImg="textures/mercury.jpg" if highDef else
                     "textures/old/mercury.jpg",
                     radius=2.4,
                     mass=3.30104e23,
                     velocity=vec3([0, 0, 4.74e-5]),
                     distance=50.32,
                     spin=58.64,
                     shininess=30,
                     ka=0.5,
                     kd=0.9,
                     ks=0.6,
                     program=classicProgram)

    venus = Planet(name="Venus",
                   parent=sun,
                   texImg="textures/venus.jpg" if highDef else
                   "textures/old/venus.jpg",
                   normalMap="textures/venusnormal.png" if highDef else None,
                   radius=6.0,
                   mass=4.86732e24,
                   velocity=vec3([0, 0, 3.5e-5]),
                   distance=108.0,
                   spin=-243.0,
                   shininess=30,
                   ka=0.5,
                   kd=0.9,
                   ks=0.6,
                   program=p)

    earth = Planet(name="Earth",
                   parent=sun,
                   texImg="textures/earth.png" if highDef else
                   "textures/old/earth.jpg",
                   normalMap="textures/earthnormal.png" if highDef else None,
                   radius=6.3,
                   mass=5.9722e24,
                   velocity=vec3([0, 0, 2.963e-5]),
                   distance=150,
                   spin=1.0,
                   shininess=30,
                   ka=0.5,
                   kd=0.9,
                   ks=0.6,
                   program=p)

    mars = Planet(name="Mars",
                  parent=sun,
                  texImg="textures/mars.png" if highDef else
                  "textures/old/mars.jpg",
                  normalMap="textures/marsnormal.png" if highDef else None,
                  radius=3.3,
                  mass=6.41693e23,
                  velocity=vec3([0, 0, 2.228175e-5]),
                  distance=227.94,
                  spin=1.05,
                  shininess=30,
                  ka=0.5,
                  kd=0.9,
                  ks=0.6,
                  program=p)

    return [sun, mercury, venus, earth, mars]


