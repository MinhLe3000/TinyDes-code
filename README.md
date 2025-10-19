# TinyDES - Thuật toán mã hóa DES thu nhỏ

## 📖 Giới thiệu

TinyDES là phiên bản thu nhỏ của thuật toán DES (Data Encryption Standard), được thiết kế để học tập và nghiên cứu về mật mã học. Đây là một hệ thống mã hóa đối xứng sử dụng kiến trúc Feistel với 3 rounds.

## 🔧 Đặc điểm kỹ thuật

- **Block size**: 8 bit (chia thành 2 phần 4-bit: L0 và R0)
- **Key size**: 8 bit (chia thành KL0 và KR0, mỗi phần 4-bit)
- **Subkey size**: 6 bit cho mỗi round
- **Số rounds**: 3 rounds Feistel
- **Kiến trúc**: Feistel cipher

## 🚀 Cài đặt và chạy chương trình

### Yêu cầu hệ thống
- Python 3.6 trở lên
- Không cần cài đặt thư viện bên ngoài

### Chạy chương trình
```bash
python tinydes.py
```

Khi chạy, chương trình sẽ hiển thị menu chọn chế độ:
- **Chế độ 1**: Chế độ tương tác (nhập dữ liệu)
- **Chế độ 2**: Chế độ test tự động

## 📋 Hướng dẫn sử dụng chi tiết

### 1. Chế độ tương tác (Interactive Mode)

Khi chọn chế độ 1, bạn sẽ thấy menu chính với 5 tùy chọn:

#### 🔐 1. Mã hóa dữ liệu
- **Chức năng**: Mã hóa plaintext 8-bit thành ciphertext
- **Input formats**: 
  - Binary: `01011100` (8 bit)
  - Hexadecimal: `0x5C` hoặc `5C` (2 ký tự hex)
  - Decimal: `92` (0-255)

**Ví dụ sử dụng:**
```
🔸 Plaintext: 01011100
🔸 Key: 01101010
```

**Kết quả:**
```
✅ KẾT QUẢ MÃ HÓA:
📄 Plaintext:  01011100 (binary)
🔑 Key:        01101010 (binary)
🔐 Ciphertext: 11010010 (binary)
🔐 Ciphertext: 0xd2 (hex)
🔐 Ciphertext: 210 (decimal)
```

#### 🔓 2. Giải mã dữ liệu
- **Chức năng**: Giải mã ciphertext 8-bit thành plaintext ban đầu
- **Input formats**: Tương tự như mã hóa

**Ví dụ sử dụng:**
```
🔸 Ciphertext: 11010010
🔸 Key: 01101010
```

**Kết quả:**
```
✅ KẾT QUẢ GIẢI MÃ:
🔐 Ciphertext: 11010010 (binary)
🔑 Key:        01101010 (binary)
📄 Plaintext:  01011100 (binary)
📄 Plaintext:  0x5c (hex)
📄 Plaintext:  92 (decimal)
```

#### 🧪 3. Test các hàm riêng lẻ
Cho phép test từng thành phần của thuật toán:

##### a) Expand Function (4 bit → 6 bit)
- **Chức năng**: Mở rộng 4 bit thành 6 bit theo quy tắc: `b2b3b1b2b1b0`
- **Ví dụ**: `1100` → `001100`

##### b) S-box Lookup (6 bit → 4 bit)
- **Chức năng**: Tra cứu bảng S-box 4×16
- **Cách hoạt động**: 
  - Row index: bit đầu và cuối (b0b5)
  - Column index: 4 bit giữa (b1b2b3b4)

##### c) P-box Permutation (4 bit → 4 bit)
- **Chức năng**: Hoán vị bit theo quy tắc: `b0b1b2b3` → `b2b0b3b1`
- **Ví dụ**: `1000` → `0100`

##### d) Key Compression (8 bit → 6 bit)
- **Chức năng**: Nén khóa 8 bit thành 6 bit theo quy tắc: `k5k1k3k2k7k0`
- **Input**: KL (4 bit) và KR (4 bit)
- **Ví dụ**: KL=`0011`, KR=`0101` → `100111`

#### 📚 4. Hiển thị thông tin về TinyDES
Hiển thị thông tin chi tiết về:
- Đặc điểm của thuật toán
- Các thành phần chính
- Ví dụ sử dụng

#### 🚪 5. Thoát chương trình
Kết thúc chương trình với thông báo cảm ơn.

### 2. Chế độ test tự động

Chế độ này chạy các test case mặc định để kiểm tra tính đúng đắn của thuật toán:

- Test các hàm riêng lẻ (Expand, S-box, P-box, Compress)
- Test mã hóa/giải mã với dữ liệu mẫu
- Test với các định dạng khác nhau (binary, hex, decimal)

## 🔬 Chi tiết kỹ thuật về thuật toán

### Kiến trúc Feistel
TinyDES sử dụng kiến trúc Feistel với 3 rounds:

1. **Round 1**: 
   - Shift key: 1 bit
   - Feistel function: F(R0, K1)

2. **Round 2**: 
   - Shift key: 2 bit
   - Feistel function: F(R1, K2)

3. **Round 3**: 
   - Shift key: 1 bit
   - Feistel function: F(R2, K3)

### Quá trình mã hóa
```
Plaintext (8-bit) → Split (L0, R0) → 3 Feistel Rounds → Ciphertext (8-bit)
```

### Quá trình giải mã
```
Ciphertext (8-bit) → Split (L3, R3) → 3 Feistel Rounds (reverse) → Plaintext (8-bit)
```

### Feistel Function
Mỗi round thực hiện:
1. **Expand**: Mở rộng R từ 4→6 bit
2. **XOR**: Với subkey 6-bit
3. **S-box**: Tra cứu bảng thay thế
4. **P-box**: Hoán vị bit

### Key Schedule
- **KL0, KR0**: Khóa ban đầu (4-bit mỗi phần)
- **K1**: Compress(shift1(KL0), shift1(KR0))
- **K2**: Compress(shift2(KL1), shift2(KR1))
- **K3**: Compress(shift1(KL2), shift1(KR2))

## 📊 Ví dụ thực tế

### Ví dụ 1: Mã hóa cơ bản
```
Input:
- Plaintext: 01011100 (92 decimal, 0x5C hex)
- Key: 01101010 (106 decimal, 0x6A hex)

Output:
- Ciphertext: 11010010 (210 decimal, 0xD2 hex)
```

### Ví dụ 2: Test các hàm riêng lẻ
```
Expand(1100) = 001100
S-box(100101) = 0111
P-box(1000) = 0100
Compress(0011, 0101) = 100111
```

## ⚠️ Lưu ý quan trọng

1. **Mục đích giáo dục**: TinyDES được thiết kế cho mục đích học tập, không nên sử dụng trong môi trường thực tế
2. **Độ dài khóa ngắn**: 8-bit key có thể bị brute force dễ dàng
3. **Ít rounds**: 3 rounds có thể không đủ để đảm bảo tính bảo mật cao
4. **Format dữ liệu**: Chương trình hỗ trợ nhiều format input nhưng luôn chuyển về binary để xử lý

## 🐛 Xử lý lỗi

Chương trình có các cơ chế xử lý lỗi:
- Kiểm tra format input hợp lệ
- Validation độ dài bit
- Thông báo lỗi rõ ràng bằng tiếng Việt
- Gợi ý format đúng cho người dùng

## 📝 Tác giả

Code được phát triển cho mục đích học tập môn An toàn bảo mật thông tin (ATBMTT).

## 📄 License

Mã nguồn mở cho mục đích giáo dục và nghiên cứu.
