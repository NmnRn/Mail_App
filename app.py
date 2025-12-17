import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import quickstart as qs  # Must provide: gmail_send_message(...) and get_mails(limit=20)


# -----------------------------
# App Theme (Navy)
# -----------------------------
NAVY_BG = "#0B1220"
NAVY_PANEL = "#0F1A2B"
NAVY_ACCENT = "#1D4ED8"
NAVY_TEXT = "#E5E7EB"
NAVY_MUTED = "#9CA3AF"
NAVY_BORDER = "#1F2A44"
ENTRY_BG = "#0B1628"


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My Mails")
        self.minsize(650, 650)
        self.configure(bg=NAVY_BG)

        self._setup_styles()

        self.pages = {}
        self.show_page(MainPage)

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=NAVY_BG)
        style.configure("Panel.TFrame", background=NAVY_PANEL)

        style.configure("TLabel", background=NAVY_PANEL, foreground=NAVY_TEXT, font=("Segoe UI", 11))
        style.configure("Title.TLabel", background=NAVY_PANEL, foreground=NAVY_TEXT, font=("Segoe UI", 18, "bold"))
        style.configure("Muted.TLabel", background=NAVY_PANEL, foreground=NAVY_MUTED, font=("Segoe UI", 10))

        style.configure(
            "TButton",
            font=("Segoe UI", 11),
            padding=(12, 8),
            background=NAVY_BORDER,
            foreground=NAVY_TEXT,
            borderwidth=0,
        )
        style.map("TButton", background=[("active", "#223152"), ("pressed", "#17233C")])

        style.configure("Accent.TButton", background=NAVY_ACCENT, foreground="white", padding=(12, 10))
        style.map("Accent.TButton", background=[("active", "#2563EB"), ("pressed", "#1E40AF")])

        style.configure(
            "TEntry",
            fieldbackground=ENTRY_BG,
            foreground=NAVY_TEXT,
            insertcolor=NAVY_TEXT,
            padding=(10, 8),
            bordercolor=NAVY_BORDER,
            lightcolor=NAVY_BORDER,
            darkcolor=NAVY_BORDER,
        )

    def show_page(self, page_class):
        name = page_class.__name__

        if name not in self.pages:
            page = page_class(self)
            self.pages[name] = page
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        page = self.pages[name]
        page.tkraise()

        if hasattr(page, "on_show"):
            page.on_show()


class MainPage(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master, bg=NAVY_BG)

        header = ttk.Frame(self, style="Panel.TFrame")
        header.pack(fill="x", padx=18, pady=(18, 10))

        ttk.Label(header, text="My Mails", style="Title.TLabel").pack(anchor="w", padx=16, pady=(14, 2))
        ttk.Label(header, text="Compose and manage your messages", style="Muted.TLabel").pack(
            anchor="w", padx=16, pady=(0, 14)
        )

        card = ttk.Frame(self, style="Panel.TFrame")
        card.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        ttk.Button(card, text="Create Mail", style="Accent.TButton", command=lambda: master.show_page(ComposePage)).pack(
            anchor="w", padx=16, pady=(16, 10)
        )
        ttk.Button(card, text="Inbox", command=lambda: master.show_page(InboxPage)).pack(
            anchor="w", padx=16, pady=(0, 10)
        )

        self.clock_label = tk.Label(card, text="", bg=NAVY_PANEL, fg=NAVY_TEXT, font=("Consolas", 20, "bold"))
        self.clock_label.pack(anchor="w", padx=16, pady=(10, 16))
        self._update_clock()

        spacer = tk.Frame(card, bg=NAVY_PANEL)
        spacer.pack(fill="both", expand=True)

    def _update_clock(self):
        self.clock_label["text"] = datetime.now().strftime("%H:%M:%S")
        self.after(1000, self._update_clock)


class ComposePage(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master, bg=NAVY_BG)

        header = ttk.Frame(self, style="Panel.TFrame")
        header.pack(fill="x", padx=18, pady=(18, 10))

        ttk.Label(header, text="Compose", style="Title.TLabel").pack(anchor="w", padx=16, pady=(14, 2))
        ttk.Label(header, text="Write your email below", style="Muted.TLabel").pack(anchor="w", padx=16, pady=(0, 14))

        card = ttk.Frame(self, style="Panel.TFrame")
        card.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        ttk.Label(card, text="To").pack(anchor="w", padx=16, pady=(16, 6))
        self.to_entry = ttk.Entry(card)
        self.to_entry.pack(fill="x", padx=16, pady=(0, 12))

        ttk.Label(card, text="Subject").pack(anchor="w", padx=16, pady=(0, 6))
        self.subject_entry = ttk.Entry(card)
        self.subject_entry.pack(fill="x", padx=16, pady=(0, 12))

        ttk.Label(card, text="Message").pack(anchor="w", padx=16, pady=(0, 6))
        self.body_text = tk.Text(
            card,
            width=60,
            height=18,
            bg=ENTRY_BG,
            fg=NAVY_TEXT,
            insertbackground=NAVY_TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=NAVY_BORDER,
            highlightcolor=NAVY_ACCENT,
            padx=10,
            pady=10,
            font=("Segoe UI", 11),
        )
        self.body_text.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        btn_row = tk.Frame(card, bg=NAVY_PANEL)
        btn_row.pack(fill="x", padx=16, pady=(0, 16))

        ttk.Button(btn_row, text="Send", style="Accent.TButton", command=self.send_email).pack(side="left")
        ttk.Button(btn_row, text="Inbox", command=lambda: master.show_page(InboxPage)).pack(side="left", padx=10)
        ttk.Button(btn_row, text="Back", command=lambda: master.show_page(MainPage)).pack(side="right")

    def send_email(self):
        to_addr = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        content = self.body_text.get("1.0", "end-1c").strip()

        if not to_addr:
            return messagebox.showerror("Error", "Please enter a recipient email address.")
        if not content:
            return messagebox.showerror("Error", "Please enter an email message.")

        try:
            ok = qs.gmail_send_message(to=to_addr, subject=subject, content=content)
            if ok is False:
                return messagebox.showerror("Error", "Email could not be sent.")
        except Exception as e:
            return messagebox.showerror("Error", f"Email could not be sent:\n{e}")

        self.to_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)

        return messagebox.showinfo("Success", "Email sent successfully.")


class InboxPage(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master, bg=NAVY_BG)

        header = ttk.Frame(self, style="Panel.TFrame")
        header.pack(fill="x", padx=18, pady=(18, 10))

        ttk.Label(header, text="Inbox", style="Title.TLabel").pack(anchor="w", padx=16, pady=(14, 2))
        ttk.Label(header, text="Your latest messages", style="Muted.TLabel").pack(anchor="w", padx=16, pady=(0, 14))

        card = ttk.Frame(self, style="Panel.TFrame")
        card.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.status_label = tk.Label(card, text="", bg=NAVY_PANEL, fg=NAVY_MUTED, font=("Segoe UI", 10))
        self.status_label.pack(anchor="w", padx=14, pady=(12, 0))

        self.canvas = tk.Canvas(card, bg=NAVY_PANEL, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, pady=(8, 0))

        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.list_frame = tk.Frame(self.canvas, bg=NAVY_PANEL)
        self.window_id = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        btn_row = tk.Frame(self, bg=NAVY_BG)
        btn_row.pack(fill="x", padx=18, pady=(0, 18))

        ttk.Button(btn_row, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(btn_row, text="Compose", style="Accent.TButton", command=lambda: master.show_page(ComposePage)).pack(
            side="left", padx=10
        )
        ttk.Button(btn_row, text="Back", command=lambda: master.show_page(MainPage)).pack(side="right")

        self._loading = False

    def on_show(self):
        self.refresh()

    def refresh(self):
        if self._loading:
            return

        self._loading = True
        self.status_label.config(text="Loading emails...")
        self.render_cards([])

        threading.Thread(target=self._load_worker, daemon=True).start()

    def _load_worker(self):
        try:
            mails = qs.get_mails(limit=20)  # expects list[dict]: from/subject/snippet
            if mails is False or mails is None:
                mails = []
        except Exception as e:
            mails = []
            err = str(e)
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to load inbox:\n{err}"))

        self.after(0, lambda: self._apply_mails(mails))

    def _apply_mails(self, mails):
        self._loading = False
        if not mails:
            self.status_label.config(text="No messages found (or failed to load).")
        else:
            self.status_label.config(text=f"Showing {len(mails)} messages")
        self.render_cards(mails)

    def _on_frame_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def render_cards(self, messages):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for msg in messages:
            self._create_mail_card(
                parent=self.list_frame,
                sender=msg.get("from", "Unknown"),
                subject=msg.get("subject", "(No subject)"),
                snippet=msg.get("snippet", ""),
            )

    def _create_mail_card(self, parent, sender, subject, snippet):
        card = tk.Frame(parent, bg=ENTRY_BG, highlightthickness=1, highlightbackground=NAVY_BORDER)
        card.pack(fill="x", padx=14, pady=10)

        top = tk.Frame(card, bg=ENTRY_BG)
        top.pack(fill="x", padx=12, pady=(10, 4))

        tk.Label(top, text=sender, bg=ENTRY_BG, fg=NAVY_TEXT, font=("Segoe UI", 11, "bold")).pack(side="left")

        tk.Label(card, text=subject, bg=ENTRY_BG, fg=NAVY_TEXT, font=("Segoe UI", 11)).pack(
            anchor="w", padx=12, pady=(0, 4)
        )

        tk.Label(
            card,
            text=snippet,
            bg=ENTRY_BG,
            fg=NAVY_MUTED,
            font=("Segoe UI", 10),
            wraplength=540,
            justify="left",
        ).pack(anchor="w", padx=12, pady=(0, 10))

        card.bind("<Button-1>", lambda _e: messagebox.showinfo("Message", f"{sender}\n\n{subject}\n\n{snippet}"))


if __name__ == "__main__":
    app = App()
    app.mainloop()
