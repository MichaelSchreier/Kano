STYLE_ITEM_LIST = (
	"""
	QListWidget {
		outline: 0;
		background-color: rgb(247, 247, 247);
		border-bottom-left-radius: 5px;
		border-bottom-right-radius: 5px;
		background-image: url(img/drop_large_text.png);
		background-repeat: false;
		background-position: center;
		background-attachment: fixed;
		border: 1px solid;
		border-color: rgb(254, 254, 254) rgb(232, 232, 232) rgb(232, 232, 232) rgb(232, 232, 232);
	}
	"""
)

STYLE_MAIN_WINDOW = (
	"""
	QToolBar {
		border: 1px solid;
		background-color: rgb(247, 247, 247);
		border-top-left-radius: 5px;
		border-top-right-radius: 5px;
		border-color: rgb(232, 232, 232);
	}
	QToolButton {
		border: 0px;
		background: transparent;
	}
	QToolButton:hover {
		border: 0px;
		border-radius: 5px;
		background: rgb(217, 217, 217);
	}
	QToolButton:checked {
		border: 0px;
		border-radius: 5px;
		background: rgb(189, 189, 189);
	}
	QListWidget::item:selected:active {
		background: rgba(189, 189, 189, 0.95);
	}
	QListWidget::item {
		color: black;
		background-color: rgba(217, 217, 217, 0.95);
		border-width: 1px;
		border-radius: 5px;
		border-style: solid;
		border-color: rgb(232, 232, 232) transparent rgb(202, 202, 202) transparent;
	}
	QScrollBar:vertical {
		border: 0px;
 		background: rgb(189, 189, 189);
		margin: 0 0 0 0;
		width: 12px;
		border-bottom-right-radius: 5px;
 	}
	QScrollBar::handle:vertical {
 		background: rgb(99, 99, 99);
		border-radius: 5px;
 	}
	QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
		background: transparent;
	}
	QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
		height: 0;
	}
	QTextEdit {
		border: 0px;
		background-color: rgb(247, 247, 247);
		border-bottom-left-radius: 5px;
		border-bottom-right-radius: 5px;
		border: 1px solid;
		border-color: rgb(254, 254, 254) rgb(232, 232, 232) rgb(232, 232, 232) rgb(232, 232, 232);
	}
	"""
)

STYLE_ADJUST_ITEM_LIST = (
	"""
	QListWidget {
		outline: 0;
		background-color: rgb(247, 247, 247);
		border: 1px solid;
		border-color: rgb(254, 254, 254) rgb(232, 232, 232) rgb(232, 232, 232) rgb(232, 232, 232);
		}
	"""
)

STYLE_SET_ARCHIVE_DIALOG = (
	"""
	QDialog {
		background-color: rgb(247, 247, 247);
		border-bottom-left-radius: 5px;
		border-bottom-right-radius: 5px;
		border: 1px solid;
		border-color: rgb(254, 254, 254) rgb(232, 232, 232) rgb(232, 232, 232) rgb(232, 232, 232);
	}
	QPushButton {
		background-color: rgb(232, 232, 232);
		border-radius: 3px;
		height: 20;
		border: 1px solid;
		border-color: rgb(217, 217, 217);
	}
	QPushButton:hover {
		background-color: rgb(217, 217, 217);
		border-color: rgb(189, 189, 189);
	}
	QPushButton:pressed {
		background-color: rgb(189, 189, 189);
		border-color: rgb(150, 150, 150);
	}
	QLineEdit {
		height: 18;
		border: 1px solid black;
		border-radius: 2px;
		selection-background-color: rgb(189, 189, 189);
	}
	"""
)

STYLE_SET_ARCHIVE_LINEEDIT = (
	"""
	QLineEdit {
		height: 18;
		border: 1px solid black;
		border-radius: 2px;
		color: rgb(82, 82, 82);
		background-color: rgb(217, 217, 217);
		selection-background-color: rgb(189, 189, 189);
	}
	"""
)

STYLE_NEW_ITEM_DIALOG = (
	"""
	QDialog {
		background-color: rgb(247, 247, 247);
		border-bottom-left-radius: 5px;
		border-bottom-right-radius: 5px;
		border: 1px solid;
		border-color: rgb(254, 254, 254) rgb(232, 232, 232) rgb(232, 232, 232) rgb(232, 232, 232);		
	}
	QPushButton {
		background-color: rgb(232, 232, 232);
		border-radius: 3px;
		height: 20;
		border: 1px solid;
		border-color: rgb(217, 217, 217);
	}
	QPushButton:hover {
		background-color: rgb(217, 217, 217);
		border-color: rgb(189, 189, 189);
	}
	QPushButton:pressed {
		background-color: rgb(189, 189, 189);
		border-color: rgb(150, 150, 150);
	}
	"""
)

STYLE_SETTINGS_WINDOW = (
	"""
	QDialog {
		background-color: rgb(247, 247, 247);
	}
	QScrollArea {
		background-color: rgb(247, 247, 247);
		border-bottom-left-radius: 5px;
		border-bottom-right-radius: 5px;
		border: 1px solid;
		border-color: rgb(254, 254, 254) rgb(232, 232, 232) rgb(232, 232, 232) rgb(232, 232, 232);
	}
	QSpinBox {
		border-width: 0px;
		background-color: rgb(232, 232, 232);
		selection-background-color: rgb(99, 99, 99);
		border: 1px solid;
		height: 20;
		border-color: rgb(217, 217, 217);
	}
	QCheckBox::indicator {
		width: 20px;
		height: 20px;
	}
	QCheckBox::indicator:unchecked {
		image: url(img/switch_off.png);
	}
	QCheckBox::indicator:unchecked:hover {
		image: url(img/switch_off_hover.png);
	}
	QCheckBox::indicator:checked {
		image: url(img/switch_on.png);
	}			
	QCheckBox::indicator:checked:hover {
		image: url(img/switch_on_hover.png);
	}
	QSpinBox::up-button {
		subcontrol-origin: border;
		subcontrol-position: top right;
		width: 16px;
		border-image: url(img/arrow_up.png) 1;
	}
	QSpinBox::up-button:hover {
		background-color: rgb(217, 217, 217);
	}
	QSpinBox::up-button:pressed {
		background-color: rgb(189, 189, 189);
	}
	QSpinBox::down-button {
		subcontrol-origin: border;
		subcontrol-position: bottom right;
		width: 16px;
		border-image: url(img/arrow_down.png) 1;
		border-top-width: 0;
	}
	QSpinBox::down-button:hover {
		background-color: rgb(217, 217, 217);
	}
	QSpinBox::down-button:pressed {
		background-color: rgb(189, 189, 189);
	}
	QPushButton {
		background-color: rgb(232, 232, 232);
		border-radius: 3px;
		height: 20;
		border: 1px solid;
		border-color: rgb(217, 217, 217);
	}
	QPushButton:hover {
		background-color: rgb(217, 217, 217);
		border-color: rgb(189, 189, 189);
	}
	QPushButton:pressed {
		background-color: rgb(189, 189, 189);
		border-color: rgb(150, 150, 150);
	}
	"""
)