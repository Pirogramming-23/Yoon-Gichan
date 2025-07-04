#함수 이름은 변경 가능합니다.

student_dict = {}

##############  menu 1
def Menu1(name, mid_score, final_score):
    #사전에 학생 정보 저장하는 코딩
    student_dict[name] = {
        'mid': mid_score,
        'final': final_score
    }

##############  menu 2
def Menu2():
    #학점 부여 하는 코딩
    for name, info in student_dict.items():
        if 'grade' not in info:
            avg = (info['mid'] + info['final']) / 2
            if avg >= 90:
                grade = 'A'
            elif avg >= 80:
                grade = 'B'
            elif avg >= 70:
                grade = 'C'
            else:
                grade = 'D'
            info['grade'] = grade

##############  menu 3
def Menu3():
    print("-" * 40)
    print("name\tmid\tfinal\tgrade")
    print("-" * 40)
    for name, info in sorted(student_dict.items()):
        print(f"{name}\t{info['mid']}\t{info['final']}\t{info['grade']}")

##############  menu 4
def Menu4(name):
    del student_dict[name]

#학생 정보를 저장할 변수 초기화
print("*Menu*******************************")
print("1. Inserting students Info(name score1 score2)")
print("2. Grading")
print("3. Printing students Info")
print("4. Deleting students Info")
print("5. Exit program")
print("*************************************")
while True :
    choice = input("Choose menu 1, 2, 3, 4, 5 : ")
    if choice == "1":
        #학생 정보 입력받기
        try:
            data = input('Enter name mid-score final-score : ').split()
            #예외사항 처리(데이터 입력 갯수, 이미 존재하는 이름, 입력 점수 값이 양의 정수인지)
            if len(data) != 3:
                raise ValueError("Num of data is not 3!")
            name, mid_score, final_score = data
            if not (mid_score.isdigit() and final_score.isdigit()):
                raise ValueError("Score is not positive integer!")
            mid_score = int(mid_score)
            final_score = int(final_score)
            if mid_score < 0 or final_score < 0:
                raise ValueError("Score is not positive integer!")
            if name in student_dict:
                raise ValueError("Already exist name!")
        except ValueError as e:
            print(e)
        #예외사항이 아닌 입력인 경우 1번 함수 호출
        else: Menu1(name, mid_score, final_score)

    elif choice == "2" :
        #예외사항 처리(저장된 학생 정보의 유무)
        if not student_dict:
            print("No student data!")
        else:
            #예외사항이 아닌 경우 2번 함수 호출
            #"Grading to all students." 출력
            Menu2()
            print("Grading to all students.")

    elif choice == "3" :
        try:
            # 저장된 학생 정보가 없으면 예외 발생
            if not student_dict:
                raise ValueError("No student data!")
            # 학점이 부여되지 않은 학생이 하나라도 있으면 예외 발생
            elif not all('grade' in info for info in student_dict.values()):
                raise ValueError("There is a student who didn't get grade.")
            else:
                # 모든 조건 만족 시 출력 함수 호출
                Menu3()
        except ValueError as e:
            # 발생한 예외 메시지 출력
            print(e)

    elif choice == "4" :
        try:
            # 저장된 학생 정보가 없으면 예외 발생
            if not student_dict:
                raise ValueError("No student data!")
            # 삭제할 학생 이름 입력 받기
            name = input("Enter the name to delete : ")
            # 해당 이름이 존재하지 않으면 예외 발생
            if name not in student_dict:
                raise ValueError("Not exist name!")
            # 삭제 수행
            Menu4(name)
            # 삭제 완료 메시지 출력
            print(f"{name} student information is deleted.")
        except ValueError as e:
            # 발생한 예외 메시지 출력
            print(e)

    elif choice == "5" :
        #프로그램 종료 메세지 출력
        #반복문 종료
        print("Exit Program!")
        break

    else :
        #"Wrong number. Choose again." 출력
        print("Wrong number. Choose again.")