import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from tkcalendar import Calendar
import json

#فایل ذخیره اطلاعات بلیط
TICKET_FILE = "tickets.json"
#ایجاد فیلد های اطلاعات گیر
class TicketSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("رزرو بلیط")
        self.root.geometry("600x700")
        self.root.configure(bg="#58B19F")
        self.default_font = ("B Nazanin", 16)
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#58B19F")
        frame.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(frame, text="نام:", font=self.default_font, bg="#58B19F").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_name = tk.Entry(frame, font=self.default_font)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="تاریخ:", font=self.default_font, bg="#58B19F").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.calendar = Calendar(frame, date_pattern="yyyy-mm-dd", font=self.default_font)
        self.calendar.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="مبدا:", font=self.default_font, bg="#58B19F").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_Origin = tk.Entry(frame, font=self.default_font)
        self.entry_Origin.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(frame, text="مقصد:", font=self.default_font, bg="#58B19F").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_destination = tk.Entry(frame, font=self.default_font)
        self.entry_destination.grid(row=3, column=1, padx=10, pady=10, sticky="w")

#دکمه‌‌ های ثبت بلیط
        ttk.Button(frame, text=" ثبت بلیط", style="TButton", command=self.save_tickets).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="جستجو بلیط", style="TButton", command=self.search_tickets).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="ویرایش بلیط", style="TButton", command=self.edit_ticket).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text=" حذف بلیط", style="TButton", command=self.delete_ticket).grid(row=7, column=0, columnspan=2, pady=10)

    def save_tickets(self):
        name = self.entry_name.get().strip()
        date = self.calendar.get_date()
        origin = self.entry_Origin.get().strip()
        destination = self.entry_destination.get().strip()

        if name and date and origin and destination:
            ticket = {
                "name": name,
                "date": date,
                "Origin": origin,
                "destination": destination,
            }
            self.save_to_file(ticket)
            messagebox.showinfo("ثبت بلیط", "بلیط شما با موفقیت ثبت گردید")

#پاک کردن فیلد های پر شده پس از ثبت بلیط
            self.clear_fields()
        else:
            messagebox.showerror("خطا", "لطفاً فرمی را خالی نگذارید")
    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_Origin.delete(0, tk.END)
        self.entry_destination.delete(0, tk.END)
        self.calendar.selection_clear()

#خواندن اطلاعات ذخیره شده
    def save_to_file(self, ticket):
        try:
            with open(TICKET_FILE, "r", encoding="utf-8") as file:
                tickets = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            tickets = []
        tickets.append(ticket)
        with open(TICKET_FILE, "w", encoding="utf-8") as file:
            json.dump(tickets, file, ensure_ascii=False, indent=4)
    
    def search_tickets(self):
        tickets = self.load_from_file()
        if not tickets:
            messagebox.showinfo("جستجو", "بلیط مورد نظر شما یافت نشد")
            return

        # Create search window
        search_name = simpledialog.askstring("جستجو", "نام یا بخش از نام را وارد کنید:")
        matching_tickets = [t for t in tickets if search_name in t["name"]]
        
        if matching_tickets:
            self.show_ticket_results(matching_tickets)
        else:
            messagebox.showinfo("جستجو", "هیچ نتیجه‌ای یافت نشد")

    def show_ticket_results(self, tickets):
        result_window = tk.Toplevel(self.root)                                    
        result_window.title("نتایج جستجو")
        result_window.geometry("600x500")
        result_window.configure(bg="#ffffff")

        tree = ttk.Treeview(result_window, columns=("نام", "تاریخ", "مبدا", "مقصد"), show="headings")
        for i in ("نام", "تاریخ", "مبدا", "مقصد"):
            tree.heading(i, text=i)
        for ticket in tickets:
            tree.insert("", "end", values=(ticket["name"], ticket["date"], ticket["Origin"], ticket["destination"]))

        tree.pack(padx=20, pady=20, expand=True, fill="both")

    def load_from_file(self):
        try:
            with open(TICKET_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def edit_ticket(self):
        tickets = self.load_from_file()
        if not tickets:
            messagebox.showinfo("ویرایش", "هیچ بلیطی برای ویرایش وجود ندارد.")
            return

        search_name = simpledialog.askstring("ویرایش", "نام بلیطی را که می‌خواهید ویرایش کنید وارد کنید:")
        ticket_to_edit = next((t for t in tickets if t["name"] == search_name), None)

        if ticket_to_edit:
            name = simpledialog.askstring("ویرایش", "نام جدید:", initialvalue=ticket_to_edit["name"])
            date = simpledialog.askstring("ویرایش", "تاریخ جدید:", initialvalue=ticket_to_edit["date"])
            origin = simpledialog.askstring("ویرایش", "مبدا جدید:", initialvalue=ticket_to_edit["Origin"])
            destination = simpledialog.askstring("ویرایش", "مقصد جدید:", initialvalue=ticket_to_edit["destination"])

            if name and date and origin and destination:
                ticket_to_edit.update({"name": name, "date": date, "Origin": origin, "destination": destination})
                self.save_updated_tickets(tickets)
                messagebox.showinfo("ویرایش", "بلیط با موفقیت ویرایش شد")
            else:
                messagebox.showerror("خطا", "لطفاً فرمی را خالی نگذارید")
        else:
            messagebox.showerror("خطا", "بلیطی با این نام یافت نشد")

    def save_updated_tickets(self, tickets):
        with open(TICKET_FILE, "w", encoding="utf-8") as file:
            json.dump(tickets, file, ensure_ascii=False, indent=4)

    def delete_ticket(self):
        tickets = self.load_from_file()
        if not tickets:
            messagebox.showinfo("حذف", "هیچ بلیطی برای حذف وجود ندارد.")
            return

        search_name = simpledialog.askstring("حذف", "نام بلیطی را که می‌خواهید حذف کنید وارد کنید:")
        tickets = [t for t in tickets if t["name"] != search_name]
        with open(TICKET_FILE, "w", encoding="utf-8") as file:
            json.dump(tickets, file, ensure_ascii=False, indent=4)
        messagebox.showinfo("حذف", "بلیط با موفقیت حذف شد")

#استایل دکمه ها
style = ttk.Style()
style.configure("TButton", font=("B Nazanin", 16), background="#00b894", padding=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketSystem(root)
    root.mainloop()