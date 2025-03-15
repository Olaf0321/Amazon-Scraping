import tkinter as tk
from tkinter import ttk
import threading
import time

class SegmentedProgressBar(tk.Canvas):
    def __init__(self, parent, segments=10, width=400, height=30, bg="#E0E0E0", fg="#4CAF50", **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0, **kwargs)
        self.segments = segments
        self.fg = fg
        self.segment_width = width / segments
        self.height = height
        self.filled_segments = 0
        self.segment_items = []

        for i in range(segments):
            x1 = i * self.segment_width + 2
            x2 = (i + 1) * self.segment_width - 2
            rect = self.create_rectangle(x1, 2, x2, height - 2, fill=bg, outline="#AAA", width=2)
            self.segment_items.append(rect)

    def update_progress(self, value):
        self.filled_segments = int(value * self.segments)
        for i in range(self.segments):
            if i < self.filled_segments:
                self.itemconfig(self.segment_items[i], fill=self.fg)
            else:
                self.itemconfig(self.segment_items[i], fill="#E0E0E0")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Amazon Products Scraping")
        self.root.geometry("600x400")
        self.root.configure(bg="#F0F0F0")

        self.progress_bar = SegmentedProgressBar(root, segments=15, width=500, height=40)
        self.progress_bar.pack(pady=50)

        self.start_button = ttk.Button(root, text="Start", command=self.start_scraping)
        self.start_button.pack(pady=20)

        self.status_label = ttk.Label(root, text="Status: Waiting", font=("Helvetica", 12), background="#F0F0F0")
        self.status_label.pack(pady=10)

        self.progress_value = 0
        self.total_rows = 20  # Simulate a total number of rows to process
        self.running = False

    def start_scraping(self):
        if self.running:
            return
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text="Processing...")

        threading.Thread(target=self.process_data, daemon=True).start()

    def process_data(self):
        for i in range(1, self.total_rows + 1):
            if not self.running:
                break
            
            # Simulate row processing
            time.sleep(0.5)

            # Update progress bar dynamically
            progress_fraction = i / self.total_rows
            self.root.after(0, self.update_ui, progress_fraction, i)

        self.root.after(0, self.finish_processing)

    def update_ui(self, progress_fraction, row_num):
        self.progress_bar.update_progress(progress_fraction)
        self.status_label.config(text=f"Processing row {row_num}/{self.total_rows}...")

    def finish_processing(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Processing Completed")

    def stop_scraping(self):
        self.running = False
        self.status_label.config(text="Processing Stopped")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
