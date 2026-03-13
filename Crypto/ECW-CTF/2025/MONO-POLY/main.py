try:
    with open('./ciphertext.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # Định nghĩa các ký tự gốc và ký tự thay thế tương ứng
    from_chars = "ABCEFGHIJKLMNOPQRSUVWXYZ"  
    to_chars   = "MSULEXORCHJGKPYAFZWQBVNI"  
    # Tạo bảng tra cứu (translation table)
    translation_table = str.maketrans(from_chars, to_chars)
    # Áp dụng bảng tra cứu lên toàn bộ nội dung
    mapped_content = content.translate(translation_table)

    print(mapped_content)
except FileNotFoundError:
    print("File not found")