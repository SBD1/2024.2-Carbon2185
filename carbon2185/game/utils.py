def display_message(message: str, border: str = "=", padding: int = 2):
    border_length = len(message) + 4
    border_line = border * border_length

    print(border_line)
    for _ in range(padding):
        print(border * 2 + " " * (border_length - 4) + border * 2)
    print(f"{border * 2} {message} {border * 2}")
    for _ in range(padding):
        print(border * 2 + " " * (border_length - 4) + border * 2)
    print(border_line)
