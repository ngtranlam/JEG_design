# 🔐 JEG Design Extract - Account System Setup Guide

## 📋 Overview

Hệ thống tài khoản đã được tích hợp vào JEG Design Extract với các tính năng:

- ✅ **User Authentication** - Đăng nhập với username/password
- ✅ **Usage Tracking** - Theo dõi số lượt sử dụng và chi phí
- ✅ **Password Management** - Đổi mật khẩu lần đầu đăng nhập
- ✅ **Account Dashboard** - Xem thông tin và thống kê sử dụng
- ✅ **API Integration** - Đồng bộ dữ liệu lên website
- ✅ **Local Storage** - Lưu trữ dữ liệu local an toàn

## 🏗️ Architecture

```
JEG Design Extract
├── user_manager.py          # Core user management
├── login_dialog.py          # Login popup
├── password_change_dialog.py # Password change dialog
├── account_tab.py           # Account dashboard UI
└── jeg_design_extract.py    # Main app (updated)
```

## 💰 Pricing Structure

| Feature | Cost per Usage |
|---------|----------------|
| **Image Processing** | $0.0203 |
| **Video Generation** | $6.40 |

## 👥 Predefined Users

Tất cả users có password mặc định: `jeg@12345`

```
lamdev, huynhtan, nguyen, toniwintheiser15754, minhductran1996,
hoangbao2411, quangduc.24696@gmail.com, ducmy10081987@gmail.com,
linkkany21, thucuyen97, hoanguyen14, chautuan154, tongthaomy,
ngockim96, chaulien1807, nguyentuyenktdt@gmail.com, Vantich2021,
thao1607, HongNhung, phamthuyvan9x, sumydn, XuanThuy,
trucquynh1099@gmail.com, congnguyen0312@gmail.com, hoang0806,
chienpv96, nthaqtkd, thanhtd, thuthaokt982023, thaoptt235@gmail.com,
ngocanh25101996, nguyenngocvnhcm, anhthu27901, tuyetsuong2k1,
nhnguyen12a1@gmail, tranhien, anhthu309, tranhainam,
ngocsanghuynh, baongocle, minhtiendao, hoang1492001,
nguyentung, Nguyendo, phuongtrinhjeg, anbinhjeg, lethangjeg,
khanhhung, ngochuyenjeg, ngocthanhjeg
```

## 🚀 Installation & Setup

### 1. Files Created

Các files mới đã được tạo:
- `user_manager.py` - Quản lý user và usage tracking
- `login_dialog.py` - Dialog đăng nhập
- `password_change_dialog.py` - Dialog đổi mật khẩu
- `account_tab.py` - Tab Account trong UI chính
- `test_account_system.py` - Script test hệ thống

### 2. Main App Integration

File `jeg_design_extract.py` đã được cập nhật:
- ✅ Import các modules account
- ✅ Khởi tạo UserManager
- ✅ Login dialog khi khởi động
- ✅ Account tab trong sidebar
- ✅ Usage tracking trong các methods xử lý

### 3. Data Storage

Dữ liệu được lưu tại:
```
~/JEGDesignExtract/user_data/
├── users.json      # User database
├── session.json    # Current session
└── device_id.txt   # Unique device ID
```

## 🔧 Configuration

### API Endpoint

Cập nhật API endpoint trong `user_manager.py`:

```python
def __init__(self, api_endpoint: str = None):
    self.api_endpoint = api_endpoint or "https://your-website.com/api"
```

### API Format

Usage data được gửi đến API với format:

```json
{
    "username": "lamdev",
    "usage_type": "image",  // "image" hoặc "video"
    "count": 1,
    "cost": 0.0203,
    "timestamp": "2024-10-20T14:30:00",
    "device_id": "uuid-device-id"
}
```

## 🧪 Testing

Chạy test script:

```bash
python test_account_system.py
```

Test cases:
- ✅ User authentication
- ✅ Password change
- ✅ Usage recording
- ✅ Stats calculation
- ✅ UI components
- ✅ Integration

## 🎯 User Flow

### 1. First Time Login
1. App khởi động → Login dialog
2. User nhập username + password mặc định
3. **Password change dialog** (chỉ hiện 1 lần/device)
4. Đổi password thành công → Vào app

### 2. Subsequent Logins
1. App khởi động → Login dialog
2. User nhập username + password mới
3. Vào app trực tiếp

### 3. Using Features
1. **Extract Design** → Record image usage ($0.0203)
2. **AI Upscale** → Record image usage ($0.0203)
3. **Video Generation** → Record video usage ($6.40)
4. Data tự động sync lên API

### 4. Account Management
1. Click **Account tab**
2. Xem usage stats và costs
3. Change password, sync data, logout

## 🔒 Security Features

- ✅ **Password Hashing** - SHA-256
- ✅ **Device Tracking** - Unique device IDs
- ✅ **Session Management** - Auto restore sessions
- ✅ **Local Storage** - Encrypted user data
- ✅ **API Security** - Background sync with timeout

## 📊 Usage Tracking

### Automatic Tracking

Usage được track tự động khi:
- `process_with_gemini_api()` - Extract Design Print
- `process_with_gemini_embroidery()` - Extract Design Embroidery  
- `_process_upscale_thread()` - AI Upscale single
- `_process_upscale_batch_thread()` - AI Upscale batch
- `_generate_video_thread()` - Video Generation

### Manual Tracking

```python
# Record image processing
self.record_image_usage(count=1)

# Record video generation  
self.record_video_usage(count=1)
```

## 🌐 API Integration

### Endpoint Setup

Tạo API endpoint nhận POST requests:

```
POST /api/usage
Content-Type: application/json

{
    "username": "lamdev",
    "usage_type": "image",
    "count": 1,
    "cost": 0.0203,
    "timestamp": "2024-10-20T14:30:00",
    "device_id": "uuid"
}
```

### Response Format

```json
{
    "success": true,
    "message": "Usage recorded successfully"
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   - Đảm bảo tất cả files account system trong cùng thư mục
   - Check Python path

2. **Login Dialog không hiện**
   - Check `self.user_manager.restore_session()` 
   - Xóa `session.json` để force login

3. **Usage không được track**
   - Check `self.user_manager.is_logged_in()`
   - Verify method calls trong processing functions

4. **API sync fails**
   - Check network connection
   - Verify API endpoint URL
   - Check API response format

### Debug Mode

Thêm debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Future Enhancements

### Planned Features
- [ ] **Cloud Sync** - Sync across devices
- [ ] **Usage Reports** - Monthly/yearly reports  
- [ ] **Payment Integration** - Stripe/PayPal
- [ ] **Admin Panel** - User management
- [ ] **Bulk User Import** - CSV import
- [ ] **Usage Limits** - Set monthly limits
- [ ] **Notifications** - Usage alerts

### API Enhancements
- [ ] **Batch Sync** - Multiple usage records
- [ ] **Offline Mode** - Queue when offline
- [ ] **Data Export** - CSV/JSON export
- [ ] **Analytics** - Usage analytics

## 📞 Support

Nếu có vấn đề với account system:

1. Chạy `test_account_system.py` để debug
2. Check logs trong console
3. Verify data files trong `~/JEGDesignExtract/user_data/`
4. Contact developer với error details

---

**✅ Account System Setup Complete!**

Hệ thống tài khoản đã sẵn sàng sử dụng với đầy đủ tính năng authentication, usage tracking, và billing integration.
