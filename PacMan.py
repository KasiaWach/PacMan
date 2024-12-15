import pygame
import sys
import time
import random
import math
from abc import ABC, abstractmethod

class Plansza:
    def __init__(self, map_string: str, szerokosc: int, wysokosc: int):
        self.__mapa = map_string.splitlines()
        self.__szerokosc = szerokosc
        self.__wysokosc = wysokosc
        self.__rozmiar_komorki = 40 
        self.__obiekty = [] 

    @property
    def mapa(self) -> list:
        return self.__mapa

    @property
    def szerokosc(self) -> int:
        return self.__szerokosc

    @property
    def wysokosc(self) -> int:
        return self.__wysokosc

    @property
    def rozmiar_komorki(self) -> int:
        return self.__rozmiar_komorki
    
    @property
    def obiekty(self) -> list:
        return self.__obiekty

    def czy_sciana(self, x: int, y: int) -> bool:
        return self.__mapa[y][x] == '#'

    def mozliwe_ruchy(self, x: int, y: int) -> list:
        ruchy = []
        if x > 0 and not self.czy_sciana(x-1, y):
            ruchy.append(('L', x-1, y))
        if x < self.__szerokosc - 1 and not self.czy_sciana(x+1, y):
            ruchy.append(('P', x+1, y))
        if y > 0 and not self.czy_sciana(x, y-1):
            ruchy.append(('G', x, y-1))
        if y < self.__wysokosc - 1 and not self.czy_sciana(x, y+1):
            ruchy.append(('D', x, y+1))
        return ruchy
    
    def dodaj_obiekt(self, obiekt: 'Element'):
        self.__obiekty.append(obiekt)

    def usun_obiekt(self, obiekt_do_usuniecia: 'Element'):
        if obiekt_do_usuniecia in self.__obiekty:
            self.__obiekty.remove(obiekt_do_usuniecia)

    def rysuj_sciany(self, ekran: pygame.Surface):
        for y, linia in enumerate(self.__mapa):
            for x, znak in enumerate(linia):
                if znak == '#':
                    pygame.draw.rect(ekran, (0, 0, 255), (x * self.__rozmiar_komorki, y * self.__rozmiar_komorki, self.__rozmiar_komorki, self.__rozmiar_komorki))
    
    def rysuj_obiekty(self, ekran: pygame.Surface):
        for obiekt in self.__obiekty:
            obiekt.rysuj(ekran)

    def czy_puste_pole(self, x: int, y: int) -> bool:
        if self.czy_sciana(x, y):
            return False
        for obiekt in self.__obiekty:
            if obiekt.x == x * self.__rozmiar_komorki + 20 and obiekt.y == y * self.__rozmiar_komorki + 20:
                return False
        return True
    
    def rysuj_info_pacmana(self, ekran: pygame.Surface, pacman: 'PacMan'):
        czcionka = pygame.font.Font(None, 36)
        zycia_tekst = czcionka.render('Życia: ' + str(pacman.zycia), True, (255, 255, 255))
        monety_tekst = czcionka.render('Monety: ' + str(pacman.monety), True, (255, 255, 255))

        ekran.blit(zycia_tekst, (self.__szerokosc * self.__rozmiar_komorki + 10, 30))
        ekran.blit(monety_tekst, (self.__szerokosc * self.__rozmiar_komorki + 10, 70))

    def wyswietl_komunikat(self, ekran: pygame.Surface, komunikat: str):
        czcionka = pygame.font.Font(None, 74)
        tekst = czcionka.render(komunikat, True, (255, 255, 255))
        tekst_rect = tekst.get_rect(center=(ekran.get_width()/2, ekran.get_height()/2))
        ekran.blit(tekst, tekst_rect)
        pygame.display.flip()
        time.sleep(3)


class Timer:
    def __init__(self, duration: int):
        self.__duration = duration
        self.__start_time = None

    def start(self):
        self.__start_time = time.time()

    def is_running(self) -> bool:
        if self.__start_time is None:
            return False
        return (time.time() - self.__start_time) < self.__duration

    def stop(self):
        self.__start_time = None


class Element(ABC):
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        self.__x = int(x * 40 + 20)
        self.__y = int(y * 40 + 20)
        self.__width = width
        self.__height = height
        self.__color = color

    @property
    def x(self) -> int: return self.__x
    
    @x.setter
    def x(self, new_x: int): self.__x = int(new_x * 40 + 20)

    @property
    def y(self) -> int: return self.__y
    
    @y.setter
    def y(self, new_y: int): self.__y = int(new_y * 40 + 20)

    @property
    def width(self) -> int: return self.__width
    
    @width.setter
    def width(self, new_width: int): self.__width = new_width

    @property
    def height(self) -> int: return self.__height
    
    @height.setter
    def height(self, new_height: int): self.__height = new_height

    @property
    def color(self) -> tuple[int, int, int]: return self.__color
    
    @color.setter
    def color(self, new_color: tuple[int, int, int]): self.__color = new_color

    @abstractmethod
    def rysuj(self, ekran): pass

    @abstractmethod
    def modyfikacja(self): pass


class PacMan(Element):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 20, 20, (255, 255, 0))
        self.__monety = 0
        self.__zycia = 3
        self.__niesmiertelny = False

    @property
    def monety(self) -> int:
        return self.__monety

    @monety.setter
    def monety(self, value: int):
        self.__monety = value

    @property
    def zycia(self) -> int:
        return self.__zycia

    @zycia.setter
    def zycia(self, value: int):
        self.__zycia = value

    @property
    def niesmiertelny(self) -> bool:
        return self.__niesmiertelny

    @niesmiertelny.setter
    def niesmiertelny(self, value: bool):
        self.__niesmiertelny = value

    def rysuj(self, ekran: pygame.Surface):
        pygame.draw.circle(ekran, self._Element__color, (self.x, self.y), self._Element__width // 2)

    def modyfikacja(self):
        pass

    def reset_effect(self):
        self.color = (255, 255, 0)
        self.niesmiertelny = False


class Duszek(Element):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 20, 20, (255, 255, 255))  
        self.__strategie = [StrategiaGonieniaPacMana, StrategiaLosowegoRuchu]
        self.__strategia = StrategiaLosowegoRuchu
        self.__timer = Timer(random.randint(3, 7))
        self.__timer.start()

    @property
    def strategia(self): return self.__strategia
    
    @strategia.setter
    def strategia(self, new_strategia): self.__strategia = new_strategia

    def rysuj(self, ekran: pygame.Surface):
        pygame.draw.circle(ekran, self.color, (self.x, self.y), self.width// 2)

    def modyfikacja(self): pass

    def reset_effect(self):
        self.color = (255, 255, 255)

    def wykonaj_ruch(self, duszek, plansza, pacman):
        if not self.__timer.is_running():
            self.__strategia = random.choice(self.__strategie)
            self.__timer = Timer(random.randint(1, 3)) 
            self.__timer.start()
        self.__strategia.wykonaj_ruch(self, duszek, plansza, pacman)


class Moneta(Element):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 5, 5, (255, 165, 0))  
    
    def rysuj(self, ekran: pygame.Surface):
        pygame.draw.circle(ekran, self.color, (self.x, self.y), self.width// 2)

    def modyfikacja(self): pass


class Wisnia(Element):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 15, 15, (255, 0, 0))  
    
    def rysuj(self, ekran: pygame.Surface):
        pygame.draw.circle(ekran, self.color, (self.x, self.y), self.width// 2)

    def modyfikacja(self): pass


class Effect(Element):
    def __init__(self, element: Element):
        self._element = element

    @abstractmethod
    def modyfikacja(self): pass


class Niesmiertelnosc(Effect):
    def __init__(self, element: Element):
        super().__init__(element)
    
    def rysuj(self, ekran: pygame.Surface):
        self.modyfikacja()
        pygame.draw.circle(ekran, self._element.color, (self._element.x, self._element.y), self._element.width// 2)
    
    def modyfikacja(self):
        self._element.color = (255, 100, 100)
        self._element.niesmiertelny = True

class PoStracieZycia(Effect):
    def __init__(self, element: Element):
        super().__init__(element)
    
    def rysuj(self, ekran: pygame.Surface, pacman: PacMan):
        self.modyfikacja(pacman)
        pygame.draw.circle(ekran, self._element.color, (self._element.x, self._element.y), self._element.width// 2)
    
    def modyfikacja(self, pacman: PacMan): 
        self._element.color = (180, 0, 255)
        self._element.timer = Timer(5)
        self._element.strategia = StrategiaOddalaniaOdPacMana
        pacman.niesmiertelny = True


class CollisionAction(ABC):
    @abstractmethod
    def dispatch(self, a_PacMan: PacMan): pass


class PacManxDuszek(CollisionAction):
    def dispatch(self, a_PacMan: PacMan, duszki: list[Duszek], ekran: pygame.Surface, effect_end: int): 
        if not a_PacMan.niesmiertelny:
            a_PacMan.zycia -= 1
            for duszek in duszki:
                decorated = PoStracieZycia(duszek)
                decorated.rysuj(ekran, a_PacMan)
            pygame.time.set_timer(effect_end, 5000)


class PacManxMoneta(CollisionAction):
    def dispatch(self, a_PacMan: PacMan): a_PacMan.monety += 1


class PacManxWisnia(CollisionAction):
    def dispatch(self, a_PacMan: PacMan, ekran: pygame.Surface, effect_end: int): 
        decorated = Niesmiertelnosc(a_PacMan)
        decorated.rysuj(ekran)
        pygame.time.set_timer(effect_end, 5000)


class CollisionDispatch:
    def __init__(self, plansza: Plansza, ekran: pygame.Surface, duszki: list[Duszek], effect_end: int):
        self.__dict = {}
        self.plansza = plansza
        self.ekran = ekran
        self.duszki = duszki
        self.effect_end = effect_end

    def register(self, cls_name: str, action: CollisionAction):
        self.__dict[cls_name] = action

    def dispatch(self, element: Element, a_PacMan: PacMan):
        cls_name = element.__class__.__name__
        
        if cls_name in self.__dict:
            action = self.__dict[cls_name]
            if isinstance(element, Wisnia):
                action.dispatch(a_PacMan, self.ekran, self.effect_end)
            elif isinstance(element, Duszek):
                action.dispatch(a_PacMan, self.duszki, self.ekran, self.effect_end) 
            else:
                action.dispatch(a_PacMan)  
            if isinstance(element, Moneta) or isinstance(element, Wisnia):
                self.plansza.usun_obiekt(element)
    
    def check_collision(self, element1: Element, element2: Element) -> bool:
        dx = abs(element1.x - element2.x)
        dy = abs(element1.y - element2.y)
        return dx < (element1.width + element2.width) / 2.0 and dy < (element1.height + element2.height) / 2.0


class RuchDuszkaStrategia(ABC):
    @abstractmethod
    def wykonaj_ruch(self, duszek, plansza, pacman):
        pass


class StrategiaLosowegoRuchu(RuchDuszkaStrategia):
    def wykonaj_ruch(self, duszek: Duszek, plansza: Plansza, pacman: PacMan):
        mozliwe_kierunki = plansza.mozliwe_ruchy(int((duszek.x-20)/40), int((duszek.y-20)/40))
        if mozliwe_kierunki:
            kierunek, nowe_x, nowe_y = random.choice(mozliwe_kierunki)
            duszek.x = nowe_x 
            duszek.y = nowe_y 


class StrategiaGonieniaPacMana(RuchDuszkaStrategia):
    def wykonaj_ruch(self, duszek: Duszek, plansza: Plansza, pacman: PacMan):
        duszek_x, duszek_y = int((duszek.x-20)/40), int((duszek.y-20)/40)
        pacman_x, pacman_y = int((pacman.x-20)/40), int((pacman.y-20)/40)

        mozliwe_kierunki = plansza.mozliwe_ruchy(duszek_x, duszek_y)

        minimalna_odleglosc = float('inf')
        najlepszy_kierunek = None
        for kierunek in mozliwe_kierunki:
            _, nowe_x, nowe_y = kierunek
            odleglosc = math.sqrt((nowe_x - pacman_x) ** 2 + (nowe_y - pacman_y) ** 2)
            if odleglosc < minimalna_odleglosc:
                minimalna_odleglosc = odleglosc
                najlepszy_kierunek = kierunek

        if najlepszy_kierunek:
            _, nowe_x, nowe_y = najlepszy_kierunek
            duszek.x, duszek.y = nowe_x , nowe_y 


class StrategiaOddalaniaOdPacMana(RuchDuszkaStrategia):
    def wykonaj_ruch(self, duszek: Duszek, plansza: Plansza, pacman: PacMan):
        duszek_x, duszek_y = int((duszek.x-20)/40), int((duszek.y-20)/40)
        pacman_x, pacman_y = int((pacman.x-20)/40), int((pacman.y-20)/40)

        mozliwe_kierunki = plansza.mozliwe_ruchy(duszek_x, duszek_y)

        najlepszy_kierunek = None
        maksymalna_odleglosc = 0
        for kierunek in mozliwe_kierunki:
            _, nowe_x, nowe_y = kierunek
            odleglosc = math.sqrt((nowe_x - pacman_x) ** 2 + (nowe_y - pacman_y) ** 2)
            if odleglosc > maksymalna_odleglosc:
                najlepszy_kierunek = kierunek
                maksymalna_odleglosc = odleglosc

        if najlepszy_kierunek:
            _, nowe_x, nowe_y = najlepszy_kierunek
            duszek.x, duszek.y = nowe_x , nowe_y 


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class MoveLeftCommand(Command):
    def __init__(self, pacman: PacMan, plansza: Plansza):
        self.pacman = pacman
        self.plansza = plansza

    def execute(self):
        new_x = int((self.pacman.x - 20)/40 - 1)
        y = int((self.pacman.y - 20)/40)
        if not self.plansza.czy_sciana(new_x, y):
            self.pacman.x = new_x


class MoveRightCommand(Command):
    def __init__(self, pacman: PacMan, plansza: Plansza):
        self.pacman = pacman
        self.plansza = plansza

    def execute(self):
        new_x = int((self.pacman.x - 20)/40 + 1)
        y = int((self.pacman.y - 20)/40)
        if not self.plansza.czy_sciana(new_x, y):
            self.pacman.x = new_x


class MoveUpCommand(Command):
    def __init__(self, pacman: PacMan, plansza: Plansza):
        self.pacman = pacman
        self.plansza = plansza

    def execute(self):
        new_y = int((self.pacman.y - 20)/40 - 1)
        x = int((self.pacman.x - 20)/40)
        if not self.plansza.czy_sciana(x, new_y):
            self.pacman.y = new_y


class MoveDownCommand(Command):
    def __init__(self, pacman: PacMan, plansza: Plansza):
        self.pacman = pacman
        self.plansza = plansza

    def execute(self):
        new_y = int((self.pacman.y - 20)/40 + 1)
        x = int((self.pacman.x - 20)/40)
        if not self.plansza.czy_sciana(x, new_y):
            self.pacman.y = new_y


class GameController:
    def __init__(self):
        self.commands = {}

    def set_command(self, key: str, command: Command):
        self.commands[key] = command

    def execute_command(self, key: str):
        if key in self.commands:
            self.commands[key].execute()


if '__main__' == __name__:
    pygame.init()
    mapa_gry = """
#####################
#ooooooooooooooooooo#
#o####o#o###o#o####o#
#oooooooo###oooooooo#
##o#o###########o#o##
##ooooooooooooooooo##
##o#o#o###o###o#o#o##
##ooo#o#ooooo#o#ooo##
##o#o#o#######o#o#o##
#oooooooo###oooooooo#
#o####o#o###o#o####o#
#ooooooooooooooooooo#
#####################
"""
    plansza = Plansza(mapa_gry.strip(), 21, 13)
    rozmiar_okna = ((plansza.szerokosc + 6) * plansza.rozmiar_komorki, plansza.wysokosc * plansza.rozmiar_komorki)
    ekran = pygame.display.set_mode(rozmiar_okna)
    pygame.display.set_caption('Pac-Man')
    game_controller = GameController()
    strategia_losowa = StrategiaLosowegoRuchu()

    plansza.dodaj_obiekt(PacMan(10, 1))
    
    duszki = [
    Duszek(10, 7),
    Duszek(11, 7),
    Duszek(9, 7)]

    for duszek in duszki:
        plansza.dodaj_obiekt(duszek)

    plansza.dodaj_obiekt(Wisnia(1, 1))
    plansza.dodaj_obiekt(Wisnia(19, 1))
    plansza.dodaj_obiekt(Wisnia(1, 11))
    plansza.dodaj_obiekt(Wisnia(19, 11))

    monety = 0
    for y, linia in enumerate(plansza.mapa):
            for x, znak in enumerate(linia):
                if plansza.czy_puste_pole(x, y):
                    plansza.dodaj_obiekt(Moneta(x, y))
                    monety += 1

    EFFECT_END = pygame.USEREVENT + 1

    collisions = CollisionDispatch(plansza, ekran, duszki, EFFECT_END)
    collisions.register('Moneta', PacManxMoneta())
    collisions.register('Duszek', PacManxDuszek())
    collisions.register('Wisnia', PacManxWisnia())

    pacman = [obiekt for obiekt in plansza.obiekty if isinstance(obiekt, PacMan)][0]

    game_controller.set_command(pygame.K_LEFT, MoveLeftCommand(pacman, plansza))
    game_controller.set_command(pygame.K_RIGHT, MoveRightCommand(pacman, plansza))
    game_controller.set_command(pygame.K_UP, MoveUpCommand(pacman, plansza))
    game_controller.set_command(pygame.K_DOWN, MoveDownCommand(pacman, plansza))


    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ekran.fill((0, 0, 0)) 
        plansza.rysuj_sciany(ekran)
        plansza.rysuj_obiekty(ekran)

        if event.type == pygame.KEYDOWN:
            game_controller.execute_command(event.key)

        for duszek in duszki:
            duszek.wykonaj_ruch(duszek, plansza, pacman)

        for actor in plansza.obiekty:
            if collisions.check_collision(pacman, actor):
                collisions.dispatch(actor, pacman)

        if event.type == EFFECT_END:
            pacman.reset_effect()
            for duszek in duszki:
                duszek.reset_effect()
            pygame.time.set_timer(EFFECT_END, 0)

        plansza.rysuj_info_pacmana(ekran, pacman)

        if pacman.zycia <= 0:
            plansza.wyswietl_komunikat(ekran, "Przegrałeś!")
            pygame.quit()
            sys.exit()

        if pacman.monety == monety:
            plansza.wyswietl_komunikat(ekran, "Wygrałeś!")
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(10) 

