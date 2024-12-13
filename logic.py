from PyQt6.QtWidgets import *
from gui import *
import math

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Calculator")
        self.label_heading.setText("Please choose a calculator.")
        self.equation = ""
        self.area_val = ""
        self.calc_mode()
        self.hide_buttons()

    def clear_all(self) -> None:
        '''
        This method will clear all input/memory from the calculator. This includes radio buttons, text boxes,
        current calculations, and the main window. It is used when switching between modes so that input
        from each mode does not get mixed up.
        :return:
        '''
        self.window_val.clear()
        self.input_height.clear()
        self.input_width.clear()
        self.input_radius.clear()
        self.equation = ""
        self.area_val = ""
        self.buttonGroup.setExclusive(False)
        for button in self.buttonGroup.buttons():
            button.setChecked(False)
        self.buttonGroup.setExclusive(True)

    def hide_buttons(self) -> None:
        '''
        This method hides the radio buttons/text boxes for the area mode so that the interface is not too
        confusing. It also enables the calculator buttons so that they can be used for calculator mode.
        :return:
        '''
        self.label_height.setVisible(False)
        self.input_height.setVisible(False)
        self.label_width.setVisible(False)
        self.input_width.setVisible(False)
        self.label_radius.setVisible(False)
        self.input_radius.setVisible(False)
        self.radio_square.setVisible(False)
        self.radio_triangle.setVisible(False)
        self.radio_circle.setVisible(False)
        self.radio_rectangle.setVisible(False)

        buttons = ["plus", "ac", "div", "minus", "x", "del", "period", 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        for button in buttons:
            button = self.findChild(QPushButton, f"button_{button}")
            button.setEnabled(True)

    def show_buttons(self) -> None:
        '''
        This method shows all of the radio buttons/text boxes for the area mode when the area mode is
        selected. It also disables the calculator buttons so that the interface is not too confusing.
        :return:
        '''
        self.label_height.setVisible(True)
        self.input_height.setVisible(True)
        self.label_width.setVisible(True)
        self.input_width.setVisible(True)
        self.label_radius.setVisible(True)
        self.input_radius.setVisible(True)
        self.radio_square.setVisible(True)
        self.radio_triangle.setVisible(True)
        self.radio_circle.setVisible(True)
        self.radio_rectangle.setVisible(True)

        buttons = ["plus", "ac", "div", "minus", "x", "del", "period", 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        for button in buttons:
            button = self.findChild(QPushButton, f"button_{button}")
            button.setEnabled(False)

    def calc_mode(self) -> None:
        '''
        This method sets the calculator into calculator/area mode based on the buttons pressed by the user.
        It will connect the buttons to their corresponding methods.
        :return:
        '''
        self.button_area.clicked.connect(self.area_mode)
        self.button_calculator.clicked.connect(self.calculator)

    def area_mode(self) -> None:
        '''
        This method shows the buttons for the area mode and sets the label to Area Calculator. It also clears
        previous input. Then, it disconnects previous buttons and connects to the area_calculate method.
        :return:
        '''
        self.show_buttons()
        self.label_heading.setText("Area Calculator")
        self.clear_all()
        try:
            self.button_equal.clicked.disconnect()
        except Exception:
            pass
        self.button_equal.clicked.connect(self.area_calculate)

    def area_calculate(self) -> None:
        '''
        This method looks for the = button to be pressed and then analyzes input from the radio buttons and
        text boxes. It will check the input values, calculate them, then display them in the window. An error
        will be displayed in the heading label if incorrect values are submit.
        :return:
        '''
        self.show_buttons()
        button = self.sender()
        if button:
            button_text = button.text()
            if button_text == "=":
                error_message = False
                shape = ""

                if self.radio_circle.isChecked():
                    shape = "circle"
                elif self.radio_square.isChecked():
                    shape = "square"
                elif self.radio_rectangle.isChecked():
                    shape = "rectangle"
                elif self.radio_triangle.isChecked():
                    shape = "triangle"


                height_val = self.input_height.text()
                width_val = self.input_width.text()
                radius_val = self.input_radius.text()

                if height_val == '':
                    height_val = 0
                if width_val == '':
                    width_val = 0
                if radius_val == '':
                    radius_val = 0

                try:
                    height_val = float(height_val)
                    width_val = float(width_val)
                    radius_val = float(radius_val)
                except Exception:
                    error_message = True
                    pass

                try:
                    if height_val < 0 or width_val < 0 or radius_val < 0:
                        error_message = True
                    else:
                        error_message = False
                except Exception:
                    error_message = True
                    pass


                if error_message == False:
                    self.label_heading.setText("Area Calculator")
                    if shape == "circle":
                        self.area_val = radius_val * radius_val * math.pi
                    elif shape == "square":
                        self.area_val = height_val * height_val
                    elif shape == "rectangle":
                        self.area_val = height_val * width_val
                    elif shape == "triangle":
                        self.area_val = (height_val * width_val) / 2

                    self.area_val = str(self.area_val)

                    self.window_val.setText(self.area_val)
                else:
                    self.label_heading.setText("Please enter the correct values.")


    def calculator(self) -> None:
        '''
        This method will analyze all of the calculator buttons for input and disconnect previous buttons. It
        also clears previous input, sets the heading label to Calculator, and hides the area buttons.
        :return:
        '''
        self.label_heading.setText("Calculator")
        self.clear_all()
        self.hide_buttons()
        buttons = ["plus", "ac", "div", "minus", "x","del", "equal", "period", 1 , 2, 3, 4, 5, 6, 7, 8, 9, 0]
        try:
            for button in buttons:
                button = self.findChild(QPushButton, f"button_{button}")
                if button:
                    button.clicked.disconnect()
                    print(4)
        except Exception:
            pass
        for button in buttons:
            button = self.findChild(QPushButton, f"button_{button}")
            if button:
                button.clicked.connect(self.do_equation)

    def do_equation(self) -> None:
        '''
        This method will display the buttons pressed to the main window and do operations based on the
        operator buttons that are pressed. It then displays the value.
        :return:
        '''
        button = self.sender()
        if button:

            button_text = button.text()
            if button_text == "AC":
                self.equation = ""
                self.label_heading.setText("Calculator")

            if button_text == "DEL":
                self.equation = self.equation[:-1]

            if button_text == "=":
                try:
                    self.equation = str(eval(self.equation))

                except Exception:
                    self.label_heading.setText("Please enter the correct values.")
                    self.equation = ""
            elif not(button_text == "AC" or button_text == "DEL"):
                self.equation += button_text

            self.window_val.setText(self.equation)





