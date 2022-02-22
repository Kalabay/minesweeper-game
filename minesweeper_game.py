import random, copy

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
        
    def __str__(self):
        return str(self.x) + " " + str(self.y)


Move = [Point(-1, -1), Point(-1, 0), Point(-1, 1), Point(0, -1), Point(0, 1), Point(1, -1), Point(1, 0), Point(1, 1)]


class OneGame:
    def __init__(self, typeGame = 0, n = 5, m = 5, cntBomb = 0):
        self.n = n
        self.m = m
        self.cntBomb = cntBomb
        self.tableUser = []
        self.tableFull = []
        self.typeGame = typeGame
        
    def Save(self):
        file = open('SaveGame.txt', 'w')
        file.write(str(self.n) + '\n')
        file.write(str(self.m) + '\n')
        file.write(str(self.cntBomb) + '\n')
        for y in range(self.n):
            for x in range(self.m):
                file.write(str(ord(str(self.tableFull[y][x])) * min(self.n, self.m) + (x + 1) * (y + 1) * 179) + '\n')
        for y in range(self.n):
            for x in range(self.m):
                file.write(str(ord(str(self.tableUser[y][x])) * min(self.n, self.m) + (x + 1) * (y + 1) * 179) + '\n')
        file.close()
        
    def GenerateTable(self, other):
        self.tableFull = [["?" for j in range(self.m)] for i in range(self.n)]
        unoccupied = []
        for y in range(self.n):
            for x in range(self.m):
                now = Point(x, y)
                if not(other.x == now.x and other.y == now.y):
                    unoccupied.append(now)
        random.shuffle(unoccupied)
        for i in range(self.cntBomb):
            bomb = unoccupied[i]
            self.tableFull[bomb.y][bomb.x] = "*"
        for y in range(self.n):
            for x in range(self.m):
                now = Point(x, y)
                if self.tableFull[now.y][now.x] != "*":
                    self.tableFull[now.y][now.x] = 0
                    for moveTo in Move:
                        moveNow = now + moveTo
                        if moveNow.x >= 0 and moveNow.x < self.m and moveNow.y >= 0 and moveNow.y < self.n and self.tableFull[moveNow.y][moveNow.x] == "*":
                            self.tableFull[now.y][now.x] += 1
        self.Open(other)
    
    def Open(self, other):
        if self.tableFull[other.y][other.x] == "*":
            self.tableUser[other.y][other.x] = "*"
            return -1
        if self.tableUser[other.y][other.x] != "?" and self.tableUser[other.y][other.x] != "F":
            return 0
        if self.tableFull[other.y][other.x] == 0:
            queueBfs = [other]
            index = 0
            while index != len(queueBfs):
                now = queueBfs[index]
                self.tableUser[now.y][now.x] = self.tableFull[now.y][now.x]
                for moveTo in Move:
                    moveNow = now + moveTo
                    if moveNow.x >= 0 and moveNow.x < self.m and moveNow.y >= 0 and moveNow.y < self.n:
                        if self.tableFull[moveNow.y][moveNow.x] == 0 and (self.tableUser[moveNow.y][moveNow.x] == "?" or self.tableUser[moveNow.y][moveNow.x] == "F"):
                            queueBfs.append(moveNow)
                        elif (self.tableUser[moveNow.y][moveNow.x] == "?" or self.tableUser[moveNow.y][moveNow.x] == "F") and self.tableFull[moveNow.y][moveNow.x] != "*":
                            self.tableUser[moveNow.y][moveNow.x] = self.tableFull[moveNow.y][moveNow.x]                    
                index += 1
        self.tableUser[other.y][other.x] = self.tableFull[other.y][other.x]
        return 1
    
    def Flag(self, other):
        if self.tableUser[other.y][other.x] == "?":
            self.tableUser[other.y][other.x] = "F"
        elif self.tableUser[other.y][other.x] == "F":
            self.tableUser[other.y][other.x] = "?"
    
    def CheckBombs(self, inf, left, right):
        try:
            if left <= int(inf) <= right:
                return 1
            else:
                return 0
        except:
            return -1
    
    def ConvertToNormal(self, inf):
        try:
            if "[" in inf and "," in inf and "]" in inf:
                i = 0
                new_inf = ""
                while inf[i] == " ":
                    i += 1
                if inf[i] != "[":
                    return -1
                i += 1
                while inf[i] != ",":
                    new_inf += inf[i]
                    i += 1
                i += 1
                while inf[i] == " ":
                    new_inf += inf[i]
                    i += 1
                if inf[i] == ",":
                    return -1
                while inf[i] != ",":
                    new_inf += inf[i]
                    i += 1
                i += 1
                new_inf += inf[i:]
                j = -1
                while new_inf[j] == " ":
                    j -= 1
                if new_inf[j] != "]":
                    return -1
                new_inf = new_inf[:j]
                inf = new_inf
            now = inf.split()
            if len(now) != 3 or (now[-1] != "Flag" and now[-1] != "Open"):
                return -1
            now[0] = int(now[0]) - 1
            now[1] = int(now[1]) - 1
            if 0 <= now[0] < self.m and 0 <= now[1] < self.n:
                return now
            return -1
        except:
            return -1
    
    def CheckWin(self):
        cnt = 0
        for y in range(self.n):
            for x in range(self.m):
                if self.tableUser[y][x] != "?" and self.tableUser[y][x] != "F":
                    cnt += 1
        return cnt == self.n * self.m - self.cntBomb
    
    def CheckNM(self, inf):
        try:
            n, m = map(int, inf.split())
            if n <= 0 or m <= 0:
                return False
            if n == 1 and m == 1:
                print("1x1??? Так не интересно.")
                return False
            return True
        except:
            return False
    
    def FirstAndSecondMode(self):
        if self.typeGame == 1:
            print("Размер поля 5x5.")
            self.n = 5
            self.m = 5
        else:
            print("Введите размеры поля через пробел.")
            information = input()
            while not self.CheckNM(information):
                print("Некорректный ввод.")
                print("Пожалуйста, повторите попытку.")
                information = input()
            n, m = map(int, information.split())
            self.n = n
            self.m = m
        print("Введите количество бомб.")
        if self.typeGame == 1:
            left = 2
            right = 5
            print("Не меньше 2 и не больше 5!")
        else:
            left = 1
            right = n * m - 1
            print("Не меньше 1 и не больше " + str(n * m - 1) + "!")
        information = input()
        while self.CheckBombs(information, left, right) != 1:
            print("Некорректный ввод.")
            if self.CheckBombs(information, left, right) == 0:
                print("Число не попадает в границы!")
            else:
                print("Вы ввели не число!")
            print("Пожалуйста, повторите попытку.")
            information = input()
        self.cntBomb = int(information)            
        self.tableUser = [["?" for j in range(self.m)] for i in range(self.n)]
        self.Print()
        First = True
        while True:
            print("Введите ваш запрос.")
            information = input() 
            now = self.ConvertToNormal(information)
            while now == -1:
                print("Некорректный ввод.")
                print("Пожалуйста, повторите попытку.")
                information = input()
                now = self.ConvertToNormal(information)
            if now[-1] == "Flag":
                self.Flag(Point(now[0], now[1]))
            elif First:
                self.GenerateTable(Point(now[0], now[1]))
                First = False
                self.Save()
            else:
                check = self.Open(Point(now[0], now[1]))
                self.Save()
                if check == -1:
                    self.Print2()
                    return False
            if self.CheckWin():
                self.Print2()
                return True            
            self.Print()
            
    def Beginning(self):
        print("Выберете режим игры:")
        print("1. Для слабаков.")
        print("2. Кастомная игра.")
        print("Введите цифру от 1 до 2.")
        information = input()
        information.replace(" ", "")
        while len(information) != 1 or information > "2" or information < "1":
            print("Некорректный ввод.")
            print("Пожалуйста, повторите попытку.")
            information = input()
            information.replace(" ", "")
        self.typeGame = int(information)
        if self.typeGame != 3:
            check = self.FirstAndSecondMode()
            if check:
                print("Победа.")
            else:
                print("Поражение.")
        
    def DownloadAndStart(self):
        try:
            self.typeGame = 2
            file = open('SaveGame.txt', 'r')
            self.n = int(file.readline())
            self.m = int(file.readline())
            self.cntBomb = int(file.readline())
            self.tableFull = [["?" for j in range(self.m)] for i in range(self.n)]
            self.tableUser = [["?" for j in range(self.m)] for i in range(self.n)]
            for y in range(self.n):
                for x in range(self.m):
                    now = int(file.readline())
                    now -= (x + 1) * (y + 1) * 179
                    now = chr(now // min(self.n, self.m))
                    if now >= '0' and now <= '9':
                        now = int(now)
                    self.tableFull[y][x] = now
            for y in range(self.n):
                for x in range(self.m):
                    now = int(file.readline())
                    now -= (x + 1) * (y + 1) * 179
                    now = chr(now // min(self.n, self.m))
                    if now >= '0' and now <= '9':
                        now = int(now)
                    self.tableUser[y][x] = now
            file.close()
            while True:
                self.Print()  
                print("Введите ваш запрос.")
                information = input() 
                now = self.ConvertToNormal(information)
                while now == -1:
                    print("Некорректный ввод.")
                    print("Пожалуйста, повторите попытку.")
                    information = input()
                    now = self.ConvertToNormal(information)
                if now[-1] == "Flag":
                    self.Flag(Point(now[0], now[1]))
                else:
                    check = self.Open(Point(now[0], now[1]))
                    self.Save()
                    if check == -1:
                        self.Print2()
                        return False
                if self.CheckWin():
                    self.Print2()
                    return True                     
        except:
            print("Файл сохранения повреждён")
            print("или нет незаконченной игры.")
            return -179
        
    def Print(self):
        for line in self.tableUser:
            for elem in line:
                print(elem, end=" ")
            print()
        
    def Print2(self):
        for line in self.tableFull:
            for elem in line:
                print(elem, end=" ")
            print()            


class Minesweeper:
    def __init__(self):
        print("Добро пожаловать в игру Сапёр!!!")
        self.notEndCheck = True
    
    def StartMenu(self):
        print("Меню:")
        print("1. Чтобы начать игру напишите START")
        print("2. Чтобы узнать правила напишите RULES")
        print("3. Чтобы загрузить сохранения напишите START_SAVE")
        print("   Сохранение происходит после каждого запроса Open")
        print("4. Чтобы закончить работу приложения напишите END")
        options = ["END", "START", "RULES", "START_SAVE"]
        information = input()
        information.replace(" ", "")
        while information not in options:
            print("Некорректный ввод.")
            print("Пожалуйста, повторите попытку.")
            information = input()
            information.replace(" ", "")
        self.notEndCheck = options.index(information)
        if self.notEndCheck == 1:
            self.Start()
        elif self.notEndCheck == 2:
            self.Rules()
        elif self.notEndCheck == 3:
            self.StartSave()
       
    def Start(self):
        game = OneGame()
        game.Beginning()
        self.StartMenu()
        
    def StartSave(self):
        game = OneGame()
        check = game.DownloadAndStart()
        if check != -179 and check:
            print("Победа.")
        elif check != -179:
            print("Поражение.")
        open('SaveGame.txt', 'w').close()
        self.StartMenu()  
        
    def Rules(self):
        print("Правила игры и ввода:")
        print("В начале игры вам предложат выбрать режим.")
        print()
        print("Если вы выбрали режим для слабаков:")
        print("Вам НЕ предложат выбрать размеры поля.")
        print("Они фиксированны и равны пятёрке.")
        print("Однако вы вольны выбрать количество бомб.")
        print("Но и тут не всё так просто.")
        print("Количество бомб больше 1, но меньше 6.")
        print("После этих настроек начинается сама игра.")
        print("Каждый ход до победы или поражения")
        print("вы будете вводить числа X и Y и 1 команду S")
        print("в одном из двух форматов: X Y S или [X, Y, S].")
        print("Клетка X Y обязана существовать. Левый верхний угол = (1, 1)")
        print("S = Flag или Open, что соответствует двум действиям")
        print("установить флажок и раскрыть содержимое клетки.")
        print("После конца игры вас автоматически перекинуть в меню.")
        print()
        print("Если вы выбрали кастомный режим:")
        print("Вам предложат выбрать размеры поля N и M.")
        print("А также количество бомб B.")
        print("Далее аналогично режимы для слабаков.")
        print()
        print("Остальную информацию вы можете найти в Википедии")
        print("https://ru.wikipedia.org/wiki/Сапёр_(игра)")
        print("Обозначения:")
        print("* - бомба.")
        print("? - закрытая клетка.")
        print("F - флаг.")
        print("Иначе число = количеству бомб поблизости")
        print("Удачи!")
        print()
        self.StartMenu()
        
game = Minesweeper()
game.StartMenu()