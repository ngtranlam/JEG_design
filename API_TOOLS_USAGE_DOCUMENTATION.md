# 🛠️ Tools Usage API Documentation

## 📋 Overview
API để gửi dữ liệu sử dụng tools từ external applications về hệ thống Tools Report.

---

## 🚀 API Endpoint

### **POST** `/api/tools/update`

**Full URL:** `https://jegdn.com/api/tools/update`

**Content-Type:** `application/x-www-form-urlencoded`

**Authentication:** None (Public API)

---

## 📊 Request Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `userName` | string | **Yes** | Tên đăng nhập của user | `admin.tu` |
| `image_count` | integer | No | Số lượng ảnh tạo | `5` |
| `image_cost` | decimal | No | Chi phí tạo ảnh ($) | `10.50` |
| `video_count` | integer | No | Số lượng video tạo | `3` |
| `video_cost` | decimal | No | Chi phí tạo video ($) | `15.75` |
| `total_cost` | decimal | No | Tổng chi phí ($) | `26.25` |
| `timestamp` | string | No | Thời gian (ISO format) | `2025-10-21 14:30:00` |

### 📝 Notes:
- **`userName`** phải tồn tại trong hệ thống với `roles = 3` (seller) và `status = 1`
- **`total_cost`** sẽ được tự động tính = `image_cost + video_cost` nếu không gửi
- **`timestamp`** sẽ dùng thời gian hiện tại nếu không gửi
- Tất cả parameters khác `userName` đều optional, default = 0

---

## 📤 Response Format

### ✅ Success Response (200)
```json
{
  "status": "success",
  "message": "Tools usage data logged successfully",
  "data": {
    "record_id": 123,
    "userName": "admin.tu",
    "user_id": 24,
    "logged_data": {
      "image_count": 5,
      "image_cost": 10.50,
      "video_count": 3,
      "video_cost": 15.75,
      "total_cost": 26.25,
      "timestamp": "2025-10-21 14:30:00"
    }
  }
}
```

### ❌ Error Responses

**400 - Missing userName**
```json
{
  "status": "error",
  "message": "userName is required"
}
```

**404 - User Not Found**
```json
{
  "status": "error",
  "message": "User not found or not a seller"
}
```

**500 - Server Error**
```json
{
  "status": "error",
  "message": "Internal server error: [error details]"
}
```

---

## 🔧 Code Examples

### PHP (cURL)
```php
<?php
$url = 'https://jegdn.com/api/tools/update';
$data = [
    'userName' => 'admin.tu',
    'image_count' => 5,
    'image_cost' => 10.50,
    'video_count' => 3,
    'video_cost' => 15.75,
    'timestamp' => date('Y-m-d H:i:s')
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/x-www-form-urlencoded'
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

$result = json_decode($response, true);
if ($httpCode == 200 && $result['status'] == 'success') {
    echo "Success! Record ID: " . $result['data']['record_id'];
} else {
    echo "Error: " . $result['message'];
}
?>
```

### JavaScript (Fetch)
```javascript
const apiUrl = 'https://jegdn.com/api/tools/update';
const data = {
    userName: 'admin.tu',
    image_count: 5,
    image_cost: 10.50,
    video_count: 3,
    video_cost: 15.75,
    timestamp: new Date().toISOString().slice(0, 19).replace('T', ' ')
};

// Convert to URLSearchParams
const params = new URLSearchParams();
Object.keys(data).forEach(key => {
    if (data[key] !== null && data[key] !== '') {
        params.append(key, data[key]);
    }
});

fetch(apiUrl, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: params
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log('Success!', data.data);
    } else {
        console.error('Error:', data.message);
    }
})
.catch(error => {
    console.error('Network Error:', error);
});
```

### Python (requests)
```python
import requests
from datetime import datetime

url = 'https://jegdn.com/api/tools/update'
data = {
    'userName': 'admin.tu',
    'image_count': 5,
    'image_cost': 10.50,
    'video_count': 3,
    'video_cost': 15.75,
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

response = requests.post(url, data=data)
result = response.json()

if response.status_code == 200 and result['status'] == 'success':
    print(f"Success! Record ID: {result['data']['record_id']}")
else:
    print(f"Error: {result['message']}")
```

### Node.js (axios)
```javascript
const axios = require('axios');
const qs = require('querystring');

const apiUrl = 'https://jegdn.com/api/tools/update';
const data = {
    userName: 'admin.tu',
    image_count: 5,
    image_cost: 10.50,
    video_count: 3,
    video_cost: 15.75,
    timestamp: new Date().toISOString().slice(0, 19).replace('T', ' ')
};

axios.post(apiUrl, qs.stringify(data), {
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
})
.then(response => {
    if (response.data.status === 'success') {
        console.log('Success!', response.data.data);
    } else {
        console.error('Error:', response.data.message);
    }
})
.catch(error => {
    console.error('Error:', error.response?.data || error.message);
});
```

---

## 🎯 Data Flow

1. **External Tool** → Gửi usage data qua API
2. **API** → Validate user và tạo record mới trong `tools_usage`
3. **Tools Report** → Hiển thị SUM của tất cả records theo date filter

### 📊 Database Structure
```sql
-- Mỗi API call tạo 1 record mới
INSERT INTO tools_usage (
    user_id, image_count, image_cost, 
    video_count, video_cost, total_cost, 
    created_at, updated_at
) VALUES (24, 5, 10.50, 3, 15.75, 26.25, NOW(), NOW());

-- Report tính SUM theo date range
SELECT user_id, 
       SUM(image_count) as total_images,
       SUM(total_cost) as total_cost
FROM tools_usage 
WHERE created_at BETWEEN '2025-10-01' AND '2025-10-31'
GROUP BY user_id;
```

---

## 🧪 Testing

### Test Page
**URL:** `https://jegdn.com/test_tools_api.html`

Form test với:
- Input fields cho tất cả parameters
- Real-time validation
- Response display
- Auto-calculate total cost

### Manual Testing
```bash
# Test với curl
curl -X POST https://jegdn.com/api/tools/update \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "userName=admin.tu&image_count=5&image_cost=10.50&video_count=3&video_cost=15.75"
```

---

## 🔍 Troubleshooting

### Common Issues

**1. "User not found or not a seller"**
- Kiểm tra `userName` có đúng không
- User phải có `roles = 3` và `status = 1`

**2. "userName is required"**
- Parameter `userName` bị thiếu hoặc empty

**3. Network Error**
- Kiểm tra URL: `https://jegdn.com/api/tools/update`
- Kiểm tra Content-Type: `application/x-www-form-urlencoded`

**4. CORS Issues**
- API không có CORS restrictions
- Có thể gọi từ bất kỳ domain nào

### Debug Logs
API logs được ghi trong `storage/logs/laravel.log`:
```
[2025-10-21 14:30:00] Tools usage logged via API: {
  "userName": "admin.tu",
  "user_id": 24,
  "record_id": 123,
  "ip": "192.168.1.100"
}
```

---

## 📈 Rate Limiting
- **No rate limiting** hiện tại
- Khuyến nghị: Không spam API, gửi batch data nếu có nhiều records

---

## 🔐 Security Notes
- API **không cần authentication** (internal system)
- Chỉ accept users với `roles = 3` (sellers)
- CSRF protection đã được disable cho endpoint này
- Validate tất cả input data

---

## 📞 Support
- **Developer:** Lam Nguyen
- **System:** jegdn.com
- **Environment:** Production
- **Last Updated:** October 21, 2025

---

## 📝 Changelog

### v1.0 (2025-10-21)
- ✅ Initial API release
- ✅ Support for image/video usage tracking
- ✅ Automatic total cost calculation
- ✅ Date filtering support
- ✅ Comprehensive logging
- ✅ Test page included
