def binary_to_text(binary_str):
    """
    Hàm này nhận một chuỗi nhị phân (ví dụ '0110000101100010')
    và chuyển nó thành văn bản (ví dụ 'ab').
    """
    
    # Lọc ra chỉ các ký tự '0' và '1' (loại bỏ các ký tự rác)
    cleaned_binary_str = "".join(filter(lambda x: x in '01', binary_str))
    
    # Chia chuỗi thành các khối 8-bit (1 byte)
    byte_chunks = [cleaned_binary_str[i:i+8] for i in range(0, len(cleaned_binary_str), 8)]
    
    text_result = ""
    for byte in byte_chunks:
        if len(byte) == 8:
            try:
                # Chuyển nhị phân (hệ 2) sang số nguyên
                decimal_value = int(byte, 2)
                # Chuyển số nguyên sang ký tự ASCII
                text_result += chr(decimal_value)
            except Exception:
                text_result += "[?]" # Bỏ qua byte lỗi
        
    return text_result

def main():
    file_name = 'txt'
    
    # ---- ĐÂY LÀ PHẦN QUAN TRỌNG NHẤT ----
    # 
    # Định nghĩa các ký tự "tàng hình"
    # Ký tự này ' ' (non-breaking space) KHÁC với ký tự này ' ' (space)
    
    non_breaking_space = ' ' 
    space = ' '
    tab = '\t'
    
    # -------------------------------------

    try:
        # Đọc toàn bộ file
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        binary_string_h1 = "" # Giả thuyết 1: Space = 0, Tab = 1
        binary_string_h2 = "" # Giả thuyết 2: Space = 1, Tab = 0

        # Tách nội dung thành các dòng để xử lý
        for line in content.splitlines():
            # Bỏ qua các dòng trống
            if not line.strip():
                continue
            
            # --- Áp dụng 2 giả thuyết (VỚI CODE ĐÃ SỬA) ---
            
            # Giả thuyết 1: Cả 2 loại Space = '0', Tab = '1'
            binary_string_h1 += line.replace(space, '0').replace(non_breaking_space, '0').replace(tab, '1')
            
            # Giả thuyết 2: Cả 2 loại Space = '1', Tab = '0'
            binary_string_h2 += line.replace(space, '1').replace(non_breaking_space, '1').replace(tab, '0')

        # --- In kết quả ---
        print("="*40)
        
        print("\n[Kết quả Giả thuyết 1: (Space = 0, Tab = 1)]")
        result_h1 = binary_to_text(binary_string_h1)
        print(result_h1)
        
        print("\n[Kết quả Giả thuyết 2: (Space = 1, Tab = 0)]")
        result_h2 = binary_to_text(binary_string_h2)
        print(result_h2)
        
        print("\n" + "="*40)

    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file '{file_name}'.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Dòng này để chạy hàm main() khi bạn thực thi file
if __name__ == "__main__":
    main()