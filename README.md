# HỆ THỐNG MÃ HÓA TINYDES

## Giới thiệu

**HỆ THỐNG MÃ HÓA TINYDES** là ứng dụng web chuyên nghiệp cho thuật toán mã hóa TinyDES sử dụng FastAPI + HTML/CSS. Hệ thống được thiết kế với giao diện hiện đại, dễ sử dụng và trực quan.

### 🎨 **Giao diện mới:**

- **Header chuyên nghiệp** với logo Đại học Kinh tế Quốc dân, tên hệ thống nổi bật
- **Sidebar navigation** với profile và menu quản lý
- **Layout responsive** hoạt động tốt trên mọi thiết bị
- **Avatar robot** thân thiện trong phần profile
- **Tabs navigation** trực quan cho các chức năng

## 🌐 Truy cập trực tuyến

Nếu muốn xem hệ thống, bạn có thể truy cập trực tuyến tại: **[https://tinydes.onrender.com/](https://tinydes.onrender.com/)**

Hệ thống đã được triển khai trên Render, bạn có thể sử dụng ngay mà không cần cài đặt hay chạy local.

## Kiến trúc hệ thống

### 🎯 **Frontend vs Backend**

**Frontend (Giao diện người dùng):**
- `templates/index.html` - Giao diện HTML với layout header, sidebar và main content
- `static/style.css` - Styling chuyên nghiệp với responsive design
- `static/robotava.jpg` - Avatar robot cho profile section
- JavaScript cơ bản cho tab navigation và UX enhancements

**Backend (Xử lý logic):**
- `main.py` - FastAPI server xử lý requests và routing
- `tinydes.py` - Thuật toán mã hóa TinyDES (core logic)
- `run_server.py` - Script khởi động server

### 🔄 **Cách FastAPI hoạt động:**

```
Người dùng → mở trình duyệt (HTML) → nhập dữ liệu (VD: plaintext, key)

HTML (frontend) → gửi yêu cầu (POST request) đến FastAPI (backend)

FastAPI → nhận dữ liệu → gọi file thuật toán tinydes.py để xử lý → nhận kết quả → trả lại cho HTML để hiển thị
```

**Chi tiết luồng hoạt động:**
1. **User** nhập dữ liệu vào form HTML trong tab tương ứng
2. **Form submission** → gửi POST request đến `/encrypt` hoặc `/decrypt`
3. **FastAPI** nhận request → validate dữ liệu
4. **FastAPI** gọi `tinydes.py` để thực hiện mã hóa/giải mã
5. **TinyDES** trả về kết quả
6. **FastAPI** render HTML template với kết quả trong tab tương ứng
7. **Browser** hiển thị kết quả trong tab đúng (encrypt tab cho mã hóa, decrypt tab cho giải mã)

## Cài đặt và Chạy

### 1. Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy Server
```bash
python run_server.py
```

### 3. Truy cập
Mở trình duyệt: **http://localhost:8000**

Hệ thống sẽ tự động:
- Copy ảnh lý thuyết vào static folder
- Copy ảnh avatar robot vào static folder
- Khởi động server FastAPI

## Cấu trúc Project

```
TinyDes-code/
├── main.py                 # 🔧 BACKEND: FastAPI server
├── tinydes.py             # 🔧 BACKEND: Thuật toán TinyDES
├── run_server.py          # 🔧 BACKEND: Script chạy server
├── requirements.txt       # 📦 Dependencies
├── templates/             # 🎨 FRONTEND: HTML templates
│   ├── index.html        # 🎨 FRONTEND: Template chính (layout mới)
│   └── robotava.jpg      # 🎨 FRONTEND: Avatar robot
├── static/               # 🎨 FRONTEND: Static files
│   ├── style.css         # 🎨 FRONTEND: CSS styling (giao diện mới)
│   ├── neu-logo.jpg      # 🎨 FRONTEND: Logo Đại học Kinh tế Quốc dân
│   ├── CautruccuaTinyDes.png  # 🎨 FRONTEND: Hình ảnh cấu trúc TinyDES
│   └── robotava.jpg      # 🎨 FRONTEND: Avatar robot (auto-copied)
├── Lý thuyết/            # 📚 Tài liệu lý thuyết
│   └── CautruccuaTinyDes.png
└── README.md             # 📚 Hướng dẫn này
```

### 📁 **Phân loại file:**

**🔧 Backend Files:**
- `main.py` - FastAPI server với routes, form handling và auto-copy images
- `tinydes.py` - Thuật toán mã hóa TinyDES (core logic)
- `run_server.py` - Script khởi động server

**🎨 Frontend Files:**
- `templates/index.html` - Giao diện HTML với layout mới (header, sidebar, main content)
- `static/style.css` - CSS styling cho giao diện chuyên nghiệp
- `static/robotava.jpg` - Avatar robot cho profile section
- `static/neu-logo.jpg` - Logo trường Đại học Kinh tế Quốc dân

**📦 Config Files:**
- `requirements.txt` - Danh sách thư viện cần thiết

## Tính năng

### ✅ **Các chức năng chính:**

1. **📖 Lý thuyết TinyDES**
   - Giới thiệu về thuật toán
   - Tính chất của hệ mã
   - Cấu trúc TinyDES
   - Các vòng Feistel
   - Thuật toán sinh khóa con
   - Đặc điểm bảo mật

2. **🔒 Mã hóa**
   - Mã hóa dữ liệu 8-bit
   - Hỗ trợ Binary, Hex, Decimal input
   - Hiển thị kết quả trong tab "Mã hóa"
   - Kết quả hiển thị: Ciphertext (Binary, Hex, Decimal)

3. **🔓 Giải mã**
   - Giải mã dữ liệu 8-bit
   - Hỗ trợ Binary, Hex, Decimal input
   - Hiển thị kết quả trong tab "Giải mã"
   - Kết quả hiển thị: Plaintext (Binary, Hex, Decimal)

4. **⚙️ Quy trình chi tiết**
   - Xem quy trình mã hóa/giải mã từng bước
   - Hiển thị sinh khóa con (Subkeys)
   - Chi tiết các vòng Feistel
   - Expansion, S-box, P-box operations

5. **🧪 Test Functions**
   - Test Expand function (4-bit → 6-bit)
   - Test S-box Lookup (6-bit → 4-bit)
   - Test P-box Permutation (4-bit → 4-bit)
   - Test Compress Key function
   - Test Full Encryption

### 🎨 **Giao diện:**

- ✅ Layout chuyên nghiệp với header, sidebar và main content
- ✅ Sidebar navigation với profile section (avatar robot)
- ✅ Menu "QUẢN LÝ MÃ HÓA" với các tab chức năng
- ✅ Header với logo NEU và tên hệ thống rõ ràng
- ✅ Tabs navigation trong main content area
- ✅ Responsive design cho mobile và tablet
- ✅ Màu sắc nhất quán (xanh dương #1976d2 và vàng #ffc107)
- ✅ Hover effects và transitions mượt mà
- ✅ Kết quả hiển thị đúng tab (mã hóa/giải mã)

## Cách sử dụng

### 🎯 **Quy trình sử dụng:**

1. **Mở trình duyệt** → Truy cập `http://localhost:8000`
2. **Chọn tab từ sidebar** hoặc **tabs ở main content**:
   - 📖 **Lý thuyết** - Xem thông tin về TinyDES
   - 🔒 **Mã hóa** - Thực hiện mã hóa dữ liệu
   - 🔓 **Giải mã** - Thực hiện giải mã dữ liệu
   - ⚙️ **Quy trình** - Xem quy trình chi tiết
   - 🧪 **Test Functions** - Test từng hàm riêng lẻ

3. **Nhập dữ liệu** vào form trong tab tương ứng:
   - **Mã hóa**: Plaintext + Key
   - **Giải mã**: Ciphertext + Key
   - **Quy trình**: Chọn loại (Mã hóa/Giải mã) + Input + Key

4. **Nhấn nút** tương ứng (Mã hóa, Giải mã, Xem Quy trình, v.v.)

5. **Xem kết quả**:
   - Kết quả mã hóa hiển thị trong tab "Mã hóa"
   - Kết quả giải mã hiển thị trong tab "Giải mã"
   - Quy trình chi tiết hiển thị trong tab "Quy trình"

### 📝 **Ví dụ sử dụng:**

**Mã hóa:**
- Plaintext: `01011100` (binary) hoặc `5C` (hex) hoặc `92` (decimal)
- Key: `01101010` (binary) hoặc `6A` (hex) hoặc `106` (decimal)
- Kết quả: Ciphertext sẽ được hiển thị trong tab "Mã hóa"

**Giải mã:**
- Ciphertext: (kết quả từ bước mã hóa)
- Key: `01101010` (cùng key đã dùng mã hóa)
- Kết quả: Plaintext gốc sẽ được hiển thị trong tab "Giải mã"

### 🔄 **Luồng xử lý chi tiết:**

```
1. User chọn tab → Nhập dữ liệu vào form HTML
2. Submit form → POST request đến FastAPI
3. FastAPI nhận request → Validate dữ liệu
4. FastAPI gọi tinydes.py → Xử lý mã hóa/giải mã
5. TinyDES trả kết quả → FastAPI
6. FastAPI render template với result trong tab tương ứng → HTML response
7. Browser hiển thị kết quả trong tab đúng → User
```

### 🎨 **Định dạng input được hỗ trợ:**

- **Binary**: `01011100` (8 bit)
- **Hex**: `5C` hoặc `0x5C`
- **Decimal**: `92`

## Giao diện mới

### 📐 **Layout Structure:**

```
┌─────────────────────────────────────────────┐
│           HEADER                            │
│  [Logo NEU] [HỆ THỐNG MÃ HÓA TINYDES] [Info]│
├──────────┬──────────────────────────────────┤
│          │  Tiện ích mã hóa TinyDES         │
│ SIDEBAR  │  ┌─────────────────────────┐    │
│          │  │ [Tabs Navigation]       │    │
│ [Avatar] │  ├─────────────────────────┤    │
│ Profile  │  │                         │    │
│ Info     │  │   Tab Content Area     │    │
│          │  │   (Forms, Results)      │    │
│ [Menu]   │  │                         │    │
│ - Lý     │  │                         │    │
│   thuyết │  │                         │    │
│ - Mã hóa │  └─────────────────────────┘    │
│ - Giải   │                                  │
│   mã     │                                  │
│ - Quy    │                                  │
│   trình  │                                  │
│ - Test   │                                  │
└──────────┴──────────────────────────────────┘
```

### 🎨 **Màu sắc chủ đạo:**

- **Xanh dương chính**: `#1976d2` (primary blue)
- **Xanh dương đậm**: `#1565c0` (dark blue)
- **Vàng nhấn**: `#ffc107` (accent yellow)
- **Nền**: `#f5f5f5` (light gray background)

### 📱 **Responsive Design:**

- **Desktop**: Full layout với sidebar và main content
- **Tablet**: Layout điều chỉnh, sidebar có thể thu gọn
- **Mobile**: Layout dọc, sidebar chuyển thành menu trên

## Tác giả và Thông tin

- **Trường**: Đại học Kinh tế Quốc dân (NEU)
- **Khoa**: Khoa CNTT
- **Hệ thống**: HỆ THỐNG MÃ HÓA TINYDES
- **Phiên bản**: 2.0 (Giao diện mới)

## License

Dự án này được phát triển cho mục đích giáo dục và học tập.
