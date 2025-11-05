# 📊 API GET Stats Requirement

## 🎯 Mục đích
Tool cần lấy số liệu usage thực tế từ server để hiển thị chính xác cho user, hỗ trợ filter theo thời gian.

---

## 🚀 API Endpoint Cần Bổ Sung

### **GET** `/api/tools/stats/{userName}`

**Full URL:** `https://jegdn.com/api/tools/stats/{userName}`

**Method:** GET

**Authentication:** None (giống như POST API hiện tại)

---

## 📊 Request Parameters

### **Path Parameter:**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `userName` | string | **Yes** | Tên đăng nhập của user | `admin.tu` |

### **Query Parameters (Optional - cho filter):**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `date_from` | string | No | Ngày bắt đầu (Y-m-d) | `2025-11-01` |
| `date_to` | string | No | Ngày kết thúc (Y-m-d) | `2025-11-05` |
| `period` | string | No | Kỳ báo cáo: `today`, `yesterday`, `this_week`, `last_week`, `this_month`, `last_month`, `all_time` | `this_month` |

### **Ưu tiên xử lý:**
1. Nếu có `date_from` và `date_to` → Dùng range này
2. Nếu có `period` → Dùng period predefined
3. Nếu không có gì → Trả về `all_time`

---

## 📤 Response Format

### ✅ **Success Response (200)**
```json
{
  "status": "success",
  "data": {
    "userName": "admin.tu",
    "user_id": 24,
    "filter": {
      "period": "this_month",
      "date_from": "2025-11-01",
      "date_to": "2025-11-30",
      "description": "This Month (November 2025)"
    },
    "stats": {
      "total_image_count": 150,
      "total_image_cost": 3.045,
      "total_video_count": 25,
      "total_video_cost": 160.00,
      "total_cost": 163.045
    },
    "last_updated": "2025-11-05 10:13:00"
  }
}
```

### ❌ **Error Responses**

**404 - User Not Found**
```json
{
  "status": "error",
  "message": "User not found or not a seller"
}
```

**400 - Invalid Date Range**
```json
{
  "status": "error",
  "message": "Invalid date range: date_from must be before date_to"
}
```

---

## 🔧 Backend Logic Yêu Cầu

### **Database Query Logic:**
```sql
-- Tính SUM từ bảng tools_usage theo filter
SELECT 
    SUM(image_count) as total_image_count,
    SUM(image_cost) as total_image_cost,
    SUM(video_count) as total_video_count,
    SUM(video_cost) as total_video_cost,
    SUM(total_cost) as total_cost
FROM tools_usage 
WHERE user_id = ? 
  AND created_at >= ? 
  AND created_at <= ?
```

### **Period Mapping:**
| Period | Logic |
|--------|-------|
| `today` | `DATE(created_at) = CURDATE()` |
| `yesterday` | `DATE(created_at) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)` |
| `this_week` | `YEARWEEK(created_at) = YEARWEEK(NOW())` |
| `last_week` | `YEARWEEK(created_at) = YEARWEEK(NOW()) - 1` |
| `this_month` | `YEAR(created_at) = YEAR(NOW()) AND MONTH(created_at) = MONTH(NOW())` |
| `last_month` | `YEAR(created_at) = YEAR(DATE_SUB(NOW(), INTERVAL 1 MONTH)) AND MONTH(created_at) = MONTH(DATE_SUB(NOW(), INTERVAL 1 MONTH))` |
| `all_time` | Không có WHERE condition về thời gian |

---

## 📋 Use Cases

### **1. Hiển thị tổng số liệu khi mở tool**
```
GET /api/tools/stats/admin.tu
→ Trả về all_time stats
```

### **2. Filter theo tháng hiện tại**
```
GET /api/tools/stats/admin.tu?period=this_month
→ Trả về stats tháng 11/2025
```

### **3. Filter theo range tùy chọn**
```
GET /api/tools/stats/admin.tu?date_from=2025-11-01&date_to=2025-11-05
→ Trả về stats từ 1/11 đến 5/11
```

### **4. Filter hôm nay**
```
GET /api/tools/stats/admin.tu?period=today
→ Trả về stats hôm nay
```

---

## 🧪 Test Cases

### **Test 1: Valid User - All Time**
```bash
curl "https://jegdn.com/api/tools/stats/admin.tu"
# Expected: 200 với all_time stats
```

### **Test 2: Valid User - This Month**
```bash
curl "https://jegdn.com/api/tools/stats/admin.tu?period=this_month"
# Expected: 200 với this_month stats
```

### **Test 3: Valid User - Date Range**
```bash
curl "https://jegdn.com/api/tools/stats/admin.tu?date_from=2025-11-01&date_to=2025-11-05"
# Expected: 200 với filtered stats
```

### **Test 4: Invalid User**
```bash
curl "https://jegdn.com/api/tools/stats/nonexistent"
# Expected: 404 User not found
```

### **Test 5: Invalid Date Range**
```bash
curl "https://jegdn.com/api/tools/stats/admin.tu?date_from=2025-11-05&date_to=2025-11-01"
# Expected: 400 Invalid date range
```

---

## 🔐 Security & Validation

### **User Validation:**
- User phải tồn tại với `roles = 3` (seller) và `status = 1`
- Giống logic validation của POST API hiện tại

### **Date Validation:**
- `date_from` và `date_to` phải có format `Y-m-d`
- `date_from` phải <= `date_to`
- Không được query quá xa (khuyến nghị max 1 năm)

### **Period Validation:**
- Chỉ accept: `today`, `yesterday`, `this_week`, `last_week`, `this_month`, `last_month`, `all_time`

---

## ⚡ Performance Notes

### **Database Index:**
Cần index trên:
- `user_id` (đã có)
- `created_at` (cần bổ sung nếu chưa có)
- Composite index: `(user_id, created_at)` (optimal)

### **Caching:**
- Cache kết quả cho `all_time` stats (ít thay đổi)
- Cache TTL: 5-10 phút cho real-time data

---

## 📞 Implementation Priority

### **Phase 1 (Bắt buộc):**
- ✅ Basic GET endpoint với all_time stats
- ✅ User validation
- ✅ Error handling

### **Phase 2 (Khuyến nghị):**
- ✅ Period filter support
- ✅ Date range filter
- ✅ Response format chuẩn

### **Phase 3 (Tùy chọn):**
- ✅ Performance optimization
- ✅ Caching layer
- ✅ Rate limiting

---

## 📝 Notes

- API này chỉ **READ-ONLY**, không modify data
- Response format tương tự POST API để consistency
- Hỗ trợ CORS như POST API hiện tại
- Logging format giống POST API

**Ưu tiên implement Phase 1 trước để tool có thể hoạt động cơ bản!**
