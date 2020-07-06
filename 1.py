import random


class Card:
    _title: str
    _numbers: list
    _line: int
    _lines: list

    def __init__(self, title='Карточка'):

        self._title = title
        self._numbers = list(range(1, 91))
        self._line = 3
        self._lines = list(self)

    def __iter__(self):
        return self

    def __next__(self):
        if self._line:

            line = list(
                map(lambda x: ' ' + str(x) if len(str(x)) == 1 else str(x),
                    sorted(random.sample(self._numbers, 9))))

            for i in random.sample(line, 4):
                line = list(map(lambda x: x.replace(i, '  '), line))

            self._numbers = list(
                set(self._numbers) - set([int(x) if x != '  ' else 0 for x in line]))

            self._line -= 1

            return line
        else:
            raise StopIteration

    def __str__(self):
        return '{:-^26}\n{}\n{:-^26}' ''.format(self._title, '\n'.join(
            list(map(lambda x: ' '.join(x), self._lines))), '-')

    def is_include(self, num):
        return len([line for line in self._lines if
                    f'{" " + str(num) if len(str(num)) == 1 else str(num)}'
                    in line]) > 0

    def deletion(self, num):
        self._lines = [list(map(lambda x: x.replace(
            f'{" " + str(num) if len(str(num)) == 1 else str(num)}', ' -'),
                                line)) for line in self._lines]
        return self

    def is_win(self):
        return len(list(filter(lambda x: x.count(' -') != 5, self._lines))) == 0


class Barrel:
    _numbers: list
    _barrel: int

    def __init__(self):

        self._numbers = list(range(1, 91))
        self._barrel = 0

    def __iter__(self):
        return self

    def __str__(self):
        return str(next(self))

    def __next__(self):
        if len(self._numbers):
            self._barrel = random.choice(self._numbers)
            self._numbers.remove(self._barrel)
            return self._barrel
        else:
            raise StopIteration

    @property
    def length(self):
        return len(self._numbers)

    @property
    def current_number(self):
        return self._barrel


class Game:
    _player: Card
    _ai: Card
    _barrel: Barrel

    def __init__(self):
        self._player = Card(' Ваша карточка ')
        self._ai = Card(' Карточка компьютера ')
        self._barrel = Barrel()

    def check_win(self):
        win = True

        if self._player.is_win() and self._ai.is_win():
            print('\nНичья!')
        elif self._player.is_win() and not self._ai.is_win():
            print('\nПоздравляем!\nВы победили!')
        elif self._ai.is_win() and not self._player.is_win():
            print('\nВы проиграли!\nКомпьютер зачеркнул все цифры на своей карте.')
        else:
            win = False

        return win

    def step(self):
        repeat = False
        while True:
            if not repeat:
                if self.check_win():
                    return False
                print(
                    f'\nНовый бочонок {self._barrel} (осталось {self._barrel.length})\n{self._player}\n{self._ai}')
            try:
                player_answer = input('Зачеркнуть цифру? (y/n): ')
                barrel_current_number = self._barrel.current_number
                if self._ai.is_include(barrel_current_number):
                    self._ai.deletion(barrel_current_number)

                if player_answer == 'y':
                    if self._player.is_include(barrel_current_number):
                        self._player.deletion(barrel_current_number)
                        return True
                    else:
                        print(
                            f'\nВы проиграли!\nЦифры {barrel_current_number} нет на Вашей карточке.')
                        return False
                elif player_answer == 'n':
                    if not self._player.is_include(barrel_current_number):
                        return True
                    else:
                        print(
                            f'\nВы проиграли!\nПропущена цифра {barrel_current_number}')
                        return False
                else:
                    raise ValueError
            except ValueError:
                print(f'Введена неизвестная команда.')
                player_answer = input('\nДля продолжения игры введите "y": ')
                if player_answer == 'y':
                    repeat = True
                    continue
                else:
                    print('Игра завершена...')
                    return False

    def start(self):

        while True:
            if not self.step() is True:
                user_answer = input('\nВведите "y", чтобы начать новую игру: ')
                if user_answer == 'y':
                    return new_game()
                else:
                    print('Выход из программы')
                    break


def new_game():
    game = Game()
    game.start()


if __name__ == '__main__':
    new_game()