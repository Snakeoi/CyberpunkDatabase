import random

def get_inventory(role) -> list[str]:

    rocker = [
        "Agent",
        "Komputer",
        'Farba świecąca ×5',
        'Wzmacniacz kieszonkowy',
        'Radio/odtwarzacz muzyki',
        'Kamera wideo',
        'Typowy Szyk: Kurtka, Ozdoby×3, Tułów ×4',
        'Sportowy: Ozdoby, Lustrzanki, Stopy',
        'Miejski Błysk: Nogi, Tułów',
    ] + random.choice([
        ['Gitara elektryczna'],
        ['Wykrywacz podsłuchu']
    ])

    solo = [
        'Agent',
        'Sportowy: Stopy ×2, Kurtka ×3, Lustrzanki, Nogi ×2, Tułów ×2',
    ]

    netrunner = [
        'Agent',
        'Cyberdek (7 gniazd)',
        'Gogle wirtualowe',
        'Program: Pancerz',
        'Program: Miecz',
        'Typowy Szyk: Tułów ×10'
        'Sportowy: Stopy ×2, Ozdoby, Nogi ×2'
        'Miejski Błysk: Kurtka'
    ] + random.choice([
        ['Program: Mam cię'],
        ['Program: Gumka'],
    ]) + random.choice([
        ['Program: Miecz'],
        ['Program: Muzgoklep'],
    ]) + random.choice([
        ['Program: Miecz'],
        ['Program: Robak'],
    ])

    tech = [
        "Agent",
        "Maska antysmogowa",
        "Jednorazowy telefon",
        "komórkowy",
        "Mocna taśma klejąca ×5",
        "Latarka",
        "Flara alarmowa ×6",
        "Przybornik technika",
        "Typowy Szyk: Nogi ×8, Tułów ×10",
        "Sportowy: Stopy ×2",
    ]

    medic = [
        'Agent',
        'Strzykawka bezigłowa',
        'Kajdanki',
        'Latarka',
        'Typowy Szyk: Kurtka ×3',
        'Farba świecąca',
        'Torba medyka',
        'Sportowy: Stopy, Nogi ×3, Tułów ×5',
    ]

    media = [
        'Agent',
        'Rejestrator ,dźwięku'
        'Lornetka',
        'haków',
        'Latarka',
        'Komputer',
        'Radio/,odtwarzacz muzyki'
        'Koder/,dekoder'
        'Kamera ,wideo'
        'Typowy ,Szyk: Stopy, Nogi, Tułów'
        'Sportowy:, Kurtka'
        'Miejski ,Błysk: Lustrzanki'
    ] + random.choice([
        ['Jednorazowy telefon komórkowy ×2'],
        ['wyrzutnia haków'],
    ])

    cop = [
        'Agent',
        'Latarka',
        'Kajdanki ×2',
        'Radiokomunikator',
        'Flara alarmowa ×10',
        'Typowy Szyk: Kurtka, Nogi ×2, Tułów ×3',
        'Sportowy: Stopy ×2, Kurtka ×3, Lustrzanki, Nogi ×2, Top ×2',
    ]

    corp = [
        'Radiokomunikator',
        'Koder/dekoder',
        'Biznesowy: Stopy, Kurtka,',
        'Nogi, Lustrzanki, Tułów, Ozdoby ×2',
    ]

    fixer = [
        'Agent',
        'Wykrywacz podsłuchu',
        'Komputer',
        'Jednorazowy telefon komórkowy ×2',
        'Typowy Szyk: Szkła kontaktowe, Ozdoby',
        'Sportowy: Lustrzanki',
        'Miejski Błysk: Stopy, Kurtka, Nogi, Tułów',
    ]

    nomad = [
        'Agent',
        'Maska antysmogowa',
        'Mocna taśma klejąca',
        'Latarka',
        'Wyrzutnia haków',
        'Nadmuchiwany materac i śpiwór',
        'Torba medyka',
        'Radiokomunikator ×2',
        'Lina',
        'Technarzędzie',
        'Namiot i sprzęt biwakowy',
        'Romantyczny: Ozdoby',
        'Skóry Nomady: Tułów ×4, Nogi ×2, Stopy ×2, Kurtka, Nakrycie głowy',
    ]

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
        "nomad": nomad
    }[role]