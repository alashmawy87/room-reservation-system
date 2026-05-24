# Room Reservation System

A comprehensive Python-based room reservation system with hourly and daily booking capabilities, complete with persistent database storage.

## 🎯 Features

✅ **Hourly Booking** - Book rooms by specific hours (0-23 in 24-hour format)  
✅ **Daily Booking** - Book entire days or multiple consecutive days  
✅ **Multiple Rooms** - Manage unlimited rooms simultaneously  
✅ **Availability Tracking** - View available and reserved time slots  
✅ **Persistent Storage** - SQLite database + JSON backup  
✅ **Reservation Management** - Book, cancel, and view reservations  
✅ **History Tracking** - Complete reservation history  
✅ **Statistics** - Occupancy and usage statistics  

---

## 📋 Installation

### Prerequisites
- Python 3.7+
- No external dependencies required (uses built-in libraries)

### Setup

```bash
# Clone the repository
git clone https://github.com/alashmawy87/room-reservation-system.git
cd room-reservation-system

# Run the system
python reservation_system.py
```

---

## 🚀 Quick Start

### Basic Usage

```python
from reservation_system import ReservationManager

# Initialize manager
manager = ReservationManager()

# Add rooms
manager.add_room("Room 101")
manager.add_room("Room 102")
manager.add_room("Room 103")

# Book a room by hours (9 AM to 12 PM)
manager.book_room("John Doe", "Room 101", "2026-05-10", 9, 12)

# Book an entire day (0:00 to 24:00)
manager.book_room("Jane Smith", "Room 102", "2026-05-11", 0, 24)

# View schedule
manager.view_schedule("Room 101", "2026-05-10")

# Get available hours
available = manager.get_available_hours("Room 101", "2026-05-10")
print(f"Available hours: {available}")

# Get reserved hours with guest info
reserved = manager.get_reserved_hours("Room 101", "2026-05-10")
print(f"Reserved slots: {reserved}")

# Cancel a reservation
manager.cancel_reservation("RES20260510001")

# View statistics
manager.display_statistics()

# View all reservations
manager.view_all_schedules("2026-05-10")
```

---

## 📚 API Reference

### ReservationManager Class

#### `add_room(room_id: str) -> bool`
Add a new room to the system.

```python
manager.add_room("Room 201")
```

#### `book_room(guest_name: str, room_id: str, date: str, start_hour: int, end_hour: int) -> Optional[str]`
Book a room for specific hours. Returns reservation ID if successful.

```python
# Book 9 AM to 5 PM
res_id = manager.book_room("Alice Brown", "Room 101", "2026-05-12", 9, 17)

# Book entire day (24 hours)
res_id = manager.book_room("Bob Johnson", "Room 102", "2026-05-13", 0, 24)

# Book morning slot
res_id = manager.book_room("Charlie Wilson", "Room 103", "2026-05-14", 0, 12)
```

**Parameters:**
- `guest_name` (str): Guest's name
- `room_id` (str): Room identifier
- `date` (str): Date in YYYY-MM-DD format
- `start_hour` (int): Check-in hour (0-23)
- `end_hour` (int): Check-out hour (1-24)

**Returns:**
- Reservation ID (str) if successful
- None if booking fails

#### `cancel_reservation(reservation_id: str) -> bool`
Cancel an existing reservation.

```python
manager.cancel_reservation("RES20260510001")
```

#### `get_available_hours(room_id: str, date: str) -> List[int]`
Get list of available hours for a specific date.

```python
available = manager.get_available_hours("Room 101", "2026-05-15")
# Output: [0, 1, 2, ..., 23]
```

#### `get_reserved_hours(room_id: str, date: str) -> List[Dict]`
Get reserved hours with guest information.

```python
reserved = manager.get_reserved_hours("Room 101", "2026-05-15")
# Output: [
#   {"hour": 9, "guest": "John Doe", "reservation_id": "RES20260515001"},
#   {"hour": 10, "guest": "John Doe", "reservation_id": "RES20260515001"}
# ]
```

#### `view_schedule(room_id: str, date: str)`
Display the full schedule for a room on a specific date.

```python
manager.view_schedule("Room 101", "2026-05-15")
```

**Output:**
```
============================================================
Room Room 101 - Schedule for 2026-05-15
============================================================
00:00 - 01:00: Available
09:00 - 10:00: Reserved (John Doe)
10:00 - 11:00: Reserved (John Doe)
12:00 - 13:00: Available
...
============================================================
```

#### `view_all_schedules(date: str)`
Display schedules for all rooms on a specific date.

```python
manager.view_all_schedules("2026-05-15")
```

#### `get_reservation_history(room_id: Optional[str] = None) -> List[Reservation]`
Get reservation history for a specific room or all rooms.

```python
# All reservations
all_history = manager.get_reservation_history()

# Single room
room_history = manager.get_reservation_history("Room 101")

for reservation in room_history:
    print(reservation)
```

#### `display_statistics()`
Display reservation statistics.

```python
manager.display_statistics()
```

**Output:**
```
============================================================
RESERVATION STATISTICS
============================================================
Total Rooms: 3
Total Active Reservations: 5
  Room 101: 2 active reservations
  Room 102: 2 active reservations
  Room 103: 1 active reservations
============================================================
```

---

## 📁 File Structure

```
room-reservation-system/
├── reservation_system.py      # Main system file
├── reservations.db            # SQLite database (auto-created)
├── reservations.json          # JSON backup (auto-created)
├── README.md                  # This file
└── .gitignore                # Git ignore rules
```

---

## 💾 Data Persistence

### SQLite Database (`reservations.db`)

The system automatically creates and maintains a SQLite database with the following tables:

**reservations table:**
```sql
CREATE TABLE reservations (
    reservation_id TEXT PRIMARY KEY,
    guest_name TEXT NOT NULL,
    room_id TEXT NOT NULL,
    date TEXT NOT NULL,
    start_hour INTEGER NOT NULL,
    end_hour INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL,
    cancelled_at TEXT
)
```

**rooms table:**
```sql
CREATE TABLE rooms (
    room_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL
)
```

### JSON Backup (`reservations.json`)

All active reservations are also saved to a JSON file for easy viewing and backup:

```json
[
  {
    "reservation_id": "RES20260510001",
    "guest_name": "John Doe",
    "room_id": "Room 101",
    "date": "2026-05-10",
    "start_hour": 9,
    "end_hour": 12,
    "created_at": "2026-05-10T14:30:00.123456",
    "status": "Active"
  }
]
```

---

## 📊 Example Usage

### Example 1: Hotel Room Booking

```python
from reservation_system import ReservationManager

# Initialize
manager = ReservationManager()

# Add hotel rooms
for i in range(1, 6):
    manager.add_room(f"Room {100 + i}")

# Make bookings
print("=== Making Bookings ===\n")
manager.book_room("John Smith", "Room 101", "2026-05-15", 9, 17)      # 8 hours
manager.book_room("Jane Doe", "Room 101", "2026-05-15", 18, 24)       # 6 hours
manager.book_room("Bob Johnson", "Room 102", "2026-05-15", 0, 24)     # Full day
manager.book_room("Alice Brown", "Room 103", "2026-05-16", 10, 14)    # 4 hours

# View schedules
print("\n=== Room Schedules ===\n")
manager.view_all_schedules("2026-05-15")

# Get availability
print("\n=== Availability Check ===")
for room_id in ["Room 101", "Room 102", "Room 103"]:
    available = manager.get_available_hours(room_id, "2026-05-15")
    print(f"{room_id}: {len(available)} hours available")

# Statistics
manager.display_statistics()
```

### Example 2: Conference Room Booking

```python
from reservation_system import ReservationManager

manager = ReservationManager()

# Add conference rooms
manager.add_room("Conference A")
manager.add_room("Conference B")

# Book for meetings
manager.book_room("Team Alpha", "Conference A", "2026-05-20", 9, 11)    # 2 hours
manager.book_room("Team Beta", "Conference A", "2026-05-20", 11, 13)    # 2 hours
manager.book_room("Team Gamma", "Conference B", "2026-05-20", 14, 16)   # 2 hours

# View reservations
reservations = manager.get_reservation_history()
for res in reservations:
    print(f"Meeting: {res.guest_name} in {res.room_id}")
```

---

## 🔄 Date & Time Format

### Dates
- Format: `YYYY-MM-DD` (e.g., "2026-05-10")
- Example: `"2026-12-25"` for December 25, 2026

### Hours
- Format: 0-24 (24-hour clock)
- 0 = 00:00 (midnight)
- 9 = 09:00 (9 AM)
- 12 = 12:00 (noon)
- 17 = 17:00 (5 PM)
- 24 = 00:00 (end of day)

### Examples:
```python
# 9 AM to 5 PM
manager.book_room("John", "Room 101", "2026-05-10", 9, 17)

# All day (midnight to midnight)
manager.book_room("Jane", "Room 102", "2026-05-10", 0, 24)

# Morning shift
manager.book_room("Bob", "Room 103", "2026-05-10", 0, 12)

# Afternoon shift
manager.book_room("Alice", "Room 104", "2026-05-10", 12, 24)

# Single hour
manager.book_room("Charlie", "Room 105", "2026-05-10", 14, 15)
```

---

## 🛠️ Advanced Features

### Search by Date Range

```python
# Get all reservations for a specific date
reservations = manager.get_reservation_history()
date_reservations = [r for r in reservations if r.date == "2026-05-15"]
```

### Check Room Availability for Multiple Days

```python
def check_availability_range(manager, room_id, start_date, end_date):
    """Check if room is available for a date range"""
    from datetime import datetime, timedelta
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    current = start
    while current <= end:
        available = manager.get_available_hours(room_id, current.strftime("%Y-%m-%d"))
        if len(available) < 24:  # Not completely free
            return False
        current += timedelta(days=1)
    
    return True

# Usage
is_available = check_availability_range(manager, "Room 101", "2026-05-15", "2026-05-17")
```

### Generate Booking Report

```python
def generate_report(manager, date):
    """Generate occupancy report for a date"""
    print(f"\n{'='*60}")
    print(f"Occupancy Report - {date}")
    print(f"{'='*60}")
    
    for room_id in sorted(manager.rooms.keys()):
        reserved = manager.get_reserved_hours(room_id, date)
        total_hours = len(reserved)
        occupancy = (total_hours / 24) * 100
        print(f"{room_id}: {total_hours}/24 hours ({occupancy:.1f}% occupied)")
    
    print(f"{'='*60}\n")

# Usage
generate_report(manager, "2026-05-15")
```

---

## 🐛 Error Handling

```python
from reservation_system import ReservationManager

manager = ReservationManager()
manager.add_room("Room 101")

# Booking a non-existent room
result = manager.book_room("John", "Room 999", "2026-05-10", 9, 12)
# Output: ❌ Room Room 999 does not exist!

# Invalid hours
result = manager.book_room("Jane", "Room 101", "2026-05-10", 25, 30)
# Output: ❌ Invalid hours! Must be between 0-23, and end_hour > start_hour

# Room already booked
manager.book_room("Bob", "Room 101", "2026-05-10", 9, 12)
result = manager.book_room("Alice", "Room 101", "2026-05-10", 10, 14)
# Output: ❌ Room Room 101 is not available for 10:00 - 14:00 on 2026-05-10
```

---

## 📈 Performance

- **Database Operations**: O(1) for single reservation lookup
- **Schedule Display**: O(24) for daily schedule
- **Availability Check**: O(24) for hourly availability
- **History Search**: O(n) where n is number of reservations

---

## 🔐 Security Notes

- Database uses SQLite (file-based)
- No network communication
- Reservation data stored locally
- JSON file is plain text (consider encryption for sensitive data)

---

## 📝 License

Open source - feel free to use and modify

## 👤 Author

Created by alashmawy87

## 🤝 Contributing

Feel free to fork, modify, and improve this system!

---

## 📞 Support

For issues or questions, please open an issue on the GitHub repository.

---

**Happy Booking! 🎉**
