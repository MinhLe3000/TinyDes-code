# TinyDES Web Application

## Giới thiệu

Ứng dụng web đơn giản cho thuật toán mã hóa TinyDES sử dụng FastAPI + HTML thuần. Không cần JavaScript phức tạp!

## 🌐 Truy cập trực tuyến

Nếu muốn xem hệ thống, bạn có thể truy cập trực tuyến tại: **[https://tinydes.onrender.com/](https://tinydes.onrender.com/)**

Hệ thống đã được triển khai trên Render, bạn có thể sử dụng ngay mà không cần cài đặt hay chạy local.

## Kiến trúc hệ thống

### 🎯 **Frontend vs Backend**

**Frontend (Giao diện người dùng):**
- `templates/index.html` - Giao diện HTML với forms
- `static/style.css` - Styling và responsive design
- Không có JavaScript phức tạp, chỉ dùng HTML forms

**Backend (Xử lý logic):**
- `main.py` - FastAPI server xử lý requests
- `tinydes.py` - Thuật toán mã hóa TinyDES
- `run_server.py` - Script khởi động server

### 🔄 **Cách FastAPI hoạt động:**

```
Người dùng → mở trình duyệt (HTML) → nhập dữ liệu (VD: plaintext, key)

HTML (frontend) → gửi yêu cầu (POST request) đến FastAPI (backend)

FastAPI → nhận dữ liệu → gọi file thuật toán tinydes.py để xử lý → nhận kết quả → trả lại cho HTML để hiển thị
```

**Chi tiết luồng hoạt động:**
1. **User** nhập dữ liệu vào form HTML
2. **Form submission** → gửi POST request đến `/encrypt` hoặc `/decrypt`
3. **FastAPI** nhận request → validate dữ liệu
4. **FastAPI** gọi `tinydes.py` để thực hiện mã hóa/giải mã
5. **TinyDES** trả về kết quả
6. **FastAPI** render HTML template với kết quả
7. **Browser** hiển thị kết quả cho user

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

## Cấu trúc Project

```
TinyDes/
├── main.py                 # 🔧 BACKEND: FastAPI server
├── tinydes.py             # 🔧 BACKEND: Thuật toán TinyDES
├── run_server.py          # 🔧 BACKEND: Script chạy server
├── requirements.txt       # 📦 Dependencies
├── templates/             # 🎨 FRONTEND: HTML templates
│   └── index.html        # 🎨 FRONTEND: Template chính
├── static/               # 🎨 FRONTEND: Static files
│   └── style.css        # 🎨 FRONTEND: CSS styling
└── README.md            # 📚 Hướng dẫn này
```

### 📁 **Phân loại file:**

**🔧 Backend Files:**
- `main.py` - FastAPI server với routes và form handling
- `tinydes.py` - Thuật toán mã hóa TinyDES (core logic)
- `run_server.py` - Script khởi động server

**🎨 Frontend Files:**
- `templates/index.html` - Giao diện HTML với forms
- `static/style.css` - CSS styling cho giao diện

**📦 Config Files:**
- `requirements.txt` - Danh sách thư viện cần thiết


## Tính năng

- ✅ Mã hóa/Giải mã 8-bit dữ liệu
- ✅ Giao diện đẹp và responsive
- ✅ Hỗ trợ Binary, Hex, Decimal input
- ✅ Server-side processing
- ✅ Form-based interface (không cần JavaScript)

## Cách sử dụng

### 🎯 **Quy trình sử dụng:**

1. **Mở trình duyệt** → Truy cập `http://localhost:8000`
2. **Chọn tab "Mã hóa"** hoặc "Giải mã"
3. **Nhập dữ liệu** vào form:
   - **Mã hóa**: Plaintext + Key
   - **Giải mã**: Ciphertext + Key
4. **Nhấn nút** "Mã hóa" hoặc "Giải mã"
5. **Xem kết quả** hiển thị ngay trên trang

### 📝 **Ví dụ sử dụng:**

**Mã hóa:**
- Plaintext: `01011100` (binary) hoặc `5C` (hex) hoặc `92` (decimal)
- Key: `01101010` (binary) hoặc `6A` (hex) hoặc `106` (decimal)
- Kết quả: Ciphertext sẽ được hiển thị

**Giải mã:**
- Ciphertext: (kết quả từ bước mã hóa)
- Key: `01101010` (cùng key đã dùng mã hóa)
- Kết quả: Plaintext gốc

### 🔄 **Luồng xử lý chi tiết:**

```
1. User nhập dữ liệu → HTML Form
2. Submit form → POST request đến FastAPI
3. FastAPI nhận request → Validate dữ liệu
4. FastAPI gọi tinydes.py → Xử lý mã hóa/giải mã
5. TinyDES trả kết quả → FastAPI
6. FastAPI render template → HTML response
7. Browser hiển thị kết quả → User
```

### 🎨 **Định dạng input được hỗ trợ:**
- **Binary**: `01011100` (8 bit)
- **Hex**: `5C` hoặc `0x5C`
- **Decimal**: `92`
