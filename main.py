
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import keyboard
import pyautogui
import io
import base64
from PIL import Image, ImageTk
import requests
import json
import os
from datetime import datetime
import configparser

class Style:

    COLORS = {
        'bg_primary': '#fafafa',
        'bg_secondary': '#ffffff',
        'bg_tertiary': '#f5f5f7',
        'accent': '#007aff',
        'accent_hover': '#0051d5',
        'success': '#30d158',
        'warning': '#ff9f0a',
        'error': '#ff453a',
        'text_primary': '#1c1c1e',
        'text_secondary': '#3a3a3c',
        'text_tertiary': '#8e8e93',
        'border_light': '#e5e5e7',
        'border_medium': '#d1d1d6',
        'shadow': '#00000008',
    }

    FONTS = {
        'display': ('Segoe UI', 32, 'normal'),
        'title': ('Segoe UI', 22, 'bold'),
        'headline': ('Segoe UI', 17, 'bold'),
        'body': ('Segoe UI', 14, 'normal'),
        'caption': ('Segoe UI', 12, 'normal'),
        'mono': ('Consolas', 12, 'normal'),
    }

    SPACING = {
        'xs': 4,
        's': 8,
        'm': 16,
        'l': 24,
        'xl': 32,
        'xxl': 48,
    }

class ScreenshotAnalyzer:

    def __init__(self):
        self.config = self.load_config()
        self.screenshot_image = None
        self.setup_gui()
        self.setup_hotkey()

    def load_config(self):
        config = configparser.ConfigParser()
        config_path = 'config.ini'

        if os.path.exists(config_path):
            config.read(config_path)
        else:

            config['API'] = {
                'api_type': 'azure',
                'azure_api_key': 'your-azure-api-key-here',
                'azure_endpoint': 'your-azure-endpoint-here',
                'azure_api_version': '2024-02-15-preview',
                'azure_deployment_name': 'your-deployment-name-here',
                'openai_api_key': 'your-openai-api-key-here',
                'model': 'gpt-4-vision-preview'
            }
            config['SHORTCUTS'] = {
                'capture_hotkey': 'ctrl+shift+s'
            }
            config['UI'] = {
                'window_width': '1000',
                'window_height': '700'
            }
            config['ADVANCED'] = {
                'max_tokens': '1500',
                'timeout': '60'
            }

            with open(config_path, 'w') as configfile:
                config.write(configfile)

        return config

    def setup_gui(self):

        self.root = tk.Tk()
        self.root.title("Screenshot Analyzer")
        self.root.geometry(f"{self.config['UI']['window_width']}x{self.config['UI']['window_height']}")
        self.root.configure(bg=Style.COLORS['bg_primary'])
        self.root.minsize(900, 650)
        self.root.withdraw()

        self.setup_styles()

        self.create_main_layout()

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Primary.TButton',
                       background=Style.COLORS['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(24, 14),
                       font=Style.FONTS['body'])

        style.map('Primary.TButton',
                 background=[('active', Style.COLORS['accent_hover']),
                           ('pressed', Style.COLORS['accent_hover'])])

        style.configure('Success.TButton',
                       background=Style.COLORS['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(24, 14),
                       font=Style.FONTS['body'])

        style.configure('Secondary.TButton',
                       background=Style.COLORS['text_tertiary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12),
                       font=Style.FONTS['caption'])

    def create_main_layout(self):

        main_container = tk.Frame(self.root, bg=Style.COLORS['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=Style.SPACING['xl'], 
                           pady=Style.SPACING['xl'])

        self.create_header(main_container)

        content_frame = tk.Frame(main_container, bg=Style.COLORS['bg_primary'])
        content_frame.pack(fill='both', expand=True, pady=(Style.SPACING['xl'], 0))

        self.create_screenshot_section(content_frame)

        self.create_question_section(content_frame)

        self.create_action_section(content_frame)

        self.create_results_section(content_frame)

        self.create_status_section(main_container)

    def create_header(self, parent):

        header_frame = tk.Frame(parent, bg=Style.COLORS['bg_primary'])
        header_frame.pack(fill='x', pady=(0, Style.SPACING['xl']))

        title_label = tk.Label(header_frame,
                              text="Screenshot Analyzer",
                              font=Style.FONTS['display'],
                              fg=Style.COLORS['text_primary'],
                              bg=Style.COLORS['bg_primary'])
        title_label.pack(pady=(0, Style.SPACING['xs']))

        subtitle_label = tk.Label(header_frame,
                                 text="AI-powered visual analysis with beautiful, intuitive design",
                                 font=Style.FONTS['body'],
                                 fg=Style.COLORS['text_secondary'],
                                 bg=Style.COLORS['bg_primary'])
        subtitle_label.pack()

    def create_card_container(self, parent, title, subtitle=None):

        card_container = tk.Frame(parent, bg=Style.COLORS['bg_primary'])
        card_container.pack(fill='x', pady=(0, Style.SPACING['l']))

        card = tk.Frame(card_container,
                       bg=Style.COLORS['bg_secondary'],
                       relief='flat',
                       bd=1,
                       highlightbackground=Style.COLORS['border_light'],
                       highlightthickness=1)
        card.pack(fill='x')

        header_frame = tk.Frame(card, bg=Style.COLORS['bg_secondary'])
        header_frame.pack(fill='x', padx=Style.SPACING['l'], 
                         pady=(Style.SPACING['l'], Style.SPACING['m']))

        title_label = tk.Label(header_frame,
                              text=title,
                              font=Style.FONTS['headline'],
                              fg=Style.COLORS['text_primary'],
                              bg=Style.COLORS['bg_secondary'])
        title_label.pack(side='left')

        if subtitle:
            subtitle_label = tk.Label(header_frame,
                                     text=subtitle,
                                     font=Style.FONTS['caption'],
                                     fg=Style.COLORS['text_tertiary'],
                                     bg=Style.COLORS['bg_secondary'])
            subtitle_label.pack(side='right')

        return card

    def create_screenshot_section(self, parent):

        card = self.create_card_container(parent, "📸 Screenshot Preview", "⌃⇧S to capture")

        preview_frame = tk.Frame(card, bg=Style.COLORS['bg_secondary'])
        preview_frame.pack(fill='x', padx=Style.SPACING['l'], 
                          pady=(0, Style.SPACING['l']))

        image_frame = tk.Frame(preview_frame, 
                              bg=Style.COLORS['bg_tertiary'],
                              height=300,
                              relief='flat',
                              bd=1)
        image_frame.pack(fill='x', pady=Style.SPACING['m'])
        image_frame.pack_propagate(False)

        self.image_label = tk.Label(image_frame,
                                   text="📸\n\nNo screenshot captured yet\n\nPress ⌃⇧S to capture a screenshot",
                                   font=Style.FONTS['body'],
                                   fg=Style.COLORS['text_tertiary'],
                                   bg=Style.COLORS['bg_tertiary'],
                                   relief='flat',
                                   bd=0)
        self.image_label.pack(fill='both', expand=True)

    def create_question_section(self, parent):

        card = self.create_card_container(parent, "💭 Your Question", "⌃⏎ to analyze")

        input_frame = tk.Frame(card, bg=Style.COLORS['bg_secondary'])
        input_frame.pack(fill='x', padx=Style.SPACING['l'], 
                        pady=(0, Style.SPACING['l']))

        self.question_text = scrolledtext.ScrolledText(input_frame,
                                                      height=5,
                                                      font=Style.FONTS['body'],
                                                      bg=Style.COLORS['bg_tertiary'],
                                                      fg=Style.COLORS['text_primary'],
                                                      insertbackground=Style.COLORS['accent'],
                                                      selectbackground=Style.COLORS['accent'],
                                                      relief='flat',
                                                      bd=0,
                                                      wrap=tk.WORD)
        self.question_text.pack(fill='x', pady=Style.SPACING['m'])

        placeholder = 

        self.question_text.insert("1.0", placeholder)
        self.question_text.configure(fg=Style.COLORS['text_tertiary'])

        self.question_text.bind('<FocusIn>', self._on_question_focus_in)
        self.question_text.bind('<FocusOut>', self._on_question_focus_out)
        self.question_text.bind('<Control-Return>', lambda e: self.analyze_screenshot())

    def create_action_section(self, parent):

        button_frame = tk.Frame(parent, bg=Style.COLORS['bg_primary'])
        button_frame.pack(fill='x', pady=(0, Style.SPACING['l']))

        button_container = tk.Frame(button_frame, bg=Style.COLORS['bg_primary'])
        button_container.pack()

        self.capture_btn = ttk.Button(button_container,
                                     text="📸 Capture Screenshot",
                                     style='Primary.TButton',
                                     command=self.capture_screenshot)
        self.capture_btn.pack(side='left', padx=(0, Style.SPACING['m']))

        self.analyze_btn = ttk.Button(button_container,
                                     text="🔍 Analyze Screenshot",
                                     style='Success.TButton',
                                     command=self.analyze_screenshot)
        self.analyze_btn.pack(side='left', padx=(0, Style.SPACING['m']))
        self.analyze_btn.configure(state='disabled')

        clear_btn = ttk.Button(button_container,
                              text="Clear All",
                              style='Secondary.TButton',
                              command=self.clear_all)
        clear_btn.pack(side='left')

    def create_results_section(self, parent):

        card = self.create_card_container(parent, "🤖 AI Analysis", "Results appear here")

        results_frame = tk.Frame(card, bg=Style.COLORS['bg_secondary'])
        results_frame.pack(fill='both', expand=True, 
                          padx=Style.SPACING['l'], 
                          pady=(0, Style.SPACING['l']))

        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     font=Style.FONTS['body'],
                                                     bg=Style.COLORS['bg_tertiary'],
                                                     fg=Style.COLORS['text_primary'],
                                                     insertbackground=Style.COLORS['accent'],
                                                     selectbackground=Style.COLORS['accent'],
                                                     relief='flat',
                                                     bd=0,
                                                     wrap=tk.WORD)
        self.results_text.pack(fill='both', expand=True, pady=Style.SPACING['m'])

        welcome_msg = 

        self.results_text.insert("1.0", welcome_msg)

    def create_status_section(self, parent):

        status_frame = tk.Frame(parent, bg=Style.COLORS['bg_primary'])
        status_frame.pack(fill='x', pady=(Style.SPACING['xl'], 0))

        status_card = tk.Frame(status_frame,
                              bg=Style.COLORS['bg_secondary'],
                              relief='flat',
                              bd=1,
                              highlightbackground=Style.COLORS['border_light'],
                              highlightthickness=1)
        status_card.pack(fill='x')

        status_content = tk.Frame(status_card, bg=Style.COLORS['bg_secondary'])
        status_content.pack(fill='x', padx=Style.SPACING['l'], 
                           pady=Style.SPACING['m'])

        self.status_label = tk.Label(status_content,
                                    text="🟢 Ready • Press ⌃⇧S to capture screenshot",
                                    font=Style.FONTS['caption'],
                                    fg=Style.COLORS['text_secondary'],
                                    bg=Style.COLORS['bg_secondary'])
        self.status_label.pack(side='left')

        api_type = self.config['API'].get('api_type', 'openai')
        api_status = f"🔵 {api_type.title()} OpenAI Ready"
        api_label = tk.Label(status_content,
                            text=api_status,
                            font=Style.FONTS['caption'],
                            fg=Style.COLORS['success'],
                            bg=Style.COLORS['bg_secondary'])
        api_label.pack(side='right')

    def setup_hotkey(self):

        hotkey = self.config['SHORTCUTS']['capture_hotkey']
        try:
            keyboard.add_hotkey(hotkey, self.hotkey_capture)
            print(f"Global hotkey '{hotkey}' registered successfully")
        except Exception as e:
            print(f"Failed to register hotkey: {e}")

    def hotkey_capture(self):

        self.capture_screenshot()
        self.show_window()

    def show_window(self):

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        self.root.attributes('-topmost', False)

    def capture_screenshot(self):

        try:
            self.status_label.config(text="Capturing screenshot...")
            self.root.withdraw()

            self.root.after(100, self._do_capture)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot: {e}")
            self.status_label.config(text="Error capturing screenshot")

    def _do_capture(self):

        try:

            screenshot = pyautogui.screenshot()
            self.screenshot_image = screenshot

            thumbnail = screenshot.copy()

            original_width, original_height = thumbnail.size
            new_height = 290
            new_width = int((new_height * original_width) / original_height)
            thumbnail = thumbnail.resize((new_width, new_height), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(thumbnail)
            self.image_label.config(image=photo, text="", 
                                   bg=Style.COLORS['bg_secondary'],
                                   relief='flat',
                                   compound='center')
            self.image_label.image = photo

            self.analyze_btn.configure(state='normal')
            self.status_label.config(text="✅ Screenshot captured! Enter a question and click 'Analyze Screenshot'",
                                   fg=Style.COLORS['success'])

            self.question_text.focus_set()
            current_text = self.question_text.get("1.0", tk.END).strip()
            if current_text.startswith("Ask me anything about your screenshot..."):
                self.question_text.delete("1.0", tk.END)
                self.question_text.configure(fg=Style.COLORS['text_primary'])

            self.show_window()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot: {e}")
            self.status_label.config(text="❌ Error capturing screenshot",
                                   fg=Style.COLORS['error'])
            self.show_window()

    def analyze_screenshot(self):

        if not self.screenshot_image:
            messagebox.showwarning("Warning", "Please capture a screenshot first")
            return

        question = self.question_text.get("1.0", tk.END).strip()
        if not question or question.startswith("Ask me anything about your screenshot..."):
            messagebox.showwarning("Warning", "Please enter a question about the screenshot")
            self.question_text.focus_set()

            if question.startswith("Ask me anything about your screenshot..."):
                self.question_text.delete("1.0", tk.END)
                self.question_text.configure(fg=Style.COLORS['text_primary'])
            return

        self.analyze_btn.configure(state='disabled', text="🔄 Analyzing...")
        self.status_label.config(text="🤖 AI is analyzing your screenshot...",
                               fg=Style.COLORS['warning'])

        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", "🔄 Processing your request...\n\nPlease wait while our AI analyzes the screenshot and generates insights.")
        self.results_text.configure(fg=Style.COLORS['text_secondary'])

        threading.Thread(target=self._analyze_thread, args=(question,), daemon=True).start()

    def _analyze_thread(self, question):

        try:
            self.root.after(0, lambda: self.status_label.config(text="Analyzing image..."))
            self.root.after(0, lambda: self.results_text.delete("1.0", tk.END))

            img_buffer = io.BytesIO()
            self.screenshot_image.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

            api_type = self.config['API'].get('api_type', 'openai').lower()

            if api_type == 'azure':

                azure_api_key = self.config['API'].get('azure_api_key', '')
                azure_endpoint = self.config['API'].get('azure_endpoint', '')
                azure_api_version = self.config['API'].get('azure_api_version', '2024-02-15-preview')
                azure_deployment = self.config['API'].get('azure_deployment_name', '')

                if azure_api_key == 'your-azure-api-key-here' or not azure_api_key:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                        "Please set your Azure OpenAI API key in config.ini"))
                    return

                if azure_endpoint == 'your-azure-endpoint-here' or not azure_endpoint:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                        "Please set your Azure OpenAI endpoint in config.ini"))
                    return

                if azure_deployment == 'your-deployment-name-here' or not azure_deployment:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                        "Please set your Azure OpenAI deployment name in config.ini"))
                    return

                azure_endpoint = azure_endpoint.rstrip('/')
                url = f"{azure_endpoint}/openai/deployments/{azure_deployment}/chat/completions?api-version={azure_api_version}"

                headers = {
                    "Content-Type": "application/json",
                    "api-key": azure_api_key
                }

                payload = {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Analyze this screenshot and answer the question: {question}\n\nPlease provide a detailed explanation with specific observations about what you see in the image."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": int(self.config['ADVANCED'].get('max_tokens', 1000))
                }

            else:

                api_key = self.config['API'].get('openai_api_key', '')
                if api_key == 'your-openai-api-key-here' or not api_key:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                        "Please set your OpenAI API key in config.ini"))
                    return

                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }

                payload = {
                    "model": self.config['API'].get('model', 'gpt-4-vision-preview'),
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Analyze this screenshot and answer the question: {question}\n\nPlease provide a detailed explanation with specific observations about what you see in the image."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": int(self.config['ADVANCED'].get('max_tokens', 1000))
                }

            timeout = int(self.config['ADVANCED'].get('timeout', 30))
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)

            if response.status_code == 200:
                result = response.json()
                analysis = result['choices'][0]['message']['content']

                self.root.after(0, lambda: self._display_result(analysis))
            else:
                error_msg = f"API Error ({api_type.upper()}): {response.status_code} - {response.text}"
                self.root.after(0, lambda: self._display_error(error_msg))

        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self._display_error(error_msg))

    def _display_result(self, analysis):

        self.results_text.delete("1.0", tk.END)

        self._configure_text_tags()

        question_text = self.question_text.get('1.0', tk.END).strip()

        self.results_text.insert("1.0", "✅ Analysis Complete\n\n", "success_header")

        self.results_text.insert(tk.END, "💭 Your Question:\n", "section_header")
        self.results_text.insert(tk.END, "━" * 70 + "\n", "separator")
        self.results_text.insert(tk.END, f"{question_text}\n\n", "question_text")

        self.results_text.insert(tk.END, "🤖 AI Analysis:\n", "section_header")
        self.results_text.insert(tk.END, "━" * 70 + "\n\n", "separator")

        self._insert_formatted_analysis(analysis)

        self.results_text.insert(tk.END, "\n" + "━" * 70 + "\n\n", "separator")
        self.results_text.insert(tk.END, "💾 Result automatically saved with timestamp\n", "footer")
        self.results_text.insert(tk.END, "✨ Ready for your next question or screenshot!", "footer")

        self.status_label.config(text="✅ Analysis complete! Ready for next screenshot or question.",
                               fg=Style.COLORS['success'])

        self.analyze_btn.configure(state='normal', text="🔍 Analyze Screenshot")

        self._save_result(analysis)

    def _configure_text_tags(self):

        self.results_text.tag_configure("success_header", 
                                       foreground=Style.COLORS['success'],
                                       font=Style.FONTS['headline'])

        self.results_text.tag_configure("section_header", 
                                       foreground=Style.COLORS['text_primary'],
                                       font=Style.FONTS['headline'])

        self.results_text.tag_configure("separator", 
                                       foreground=Style.COLORS['text_tertiary'],
                                       font=Style.FONTS['caption'])

        self.results_text.tag_configure("question_text", 
                                       foreground=Style.COLORS['accent'],
                                       font=Style.FONTS['body'])

        self.results_text.tag_configure("analysis_header", 
                                       foreground=Style.COLORS['accent'],
                                       font=Style.FONTS['headline'])

        self.results_text.tag_configure("analysis_subheader", 
                                       foreground=Style.COLORS['text_primary'],
                                       font=('Segoe UI', 15, 'bold'))

        self.results_text.tag_configure("analysis_text", 
                                       foreground=Style.COLORS['text_primary'],
                                       font=Style.FONTS['body'])

        self.results_text.tag_configure("bullet_point", 
                                       foreground=Style.COLORS['text_secondary'],
                                       font=Style.FONTS['body'],
                                       lmargin1=20, lmargin2=40)

        self.results_text.tag_configure("footer", 
                                       foreground=Style.COLORS['text_secondary'],
                                       font=Style.FONTS['caption'])

    def _insert_formatted_analysis(self, analysis):

        lines = analysis.split('\n')
        current_line = ""

        for line in lines:
            line = line.strip()

            if not line:
                if current_line:
                    self._insert_formatted_line(current_line)
                    current_line = ""
                self.results_text.insert(tk.END, "\n")
                continue

            if line.startswith('📌') or line.startswith('🔸'):
                if current_line:
                    self._insert_formatted_line(current_line)
                    current_line = ""

                header_text = line[2:].strip() if len(line) > 2 else line
                self.results_text.insert(tk.END, f"� {header_text}\n", "analysis_subheader")
                continue

            if line.startswith('**') and line.endswith('**'):
                if current_line:
                    self._insert_formatted_line(current_line)
                    current_line = ""

                header_text = line[2:-2].strip()
                self.results_text.insert(tk.END, f"{header_text}\n", "analysis_subheader")
                continue

            if line.startswith('-') or line.startswith('•'):
                if current_line:
                    self._insert_formatted_line(current_line)
                    current_line = ""

                bullet_text = line[1:].strip() if len(line) > 1 else line
                self.results_text.insert(tk.END, f"  • {bullet_text}\n", "bullet_point")
                continue

            if current_line:
                current_line += " " + line
            else:
                current_line = line

        if current_line:
            self._insert_formatted_line(current_line)

    def _insert_formatted_line(self, line):

        parts = line.split('**')
        for i, part in enumerate(parts):
            if i % 2 == 0:

                self.results_text.insert(tk.END, part, "analysis_text")
            else:

                self.results_text.insert(tk.END, part, "analysis_subheader")
        self.results_text.insert(tk.END, "\n")

    def _display_error(self, error):

        self.results_text.delete("1.0", tk.END)

        error_message = f

        self.results_text.insert("1.0", error_message)
        self.results_text.configure(fg=Style.COLORS['error'])

        self.status_label.config(text="❌ Analysis failed. Please check configuration and try again.",
                               fg=Style.COLORS['error'])

        self.analyze_btn.configure(state='normal', text="🔍 Analyze Screenshot")

    def _save_result(self, analysis):

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Question: {self.question_text.get('1.0', tk.END).strip()}\n")
                f.write(f"Analysis:\n{analysis}\n")

            print(f"Analysis saved to {filename}")
        except Exception as e:
            print(f"Failed to save analysis: {e}")

    def clear_all(self):

        self.question_text.delete("1.0", tk.END)
        placeholder_text = 
        self.question_text.insert("1.0", placeholder_text)
        self.question_text.configure(fg=Style.COLORS['text_tertiary'])

        self.results_text.delete("1.0", tk.END)
        welcome_msg = 
        self.results_text.insert("1.0", welcome_msg)
        self.results_text.configure(fg=Style.COLORS['text_secondary'])

        self.image_label.config(image="", 
                               text="📸\n\nNo screenshot captured yet\n\nPress ⌃⇧S to capture a screenshot",
                               fg=Style.COLORS['text_tertiary'],
                               bg=Style.COLORS['bg_tertiary'],
                               relief='flat',
                               bd=0)
        self.image_label.image = None
        self.screenshot_image = None

        self.analyze_btn.configure(state='disabled', text="🔍 Analyze Screenshot")

        self.status_label.config(text="🟢 Ready • Press ⌃⇧S to capture screenshot",
                               fg=Style.COLORS['text_secondary'])

    def run(self):

        print("Screenshot Analyzer started")
        print(f"Global hotkey: {self.config['SHORTCUTS']['capture_hotkey']}")
        print("Window will appear when hotkey is pressed or you can show it manually")

        self.root.mainloop()

    def _on_question_focus_in(self, event):

        current_text = self.question_text.get("1.0", tk.END).strip()
        if current_text.startswith("Ask me anything about your screenshot..."):
            self.question_text.delete("1.0", tk.END)
            self.question_text.configure(fg=Style.COLORS['text_primary'])

    def _on_question_focus_out(self, event):

        if not self.question_text.get("1.0", tk.END).strip():
            placeholder_text = 
            self.question_text.insert("1.0", placeholder_text)
            self.question_text.configure(fg=Style.COLORS['text_tertiary'])

def main():

    try:
        app = ScreenshotAnalyzer()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()