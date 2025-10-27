# Time Filter Feature Documentation

## 📅 Overview

The Time Filter feature allows users to view usage statistics and costs for specific time periods in the Account tab. This provides better insights into usage patterns and spending over time.

## ✨ Features

### Time Range Options
- **All Time** - Complete usage history
- **Today** - Current day usage (00:00 - 23:59)
- **Yesterday** - Previous day usage
- **Last 7 Days** - Rolling 7-day period
- **Last 30 Days** - Rolling 30-day period  
- **This Month** - Current month from 1st to today
- **Last Month** - Complete previous month

### UI Components
- **Dropdown Filter** - Easy selection of predefined time ranges
- **Auto-refresh** - Statistics update automatically when filter changes

## 🔧 Technical Implementation

### Data Structure
Each usage record now includes timestamp information:
```json
{
  "type": "image|video",
  "count": 1,
  "cost": 0.0203,
  "timestamp": "2025-10-21T08:27:00.123456"
}
```

### UserManager Methods
- `record_image_usage()` - Now saves timestamp with each usage
- `record_video_usage()` - Now saves timestamp with each usage
- `get_user_stats_by_date_range()` - Filter stats by date range
- `get_stats_today()` - Today's statistics
- `get_stats_yesterday()` - Yesterday's statistics
- `get_stats_last_7_days()` - Last 7 days statistics
- `get_stats_last_30_days()` - Last 30 days statistics
- `get_stats_this_month()` - This month's statistics
- `get_stats_last_month()` - Last month's statistics

### Account Tab Updates
- Added time filter dropdown UI
- Added custom date range inputs
- Updated `refresh_data()` to use filtered statistics
- Added event handlers for filter changes

## 📊 Usage Examples

### Viewing Today's Usage
1. Open Account tab
2. Select "Today" from time filter dropdown
3. Statistics automatically update to show today's usage only


### Monthly Reports
1. Select "This Month" for current month usage
2. Select "Last Month" for previous month comparison
3. Use "Last 30 Days" for rolling monthly view

## 🧪 Testing

Run the test script to verify functionality:
```bash
python3 test_time_filter.py
```

The test creates sample data across different time periods and verifies:
- ✅ Today's usage filtering
- ✅ Yesterday's usage filtering  
- ✅ Last 7 days filtering
- ✅ Custom date range filtering
- ✅ Proper cost calculations

## 💡 Benefits

### For Users
- **Better Insights** - Understand usage patterns over time
- **Cost Tracking** - Monitor spending by time period
- **Budget Planning** - Analyze historical usage for planning
- **Flexible Reporting** - Custom date ranges for specific needs

### For Business
- **Usage Analytics** - Track user engagement over time
- **Revenue Tracking** - Monitor income by time periods
- **Trend Analysis** - Identify usage patterns and seasonality
- **Customer Insights** - Understand user behavior patterns

## 🔄 Data Migration

Existing users will have their historical usage data preserved. New timestamp tracking only applies to usage recorded after the feature implementation. Historical data without timestamps will appear in "All Time" view only.

## 🚀 Future Enhancements

Potential improvements for future versions:
- **Export Reports** - Download usage reports as CSV/PDF
- **Usage Charts** - Visual graphs of usage over time
- **Alerts** - Notifications for usage thresholds
- **Comparison Views** - Side-by-side period comparisons
- **Automated Reports** - Scheduled email reports

## 📝 Notes

- All timestamps are stored in ISO format with timezone information
- Date calculations handle month/year boundaries correctly
- Custom date ranges are inclusive of both start and end dates
- Statistics refresh automatically when filters change
- Invalid date formats show user-friendly error messages
