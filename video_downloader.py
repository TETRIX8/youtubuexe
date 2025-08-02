#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os
import sys
import time

class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.splash = tk.Toplevel()
        self.splash.title("")
        self.splash.geometry("400x300")
        self.splash.resizable(False, False)
        self.splash.configure(bg='#1a1a2e')
        
        # Убираем рамку окна
        self.splash.overrideredirect(True)
        
        # Центрируем окно
        self.center_window()
        
        # Создаем содержимое заставки
        self.create_splash_content()
        
        # Запускаем таймер
        self.splash.after(2000, self.close_splash)
        
    def center_window(self):
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.splash.winfo_screenheight() // 2) - (300 // 2)
        self.splash.geometry(f"400x300+{x}+{y}")
        
    def create_splash_content(self):
        # Главный фрейм с градиентом
        main_frame = tk.Frame(self.splash, bg='#1a1a2e', width=400, height=300)
        main_frame.pack(fill='both', expand=True)
        main_frame.pack_propagate(False)
        
        # Заголовок
        title_label = tk.Label(
            main_frame,
            text="A-K PROJECT",
            font=("Arial", 28, "bold"),
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        title_label.place(relx=0.5, rely=0.4, anchor='center')
        
        # Подзаголовок
        subtitle_label = tk.Label(
            main_frame,
            text="Video Downloader",
            font=("Arial", 14),
            fg='#ffffff',
            bg='#1a1a2e'
        )
        subtitle_label.place(relx=0.5, rely=0.55, anchor='center')
        
        # Прогресс бар (анимация)
        self.progress_frame = tk.Frame(main_frame, bg='#1a1a2e')
        self.progress_frame.place(relx=0.5, rely=0.75, anchor='center')
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=200,
            mode='indeterminate',
            style='Splash.Horizontal.TProgressbar'
        )
        self.progress_bar.pack()
        self.progress_bar.start(10)
        
        # Настройка стиля прогресс бара
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Splash.Horizontal.TProgressbar',
            background='#00d4ff',
            troughcolor='#16213e',
            borderwidth=0,
            lightcolor='#00d4ff',
            darkcolor='#00d4ff'
        )
        
    def close_splash(self):
        self.progress_bar.stop()
        self.splash.destroy()
        self.parent.deiconify()

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("A-K Video Downloader")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.configure(bg='#1a1a2e')
        
        # Скрываем главное окно для показа заставки
        self.root.withdraw()
        
        # Показываем заставку
        self.splash = SplashScreen(self.root)
        
        # Переменные
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar()
        self.save_path_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Готов к работе")
        
        # Список доступных качеств
        self.available_formats = []
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка цветов для различных элементов
        style.configure('Title.TLabel', 
                       foreground='#00d4ff', 
                       background='#1a1a2e', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       foreground='#ffffff', 
                       background='#1a1a2e', 
                       font=('Arial', 10))
        
        style.configure('Custom.TEntry',
                       fieldbackground='#16213e',
                       foreground='#ffffff',
                       bordercolor='#00d4ff',
                       insertcolor='#ffffff')
        
        style.configure('Custom.TButton',
                       background='#00d4ff',
                       foreground='#1a1a2e',
                       bordercolor='#00d4ff',
                       focuscolor='none',
                       font=('Arial', 10, 'bold'))
        
        style.map('Custom.TButton',
                 background=[('active', '#0099cc'),
                           ('pressed', '#007399')])
        
        style.configure('Custom.TCombobox',
                       fieldbackground='#16213e',
                       foreground='#ffffff',
                       bordercolor='#00d4ff',
                       arrowcolor='#00d4ff')
        
        style.configure('Custom.Horizontal.TProgressbar',
                       background='#00d4ff',
                       troughcolor='#16213e',
                       borderwidth=1,
                       lightcolor='#00d4ff',
                       darkcolor='#00d4ff')
        
        style.configure('Custom.TLabelFrame',
                       background='#1a1a2e',
                       foreground='#ffffff',
                       bordercolor='#00d4ff')
        
        style.configure('Custom.TLabelFrame.Label',
                       background='#1a1a2e',
                       foreground='#00d4ff',
                       font=('Arial', 10, 'bold'))
        
    def create_widgets(self):
        # Главный контейнер
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Заголовок приложения
        title_frame = tk.Frame(main_container, bg='#1a1a2e')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🎬 A-K Video Downloader",
            font=('Arial', 20, 'bold'),
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Скачивайте видео в высоком качестве",
            font=('Arial', 12),
            fg='#ffffff',
            bg='#1a1a2e'
        )
        subtitle_label.pack()
        
        # Основная рабочая область
        work_frame = tk.Frame(main_container, bg='#16213e', relief='raised', bd=2)
        work_frame.pack(fill='both', expand=True, pady=10)
        
        # Внутренний отступ
        inner_frame = tk.Frame(work_frame, bg='#16213e')
        inner_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # URL секция
        url_section = tk.Frame(inner_frame, bg='#16213e')
        url_section.pack(fill='x', pady=(0, 15))
        
        url_label = tk.Label(
            url_section,
            text="🔗 URL видео:",
            font=('Arial', 12, 'bold'),
            fg='#00d4ff',
            bg='#16213e'
        )
        url_label.pack(anchor='w')
        
        url_input_frame = tk.Frame(url_section, bg='#16213e')
        url_input_frame.pack(fill='x', pady=(5, 0))
        
        self.url_entry = tk.Entry(
            url_input_frame,
            textvariable=self.url_var,
            font=('Arial', 11),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=5
        )
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        get_info_btn = tk.Button(
            url_input_frame,
            text="📋 Получить качества",
            command=self.get_video_info,
            bg='#00d4ff',
            fg='#1a1a2e',
            font=('Arial', 10, 'bold'),
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        get_info_btn.pack(side='right')
        
        # Качество секция
        quality_section = tk.Frame(inner_frame, bg='#16213e')
        quality_section.pack(fill='x', pady=(0, 15))
        
        quality_label = tk.Label(
            quality_section,
            text="⚙️ Качество видео:",
            font=('Arial', 12, 'bold'),
            fg='#00d4ff',
            bg='#16213e'
        )
        quality_label.pack(anchor='w')
        
        self.quality_combo = ttk.Combobox(
            quality_section,
            textvariable=self.quality_var,
            state="readonly",
            font=('Arial', 11),
            style='Custom.TCombobox'
        )
        self.quality_combo.pack(fill='x', pady=(5, 0))
        
        # Путь сохранения секция
        path_section = tk.Frame(inner_frame, bg='#16213e')
        path_section.pack(fill='x', pady=(0, 15))
        
        path_label = tk.Label(
            path_section,
            text="📁 Путь сохранения:",
            font=('Arial', 12, 'bold'),
            fg='#00d4ff',
            bg='#16213e'
        )
        path_label.pack(anchor='w')
        
        path_input_frame = tk.Frame(path_section, bg='#16213e')
        path_input_frame.pack(fill='x', pady=(5, 0))
        
        self.path_entry = tk.Entry(
            path_input_frame,
            textvariable=self.save_path_var,
            font=('Arial', 11),
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=5
        )
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            path_input_frame,
            text="📂 Обзор",
            command=self.browse_folder,
            bg='#00d4ff',
            fg='#1a1a2e',
            font=('Arial', 10, 'bold'),
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        browse_btn.pack(side='right')
        
        # Прогресс секция
        progress_section = tk.Frame(inner_frame, bg='#16213e')
        progress_section.pack(fill='x', pady=(0, 15))
        
        progress_label = tk.Label(
            progress_section,
            text="📊 Прогресс:",
            font=('Arial', 12, 'bold'),
            fg='#00d4ff',
            bg='#16213e'
        )
        progress_label.pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(
            progress_section,
            variable=self.progress_var,
            maximum=100,
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill='x', pady=(5, 0))
        
        # Кнопка скачивания
        download_frame = tk.Frame(inner_frame, bg='#16213e')
        download_frame.pack(fill='x', pady=15)
        
        self.download_btn = tk.Button(
            download_frame,
            text="⬇️ СКАЧАТЬ ВИДЕО",
            command=self.start_download,
            bg='#00d4ff',
            fg='#1a1a2e',
            font=('Arial', 14, 'bold'),
            relief='flat',
            bd=0,
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.download_btn.pack()
        
        # Статус и лог
        status_frame = tk.Frame(inner_frame, bg='#16213e')
        status_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        status_label = tk.Label(
            status_frame,
            text="📝 Статус:",
            font=('Arial', 12, 'bold'),
            fg='#00d4ff',
            bg='#16213e'
        )
        status_label.pack(anchor='w')
        
        self.status_display = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Arial', 10),
            fg='#ffffff',
            bg='#16213e',
            anchor='w'
        )
        self.status_display.pack(fill='x', pady=(5, 10))
        
        # Лог
        log_label = tk.Label(
            status_frame,
            text="📋 Лог операций:",
            font=('Arial', 12, 'bold'),
            fg='#00d4ff',
            bg='#16213e'
        )
        log_label.pack(anchor='w')
        
        log_frame = tk.Frame(status_frame, bg='#1a1a2e', relief='sunken', bd=2)
        log_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.log_text = tk.Text(
            log_frame,
            height=6,
            wrap=tk.WORD,
            bg='#1a1a2e',
            fg='#ffffff',
            insertbackground='#ffffff',
            font=('Consolas', 9),
            relief='flat',
            bd=5
        )
        
        scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Добавляем эффекты при наведении на кнопки
        self.add_hover_effects()
        
    def add_hover_effects(self):
        def on_enter(event, widget, color):
            widget.configure(bg=color)
            
        def on_leave(event, widget, color):
            widget.configure(bg=color)
            
        # Находим все кнопки и добавляем эффекты
        for widget in self.root.winfo_children():
            self.add_hover_to_buttons(widget)
            
    def add_hover_to_buttons(self, widget):
        if isinstance(widget, tk.Button):
            original_color = widget.cget('bg')
            hover_color = '#0099cc' if original_color == '#00d4ff' else original_color
            
            widget.bind('<Enter>', lambda e, w=widget, c=hover_color: w.configure(bg=c))
            widget.bind('<Leave>', lambda e, w=widget, c=original_color: w.configure(bg=c))
            
        for child in widget.winfo_children():
            self.add_hover_to_buttons(child)
        
    def log_message(self, message):
        """Добавить сообщение в лог"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def get_video_info(self):
        """Получить информацию о видео и доступных качествах"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Ошибка", "Введите URL видео")
            return
            
        self.status_var.set("🔍 Получение информации о видео...")
        self.log_message(f"Получение информации для: {url}")
        
        def fetch_info():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    # Получаем доступные форматы
                    formats = info.get('formats', [])
                    self.available_formats = []
                    
                    # Фильтруем и сортируем форматы
                    video_formats = []
                    for f in formats:
                        if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                            height = f.get('height', 0)
                            if height:
                                quality_str = f"{height}p"
                                if f.get('fps'):
                                    quality_str += f" {f['fps']}fps"
                                if f.get('ext'):
                                    quality_str += f" ({f['ext']})"
                                
                                video_formats.append({
                                    'format_id': f['format_id'],
                                    'quality': quality_str,
                                    'height': height,
                                    'filesize': f.get('filesize', 0)
                                })
                    
                    # Сортируем по качеству (по убыванию)
                    video_formats.sort(key=lambda x: x['height'], reverse=True)
                    
                    # Добавляем опцию "Лучшее качество"
                    self.available_formats = [{'format_id': 'best', 'quality': '🏆 Лучшее качество'}]
                    self.available_formats.extend(video_formats)
                    
                    # Обновляем комбобокс
                    quality_options = [f['quality'] for f in self.available_formats]
                    self.quality_combo['values'] = quality_options
                    if quality_options:
                        self.quality_combo.current(0)
                    
                    self.status_var.set("✅ Информация получена")
                    self.log_message(f"✅ Найдено {len(video_formats)} качеств видео")
                    self.log_message(f"📺 Название: {info.get('title', 'Неизвестно')}")
                    
            except Exception as e:
                self.status_var.set("❌ Ошибка получения информации")
                self.log_message(f"❌ Ошибка: {str(e)}")
                messagebox.showerror("Ошибка", f"Не удалось получить информацию о видео:\n{str(e)}")
        
        # Запускаем в отдельном потоке
        threading.Thread(target=fetch_info, daemon=True).start()
        
    def browse_folder(self):
        """Выбрать папку для сохранения"""
        folder = filedialog.askdirectory(initialdir=self.save_path_var.get())
        if folder:
            self.save_path_var.set(folder)
            self.log_message(f"📁 Выбрана папка: {folder}")
            
    def progress_hook(self, d):
        """Обновление прогресса скачивания"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                self.status_var.set(f"⬇️ Скачивание... {percent:.1f}%")
            elif '_percent_str' in d:
                percent_str = d['_percent_str'].strip('%')
                try:
                    percent = float(percent_str)
                    self.progress_var.set(percent)
                    self.status_var.set(f"⬇️ Скачивание... {percent:.1f}%")
                except:
                    pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_var.set("🎉 Скачивание завершено")
            self.log_message(f"💾 Файл сохранен: {d['filename']}")
            
    def start_download(self):
        """Начать скачивание видео"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Ошибка", "Введите URL видео")
            return
            
        if not self.available_formats:
            messagebox.showerror("Ошибка", "Сначала получите информацию о видео")
            return
            
        save_path = self.save_path_var.get().strip()
        if not save_path or not os.path.exists(save_path):
            messagebox.showerror("Ошибка", "Выберите корректный путь для сохранения")
            return
            
        # Получаем выбранный формат
        selected_quality = self.quality_var.get()
        format_id = 'best'
        for fmt in self.available_formats:
            if fmt['quality'] == selected_quality:
                format_id = fmt['format_id']
                break
                
        self.download_btn.config(state='disabled', text="⏳ Скачивание...")
        self.progress_var.set(0)
        self.status_var.set("🚀 Начинаем скачивание...")
        self.log_message(f"🚀 Скачивание: {url}")
        self.log_message(f"⚙️ Качество: {selected_quality}")
        self.log_message(f"📁 Путь: {save_path}")
        
        def download():
            try:
                ydl_opts = {
                    'format': format_id,
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
                self.log_message("🎉 Скачивание успешно завершено!")
                messagebox.showinfo("Успех", "🎉 Видео успешно скачано!")
                
            except Exception as e:
                self.status_var.set("❌ Ошибка скачивания")
                self.log_message(f"❌ Ошибка скачивания: {str(e)}")
                messagebox.showerror("Ошибка", f"Ошибка при скачивании:\n{str(e)}")
            finally:
                self.download_btn.config(state='normal', text="⬇️ СКАЧАТЬ ВИДЕО")
                
        # Запускаем скачивание в отдельном потоке
        threading.Thread(target=download, daemon=True).start()

def main():
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()

