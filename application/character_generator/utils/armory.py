import random

def get_armory(role: str) -> list[str]:
    rocker = [
        'Bardzo ciężki pistolet',
        'Zwykła amunicja do B.C. pistoletu ×50',
        'Granat łzawiący ×2',
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Duża broń biała'],
        ['Granat błyskowy']
    ])

    solo = [
        'Karabin szturmowy',
        'Bardzo ciężki pistolet',
        'Zwykła amunicja do B.C. pistoletu ×30',
        'Zwykła amunicja karabinowa ×70',
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Duża broń biała'],
        ['Tarcza kuloodporna']
    ])

    netrunner = [
        'Bardzo ciężki pistolet',
        'Zwykła amunicja do B.C. pistoletu ×30',
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Bardzo ciężki pistolet', 'Zwykła amunicja do B.C. pistoletu ×30'],
        ['Ciężki pistolet', 'Zwykła amunicja do C. pistoletu ×30'],
    ])

    tech = [
        'Granat błyskowy',
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Strzelba', 'Amunicja do strzelby ×100'],
        ['Karabin szturmowy', 'Amunicja do karabinu szturmowego ×100'],
    ])

    medic = [
        'Granat dymny ×2',
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
        'Tarcza kuloodporna',
    ] + random.choice([
        ['Strzelba', 'Amunicja do strzelby ×100', 'Zapalająca amunicja do strzelby ×10'],
        ['Karabin szturmowy', 'Amunicja do karabinu szturmowego ×100', 'Zapalająca amunicja do karabinu szturmowego ×10'],
    ])

    media = [
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Bardzo ciężki pistolet', 'Zwykła amunicja do B.C. pistoletu ×50'],
        ['Ciężki pistolet', 'Zwykła amunicja do C. pistoletu ×50'],
    ])

    cop = [
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Strzelba', 'Amunicja do strzelby ×100'],
        ['Karabin szturmowy', 'Amunicja do karabinu szturmowego ×100'],
    ]) + random.choice([
        ['Granat dymny'],
        ['Tarcza kuloodporna']
    ])


    corp = [
        'Bardzo ciężki pistolet',
        'Zwykła amunicja do B.C. pistoletu ×50',
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ]

    fixer = [
        'lekka broń biała',
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Bardzo ciężki pistolet', 'Zwykła amunicja do B.C. pistoletu ×50'],
        ['Ciężki pistolet', 'Zwykła amunicja do C. pistoletu ×50'],
    ])

    nomad = [
        'Lekka kurtka kuloodporna Ciało (OB 11)',
        'Lekka kurtka kuloodporna Głowa (OB 11)',
    ] + random.choice([
        ['Bardzo ciężki pistolet', 'Zwykła amunicja do B.C. pistoletu ×100'],
        ['Ciężki pistolet', 'Zwykła amunicja do C. pistoletu ×100'],
    ]) + random.choice([
        ['Duża broń biała'],
        ['Ciężki pistolet', 'Zwykła amunicja do C. pistoletu ×100'],
    ])

    return {
        "rocker": rocker,
        "solo": solo,
        "netrunner": netrunner,
        "tech": tech,
        "medic": medic,
        "media": media,
        "cop": cop,
        "corp": corp,
        "fixer": fixer,
        "nomad": nomad,
    }[role]