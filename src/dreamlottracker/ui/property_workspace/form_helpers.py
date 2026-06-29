from PySide6.QtWidgets import QCheckBox, QComboBox, QDoubleSpinBox, QSpinBox


def combo(values: list[str], current: str):
    widget = QComboBox()
    widget.addItems(values)
    widget.setCurrentText(current)
    return widget


def check(value):
    widget = QCheckBox()
    widget.setChecked(bool(value) if value is not None else False)
    return widget


def money(value):
    widget = QDoubleSpinBox()
    widget.setMaximum(100000000)
    widget.setPrefix("$")
    widget.setDecimals(0)
    widget.setValue(float(value or 0))
    return widget


def double(maximum, decimals, value, minimum=0):
    widget = QDoubleSpinBox()
    widget.setRange(minimum, maximum)
    widget.setDecimals(decimals)
    widget.setValue(float(value or 0))
    return widget


def spin(value):
    widget = QSpinBox()
    widget.setMaximum(10000)
    widget.setValue(int(value or 0))
    return widget
