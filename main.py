import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns


class DataAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Data Analyzer')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Кнопка для загрузки данных
        self.load_button = QPushButton('Загрузить данные CSV')
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        # Метка для отображения статистики
        self.stat_label = QLabel('Статистика по данным:')
        self.layout.addWidget(self.stat_label)

        # Выпадающий список для выбора типа графика
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(['Линейный график', 'Гистограмма', 'Круговая диаграмма'])
        self.graph_type_combo.currentIndexChanged.connect(self.update_graph)  # Обработчик изменения типа графика
        self.layout.addWidget(self.graph_type_combo)

        # Поле для отображения графиков
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

        # Данные для загрузки
        self.data = None

    def load_data(self):
        # Открытие диалога для выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть CSV файл', '', 'CSV Files (*.csv)')
        if file_path:
            # Загрузка данных в pandas DataFrame
            self.data = pd.read_csv(file_path)
            self.display_statistics()
            self.update_graph()  # Обновление графика после загрузки данных

    def display_statistics(self):
        if self.data is not None:
            # Вывод статистики по данным
            stats = f"Количество строк: {len(self.data)}\n"
            stats += f"Количество столбцов: {len(self.data.columns)}\n"
            stats += f"Минимальные значения:\n{self.data.min()}\n"
            stats += f"Максимальные значения:\n{self.data.max()}"
            self.stat_label.setText(f"Статистика по данным:\n{stats}")

    def update_graph(self):
        if self.data is not None:
            # Получаем тип графика, выбранный пользователем
            graph_type = self.graph_type_combo.currentText()

            # Очищаем старую фигуру
            self.canvas.figure.clear()

            # Добавляем новый subplot
            ax = self.canvas.figure.add_subplot(111)

            if graph_type == 'Линейный график':
                sns.lineplot(data=self.data, x='Date', y='Value1', ax=ax)
            elif graph_type == 'Гистограмма':
                sns.histplot(self.data['Value2'], kde=True, ax=ax)
            elif graph_type == 'Круговая диаграмма':
                category_counts = self.data['Category'].value_counts()
                category_counts.plot.pie(ax=ax, autopct='%1.1f%%')

            # Обновляем канвас, чтобы отобразить новый график
            self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
