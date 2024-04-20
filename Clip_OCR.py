import json
import My_OCR
import os
import customtkinter as ctk
import tkinter as tk

class Clip_OCR:
    def __init__(self, master):
        self.master = master
        self.error_log_flags = False
        self.is_help_window = False

        self.OCR = My_OCR.OCR()
        self.OCR.setup()
        self.OCR.set_run_flag()

        self.default_values = {
            "language": "日本語",
            "standby_time": 0.5,
            "paragraph_threshold_value": 1.0,
            "new_line": "有効",
            "detection_sound": "無効"
        }

        self.language_dict = {
            "日本語": "jpn+eng",
            "英語": "eng+jpn",
            "英語のみ": "eng"
            }

        self.help_text_list = [
            ["優先する言語:", "優先して検出する言語を設定します"],
            ["改行の閾値 :", "OCRの改行閾値を設定します（値を小さくすることでより改行しやすくなります）"],
            ["改行とスペース :", "有効の場合OCR結果に改行とスペースを含め、無効の場合は一行の文で出力します"],
            ["検出音 :", "OCR処理が完了した際に通知音を流します"]
            ]

            # snapping toolの自動保存が有効の場合、意図しない画像が保存されている場合があります。
            # OCRアプリを利用する際はsnapping toolの自動保存を一時的に無効にすることをお勧めします

        self.font_style = ctk.CTkFont(family="Helvetica", size=25)
        
        self.load_config()

        set_parameter_frame = ctk.CTkFrame(self.master, fg_color="#e6e6e6")

        language_label = ctk.CTkLabel(set_parameter_frame, text="優先する言語：", font=self.font_style)
        self.entry_language = ctk.CTkComboBox(set_parameter_frame, values=[language for language in self.language_dict], fg_color="#fafafa", button_color="#b3b3b3", border_width=0, border_color="#c8c8c8", justify="center", font=self.font_style, width=5)
        self.entry_language.set(self.config.get("language"))

        # 待機時間を任意に設定する場合
        # self.standby_time_var = ctk.DoubleVar(value=self.config.get("standby_time"))
        # self.standby_time_label = ctk.CTkLabel(set_parameter_frame, text="  待機時間：", font=self.font_style)
        # self.entry_standby_time = ctk.CTkEntry(set_parameter_frame, textvariable=self.standby_time_var, justify="center", font=self.font_style, width=5)

        self.paragraph_threshold_var = ctk.DoubleVar(value=self.config.get("paragraph_threshold_value"))
        paragraph_threshold_label = ctk.CTkLabel(set_parameter_frame, text="改行の閾値：", font=self.font_style)
        self.entry_paragraph_threshold = ctk.CTkEntry(set_parameter_frame, textvariable=self.paragraph_threshold_var, fg_color="#fafafa", border_width=0, border_color="#c8c8c8", justify="center", font=self.font_style, width=5)

        new_line_label = ctk.CTkLabel(set_parameter_frame, text="改行とスペース：", font=self.font_style)
        self.enable_new_line = ctk.CTkButton(set_parameter_frame, text=self.config.get("new_line"), command=self.is_new_line, font=self.font_style)

        detection_sound_label = ctk.CTkLabel(set_parameter_frame, text="検出音：", font=self.font_style)
        self.enable_detection_sound  = ctk.CTkButton(set_parameter_frame, text=self.config.get("detection_sound"), command=self.is_ditection_sound, font=self.font_style)

        # self.enable_detection_sound["text"] = self.config.get("detection_sound")

        action_frame = ctk.CTkFrame(self.master)
        action_frame.grid_rowconfigure(0, weight=1)
        action_frame.grid_columnconfigure(0, weight=1)

        self.run_button = ctk.CTkButton(action_frame, text="開始", command=self.run_or_stop, font=self.font_style)
        self.show_help_button = ctk.CTkButton(action_frame, text="ヘルプを表示", command=self.help_window, font=self.font_style)#command=lambda:self.help_window()
        self.save_config_button = ctk.CTkButton(action_frame, text="値を保存", command=self.save_config, font=self.font_style)
        self.reset_config_button = ctk.CTkButton(action_frame, text="値を初期化", command=self.reset_config, font=self.font_style)

        logs_frame = ctk.CTkFrame(self.master)
        logs_frame.grid_rowconfigure(0, weight=1)
        logs_frame.grid_columnconfigure(0, weight=1)
        self.console_text = ctk.CTkLabel(logs_frame, text="開始ボタンを押してください", justify="center", font=self.font_style)#justify="center"

        set_parameter_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        language_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_language.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # 待機時間を任意に設定する場合
        # self.standby_time_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        # self.entry_standby_time.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        paragraph_threshold_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_paragraph_threshold.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        new_line_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.enable_new_line.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        detection_sound_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.enable_detection_sound.grid(row=3, column=1,  sticky="ew", padx=5, pady=5)

        action_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.run_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.show_help_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        self.save_config_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.reset_config_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        logs_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.console_text.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.run_ocr()

        self.change_button_condition(self.enable_new_line, True)
        self.change_button_condition(self.enable_detection_sound, True)

    def change_button_condition(self, button_element, flip:bool=False):
        if flip:
            text, fg_color, hover_color = ("有効", "#3b8ed0", "#36719f") if button_element.cget("text") == "有効" else ("無効", "#ff7c5d", "#cc634a")
        else:
            text, fg_color, hover_color = ("無効", "#ff7c5d", "#cc634a") if button_element.cget("text") == "有効" else ("有効", "#3b8ed0", "#36719f")
        
        button_element.configure(text=text, fg_color=fg_color, hover_color=hover_color)

    def is_new_line(self, flip:bool=False):
        self.change_button_condition(button_element=self.enable_new_line, flip=flip)

    def is_ditection_sound(self, flip:bool=False):
        self.change_button_condition(button_element=self.enable_detection_sound, flip=flip)

    def run_ocr(self):
        try:
            language = self.language_dict[self.entry_language.get()]
            #paragraph_threshold_valueのerrorが取得できない
            paragraph_threshold_value = float(self.entry_paragraph_threshold.get())
        except KeyError:
            alert_text = "言語は選択肢から選んでください"
            self.error_log_flags = True

        except (ValueError, UnboundLocalError):
            alert_text = "改行の閾値が適切ではありません"
            self.error_log_flags = True
        except:
            print("test")
        else:
            self.run_button.configure(state="normal")
            if self.error_log_flags:
                self.console_text.configure(text="開始ボタンを押してください")
                self.error_log_flags = False

        finally:
            if self.error_log_flags:
                self.run_button.configure(state="disabled")
                self.console_text.configure(text=alert_text)
                self.master.after(200, self.run_ocr)
                return

        self.OCR.ocr(
            language = language,
            paragraph_threshold_value = paragraph_threshold_value,
            space_and_newline = True if self.enable_new_line.cget("text") == "有効" else False,
            detection_sound = True if self.enable_detection_sound.cget("text") == "有効" else False
            )

        # 待機時間を任意に設定する場合
        # standby_time = int(float(self.entry_standby_time.get()) * 1000)
        # standby_time = 100 if standby_time < 100 else standby_time #待機時間の最小値は0.1秒（100ミリ秒）

        self.master.after(200, self.run_ocr)

    def run_or_stop(self):
        is_run, condition_text, condition, fg_color, hover_color = (False, "開始", "normal", "#3b8ed0", "#36719f") if self.run_button.cget("text") == "停止" else (True, "停止", "disabled", "#ff7c5d", "#cc634a")

        self.OCR.set_run_flag(is_run = is_run)

        self.run_button.configure(fg_color=fg_color, hover_color=hover_color)

        # OCR処理開始時に値を変更できないようにしてる
        self.entry_language.configure(state=condition)
        # 待機時間を任意に設定する場合
        # self.entry_standby_time.configure(state=condition)
        self.entry_paragraph_threshold.configure(state=condition)
        # self.enable_new_line.configure(state=condition)
        self.enable_detection_sound.configure(state=condition)
        self.run_button.configure(text=condition_text)
        self.show_help_button.configure(state=condition)
        self.reset_config_button.configure(state=condition)
        self.save_config_button.configure(state=condition)

        self.console_text.configure(text=f"OCRは{'実行中です' if condition_text == '停止' else '停止中です'}")

    def reset_config(self):
        self.entry_language.set(self.default_values["language"])
        # 待機時間を任意に設定する場合
        # self.standby_time_var.set(self.default_values["standby_time"])
        self.paragraph_threshold_var.set(self.default_values["paragraph_threshold_value"])
        self.enable_detection_sound.configure(text=self.default_values["detection_sound"])
        self.enable_new_line.configure(text=self.default_values["new_line"])
        
        self.is_ditection_sound(flip=True)
        self.is_new_line(flip=True)
        
        self.console_text.configure(text="値を初期化しました")
        
    def save_config(self):
        config = {
            "language": self.entry_language.get(),
            # "standby_time": self.standby_time_var.get(),
            "paragraph_threshold_value": self.paragraph_threshold_var.get(),
            "new_line": self.enable_new_line.cget("text"),
            "detection_sound": self.enable_detection_sound.cget("text")
        }

        with open("config.json", "w") as config_file:
            json.dump(config, config_file)

        self.console_text.configure(text="値を保存しました")

    def help_window(self):
        if not self.is_help_window:

            help_window = tk.Toplevel(self.master) #ctk.CTkToplevel(self.master)
            help_window.title("ヘルプ")
            help_window.iconbitmap(os.path.join(os.path.dirname(__file__), "clip_ocr_icon.ico"))
            help_window.resizable(width=False, height=False)

            for index, help_text_line in enumerate(self.help_text_list):
                for line_index, help_text in enumerate(help_text_line):
                    help_label = ctk.CTkLabel(help_window, text=help_text, font=self.font_style)
                    help_label.grid(row=index, column=line_index, sticky=["e", "w"][line_index], padx=10, pady=5)

            close_button = ctk.CTkButton(help_window, text="閉じる", font=self.font_style, command=lambda:self.close_window(help_window=help_window))
            close_button.grid(row=len(self.help_text_list) + 1, column=0, columnspan=2, padx=10, pady=10)

            self.is_help_window = True

        elif self.is_help_window:
            self.console_text.configure(text="すでに表示しています")

    def close_window(self, help_window) :
        help_window.destroy()
        self.is_help_window = False

    def load_config(self):
        try:
            with open("config.json", "r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            # print("デフォルト値を採用")
            self.config = self.default_values

if __name__ == "__main__":
    icon_path = os.path.join(os.path.dirname(__file__), "clip_ocr_icon.ico")
    
    root = tk.Tk()
    root.title("Clip OCR")
    root.iconbitmap(icon_path)
    root.resizable(width=False, height=False)

    app = Clip_OCR(root)
    root.mainloop()