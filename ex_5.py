class Person:

    def __init__(self):     # 초기화
        self.__age = 0      # 전역변수 지정

    # @property
    def age(self):          # getter
        return self.__age

    # @age.setter
    # def age(self, value):   # setter
    #     self.__age = value


james = Person()  # 객체 생성

james.age = 20    # 객체 안의 메서드 호출 밑 갚지정
print(james.age)
