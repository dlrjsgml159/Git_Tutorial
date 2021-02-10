class student:
    def __init__(self):
        self.name = 'minsu'
        self.age = 20
        self.birth = '2000.10.10'

    def name(self):
        return self.name()

    def age(self):
        return self.age()

    def birth(self):
        return self.birth()

minsu = student()
print('이름 : ', minsu.name, '\n나이 : ', minsu.age, '\n생일 : ', minsu.birth)