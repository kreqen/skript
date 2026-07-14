"""Стили оформления приложения."""

from app.constants import COLORS

MAIN_STYLESHEET = f"""
QWidget {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['text_primary']};
}}

QMainWindow {{
    background-color: {COLORS['bg_primary']};
}}

QLabel {{
    color: {COLORS['text_primary']};
}}

QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px 10px;
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['pink_bright']};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {COLORS['pink_bright']};
}}

QComboBox {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 6px 10px;
    color: {COLORS['text_primary']};
}}

QComboBox:focus {{
    border: 2px solid {COLORS['pink_bright']};
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox::down-arrow {{
    image: none;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['pink_bright']};
    border: 1px solid {COLORS['border']};
}}

QScrollBar:vertical {{
    background-color: {COLORS['bg_secondary']};
    width: 12px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['pink_dark']};
    border-radius: 6px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['pink_bright']};
}}

QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {{
    border: none;
}}

QStatusBar {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_secondary']};
    border-top: 1px solid {COLORS['border']};
}}

QMessageBox {{
    background-color: {COLORS['bg_primary']};
}}

QMessageBox QLabel {{
    color: {COLORS['text_primary']};
}}

QMessageBox QDialogButtonBox {{
    button-layout: 0;
}}

QMessageBox QAbstractButton {{
    width: 80px;
    height: 30px;
}}
"""

GRADIENT_BUTTON_STYLESHEET = f"""
QPushButton {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['pink_bright']},
        stop:0.5 {COLORS['pink_dark']},
        stop:1 {COLORS['bg_tertiary']}
    );
    color: {COLORS['text_primary']};
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 13px;
}}

QPushButton:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['pink_light']},
        stop:0.5 {COLORS['pink_bright']},
        stop:1 {COLORS['pink_dark']}
    );
}}

QPushButton:pressed {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['pink_dark']},
        stop:0.5 {COLORS['pink_bright']},
        stop:1 {COLORS['bg_secondary']}
    );
}}

QPushButton:disabled {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_secondary']};
}}
"""

SECONDARY_BUTTON_STYLESHEET = f"""
QPushButton {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['pink_dark']};
}}

QPushButton:pressed {{
    background-color: {COLORS['border']};
}}

QPushButton:disabled {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_secondary']};
    border: 1px solid {COLORS['bg_secondary']};
}}
"""

SUBJECT_CARD_STYLESHEET = f"""
QPushButton {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: {COLORS['bg_tertiary']};
    border: 1px solid {COLORS['pink_dark']};
    color: {COLORS['text_primary']};
}}

QPushButton:pressed {{
    background-color: {COLORS['pink_dark']};
    color: {COLORS['text_primary']};
}}
"""

HEADER_STYLESHEET = f"""
QWidget {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['pink_dark']},
        stop:0.5 {COLORS['bg_secondary']},
        stop:1 {COLORS['bg_primary']}
    );
    border-bottom: 1px solid {COLORS['border']};
}}

QLabel {{
    color: {COLORS['text_primary']};
}}

QLabel#subtitle {{
    color: {COLORS['text_secondary']};
}}
"""

NAV_BUTTON_STYLESHEET = f"""
QPushButton {{
    background-color: transparent;
    color: {COLORS['text_secondary']};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 16px;
    font-size: 12px;
}}

QPushButton:hover {{
    color: {COLORS['text_primary']};
}}

QPushButton:checked {{
    color: {COLORS['pink_bright']};
    border-bottom: 2px solid {COLORS['pink_bright']};
}}

QPushButton:pressed {{
    color: {COLORS['pink_bright']};
}}
"""
