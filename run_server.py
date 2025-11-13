#!/usr/bin/env python3
"""
Script để chạy FastAPI server cho TinyDES
"""

import uvicorn
import sys
import os

def main():
    """Chạy FastAPI server"""
    # Lấy port từ environment variable (cho Render) hoặc dùng 8000 mặc định
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 Đang khởi động TinyDES API Server...")
    print(f"📡 Server sẽ chạy tại: http://0.0.0.0:{port}")
    print(f"📚 API Documentation: http://0.0.0.0:{port}/docs")
    print(f"🔧 Health Check: http://0.0.0.0:{port}/health")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            reload=False,  # Tắt reload trong production
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Đã dừng server!")
    except Exception as e:
        print(f"❌ Lỗi khi khởi động server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
