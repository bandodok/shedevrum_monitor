import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from core.main import Monitor


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    m = Monitor()
    engine.rootContext().setContextProperty("Monitor", m)
    engine.load(os.fspath(Path(__file__).resolve().parent / "gui/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    app.exec()
    sys.exit()
