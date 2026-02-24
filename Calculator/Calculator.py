"""
Calculator (PySide6)

A desktop calculator with basic arithmetic operations.

Features:
(i) Addition, subtraction, multiplication, division;
(ii) Decimal numbers;
(iii) Negation (+/-);
(iv) Backspace & clear;
(v) Division by zero handling;
(vi) Dynamic font resizing;
(vii) Proper result state handling (no digit appending after "=").
"""

import sys
from typing import Union, Optional
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase
from operator import add, sub, mul, truediv

from Calculator.ui.design import Ui_MainWindow
import ui.files_rc

operations = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
}

DEFAULT_FONT_SIZE = 16
DEFAULT_ENTRY_FONT_SIZE = 40

ERROR_ZERO_DIV = "Division by zero"
ERROR_UNDEFINED = "Result is undefined"

class Calculator(QMainWindow):
    """
    Main calculator window.
    """

    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.entry_max_len = self.ui.lineEdit.maxLength()
        self.is_result_shown = False

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        self._connect_buttons()

    # --------------------------
    # UI CONNECTIONS
    # --------------------------

    def _connect_buttons(self) -> None:
        """Connect UI buttons to logic methods."""

        for i in range(10):
            getattr(self.ui, f"btn_{i}").clicked.connect(
                lambda _, digit=str(i): self.add_digit(digit)
            )

        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_neg.clicked.connect(self.negate)
        self.ui.btn_backspace.clicked.connect(self.backspace)

        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_add.clicked.connect(lambda: self.math_operation("+"))
        self.ui.btn_sub.clicked.connect(lambda: self.math_operation("-"))
        self.ui.btn_mul.clicked.connect(lambda: self.math_operation("*"))
        self.ui.btn_div.clicked.connect(lambda: self.math_operation("/"))

    # --------------------------
    # INPUT HANDLING
    # --------------------------

    def add_digit(self, digit: str) -> None:
        """
        Add a digit to the entry field.
        Clears result if "=" was just pressed.
        """
        self.remove_error()
        self.clear_temp()

        if self.is_result_shown:
            self.ui.lineEdit.setText("0")
            self.is_result_shown = False

        current = self.ui.lineEdit.text()

        if current == "0":
            self.ui.lineEdit.setText(digit)
        else:
            self.ui.lineEdit.setText(current + digit)

        self.adjust_entry_font_size()

    def add_point(self) -> None:
        """Add decimal point if not already present."""
        self.clear_temp()

        if self.is_result_shown:
            self.ui.lineEdit.setText("0")
            self.is_result_shown = False

        if "." not in self.ui.lineEdit.text():
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + ".")
            self.adjust_entry_font_size()

    def negate(self) -> None:
        """Toggle number sign."""
        self.clear_temp()
        entry = self.ui.lineEdit.text()

        if entry.startswith("-"):
            entry = entry[1:]
        elif entry != "0":
            entry = "-" + entry

        self.ui.lineEdit.setText(entry)
        self.adjust_entry_font_size()

    def backspace(self) -> None:
        """Remove last character from entry."""
        self.remove_error()
        self.clear_temp()

        if self.is_result_shown:
            self.ui.lineEdit.setText("0")
            self.is_result_shown = False
            return

        entry = self.ui.lineEdit.text()

        if len(entry) > 1:
            self.ui.lineEdit.setText(entry[:-1])
        else:
            self.ui.lineEdit.setText("0")

        self.adjust_entry_font_size()

    def clear_all(self) -> None:
        """Reset calculator state."""
        self.remove_error()
        self.ui.lineEdit.setText("0")
        self.ui.label.clear()
        self.is_result_shown = False
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()

    # --------------------------
    # CALCULATION LOGIC
    # --------------------------

    @staticmethod
    def remove_zeros(num: str) -> str:
        """Remove unnecessary trailing .0."""
        n = str(float(num))
        return n[:-2] if n.endswith(".0") else n

    def get_entry(self) -> Union[int, float]:
        """Return current entry as number."""
        entry = self.ui.lineEdit.text()
        return float(entry) if "." in entry else int(entry)

    def get_temp(self) -> Optional[Union[int, float]]:
        """Return stored number from label."""
        if self.ui.label.text():
            temp = self.ui.label.text().split()[0]
            return float(temp) if "." in temp else int(temp)
        return None

    def get_mathsign(self) -> Optional[str]:
        """Return current operation symbol."""
        if self.ui.label.text():
            return self.ui.label.text().split()[-1]
        return None

    def calculate(self) -> Optional[str]:
        """
        Perform calculation when "=" is pressed.
        """
        if not self.ui.label.text():
            return None

        try:
            result = operations[self.get_mathsign()](
                self.get_temp(), self.get_entry()
            )
            result = self.remove_zeros(str(result))

            self.ui.label.setText(
                f"{self.get_temp()} {self.get_mathsign()} {self.ui.lineEdit.text()} ="
            )

            self.ui.lineEdit.setText(result)
            self.is_result_shown = True

            self.adjust_entry_font_size()
            self.adjust_temp_font_size()

            return result

        except ZeroDivisionError:
            if self.get_temp() == 0:
                self.show_error(ERROR_UNDEFINED)
            else:
                self.show_error(ERROR_ZERO_DIV)
        except KeyError:
            return None

    def math_operation(self, sign: str) -> None:
        """
        Handle + - * / button press.
        """
        if not self.ui.label.text():
            self.ui.label.setText(
                self.remove_zeros(self.ui.lineEdit.text()) + f" {sign}"
            )
            self.ui.lineEdit.setText("0")
        else:
            if self.get_mathsign() == "=":
                self.ui.label.setText(
                    self.remove_zeros(self.ui.lineEdit.text()) + f" {sign}"
                )
            else:
                self.ui.label.setText(
                    self.ui.label.text()[:-1] + sign
                )

        self.is_result_shown = False
        self.adjust_temp_font_size()

    # --------------------------
    # ERROR HANDLING
    # --------------------------

    def show_error(self, text: str) -> None:
        """Display error and disable operations."""
        self.ui.lineEdit.setText(text)
        self.disable_buttons(True)

    def remove_error(self) -> None:
        """Reset error state."""
        if self.ui.lineEdit.text() in (ERROR_ZERO_DIV, ERROR_UNDEFINED):
            self.ui.lineEdit.setText("0")
            self.disable_buttons(False)

    def disable_buttons(self, disable: bool) -> None:
        """Enable/disable operation buttons."""
        for btn in (
            self.ui.btn_calc,
            self.ui.btn_add,
            self.ui.btn_sub,
            self.ui.btn_mul,
            self.ui.btn_div,
        ):
            btn.setDisabled(disable)

    # --------------------------
    # FONT ADJUSTMENT
    # --------------------------

    def adjust_entry_font_size(self) -> None:
        """Auto-adjust entry font size."""
        font_size = DEFAULT_ENTRY_FONT_SIZE
        while (
            self.ui.lineEdit.fontMetrics()
            .boundingRect(self.ui.lineEdit.text())
            .width()
            > self.ui.lineEdit.width() - 15
        ):
            font_size -= 1
            self.ui.lineEdit.setStyleSheet(
                f"font-size: {font_size}pt; border: none;"
            )

    def adjust_temp_font_size(self) -> None:
        """Auto-adjust label font size."""
        font_size = DEFAULT_FONT_SIZE
        while (
            self.ui.label.fontMetrics()
            .boundingRect(self.ui.label.text())
            .width()
            > self.ui.label.width() - 10
        ):
            font_size -= 1
            self.ui.label.setStyleSheet(
                f"font-size: {font_size}pt; border: none;"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
