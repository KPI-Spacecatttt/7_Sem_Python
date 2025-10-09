import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class StudentAnalysisApp:
    """
    Головний клас додатку для аналізу успішності студентів.
    Включає в себе GUI на Tkinter, логіку аналізу на Pandas та візуалізацію на Matplotlib.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Аналіз успішності студентів")
        self.root.geometry("1200x800")

        # Ініціалізація DataFrame
        self.df = None
        self.file_path = ""

        # Створення головного фрейму
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Створення фрейму для елементів керування
        controls_frame = ttk.LabelFrame(
            main_frame, text="Панель керування", padding="10"
        )
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        # Створення фрейму для графіків
        self.plot_frame = ttk.Frame(main_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Елементи керування ---

        # Кнопка завантаження файлу
        self.load_button = ttk.Button(
            controls_frame,
            text="Завантажити StudentsPerformance.csv",
            command=self.load_csv,
        )
        self.load_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Combobox для вибору групування
        ttk.Label(controls_frame, text="Групувати за:").grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )
        self.group_by_var = tk.StringVar(value="gender")
        self.group_by_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.group_by_var,
            values=["gender", "parental level of education", "race/ethnicity", "lunch"],
            state="readonly",
        )
        self.group_by_combo.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Slider (Scale) для вибору діапазону балів
        ttk.Label(controls_frame, text="Діапазон середнього балу:").grid(
            row=0, column=3, padx=5, pady=5, sticky="w"
        )

        self.min_score_var = tk.DoubleVar(value=0)
        self.min_score_scale = ttk.Scale(
            controls_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.min_score_var,
            command=lambda s: self.min_score_label.config(text=f"{float(s):.0f}"),
        )
        self.min_score_scale.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.min_score_label = ttk.Label(controls_frame, text="0")
        self.min_score_label.grid(row=0, column=5, padx=5, pady=5)

        self.max_score_var = tk.DoubleVar(value=100)
        self.max_score_scale = ttk.Scale(
            controls_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.max_score_var,
            command=lambda s: self.max_score_label.config(text=f"{float(s):.0f}"),
        )
        self.max_score_scale.grid(row=0, column=6, padx=5, pady=5, sticky="ew")
        self.max_score_label = ttk.Label(controls_frame, text="100")
        self.max_score_label.grid(row=0, column=7, padx=5, pady=5)

        # Кнопка для оновлення аналізу
        self.update_button = ttk.Button(
            controls_frame, text="Оновити аналіз", command=self.update_analysis
        )
        self.update_button.grid(row=0, column=8, padx=20, pady=5, sticky="ew")

        controls_frame.columnconfigure(4, weight=1)
        controls_frame.columnconfigure(6, weight=1)

        # --- Область для візуалізації ---
        self.fig, self.axes = plt.subplots(1, 3, figsize=(15, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        plt.tight_layout(pad=3.0)

        self.show_initial_message()

    def show_initial_message(self):
        """Показує початкове повідомлення на графіках"""
        for ax in self.axes:
            ax.clear()

        self.axes[1].text(
            0.5,
            0.5,
            'Будь ласка, завантажте файл "StudentsPerformance.csv"',
            ha="center",
            va="center",
            fontsize=12,
            wrap=True,
        )
        self.canvas.draw()

    def load_csv(self):
        """
        Відкриває діалогове вікно для вибору CSV-файлу та завантажує дані.
        Розраховує середній бал.
        """
        self.file_path = filedialog.askopenfilename(
            title="Оберіть файл StudentsPerformance.csv",
            filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")),
        )
        if not self.file_path:
            return

        try:
            self.df = pd.read_csv(self.file_path)
            # Розрахунок середнього балу для кожного студента
            self.df["average score"] = self.df[
                ["math score", "reading score", "writing score"]
            ].mean(axis=1)
            messagebox.showinfo(
                "Успіх",
                f"Файл '{self.file_path.split('/')[-1]}' успішно завантажено.\n"
                f"Знайдено {len(self.df)} записів.",
            )
            self.update_analysis()
        except Exception as e:
            messagebox.showerror(
                "Помилка", f"Не вдалося завантажити або обробити файл:\n{e}"
            )
            self.df = None

    def update_analysis(self):
        """
        Оновлює візуалізацію на основі вибраних параметрів у GUI.
        Виконує фільтрацію та групування даних.
        """
        if self.df is None:
            messagebox.showwarning("Увага", "Спочатку завантажте CSV файл.")
            return

        group_by_col = self.group_by_var.get()
        min_score = self.min_score_var.get()
        max_score = self.max_score_var.get()

        if min_score > max_score:
            messagebox.showerror(
                "Помилка", "Мінімальний бал не може бути більшим за максимальний."
            )
            return

        # Фільтрація даних за вибраним діапазоном балів
        filtered_df = self.df[
            (self.df["average score"] >= min_score)
            & (self.df["average score"] <= max_score)
        ].copy()

        if filtered_df.empty:
            messagebox.showwarning(
                "Немає даних", "За вибраними критеріями не знайдено жодного студента."
            )
            return

        # Очищення попередніх графіків
        for ax in self.axes:
            ax.clear()

        # 1. Boxplot оцінок за вибраною групою
        try:
            grouped_data = [
                group["average score"].values
                for name, group in filtered_df.groupby(group_by_col)
            ]
            labels = [name for name, group in filtered_df.groupby(group_by_col)]

            self.axes[0].boxplot(grouped_data, labels=labels, patch_artist=True)
            self.axes[0].set_title(f'Розподіл балів за "{group_by_col}"')
            self.axes[0].set_ylabel("Середній бал")
            self.axes[0].tick_params(axis="x", rotation=25)
        except Exception as e:
            self.axes[0].text(
                0.5, 0.5, f"Помилка побудови Boxplot:\n{e}", ha="center", va="center"
            )

        # 2. Bar Chart середнього балу по групах
        try:
            mean_scores = (
                filtered_df.groupby(group_by_col)["average score"].mean().sort_values()
            )
            mean_scores.plot(kind="bar", ax=self.axes[1], color=plt.cm.viridis(0.6))
            self.axes[1].set_title(f'Середній бал по групах "{group_by_col}"')
            self.axes[1].set_xlabel("")
            self.axes[1].set_ylabel("Середній бал")
            self.axes[1].tick_params(axis="x", rotation=25)
            self.axes[1].grid(axis="y", linestyle="--", alpha=0.7)
        except Exception as e:
            self.axes[1].text(
                0.5, 0.5, f"Помилка побудови Bar Chart:\n{e}", ha="center", va="center"
            )

        # 3. Histogram розподілу балів
        try:
            filtered_df["average score"].plot(
                kind="hist",
                ax=self.axes[2],
                bins=20,
                color=plt.cm.viridis(0.8),
                edgecolor="black",
            )
            self.axes[2].set_title("Загальний розподіл середніх балів")
            self.axes[2].set_xlabel("Середній бал")
            self.axes[2].set_ylabel("Кількість студентів")
            self.axes[2].grid(axis="y", linestyle="--", alpha=0.7)
        except Exception as e:
            self.axes[2].text(
                0.5, 0.5, f"Помилка побудови Histogram:\n{e}", ha="center", va="center"
            )

        self.fig.tight_layout(pad=3.0)
        # Перемальовка полотна
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentAnalysisApp(root)
    root.mainloop()
