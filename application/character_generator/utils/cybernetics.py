import random
from dataclasses import dataclass


@dataclass
class Cybernetics:
    implants: list[str]
    humanity_loss: int


biomonitor =  ('Biomonitor - Implant podskórny nieustannie wyświetlający LED-owy odczyt aktualnego ciśnienia '
              'krwi, temperatury ciała, poziomu cukru, oddechu itp. Można podłączyć do Agenta, który będzie śledził'
              ' twój stan zdrowia.')

sound_recorder = ('Rejestrator dźwięku - Nagrywa dźwięk na czip pamięci lub połączonego Agenta. '
                  'Wymaga zestawu cyberaudio.)')

chemskin = ('Chemskóra - Farby i barwniki nasycające skórę i na stałe zmieniające jej kolor. Osoba posiadająca '
            'jednocześnie chemskórę i techfryz dodaje +2 do Atrakcyjności. '
            '(Premia nie kumuluje się z inną tego typu).')

tech_hair = ('Techfryz - Sztuczne włosy emitujące kolorowe światło. . Osoba posiadająca jednocześnie chemskórę '
            'i techfryz dodaje +2 do Atrakcyjności. (Premia nie kumuluje się z inną tego typu).')

cyber_audio = 'Zestaw cyberaudio - Ma 3 gniazda modyfikacji. Można zainstalować tylko 1 zestaw cyberaudio. '

neural_connector = ('Sprzęg neuralny - Przewodowy sztuczny system nerwowy. Konieczny do korzystania z cybersynaps '
                    'i chwytu podskórnego. Ma 5 gniazd modyfikacji.')

sandevistan = ('Sandevistan - Dopalacz prędkości. Aktywowany w ramach Akcji. Następnie przez 1 minutę '
               'dodaje +3 do Inicjatywy. Można używać co godzinę. Naraz można zainstalować tylko jeden rodzaj '
               'dopalacza prędkości. Wymaga sprzęgu neuralnego.')

wolverines = ('Rosomaki (3k6 LA 2)- Długie szpony wysuwane z kłykci. Duża broń biała. Można ją ukryć. Można zamontować '
              'jako jedyną cyborgizację w ręce biologicznej.')

interface_connector = ('Złącze interfejsu - Ulepszenie cybersynaps. Złącza w nadgarstkach lub głowie pozwalające użytkownikowi '
                       'podłączyć się do smartgunów, cyberdeków, ciężkiego sprzętu i prowadzić pojazdy, '
                       'nie używając rąk! Każde wszczepione złącze pozwala kontrolować jeden dodatkowy '
                       'przedmiot jednocześnie. Wymaga sprzęgu neuralnego.')

cyber_iris = 'Zmiantakty - Wszczepione w oko soczewki zmieniające kolor'

cyber_eye = ('Sztuczne oko. Każde cyberoko ma 3 gniazda modyfikacji. Niektóre opcje działają tylko w parze (trzeba '
             'je kupić dwukrotnie i  zainstalować w dwóch różnych cyberoczach użytkownika. '
             'UC obowiązuje każde z nich).')

micro_optics = 'Mikrooptyka - Modyfikacja cyberoka. Mikroskop oferujący powiększenie x400. Wymaga cyberoka.'

under_skin_watch = 'Zegarek podskórny - Podskórny zegarek LED.'

hand_with_tools = ('Dłoń z narzędziami - Wmontowane w palce narzędzia: śrubokręt, klucz, mała wiertarka i inne. Można '
                   'zamontować jako jedyną cyborgizację w ręce biologicznej.')

telescop = ('Teleskop - Modyfikacja cyberoka. Użytkownik widzi szczegóły odległe do 800 metrów. Strzelając do celu '
            'odległego o co najmniej 51 metrów z broni w trybie jednego strzału lub wykonując Celowanie, możesz '
            'dodać +1 do Testu. Instalacja kilku takich wszczepów nie powoduje zwiększenia premii. Nie kumuluje się '
            'z dodatkiem do broni Snajperska luneta celownicza. Wymaga cyberoka.')

nasal_filters = 'Filtry nosowe - Użytkownik jest niepodatny na gaz trujący, wyziewy i podobne niebezpieczeństwa.'

detoksycator = ('Detoksykator - Użytkownik dodaje +2 do Odporności na tortury/narkotyki. Instalacja kilku takich '
                'wszczepów nie powoduje zwiększenia premii.')

light_tattoo = ('Tatuaż świetlny - Świecący, podskórny implant w postaci tatuażu. Wyświetla wzory pod skórą. +2 do '
                'Mody i stylu, jeśli użytkownik ma co najmniej 3 tatuaże.')

better_hearing = 'Ulepszony słuch - Percepcja +2 w Testach związanych ze słuchem. Wymaga zestawu cyberaudio.'

inner_agent = ('Agent wewnętrzny - Modyfikacja cyberaudio. Agent z wszystkimi standardowymi opcjami (patrz Osprzęt '
               'str. 352), kontrolowany wyłącznie polecaniami głosowymi. Opisuje obraz, ale dla wygody można go '
               'połączyć z cyberokiem z modyfikacją Wyświetlacza lub pobliskim ekranem. Wszczepiony czip pamięci '
               'Agenta można usunąć tylko chirurgicznie. Wymaga zestawu cyberaudio.')

stress_analyzer = ('Analizator stresu w głosie - +2 w rzutach na Odczytywanie emocji i Przesłuchiwanie. '
                   'Wymaga zestawu cyberaudio.')

underskin_pocket = 'Podskórna kieszeń - Przestrzeń 5 cm × 10 cm umieszczona tuż pod skórą z suwakiem RealSkinn™'

hidden_gun_pocket = ('Ukryta kabura - Kabura wewnątrz ciała użytkownika. Można w niej nosić broń, którą da się ukryć '
                     'i dzięki kaburze nie trzeba wykonywać Testu na Ukrywanie. O ile kaburę wszczepiono w łatwo '
                     'dostępne miejsce na ciele, broni można dobyć bez użycia Akcji. Jeśli nosisz spodnie, '
                     'lepiej nie instaluj jej w udzie!')

def get_cybernetics(role: str) -> Cybernetics:

    rocker = Cybernetics(
        humanity_loss=9,
        implants=[
            sound_recorder,
            chemskin,
            tech_hair,
            cyber_audio
        ]
    )

    solo = Cybernetics(
        humanity_loss=14,
        implants=[
            biomonitor,
            neural_connector,
        ] + random.choice([
            [sandevistan],
            [wolverines],
        ])
    )

    netrunner = Cybernetics(
        humanity_loss=14,
        implants=[
            neural_connector,
            interface_connector,
            cyber_iris,
        ]
    )

    tech = Cybernetics(
        humanity_loss=12,
        implants=[
            cyber_eye,
            micro_optics,
            under_skin_watch,
            hand_with_tools,
        ]
    )

    medic = Cybernetics(
        humanity_loss=12,
        implants=[
            biomonitor,
            cyber_eye,
            telescop,
        ] + random.choice([
            [nasal_filters],
            [detoksycator],
        ])
    )

    media = Cybernetics(
        humanity_loss=10,
        implants=[
            cyber_audio,
            light_tattoo,
        ] + random.choice([
            [better_hearing],
            [stress_analyzer],
        ])
    )

    cop = Cybernetics(
        humanity_loss=10,
        implants=[
            hidden_gun_pocket,
            underskin_pocket,
        ]
    )

    corp = Cybernetics(
        humanity_loss=12,
        implants=[
            cyber_audio,
            inner_agent,
        ] + random.choice([
            [biomonitor],
            [tech_hair],
        ]) + random.choice([
            [nasal_filters],
            [detoksycator],
        ])
    )

    fixer = Cybernetics(
        humanity_loss=16,
        implants=[
            cyber_audio,
            inner_agent,
            underskin_pocket,
        ] + random.choice([
            [stress_analyzer],
            [better_hearing],
        ])
    )

    nomad = Cybernetics(
        humanity_loss=14,
        implants=[
            neural_connector
        ] + random.choice([
            [interface_connector],
            [wolverines],
        ])
    )

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