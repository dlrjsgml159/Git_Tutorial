import ex_3

def func(a):
    print("입력숫자 :" ,a)
    print("name : ", __name__)

if __name__ == "__main__":
    print("모듈을 직접실행")
    func(3)
    func(4)

else:
    print("모듈을 임포트해서 실행")
