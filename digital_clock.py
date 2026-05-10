import tkinter as tk
from datetime import datetime
import pytz
from tkinter import font as tkFont


class DigitalClockApp:
    """Multi-timezone digital clock application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock - Multiple Time Zones")
        self.root.geometry("900x600")
        self.root.configure(bg="#1a1a1a")
        
        # Configure styles
        self.bg_color = "#1a1a1a"
        self.fg_color = "#00ff00"
        self.accent_color = "#00cc00"
        
        # Time zones to display
        self.timezones = [
            ("New York", "America/New_York"),
            ("London", "Europe/London"),
            ("Tokyo", "Asia/Tokyo"),
            ("Sydney", "Australia/Sydney"),
            ("Dubai", "Asia/Dubai"),
            ("Singapore", "Asia/Singapore"),
            ("Los Angeles", "America/Los_Angeles"),
            ("Toronto", "America/Toronto"),
        ]
        
        # Create main frame
        self.create_ui()
        
        # Start clock update
        self.update_clocks()
    
    def create_ui(self):
        """Create the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🕐 GLOBAL TIME ZONES 🕐",
            font=("Courier New", 28, "bold"),
            fg=self.fg_color,
            bg=self.bg_color
        )
        title_label.pack()
        
        # Clock grid frame
        self.clock_frame = tk.Frame(self.root, bg=self.bg_color)
        self.clock_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Create clock displays
        self.clock_labels = {}
        self.timezone_labels = {}
        
        for i, (city, tz) in enumerate(self.timezones):
            # Calculate grid position
            row = i // 2
            col = i % 2
            
            # Create frame for each timezone
            tz_frame = tk.Frame(
                self.clock_frame,
                bg="#2a2a2a",
                relief=tk.RIDGE,
                bd=3
            )
            tz_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Configure grid weights
            self.clock_frame.grid_rowconfigure(row, weight=1)
            self.clock_frame.grid_columnconfigure(col, weight=1)
            
            # City name
            city_label = tk.Label(
                tz_frame,
                text=city,
                font=("Courier New", 18, "bold"),
                fg=self.accent_color,
                bg="#2a2a2a"
            )
            city_label.pack(pady=(15, 5))
            
            # Time display
            time_label = tk.Label(
                tz_frame,
                text="00:00:00",
                font=("Courier New", 48, "bold"),
                fg=self.fg_color,
                bg="#2a2a2a"
            )
            time_label.pack(pady=10)
            
            # Date display
            date_label = tk.Label(
                tz_frame,
                text="Loading...",
                font=("Courier New", 12),
                fg="#666666",
                bg="#2a2a2a"
            )
            date_label.pack(pady=(5, 15))
            
            # Store references
            self.clock_labels[tz] = (time_label, date_label)
            self.timezone_labels[tz] = city
        
        # Bottom status frame
        status_frame = tk.Frame(self.root, bg="#2a2a2a", height=50)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="Live Clock - Updates Every Second",
            font=("Courier New", 11),
            fg=self.accent_color,
            bg="#2a2a2a"
        )
        self.status_label.pack(pady=10)
    
    def update_clocks(self):
        """Update all clock displays"""
        for tz, (time_label, date_label) in self.clock_labels.items():
            # Get current time in timezone
            tz_obj = pytz.timezone(tz)
            current_time = datetime.now(tz_obj)
            
            # Format time
            time_str = current_time.strftime("%H:%M:%S")
            date_str = current_time.strftime("%A, %B %d, %Y")
            
            # Update labels
            time_label.config(text=time_str)
            date_label.config(text=date_str)
        
        # Update status
        local_time = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"Last Updated: {local_time}")
        
        # Schedule next update (every 1000ms = 1 second)
        self.root.after(1000, self.update_clocks)


class AnalogClock:
    """Analog clock widget for a single timezone"""
    
    def __init__(self, parent, timezone, city_name, size=200):
        self.parent = parent
        self.timezone = timezone
        self.city_name = city_name
        self.size = size
        
        # Create canvas
        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            bg="#2a2a2a",
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.update_analog()
    
    def update_analog(self):
        """Update analog clock display"""
        self.canvas.delete("all")
        
        center_x = center_y = self.size // 2
        radius = self.size // 2 - 20
        
        # Draw clock face circle
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline="#00ff00",
            width=3
        )
        
        # Draw hour markers
        for i in range(12):
            angle = (i * 30 - 90) * 3.14159 / 180
            x1 = center_x + (radius - 15) * 3.14159 * i / 60
            y1 = center_y + (radius - 15) * 3.14159 * i / 60
            x2 = center_x + radius * 3.14159 * i / 60
            y2 = center_y + radius * 3.14159 * i / 60
            self.canvas.create_line(x1, y1, x2, y2, fill="#00ff00", width=2)
        
        # Get current time
        tz_obj = pytz.timezone(self.timezone)
        current_time = datetime.now(tz_obj)
        
        hour = current_time.hour % 12
        minute = current_time.minute
        second = current_time.second
        
        # Calculate angles
        hour_angle = (hour * 30 + minute * 0.5 - 90) * 3.14159 / 180
        minute_angle = (minute * 6 + second * 0.1 - 90) * 3.14159 / 180
        second_angle = (second * 6 - 90) * 3.14159 / 180
        
        # Draw hour hand
        hour_x = center_x + (radius * 0.5) * 3.14159 * hour / 6
        hour_y = center_y + (radius * 0.5) * 3.14159 * hour / 6
        self.canvas.create_line(
            center_x, center_y,
            hour_x, hour_y,
            fill="#00ff00",
            width=4
        )
        
        # Draw minute hand
        minute_x = center_x + (radius * 0.7) * 3.14159 * minute / 30
        minute_y = center_y + (radius * 0.7) * 3.14159 * minute / 30
        self.canvas.create_line(
            center_x, center_y,
            minute_x, minute_y,
            fill="#00ff00",
            width=3
        )
        
        # Draw second hand
        second_x = center_x + (radius * 0.8) * 3.14159 * second / 30
        second_y = center_y + (radius * 0.8) * 3.14159 * second / 30
        self.canvas.create_line(
            center_x, center_y,
            second_x, second_y,
            fill="#ff0000",
            width=1
        )
        
        # Draw center dot
        self.canvas.create_oval(
            center_x - 5,
            center_y - 5,
            center_x + 5,
            center_y + 5,
            fill="#00ff00"
        )
        
        # Schedule next update
        self.parent.after(1000, self.update_analog)


class HybridClockApp:
    """Hybrid app with both digital and analog clocks"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Clock - Digital & Analog")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1a1a1a")
        
        # Create notebook-style tabs
        self.create_ui()
    
    def create_ui(self):
        """Create hybrid UI"""
        # Menu buttons
        menu_frame = tk.Frame(self.root, bg="#2a2a2a")
        menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        
        tk.Label(
            menu_frame,
            text="TIME ZONES",
            font=("Courier New", 14, "bold"),
            fg="#00ff00",
            bg="#2a2a2a"
        ).pack(pady=10)
        
        self.timezones = {
            "New York": "America/New_York",
            "London": "Europe/London",
            "Tokyo": "Asia/Tokyo",
            "Sydney": "Australia/Sydney",
            "Dubai": "Asia/Dubai",
            "Singapore": "Asia/Singapore",
        }
        
        self.buttons = {}
        for city, tz in self.timezones.items():
            btn = tk.Button(
                menu_frame,
                text=city,
                font=("Courier New", 11),
                fg="white",
                bg="#333333",
                activeforeground="#00ff00",
                activebackground="#444444",
                width=15,
                command=lambda c=city, t=tz: self.show_clock(c, t)
            )
            btn.pack(pady=5)
            self.buttons[city] = btn
        
        # Display frame
        self.display_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show first timezone by default
        first_city = list(self.timezones.keys())[0]
        self.show_clock(first_city, self.timezones[first_city])
    
    def show_clock(self, city, timezone):
        """Show selected timezone clock"""
        # Clear display frame
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        # Title
        tk.Label(
            self.display_frame,
            text=f"📍 {city}",
            font=("Courier New", 32, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        ).pack(pady=20)
        
        # Time display
        time_frame = tk.Frame(self.display_frame, bg="#2a2a2a")
        time_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.time_label = tk.Label(
            time_frame,
            text="00:00:00",
            font=("Courier New", 80, "bold"),
            fg="#00ff00",
            bg="#2a2a2a"
        )
        self.time_label.pack(pady=20)
        
        self.date_label = tk.Label(
            time_frame,
            text="Loading...",
            font=("Courier New", 18),
            fg="#666666",
            bg="#2a2a2a"
        )
        self.date_label.pack(pady=10)
        
        self.timezone_display = timezone
        self.update_selected_clock()
    
    def update_selected_clock(self):
        """Update the selected timezone clock"""
        tz_obj = pytz.timezone(self.timezone_display)
        current_time = datetime.now(tz_obj)
        
        time_str = current_time.strftime("%H:%M:%S")
        date_str = current_time.strftime("%A, %B %d, %Y")
        
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        self.root.after(1000, self.update_selected_clock)


def main():
    """Main entry point"""
    print("🕐 Digital Clock Application")
    print("=" * 50)
    print("Choose an option:")
    print("1. Multi-Timezone Digital Clock (8 zones at once)")
    print("2. Single Timezone Selector")
    print("=" * 50)
    
    root = tk.Tk()
    
    # Default to multi-timezone view
    app = DigitalClockApp(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()
