import tensorflow as tf
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import cv2
from PIL import Image
import numpy as np


class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowIcon(QIcon('images/logo.png'))
        self.setWindowTitle('花卉识别')
        self.model = tf.keras.models.load_model("models/flower.h5")
        self.to_predict_name = "images/init.png"
        self.class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
        self.resize(700, 500)
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        font = QFont('楷体', 15)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        img_title = QLabel("测试样本")
        img_title.setFont(font)
        img_title.setAlignment(Qt.AlignCenter)
        self.img_label = QLabel()
        img_init = cv2.imread(self.to_predict_name)
        img_init = cv2.resize(img_init, (224, 224))
        cv2.imwrite('images/target.png', img_init)
        self.img_label.setPixmap(QPixmap('images/target.png'))
        left_layout.addWidget(img_title)
        left_layout.addWidget(self.img_label, 1, Qt.AlignCenter)
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        btn_change = QPushButton(" 加载测试样本 ")
        btn_change.clicked.connect(self.change_img)
        btn_change.setFont(font)
        btn_predict = QPushButton(" 识 别 花 卉 ")
        btn_predict.setFont(font)
        btn_predict.clicked.connect(self.predict_img)

        label_result = QLabel(' 识 别 结 果 ')
        self.result_label = QLabel()
        label_result.setFont(QFont('楷体', 16))
        self.result_label.setFont(QFont('楷体', 16))
        right_layout.addStretch()
        right_layout.addWidget(label_result, 0, Qt.AlignCenter)
        right_layout.addWidget(self.result_label, 0, Qt.AlignCenter)
        right_layout.addStretch()
        right_layout.addWidget(btn_change)
        right_layout.addWidget(btn_predict)
        right_layout.addStretch()
        right_widget.setLayout(right_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        main_widget.setLayout(main_layout)
        self.addTab(main_widget, '主页面')

    def change_img(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Image files(*.jpg , *.png)')
        img_name = openfile_name[0]
        if img_name == '':
            pass
        else:
            self.to_predict_name = img_name
            img_init = cv2.imread(self.to_predict_name)
            img_init = cv2.resize(img_init, (224, 224))
            cv2.imwrite('images/target.png', img_init)
            self.img_label.setPixmap(QPixmap('images/target.png'))

    def predict_img(self):
        img = Image.open('images/target.png')
        img = np.asarray(img)
        outputs = self.model.predict(img.reshape(1, 224, 224, 3))

        results = [(self.class_names[i], outputs[0][i]) for i in range(len(self.class_names))]
        results.sort(key=lambda x: x[1], reverse=True)

        result_text = "\n".join([f"{name}: {prob * 100:.2f}%" for name, prob in results])
        self.result_label.setText(result_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = MainWindow()
    x.show()
    sys.exit(app.exec_())
