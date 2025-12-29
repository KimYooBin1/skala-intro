from password import validate_password

while True:
    user_input = input("입력하세요 (!quit 입력 시 종료): ")
    is_valid, message = validate_password(user_input)
    if not is_valid:
        print(message)
        continue
    if user_input == "!quit":
        break
    print(user_input)