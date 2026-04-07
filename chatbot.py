import customtkinter as ctk
import google.generativeai as genai
import json
import os
import sys
from tkinter import filedialog
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_TITLE = "Naavya AI - Smart Glass UI V2"
WINDOW_SIZE = "1280x760"

# -------------------------
# PUT YOUR GEMINI API KEY HERE
# -------------------------
API_KEY = "AIzaSyCwuvpqvNCazepZDynjp73vC7m-WhIWouM"

# -------------------------
# EXE-SAFE FILE PATH
# -------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHAT_FILE = os.path.join(BASE_DIR, "chats.json")

# -------------------------
# COLORS
# -------------------------
BG_MAIN = "#0d0718"
BG_SIDEBAR = "#120a22"
BG_TOP = "#171028"
BG_CHAT = "#140d24"
BG_INPUT = "#171028"

BORDER = "#3b2a5c"
BOT_BUBBLE = "#2b2142"
USER_BUBBLE = "#a883ff"
BTN = "#a883ff"
BTN_HOVER = "#956fff"
BTN_DARK = "#241b38"
BTN_DARK_HOVER = "#30224a"

TEXT_MAIN = "#f7f2ff"
TEXT_SOFT = "#cfc1ec"
TEXT_DARK = "#1b1230"
ACCENT = "#d1005d"

# =========================================================
# GEMINI SETUP
# =========================================================
gemini_available = False
model = None

try:
    if API_KEY and API_KEY != "PASTE_YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        gemini_available = True
except Exception:
    gemini_available = False


# =========================================================
# APP
# =========================================================
class NaavyaAI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(1100, 680)
        self.configure(fg_color=BG_MAIN)

        self.chat_history = self.load_chats()
        self.current_theme = "Dark"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main_area()

        if self.chat_history:
            self.show_saved_chats()
        else:
            self.add_bot_message("Heyy, I’m Naavya AI 💜\nYour smart lavender chatbot is ready.")

    # =====================================================
    # FILE STORAGE
    # =====================================================
    def load_chats(self):
        if os.path.exists(CHAT_FILE):
            try:
                with open(CHAT_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception:
                return []
        return []

    def save_all_chats(self):
        try:
            with open(CHAT_FILE, "w", encoding="utf-8") as f:
                json.dump(self.chat_history, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def save_chat(self, user_text, bot_text):
        self.chat_history.append({
            "timestamp": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "user": user_text,
            "bot": bot_text
        })
        self.save_all_chats()

    def show_saved_chats(self):
        for item in self.chat_history:
            user_msg = item.get("user", "")
            bot_msg = item.get("bot", "")
            if user_msg:
                self.add_user_message(user_msg, scroll=False)
            if bot_msg:
                self.add_bot_message(bot_msg, scroll=False)
        self.after(100, self.scroll_to_bottom)

    # =====================================================
    # UI
    # =====================================================
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=280,
            fg_color=BG_SIDEBAR,
            corner_radius=0,
            border_width=1,
            border_color=BORDER
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.sidebar.grid_rowconfigure(6, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="Naavya AI",
            font=("Segoe UI", 30, "bold"),
            text_color=TEXT_MAIN
        )
        self.logo.pack(anchor="w", padx=22, pady=(28, 4))

        self.sub_logo = ctk.CTkLabel(
            self.sidebar,
            text="smart chats",
            font=("Segoe UI", 18),
            text_color=TEXT_SOFT
        )
        self.sub_logo.pack(anchor="w", padx=22, pady=(0, 20))

        self.new_chat_btn = ctk.CTkButton(
            self.sidebar,
            text="+ New Chat",
            height=58,
            corner_radius=0,
            fg_color=BTN,
            hover_color=BTN_HOVER,
            text_color=TEXT_MAIN,
            font=("Segoe UI", 18, "bold"),
            command=self.clear_chat
        )
        self.new_chat_btn.pack(fill="x", padx=18, pady=(0, 18))

        self.chat_preview = ctk.CTkLabel(
            self.sidebar,
            text="hii",
            anchor="w",
            height=44,
            fg_color="#2a1d47",
            corner_radius=0,
            text_color=TEXT_MAIN,
            font=("Segoe UI", 14)
        )
        self.chat_preview.pack(fill="x", padx=14, pady=(8, 0))

    def build_main_area(self):
        self.main = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # Top header
        self.top = ctk.CTkFrame(
            self.main,
            fg_color=BG_TOP,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
            height=110
        )
        self.top.grid(row=0, column=0, sticky="ew", padx=22, pady=(22, 18))
        self.top.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.top,
            text="Naavya AI",
            font=("Segoe UI", 34, "bold"),
            text_color=TEXT_MAIN
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=28, pady=(18, 0))

        self.subtitle_label = ctk.CTkLabel(
            self.top,
            text="current chat: hii",
            font=("Segoe UI", 18),
            text_color=TEXT_SOFT
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", padx=28, pady=(0, 18))

        self.button_frame = ctk.CTkFrame(self.top, fg_color="transparent")
        self.button_frame.grid(row=0, column=1, rowspan=2, sticky="e", padx=18)

        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            width=100,
            height=48,
            fg_color=BTN_DARK,
            hover_color=BTN_DARK_HOVER,
            text_color=TEXT_MAIN,
            corner_radius=0,
            font=("Segoe UI", 16, "bold"),
            command=self.clear_chat
        )
        self.clear_btn.pack(side="left", padx=8, pady=24)

        self.export_btn = ctk.CTkButton(
            self.button_frame,
            text="Export",
            width=100,
            height=48,
            fg_color=BTN_DARK,
            hover_color=BTN_DARK_HOVER,
            text_color=TEXT_MAIN,
            corner_radius=0,
            font=("Segoe UI", 16, "bold"),
            command=self.export_chat
        )
        self.export_btn.pack(side="left", padx=8, pady=24)

        self.theme_btn = ctk.CTkButton(
            self.button_frame,
            text="Theme",
            width=100,
            height=48,
            fg_color=BTN_DARK,
            hover_color=BTN_DARK_HOVER,
            text_color=TEXT_MAIN,
            corner_radius=0,
            font=("Segoe UI", 16, "bold"),
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="left", padx=8, pady=24)

        # Chat section
        self.chat_outer = ctk.CTkFrame(
            self.main,
            fg_color=BG_CHAT,
            corner_radius=0,
            border_width=1,
            border_color=BORDER
        )
        self.chat_outer.grid(row=1, column=0, sticky="nsew", padx=22, pady=(0, 18))
        self.chat_outer.grid_rowconfigure(1, weight=1)
        self.chat_outer.grid_columnconfigure(0, weight=1)

        self.date_label = ctk.CTkLabel(
            self.chat_outer,
            text=f"Today is {datetime.now().strftime('%d %B %Y')}",
            fg_color="#2a2142",
            text_color=TEXT_MAIN,
            font=("Segoe UI", 16),
            padx=18,
            pady=8
        )
        self.date_label.grid(row=0, column=0, sticky="w", padx=18, pady=(10, 6))

        self.chat_box = ctk.CTkScrollableFrame(
            self.chat_outer,
            fg_color=BG_CHAT,
            corner_radius=0
        )
        self.chat_box.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 10))

        # Input section
        self.input_frame = ctk.CTkFrame(
            self.main,
            fg_color=BG_INPUT,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
            height=110
        )
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=22, pady=(0, 22))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.input_frame,
            height=58,
            fg_color="#1e1630",
            border_color=BORDER,
            border_width=1,
            corner_radius=0,
            text_color=TEXT_MAIN,
            font=("Segoe UI", 18),
            placeholder_text="Type your message here..."
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(18, 12), pady=18)
        self.entry.bind("<Return>", self.send_message)

        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=110,
            height=58,
            fg_color=BTN,
            hover_color=BTN_HOVER,
            text_color=TEXT_MAIN,
            corner_radius=0,
            font=("Segoe UI", 18, "bold"),
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 18), pady=18)

    # =====================================================
    # CHAT BUBBLES
    # =====================================================
    def add_user_message(self, message, scroll=True):
        wrapper = ctk.CTkFrame(self.chat_box, fg_color="transparent")
        wrapper.pack(fill="x", pady=(10, 4), padx=8)

        name = ctk.CTkLabel(
            wrapper,
            text="You",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_SOFT
        )
        name.pack(anchor="e", padx=10, pady=(0, 4))

        bubble = ctk.CTkLabel(
            wrapper,
            text=message,
            justify="left",
            wraplength=520,
            font=("Segoe UI", 16),
            text_color=TEXT_MAIN,
            fg_color=USER_BUBBLE,
            corner_radius=0,
            padx=18,
            pady=14
        )
        bubble.pack(anchor="e", padx=10)

        if scroll:
            self.after(50, self.scroll_to_bottom)

    def add_bot_message(self, message, scroll=True):
        wrapper = ctk.CTkFrame(self.chat_box, fg_color="transparent")
        wrapper.pack(fill="x", pady=(10, 4), padx=8)

        name = ctk.CTkLabel(
            wrapper,
            text="Naavya AI",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_SOFT
        )
        name.pack(anchor="w", padx=10, pady=(0, 4))

        bubble = ctk.CTkLabel(
            wrapper,
            text=message,
            justify="left",
            wraplength=700,
            font=("Segoe UI", 16),
            text_color=TEXT_MAIN,
            fg_color=BOT_BUBBLE,
            corner_radius=0,
            padx=18,
            pady=14
        )
        bubble.pack(anchor="w", padx=10)

        if scroll:
            self.after(50, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        try:
            self.chat_box._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    # =====================================================
    # BOT LOGIC
    # =====================================================
    def get_fallback_reply(self, user_text):
        text = user_text.lower().strip()

        if any(word in text for word in ["hi", "hello", "hey", "hii"]):
            return "Heyy 💜 I’m here. What do you want to talk about?"

        if "joke" in text:
            return "I told my laptop I needed a break, now it keeps sleeping."

        if "quote" in text:
            return "Small progress is still progress."

        if "your name" in text or "who are you" in text:
            return "I’m Naavya AI — your lavender chatbot bestie."

        if "time" in text:
            return f"It’s {datetime.now().strftime('%I:%M %p')} right now."

        if "date" in text or "day" in text:
            return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

        return "I’m here with you 💜 Gemini is unavailable right now, but I can still chat."

    def get_bot_reply(self, user_text):
        if gemini_available and model is not None:
            try:
                prompt = (
                    "You are Naavya AI, a warm, stylish, helpful assistant with a calm premium tone. "
                    "Keep answers clear, friendly, and useful.\n\n"
                    f"User: {user_text}"
                )
                response = model.generate_content(prompt)
                text = getattr(response, "text", "").strip()
                if text:
                    return text
                return "I couldn’t generate a proper response just now."
            except Exception:
                return self.get_fallback_reply(user_text)
        return self.get_fallback_reply(user_text)

    # =====================================================
    # BUTTON ACTIONS
    # =====================================================
    def send_message(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.add_user_message(user_text)
        self.entry.delete(0, "end")
        self.chat_preview.configure(text=user_text[:30])
        self.subtitle_label.configure(text=f"current chat: {user_text[:40]}")

        self.update_idletasks()

        bot_reply = self.get_bot_reply(user_text)
        self.add_bot_message(bot_reply)
        self.save_chat(user_text, bot_reply)

    def clear_chat(self):
        for widget in self.chat_box.winfo_children():
            widget.destroy()

        self.chat_history = []
        self.save_all_chats()
        self.chat_preview.configure(text="new chat")
        self.subtitle_label.configure(text="current chat: new chat")
        self.add_bot_message("New chat started 💜")

    def export_chat(self):
        if not self.chat_history:
            self.add_bot_message("There’s no chat to export yet.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Chat As"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Naavya AI Chat Export\n")
                f.write("=" * 50 + "\n\n")
                for item in self.chat_history:
                    f.write(f"[{item.get('timestamp', '')}]\n")
                    f.write(f"You: {item.get('user', '')}\n")
                    f.write(f"Naavya AI: {item.get('bot', '')}\n")
                    f.write("\n" + "-" * 50 + "\n\n")
            self.add_bot_message("Chat exported successfully 💜")
        except Exception as e:
            self.add_bot_message(f"Couldn’t export chat: {e}")

    def toggle_theme(self):
        if self.current_theme == "Dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "Light"
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "Dark"


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    app = NaavyaAI()
    app.mainloop()