from planet import Planet, Sun
from spaceship import Spaceship
from asteroids import Asteroids
from skybox import Skybox
from pyrr import Vector3 as vec3

def initObjects(classicProgram, normalMapProgram, skyboxProgram, asteroidProgram):
    print 'loading planets'
    planets = initPlanets(classicProgram, normalMapProgram, highDef=True)
    print 'loading spaceship'
    spaceship = initSpaceship(classicProgram)
    print 'loading skybox'
    skybox = initSkybox(skyboxProgram, highDef=False)
    print 'loading belt'
    belt = initBelt(asteroidProgram)
    return planets, spaceship, skybox, belt

def initBelt(program):
    belt = Asteroids(filename='objects/ida.obj',
			  texImg='textures/ida.jpg',
                          shininess=30,
                          ka=0.5,
                          kd=0.9,
                          ks=0.6,
                          program=program,
                          radius=500,
                          offset=140,
                          amount=3000
                          )
    return belt
  
def initSkybox(program, highDef=False):
    if not highDef:
        # The other sides look pretty bad so we just duplicate this one
        filenames = [#"textures/galaxy/stars_xPos.png",
                     #"textures/galaxy/stars_xNeg.png",
                     #"textures/galaxy/stars_yPos.png",
                     #"textures/galaxy/stars_yNeg.png",
                     "textures/galaxy/stars_zPos1.jpg",
                     "textures/galaxy/stars_zPos1.jpg",
                     "textures/galaxy/stars_zPos1.jpg",
                     "textures/galaxy/stars_zPos1.jpg",
                     "textures/galaxy/stars_zPos1.jpg",
                     "textures/galaxy/stars_zPos1.jpg",
                     #"textures/galaxy/stars_zNeg.png"
                     ]
    else:
        filenames = ["textures/galaxy/skybox_right1.png",
                     "textures/galaxy/skybox_left2.png",
                     "textures/galaxy/skybox_top3.png",
                     "textures/galaxy/skybox_bottom4.png",
                     "textures/galaxy/skybox_front5.png",
                     "textures/galaxy/skybox_back6.png"
                     ]
    skybox = Skybox(filenames=filenames,
                    program=program)

    return skybox

def initSpaceship(program):
    spaceship = Spaceship(filename='objects/spaceship.obj',
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
                  velocity=vec3([0, 0, 2.41e-5]),
                  distance=227.94,
                  spin=1.05,
                  shininess=30,
                  ka=0.5,
                  kd=0.9,
                  ks=0.6,
                  program=p)

    jupiter = Planet(name="Jupiter",
                  parent=sun,
                  texImg="textures/jupiter.jpg",
                  radius=71.4,
                  mass=2e27,
                  velocity=vec3([0, 0, 1.31e-5]),
                  distance=778,
                  spin=0.4,
                  shininess=30,
                  ka=0.5,
                  kd=0.9,
                  ks=0.6,
                  program=classicProgram)

    saturn = Planet(name="Saturn",
                  parent=sun,
                  texImg="textures/saturn.jpg",
                  radius=60.2,
                  mass=5.7e26,
                  velocity=vec3([0, 0, 0.96e-5]),
                  distance=1427,
                  spin=0.42,
                  shininess=30,
                  ka=0.5,
                  kd=0.9,
                  ks=0.6,
                  program=classicProgram)

    uranus = Planet(name="Uranus",
                  parent=sun,
                  texImg="textures/uranus.jpg",
                  radius=25.55,
                  mass=8.7e25,
                  velocity=vec3([0, 0, 0.68e-5]),
                  distance=2871,
                  spin=0.72,
                  shininess=30,
                  ka=0.5,
                  kd=0.9,
                  ks=0.6,
                  program=p)

    neptune = Planet(name="Neptune",
                  parent=sun,
                  texImg="textures/neptune.jpg",
                  radius=24.764,
                  mass=1e26,
                  velocity=vec3([0, 0, 0.54e-5]),
                  distance=4500,
                  spin=0.62,
                  shininess=30,
                  ka=0.5,
                  kd=0.9,
                  ks=0.6,
                  program=p)



    return [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


