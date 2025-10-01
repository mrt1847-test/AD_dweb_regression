from datetime import datetime


def file_start_hour():
    # 이 모듈(파일) 내 테스트가 처음 실행될 때 한 번만 호출됨
    return datetime.now().strftime("%H")

a= file_start_hour()
b = "{:02d}".format(int(a) + 1)
# ['2997549821', '2512116583', '3101285106', '2632242759']