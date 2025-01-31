def display_message(message: str, width: int = 40, underline_char: str = ""):
    # Remove espaços extras no final da mensagem
    cleaned_message = message.strip()
    
    # Calcula o espaçamento necessário para centralizar
    padding = (width - len(cleaned_message)) // 2

    # Centraliza a mensagem
    centered_message = f"{cleaned_message.center(width)}"
    print(centered_message)

    # Centraliza a linha abaixo da mensagem
    underline = underline_char
    centered_underline = f"{underline.center(width)}"
    print(centered_underline)


