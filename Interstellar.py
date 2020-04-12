from PIL import Image
import random
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import turtle

pi = 3.14159265359
radeg = 180 / pi


def fnasin(x):
    return math.atan(x / math.sqrt(1 - x * x))


def fnacos(x):
    return pi / 2 - fnasin(x)


def fnsind(x):
    return math.sin(x / radeg)


def fncosd(x):
    return math.cos(x / radeg)


def fntand(x):
    return math.tan(x / radeg)


def fnasind(x):
    return radeg * math.atan(x / math.sqrt(1 - x * x))


def fnacosd(x):
    return 90 - fnasind(x)


def fnatand(x):
    return radeg * math.atan(x)


def fnrev(x):
    return x - int(x // 360) * 360


def fnatan2(y, x):
    return math.atan(y / x) - pi * (x < 0)


def fnatan2d(y, x):
    if x > 0:

        return fnatand(y / x)

    elif x < 0:
        if y >= 0:
            return fnatand(y / x) + 180
        else:
            return fnatand(y / x) + 180
    else:
        print("null")


def fncbrt(x):
    if x == 0:
        return 0
    elif x < 0:
        return math.exp(math.log(-x) / 3)
    else:
        return math.exp(math.log(x) / 3)


def hourdecimal(hr, min, sec):
    return hr + 1 / (60 * min) + 1 / (3600 * sec)


def decimalhour(dec):
    hr = int(dec)
    min = int((dec - hr) * 60)
    sec = ((dec - hr) * 60 - min) * 60
    return [hr, min, sec]


def sphertorect(RA, r, Decl):
    x = r * math.cos(RA) * math.cos(Decl)
    y = r * math.sin(RA) * math.cos(Decl)
    z = r * math.sin(Decl)
    return (x, y, z)


def getd(Y, M, D):
    return 367 * Y - (7 * (Y + ((M + 9) / 12))) / 4 - ((3 * (Y + (M - 9) / 7) / 100) + 1) / 4 + 275 * M / 9 + D - 730515


def RAtoHour(ra):
    return decimalhour(ra / 15)


def sunpos(d):
    '''
    :param d:
    :return: x,y,z position of the sun and RA decline and distance at given date
    '''

    w = 282.9404 + 4.70935E-5 * d
    a = 1.000000
    e = 0.016709 - 1.151E-9 * d
    global Ms  # global sun M
    Ms = fnrev(356.0470 + 0.9856002585 * d)  # degree
    oblecl = 23.4393 - 3.563E-7 * d
    global Ls
    Ls = fnrev(w + Ms)  # degree

    E = Ms + (180 / pi) * e * fnsind((Ms)) * (1 + e * fncosd((Ms)))

    x = fncosd(E) - e
    y = fnsind(E) * math.sqrt(1 - e * e)

    r = math.sqrt(x * x + y * y)
    v = fnrev(fnatan2d(y, x))

    lon = fnrev(v + w)

    x = r * fncosd(lon)
    y = r * fnsind(lon)
    z = 0.0

    xequat = x
    yequat = y * fncosd(oblecl) - 0.0 * fnsind(23.4406)
    zequat = y * fnsind(oblecl) + 0.0 * fncosd(23.4406)
    r = math.sqrt(xequat * xequat + yequat * yequat + zequat * zequat)
    RA = RAtoHour(fnatan2d(yequat, xequat))
    Decl = fnatan2d(zequat, math.sqrt(xequat * xequat + yequat * yequat))
    return {'xsun': x, 'ysun': y, 'zsun': z, 'r': r, 'RA': RA, 'Decl': Decl}


# def Moon(d):
#     N = fnrev(125.1228 - 0.0529538083 * d)
#     i = fnrev(5.1454)
#     w = fnrev(318.0634 + 0.1643573223 * d)
#     a = 60.2666
#     e = 0.054900
#     Mm = fnrev(115.3654 + 13.0649929509 * d)
#     E0 = Mm + (180 / pi) * e * fnsind(Mm) * (1 + e * fncosd(Mm))
#     E = (precise(E0, Mm, e))
#     x = a * (fncosd(E) - e)
#     y = a * math.sqrt(1 - e * e) * fnsind(E)
#     r = math.sqrt(x * x + y * y)
#     v = fnatan2d(y, x)
#     xeclip = r * (fncosd(N) * fncosd(v + w) - fnsind(N) * fnsind(v + w) * fncosd(i))
#     yeclip = r * (fnsind(N) * fncosd(v + w) + fncosd(N) * fnsind(v + w) * fncosd(i))
#     zeclip = r * fnsind(v + w) * fnsind(i)
#     long = fnatan2d(yeclip, xeclip)
#     lat = fnatan2d(zeclip, math.sqrt(xeclip * xeclip + yeclip * yeclip))
#     r = math.sqrt(xeclip * xeclip + yeclip * yeclip + zeclip * zeclip)
#     Lm = fnrev(N + w + Mm)
#     D = fnrev(Lm - Ls)
#     F = fnrev(Lm - N)
#     Per_long = -1.274 * fnsind(Mm - 2 * D) + 0.658 * fnsind(2 * D) - 0.186 * fnsind(Ms) - 0.059 * fnsind(
#         2 * Mm - 2 * D) - 0.057 * fnsind(Mm - 2 * D + Ms) + 0.053 * fnsind(Mm + 2 * D) + 0.046 * fnsind(
#         2 * D - Ms) + 0.041 * fnsind(Mm - Ms) - 0.035 * fnsind(D) - 0.031 * fnsind(Mm + Ms) - 0.015 * fnsind(
#         2 * F - 2 * D) + 0.011 * fnsind(Mm - 4 * D)
#     Per_lat = -0.173 * fnsind(F - 2 * D) - 0.055 * fnsind(Mm - F - 2 * D) - 0.046 * fnsind(
#         Mm + F - 2 * D) + 0.033 * fnsind(F + 2 * D) + 0.017 * fnsind(2 * Mm + F)
#     Lu_dis = -0.58 * fncosd(Mm - 2 * D) - 0.46 * fncosd(2 * D)
#     long += Per_long
#     lat += Per_lat
#     r += Lu_dis
#     oblecl = 23.4393 - 3.563E-7 * d
#     xeclip = fncosd(long) * fncosd(lat)
#     yeclip = fnsind(long) * fncosd(lat)
#     zeclip = fnsind(lat)
#     xequat = xeclip
#     yequat = yeclip * fncosd(oblecl) - zeclip * fnsind(oblecl)
#     zequat = yeclip * fnsind(oblecl) + zeclip * fncosd(oblecl)
#
#     RA = fnrev(fnatan2d(yequat, xequat))
#     Decl = fnatan2d(zequat, math.sqrt(xequat * xequat + yequat * yequat))
#
#     # print(RA,Decl)


def precise(E0, M, e):
    E1 = E0 - (E0 - (180 / pi) * e * fnsind(E0) - M) / (1 - e * fncosd(E0))

    while abs(E1 - E0) > 0.005:
        E0 = precise(E1, M, e)

    return E1


def planetpos(planet, d):
    E0 = planet.M + (180 / pi) * planet.e * fnsind(planet.M) * (1 + planet.e * fncosd(planet.M))

    E = (precise(E0, planet.M, planet.e))
    x = planet.a * (fncosd(E) - planet.e)
    y = planet.a * math.sqrt(1 - planet.e * planet.e) * fnsind(E)

    r = math.sqrt(x * x + y * y)
    v = fnatan2d(y, x)
    xeclip = r * (fncosd(planet.N) * fncosd(v + planet.w) - fnsind(planet.N) * fnsind(v + planet.w) * fncosd(planet.i))
    yeclip = r * (fnsind(planet.N) * fncosd(v + planet.w) + fncosd(planet.N) * fnsind(v + planet.w) * fncosd(planet.i))
    zeclip = r * fnsind(v + planet.w) * fnsind(planet.i)

    oblecl = 23.4393 - 3.563E-7 * d
    xequat = xeclip
    yequat = yeclip * fncosd(oblecl) - zeclip * fnsind(oblecl)
    zequat = yeclip * fnsind(oblecl) + zeclip * fncosd(oblecl)

    long = fnatan2d(yeclip, xeclip)
    lat = fnatan2d(zeclip, math.sqrt(xeclip * xeclip + yeclip * yeclip))
    r = math.sqrt(xeclip * xeclip + yeclip * yeclip + zeclip * zeclip)

    RA = fnrev(fnatan2d(yequat, xequat))
    Decl = fnatan2d(zequat, math.sqrt(xequat * xequat + yequat * yequat))

    if planet == 'saturn':
        long += 0.812 * fnsind(2 * jupiter.M - 5 * planet.M - 67.6) - 0.229 * fncosd(
            2 * jupiter.M - 4 * planet.M - 2) + 0.119 * fnsind(jupiter.M - 2 * planet.M - 3) + 0.046 * fnsind(
            2 * jupiter.M - 6 * planet.M - 69) + 0.014 * fnsind(jupiter.M - 3 * planet.M + 32)
        lat += -0.020 * fncosd(2 * jupiter.M - 4 * planet.M - 2) + 0.018 * fnsind(2 * jupiter.M - 6 * planet.M - 49)
    elif planet == 'uranus':
        long += +0.040 * fnsind(saturn.M - 2 * planet.M + 6) + 0.035 * fnsind(
            saturn.M - 3 * planet.M + 33) - 0.015 * fnsind(jupiter.M - planet.M + 20)
    elif planet == 'jupiter':
        long += -0.332 * fnsind(2 * jupiter.M - 5 * saturn.M - 67.6)
        -0.056 * fnsind(2 * jupiter.M - 2 * saturn.M + 21)
        +0.042 * fnsind(3 * jupiter.M - 5 * saturn.M + 21)
        -0.036 * fnsind(jupiter.M - 2 * saturn.M)
        +0.022 * fncosd(jupiter.M - saturn.M)
        +0.023 * fnsind(2 * jupiter.M - 3 * saturn.M + 52)
        -0.016 * fnsind(jupiter.M - 5 * saturn.M - 69)
    return {'xp': xeclip, 'yp': yeclip, 'zp': zeclip, 'r': r, 'RA': RA, 'Decl': Decl}
    # print(RA, Decl, r)


def Geocentri(d, planet):
    x = sunpos(d)['xsun'] + planetpos(planet, d)['xp']
    y = sunpos(d)['ysun'] + planetpos(planet, d)['yp']
    z = sunpos(d)['zsun'] + planetpos(planet, d)['zp']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z, c='r', marker='o')
    ax.scatter(0, 0, 0, c='y', marker='o')
    ax.set_xlabel("in AU")
    ax.set_ylabel("in AU")
    ax.set_zlabel("in AU")

    plt.show()


d = getd(0, 0, 0)


class mercury:
    N = fnrev(48.3313 + 3.24587E-5 * d)
    i = fnrev(7.0047 + 5.00E-8 * d)
    w = fnrev(29.1241 + 1.01444E-5 * d)
    a = 0.387098
    e = 0.205635 + 5.59E-10 * d
    M = fnrev(168.6562 + 4.0923344368 * d)


class venus:
    N = fnrev(76.6799 + 2.46590E-5 * d)
    i = fnrev(3.3946 + 2.75E-8 * d)
    w = fnrev(54.8910 + 1.38374E-5 * d)
    a = 0.723330
    e = 0.006773 - 1.302E-9 * d
    M = fnrev(48.0052 + 1.6021302244 * d)


class earth:
    N = -11.26064
    i = 23.4
    w = 102.94719
    a = 1.00000011
    e = 0.01671022
    M = 355.53


class mars:
    N = fnrev(49.5574 + 2.11081E-5 * d)
    i = fnrev(1.8497 - 1.78E-8 * d)
    w = fnrev(286.5016 + 2.92961E-5 * d)
    a = 1.523688
    e = 0.093405 + 2.516E-9 * d
    M = fnrev(18.6021 + 0.5240207766 * d)


class jupiter:
    N = fnrev(100.4542 + 2.76854E-5 * d)
    i = fnrev(1.3030 - 1.557E-7 * d)
    w = fnrev(273.8777 + 1.64505E-5 * d)
    a = 5.20256
    e = 0.048498 + 4.469E-9 * d
    M = fnrev(19.8950 + 0.0830853001 * d)


class saturn:
    N = fnrev(113.6634 + 2.38980E-5 * d)
    i = fnrev(2.4886 - 1.081E-7 * d)
    w = fnrev(339.3939 + 2.97661E-5 * d)
    a = 9.55475
    e = 0.055546 - 9.499E-9 * d
    M = fnrev(316.9670 + 0.0334442282 * d)


class uranus:
    N = fnrev(74.0005 + 1.3978E-5 * d)
    i = fnrev(0.7733 + 1.9E-8 * d)
    w = fnrev(96.6612 + 3.0565E-5 * d)
    a = 19.18171 - 1.55E-8 * d
    e = 0.047318 + 7.45E-9 * d
    M = fnrev(142.5905 + 0.011725806 * d)


class neptune:
    N = fnrev(131.7806 + 3.0173E-5 * d)
    i = fnrev(1.7700 - 2.55E-7 * d)
    w = fnrev(272.8461 - 6.027E-6 * d)
    a = 30.05826 + 3.313E-8 * d
    e = 0.008606 + 2.15E-9 * d
    M = fnrev(260.2471 + 0.005995147 * d)


print(
    "Welcome to our project- Interstellar!\nIn this project, you'll be able to access some basic information about the planets in our Solar System, and \nthere's a surprise for you after you answer a few random questions related to the content you read in the search for the planet of your choice.\nSo let's get you started!")
planet_choice = str.lower(input("Input the planet's name you want to search about:\n"))

if planet_choice == "mercury":
    print(
        "As you have chosen Mercury as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print(
        "Mercury is the closest planet (first) to the Sun and due to its proximity, it is not easily seen except during twilight.")
    print(
        "For every two orbits of the Sun, Mercury completes three rotations about its axis and up until 1965 it was thought \nthat the same side of Mercury constantly faced the Sun. Thirteen times a century Mercury can be observed from the Earth \npassing across the face of the Sun in an event called a *transit*.\n")
    print("Planet Profile:")
    print("Diameter:	4,879 km")
    print("Mass:	3.30 x 10^23 kgs (5.5% Earth)")
    print("Moon(s):	None")
    print("Orbit Distance:	57,909,227 kms (0.39 AU)")
    print("Orbit Period:	88 days")
    print("Surface Temperature:	-173°C to 427°C")
    print("First Record:	14th century BC")
    print("Recorded By:	Assyrian astronomers\n")
    print("QUICK MERCURY FACTS:")
    print("•Mercury does not have any moons or rings.")
    print("•Your weight on Mercury would be 38% of your weight on Earth.")
    print("•A day on the surface of Mercury lasts 176 Earth days.")
    print("•A year on Mercury takes 88 Earth days.")
    print("•Mercury has a diameter of 4,879 km, making it the smallest planet.")
    print("•It is not known who discovered Mercury.")
    myImage = Image.open("Images/planet-mercury.png")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quesmercury = ['How many moons does Mercury has?', 'In which direction does Mercury rotate?',
                       "What's the diameter of Mercury?"]
        choice = random.choice(quesmercury)
        print(choice)
        ansmercury = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quesmercury[0]:
            if ansmercury == "0" or ansmercury == "none" or ansmercury == "no" or ansmercury == "zero":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quesmercury[1]:
            if ansmercury == "counterclockwise" or ansmercury == "counter-clockwise" or ansmercury == "anticlockwise" or ansmercury == "anti-clockwise":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quesmercury[2]:
            if ansmercury == "4879km" or ansmercury == "4896000m" or ansmercury == "4896":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay :( As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")

elif planet_choice == "venus":
    print(
        "As you have chosen Venus as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print(
        "Venus is the second planet from the Sun and is the second brightest object in the night sky after the Moon. ")
    print(
        "Named after the Roman goddess of love and beauty, Venus is the second largest terrestrial planet and is sometimes referred to as the Earth’s sister planet due the their similar size and mass.")
    print("The surface of the planet is obscured by an opaque layer of clouds made up of sulphuric acid.\n")
    print("Venus Planet Profile:")
    print("Diameter:	12,104 km")
    print("Mass:	4.87 x 10^24 kg (81.5% Earth)")
    print("Moons:	None")
    print("Orbit Distance:	108,209,475 km (0.73 AU)")
    print("Orbit Period:	225 days")
    print("Surface Temperature:	462 °C")
    print("First Record:	17th century BC")
    print("Recorded By:	Babylonian astronomers\n")
    print("QUICK VENUS FACTS:")
    print("•Venus does not have any moons or rings.")
    print("•Venus is nearly as big as the Earth with a diameter of 12,104 km.")
    print("•Venus is thought to be made up of a central iron core, rocky mantle and silicate crust.")
    print("•A day on the surface of Venus (solar day) would appear to take 117 Earth days.")
    print("•A year on Venus takes 225 Earth days.")
    print("•The surface temperature on Venus can reach 471 °C.")
    myImage = Image.open("Images/planet-venus.png")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quesvenus = ['How many moons does Venus has?', 'In which direction does Venus rotate?',
                     "What's the diameter of Venus?"]
        choice = random.choice(quesvenus)
        print(choice)
        ansvenus = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quesvenus[0]:
            if ansvenus == "0" or ansvenus == "none" or ansvenus == "no" or ansvenus == "zero":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quesvenus[1]:
            if ansvenus == "clockwise" or ansvenus == "clock-wise":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quesvenus[2]:
            if ansvenus == "12104km" or ansvenus == "12104" or ansvenus == "1210400m":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay :( As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")

elif planet_choice == "earth":
    print(
        "As you have chosen Earth, our only home hitherto, as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print("Earth is the third planet from the Sun and is the largest of the terrestrial planets.")
    print("The Earth is the only planet in our solar system not to be named after a Greek or Roman deity.")
    print("The Earth was formed approximately 4.54 billion years ago and is the only known planet to support life.")
    print("Earth Planet Profile:")
    print("Equatorial Diameter:	12,756 km")
    print("Polar Diameter:	12,714 km")
    print("Mass:	5.97 x 10^24 kg")
    print("Moons:	1 (The Moon)")
    print("Orbit Distance:	149,598,262 km (1 AU)")
    print("Orbit Period:	365.24 days")
    print("Surface Temperature:	-88 to 58°C")
    print("QUICK EARTH FACTS:")
    print("•There are actually 23 hours, 56 minutes, 4.1 seconds in one day (Yes! It's not 24 hours)")
    print("•The Earth’s rotation is gradually slowing.")
    print("•The Earth was once believed to be the centre of the universe.")
    print("•Earth has a powerful magnetic field.")
    print("•There is only one natural satellite of the planet Earth.")
    print("•Earth is the only planet not named after a god.")
    print("•The Earth is the densest planet in the Solar System.")
    myImage = Image.open("Images/planet-earth.png")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quesearth = ['How many moons does Earth has?', 'In which direction does Earth rotate?',
                     "What's the diameter of Earth?"]
        choice = random.choice(quesearth)
        print(choice)
        ansearth = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quesearth[0]:
            if ansearth == "1" or ansearth == "one" or ansearth == "the moon" or ansearth == "moon":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quesearth[1]:
            if ansearth == "counterclockwise" or ansearth == "counter-clockwise" or ansearth == "anticlockwise" or ansearth == "anti-clockwise":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quesearth[2]:
            if ansearth == "12756km" or ansearth == "12714km" or ansearth == "12756" or ansearth == "12714":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay. As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")


elif planet_choice == "mars":
    print(
        "As you have chosen Mars as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print("Mars is the fourth planet from the Sun and is the second smallest planet in the solar system.")
    print(
        "Named after the Roman god of war, Mars is also often described as the “Red Planet” due to its reddish appearance.")
    print("Mars is a terrestrial planet with a thin atmosphere composed primarily of carbon dioxide.\n")
    print("Mars Planet Profile:")
    print("Equatorial Diameter:	6,792 km")
    print("Polar Diameter:	6,752 km")
    print("Mass:	6.42 x 10^23 kg (10.7% Earth)")
    print("Moons:	2 (Phobos & Deimos)")
    print("Orbit Distance:	227,943,824 km (1.52 AU)")
    print("Orbit Period:	687 days (1.9 years)")
    print("Surface Temperature:	-153°C to 20 °C")
    print("First Record:	2nd millennium BC")
    print("Recorded By:	Egyptian astronomers\n")
    print("QUICK MARS FACTS:")
    print("•Mars and Earth have approximately the same landmass.")
    print("•Mars is home to the tallest mountain in the solar system.")
    print("•Only 26 missions to Mars have been successful(out of 56, hitherto).")
    print("•Mars has the largest dust storms in the solar system.")
    print("•On Mars, the Sun appears about half the size as it does on Earth.")
    print("•Pieces of Mars have fallen to Earth.")
    print("•There are signs of liquid water on Mars.")
    print("•One day Mars will have a ring(but that's gonna take 20-40 million years from now, phew!).")
    myImage = Image.open("Images/planet-mars.jpg")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quesmars = ['How many moons does Mars has?', 'In which direction does Mars rotate?',
                    "What's the diameter of Mars?"]
        choice = random.choice(quesmars)
        print(choice)
        ansmars = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quesmars[0]:
            if ansmars == "2" or ansmars == "two":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quesmars[1]:
            if ansmars == "counterclockwise" or ansmars == "counter-clockwise" or ansmars == "anticlockwise" or ansmars == "anti-clockwise":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quesmars[2]:
            if ansmars == "6792km" or ansmars == "6752km" or ansmars == "6792" or ansmars == "6752":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay. As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")

elif planet_choice == "jupiter":
    print(
        "As you have chosen Jupiter as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print(
        "The planet Jupiter is the fifth planet out from the Sun, and is two and a half times more massive than all the other planets in the solar system combined.")
    print("It is made primarily of gases and is therefore known as a “gas giant”.")
    print("Jupiter Planet Profile:")
    print("Equatorial Diameter:	142,984 km")
    print("Polar Diameter:	133,709 km")
    print("Mass:	1.90 × 10^27 kg (318 Earths)")
    print("Moons:	79 (Io, Europa, Ganymede & Callisto)")
    print("Rings:	4")
    print("Orbit Distance:	778,340,821 km (5.20 AU)")
    print("Orbit Period:	4,333 days (11.9 years)")
    print("Effective Temperature:	-148 °C")
    print("First Record:	7th or 8th century BC")
    print("Recorded By:	Babylonian astronomers\n")
    print("QUICK JUPITER FACTS:")
    print("•Jupiter is the fourth brightest object in the solar system.")
    print("•The ancient Babylonians were the first to record their sightings of Jupiter.")
    print("•Jupiter has the shortest day of all the planets.")
    print("•Jupiter orbits the Sun once every 11.8 Earth years.")
    print(
        "•Jupiter has unique cloud features. The upper atmosphere of Jupiter is divided into cloud belts and zones. They are made primarily of ammonia crystals, sulfur, and mixtures of the two compounds.")
    print("•The Great Red Spot is a huge storm on Jupiter.")
    print("•Jupiter’s interior is made of rock, metal, and hydrogen compounds.")
    print("•Jupiter’s moon Ganymede is the largest moon in the solar system.")
    print("•Jupiter has a thin ring system. They are between 2,000 to 12,500 kilometres thick.")
    print("•Eight spacecrafts have visited Jupiter.")
    print(
        "•Ganymede Moon Facts: Ganymede is Jupiter’s largest moon and also the largest moon in the solar system, discovered in 1610 by astronomer Galileo Galilei.")
    myImage = Image.open("Images/planet-jupiter.png")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quesjupiter = ['How many moons does Jupiter has?', 'How many spacecrafts have visited the Jupiter?',
                       "What's the name of the storm found on the surface of the Jupiter?"]
        choice = random.choice(quesjupiter)
        print(choice)
        ansjupiter = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quesjupiter[0]:
            if ansjupiter == "79" or ansjupiter == "seventy nine" or ansjupiter == "seventy-nine" or ansjupiter == "seventynine":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quesjupiter[1]:
            if ansjupiter == "8" or ansjupiter == "eight" or ansjupiter == "08":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quesjupiter[2]:
            if ansjupiter == "the great red spot" or ansjupiter == "great red spot" or ansjupiter == "giant red spot" or ansjupiter == "the giant red spot":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay. As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")

elif planet_choice == "saturn":
    print(
        "As you have chosen Saturn-'The ringed planet' as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print("Saturn is the sixth planet from the Sun and the most distant that can be seen with the naked eye.")
    print(
        "Saturn is the second largest planet and is best known for its fabulous ring system that was first observed in 1610 by the astronomer Galileo Galilei. Like Jupiter, Saturn is a gas giant and is composed of similar gasses including hydrogen, helium and methane.")
    print("Saturn Planet Profile:")
    print("Equatorial Diameter:	120,536 km")
    print("Polar Diameter:	108,728 km")
    print("Mass:	5.68 × 10^26 kg (95 Earths)")
    print("Moons:	62 (Titan, Enceladus, Iapetus & Rhea)")
    print("Rings:	30+ (7 Groups)")
    print("Orbit Distance:	1,426,666,422 km (9.54 AU)")
    print("Orbit Period:	10,756 days (29.5 years)")
    print("Effective Temperature:	-178 °C")
    print("First Record:	8th century BC")
    print("Recorded By:	Assyrians\n")
    print("QUICK SATURN FACTS:")
    print("•Saturn can be seen with the naked eye.")
    print("•Saturn was known to the ancients, including the Babylonians and Far Eastern observers.")
    print("•Saturn is the flattest planet.")
    print("•Saturn orbits the Sun once every 29.4 Earth years.")
    print("•Saturn’s upper atmosphere is divided into bands of clouds.")
    print("•Saturn has oval-shaped storms similar to Jupiter’s.")
    print("•Saturn is made mostly of hydrogen.")
    print("•Saturn has the most extensive rings in the solar system.")
    print("•Saturn has 150 moons and smaller moonlets.")
    print("•Titan is a moon with complex and dense nitrogen-rich atmosphere.")
    print(
        "•Four spacecrafts have visited Saturn. Cassini orbited Saturn from July 2004 until September 2017, sending back a wealth of data about the planet, its moons, and rings.")
    myImage = Image.open("Images/planet-saturn.png")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quessaturn = ['How many moons does Saturn has?', 'How many spacecrafts have visited the Saturn?',
                      "Which element is abundantly found on Saturn?"]
        choice = random.choice(quessaturn)
        print(choice)
        anssaturn = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quessaturn[0]:
            if anssaturn == "150" or anssaturn == "one fifty" or anssaturn == "one hundred fifty" or anssaturn == "one hundred and fifty":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quessaturn[1]:
            if anssaturn == "4" or anssaturn == "four" or anssaturn == "04":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quessaturn[2]:
            if anssaturn == "hydrogen" or anssaturn == "h2" or anssaturn == "h":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay. As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")

elif planet_choice == "uranus":
    print(
        "As you have chosen Uranus as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print("Uranus is the seventh planet from the Sun.")
    print(
        "While being visible to the naked eye, it was not recognised as a planet due to its dimness and slow orbit. Uranus became the first planet discovered with the use of a telescope.")
    print(
        "Uranus is tipped over on its side with an axial tilt of 98 degrees. It is often described as 'rolling around the Sun on its side'.")
    print("Uranus Planet Profile:")
    print("Equatorial Diameter:	51,118 km")
    print("Polar Diameter:	49,946 km")
    print("Mass:	8.68 × 10^25 kg (15 Earths)")
    print("Moons:	27 (Miranda, Titania, Ariel, Umbriel & Oberon)")
    print("Rings:	13")
    print("Orbit Distance:	2,870,658,186 km (19.19 AU)")
    print("Orbit Period:	30,687 days (84.0 years)")
    print("Effective Temperature:	-216 °C")
    print("Discovery Date:	March 13th 1781")
    print("Discovered By:	William Herschel\n")
    print("QUICK URANUS FACTS:")
    print("•Uranus was officially discovered by Sir William Herschel in 1781.")
    print("•Uranus turns on its axis once every 17 hours, 14 minutes.")
    print("•Uranus makes one trip around the Sun every 84 Earth years.")
    print("•Uranus is often referred to as an “ice giant” planet.")
    print("•Uranus hits the coldest temperatures of any planet.")
    print("•Uranus has two sets of very thin dark coloured rings.")
    print("•Uranus’ moons are named after characters created by William Shakespeare and Alexander Pope.")
    print("•Only one spacecraft has flown by Uranus.")
    myImage = Image.open("Images/planet-uranus.jpg")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quesuranus = ['How many moons does Uranus has?', 'How many spacecrafts have flown by the Uranus?',
                      "What's the other name for the planet 'Uranus'?"]
        choice = random.choice(quesuranus)
        print(choice)
        ansuranus = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quesuranus[0]:
            if ansuranus == "27" or ansuranus == "twenty seven" or ansuranus == "twenty-seven":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quesuranus[1]:
            if ansuranus == "1" or ansuranus == "one" or ansuranus == "only one":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quesuranus[2]:
            if ansuranus == "ice giant" or ansuranus == "the ice giant" or ansuranus == "ice-giant":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay. As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")


elif planet_choice == "neptune":
    print(
        "As you have chosen Neptune as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print("Neptune is the eighth planet from the Sun making it the most distant in the solar system.")
    print(
        "This gas giant planet may have formed much closer to the Sun in early solar system history before migrating to its present position.")
    print("Neptune Planet Profile:")
    print("Equatorial Diameter:	49,528 km")
    print("Polar Diameter:	48,682 km")
    print("Mass:	1.02 × 10^26 kg (17 Earths)")
    print("Moons:	14 (Triton)")
    print("Rings:	5")
    print("Orbit Distance:	4,498,396,441 km (30.10 AU)")
    print("Orbit Period:	60,190 days (164.8 years)")
    print("Effective Temperature:	-214 °C")
    print("Discovery Date:	September 23rd 1846")
    print("Discovered By:	Urbain Le Verrier & Johann Galle\n")
    print("QUICK NEPTUNE FACTS:")
    print("•Neptune was not known to the ancients.")
    print("•Neptune spins on its axis very rapidly.")
    print("•Neptune is the smallest of the ice giants.")
    print("•The atmosphere of Neptune is made of hydrogen and helium, with some methane.")
    print("•Neptune has a very active climate.")
    print("•Neptune has a very thin collection of rings.")
    print("•Neptune has 14 moons.")
    print("•Only one spacecraft has flown by Neptune- the Voyager 2.")
    print(
        "•The Great Dark Spot in the southern atmosphere of Neptune is an incredibly large rotating storm system with winds of upto 1,500 miles per hour, the strongest winds recorded on any planet.")
    print(
        "•Neptune has an incredibly thick atmosphere comprised of 74% hydrogen, 25% helium and approximately 1% methane.")
    myImage = Image.open("Images/planet-neptune.png")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quesneptune = ['How many moons does Neptune has?', 'Name the spacecraft that flew by the Neptune',
                       "In which hemisphere of the Neptune, is the Great Dark Spot found?"]
        choice = random.choice(quesneptune)
        print(choice)
        ansneptune = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quesneptune[0]:
            if ansneptune == "14" or ansneptune == "fourteen":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quesneptune[1]:
            if ansneptune == "the voyager2" or ansneptune == "the voyager 2" or ansneptune == "voyager2" or ansneptune == "voyager 2":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quesneptune[2]:
            if ansneptune == "southern" or ansneptune == "not northern" or ansneptune == "south":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay. As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")

elif planet_choice == "pluto":
    print(
        "As you have chosen Pluto as the planet of your choice, here we present to you, some weird unknown (or maybe known) facts about it:\n")
    print("Introduction:")
    print("Pluto is the second closest dwarf planet to the Sun and was at one point classified as the ninth planet.")
    print("Pluto is the largest dwarf planet but only the second most massive, with Eris being the most massive.")
    print("Pluto Planet Profile:")
    print("Diameter:	2,372 km")
    print("Mass:	1.31 × 10^22 kg (0.17 Moons)")
    print("Orbit Distance:	5,874,000,000 km (39.26 AU)")
    print("Orbit Period:	248.0 years")
    print("Surface Temperature:	-229°C")
    print("Moons:	5 (Charon)")
    print("Discovery Date:	February 18th 1930")
    print("Discovered By:	Clyde W. Tombaugh\n")
    print("QUICK PLUTO FACTS:")
    print("•Pluto is named after the Greek god of the underworld.")
    print("•Pluto was reclassified from a planet to a dwarf planet in 2006.")
    print("•Pluto was discovered on February 18th, 1930 by the Lowell Observatory.")
    print("•Pluto has five known moons.")
    print("•Pluto is the largest dwarf planet.")
    print("•Pluto is one third water.")
    print("•Pluto is smaller than many moons.")
    print("•Pluto has a eccentric and inclined orbit.")
    print("•Pluto has been visited by one spacecraft.")
    print("•Pluto’s location was predicted by Percival Lowell in 1915.")
    print("•Pluto sometimes has an atmosphere.")
    myImage = Image.open("Images/planet-pluto.png")
    myImage.show()

    guess = str.lower(input("Are you ready to access something interesting? Type 'Y' for YES or 'N' for NO:\n"))
    print("Now answer the following question.\n")
    if guess == 'y':
        quespluto = ['How many moons does Pluto has?', 'How many spacecrafts have visited Pluto?',
                     "Pluto is one-third what?"]
        choice = random.choice(quespluto)
        print(choice)
        anspluto = str.lower(input("Enter the answer to access the interesting part:\n"))
        if choice == quespluto[0]:
            if anspluto == "5" or anspluto == "five":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Err...Sorry, study the content provided and try again.")
        elif choice == quespluto[1]:
            if anspluto == "1" or anspluto == "one":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
        elif choice == quespluto[2]:
            if anspluto == "water" or anspluto == "h2o":
                print("Awesome. You're fit for the surprise.")
                planet = eval(planet_choice)
                year = int(input('Enter the year'))
                month = int(input('Enter the month'))
                day = int(input('Enter the day'))

                d = getd(year, month, day)
                # planetpos(planet, d)
                Geocentri(d, planet)
            else:
                print("Errr...Sorry, study the content provided and try again.")
    elif guess == "n":
        print("Ummm, okay. As you say. (This is your loss though!)")
    else:
        print(
            "I don't think there was any choice other than 'Y' or 'N'.. If you pressed another key by mistake, take the pleasure of re-running the code.")


class SolarSystem:
    def __init__(self, width, height):
        self.thesun = None
        self.planets = []
        self.ssturtle = turtle.Turtle()
        self.ssturtle.hideturtle()
        self.ssscreen = turtle.Screen()
        self.ssscreen.setworldcoordinates(-width / 2.0, -height / 2.0, width / 2.0, height / 2.0)
        self.ssscreen.tracer(50)

    def addPlanet(self, aplanet):
        self.planets.append(aplanet)

    def addSun(self, asun):
        self.thesun = asun

    def showPlanets(self):
        for aplanet in self.planets:
            print(aplanet)

    def freeze(self):
        self.ssscreen.exitonclick()

    def movePlanets(self):
        G = .1
        dt = .001

        for p in self.planets:
            p.moveTo(p.getXPos() + dt * p.getXVel(), p.getYPos() + dt * p.getYVel())

            rx = self.thesun.getXPos() - p.getXPos()
            ry = self.thesun.getYPos() - p.getYPos()
            r = math.sqrt(rx ** 2 + ry ** 2)

            accx = G * self.thesun.getMass() * rx / r ** 3
            accy = G * self.thesun.getMass() * ry / r ** 3

            p.setXVel(p.getXVel() + dt * accx)

            p.setYVel(p.getYVel() + dt * accy)


class Sun:
    def __init__(self, iname, irad, im, itemp):
        self.name = iname
        self.radius = irad
        self.mass = im
        self.temp = itemp
        self.x = 0
        self.y = 0

        self.sturtle = turtle.Turtle()
        self.sturtle.shape("circle")
        self.sturtle.color("yellow")

    def getName(self):
        return self.name

    def getRadius(self):
        return self.radius

    def getMass(self):
        return self.mass

    def getTemperature(self):
        return self.temp

    def getVolume(self):
        v = 4.0 / 3 * math.pi * self.radius ** 3
        return v

    def getSurfaceArea(self):
        sa = 4.0 * math.pi * self.radius ** 2
        return sa

    def getDensity(self):
        d = self.mass / self.getVolume()
        return d

    def setName(self, newname):
        self.name = newname

    def __str__(self):
        return self.name

    def getXPos(self):
        return self.x

    def getYPos(self):
        return self.y


class Planet:

    def __init__(self, iname, irad, im, idist, ivx, ivy, ic):
        self.name = iname
        self.radius = irad
        self.mass = im
        self.distance = idist
        self.x = idist
        self.y = 0
        self.velx = ivx
        self.vely = ivy
        self.color = ic

        self.pturtle = turtle.Turtle()
        self.pturtle.up()
        self.pturtle.color(self.color)
        self.pturtle.shape("circle")
        self.pturtle.goto(self.x, self.y)
        self.pturtle.down()

    def getName(self):
        return self.name

    def getRadius(self):
        return self.radius

    def getMass(self):
        return self.mass

    def getDistance(self):
        return self.distance

    def getVolume(self):
        v = 4.0 / 3 * math.pi * self.radius ** 3
        return v

    def getSurfaceArea(self):
        sa = 4.0 * math.pi * self.radius ** 2
        return sa

    def getDensity(self):
        d = self.mass / self.getVolume()
        return d

    def setName(self, newname):
        self.name = newname

    def show(self):
        print(self.name)

    def __str__(self):
        return self.name

    def moveTo(self, newx, newy):
        self.x = newx
        self.y = newy
        self.pturtle.goto(newx, newy)

    def getXPos(self):
        return self.x

    def getYPos(self):
        return self.y

    def getXVel(self):
        return self.velx

    def getYVel(self):
        return self.vely

    def setXVel(self, newvx):
        self.velx = newvx

    def setYVel(self, newvy):
        self.vely = newvy


def createSSandAnimate():
    ss = SolarSystem(2, 2)

    sun = Sun("SUN", 5000, 10, 5800)
    ss.addSun(sun)

    m = Planet("MERCURY", 19.5, 1000, .25, 0, 2, "blue")
    ss.addPlanet(m)

    m = Planet("EARTH", 47.5, 5000, 0.3, 0, 2.0, "green")
    ss.addPlanet(m)

    m = Planet("MARS", 50, 9000, 0.5, 0, 1.63, "red")
    ss.addPlanet(m)

    m = Planet("JUPITER", 100, 49000, 0.7, 0, 1, "black")
    ss.addPlanet(m)

    m = Planet("Pluto", 1, 500, 0.9, 0, .5, "orange")
    ss.addPlanet(m)

    m = Planet("Asteroid", 1, 500, 1.0, 0, .75, "cyan")
    ss.addPlanet(m)

    numTimePeriods = 20000
    for amove in range(numTimePeriods):
        ss.movePlanets()


createSSandAnimate()
