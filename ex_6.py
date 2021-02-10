# class father():  # 부모 클래스
#     def handsome(self):
#         print("잘생겼다")
#
#
# class brother(father):  # 자식클래스(부모클래스) 아빠매소드를 상속받겠다
#     '''아들'''
#
#
# class sister(father):  # 자식클래스(부모클래스) 아빠매소드를 상속받겠다
#     def pretty(self):
#         print("예쁘다")
#
#     def handsome(self):  #제정의해버리면 물려받아서 바꿀수있다
#         '''물려받았어요'''
#
#
# brother = brother()
# brother.handsome()
#
# girl = sister()
# girl.handsome()
# girl.pretty()

a = 1

class father():  # 부모 클래스
    def __init__(self, who):
        self.who = who

    def handsome(self):
        print("{}를 닮아 잘생겼다".format(self.who))


class sister(father):  # 자식클래스(부모클래스) 아빠매소드를 상속받겠다
    def __init__(self, who, where, age):
        super().__init__(who)
        self.where = where
        self.age = age
        print("나이 : ", age)

    def choice(self):
        print("{} 말이야".format(self.where))

    def handsome(self):
        super().handsome()
        self.choice()


girl = sister("아빠", "얼굴", a)
girl.handsome()

b = [1, 2, 3]
for i in b:
    print(i)

