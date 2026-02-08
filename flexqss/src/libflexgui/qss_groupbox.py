from functools import partial

from PyQt6.QtWidgets import QComboBox, QSpinBox

STATES = ['n', 'h', 'p', 'c', 'd']
SIZE = ['min_width', 'max_width', 'min_height', 'max_height']
PADDING = ['padding_all', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left']
MARGIN = ['margin_all', 'margin_top', 'margin_right', 'margin_bottom', 'margin_left']

def startup(parent):
	parent.gb_stylesheet.setTabStopDistance(20.0)

	parent.gb_apply_style.clicked.connect(partial(create_stylesheet, parent))
	parent.gb_clear_style.clicked.connect(partial(clear_stylesheet, parent))

	# QGroupBox
	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']

	for state in STATES: # color dialog connections
		getattr(parent, f'gb_{state}_fgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'gb_{state}_fgc_var', False)
		getattr(parent, f'gb_{state}_bgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'gb_{state}_bgc_var', False)
		getattr(parent, f'gb_{state}_bdt_cb').addItems(border_types)
		getattr(parent, f'gb_{state}_bdt_cb').currentIndexChanged.connect(lambda idx: border_changed(parent))
		getattr(parent, f'gb_{state}_bdc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'gb_{state}_bdc_var', False)
		setattr(parent, f'gb_{state}_style', False)

	for item in SIZE:
		getattr(parent, f'gb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in PADDING:
		getattr(parent, f'gb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in MARGIN:
		getattr(parent, f'gb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))

	parent.gb_font_picker.clicked.connect(parent.font_dialog)
	parent.gb_font_family = False
	parent.gb_font_size = False
	parent.gb_font_weight = False
	parent.gb_font_style = False
	parent.gb_font_italic = False

	# Title items
	parent.gb_title_style = False
	origins = ['Select', 'margin', 'border', 'padding', 'content']
	parent.gb_origin_cb.addItems(origins)
	parent.gb_origin_cb.currentIndexChanged.connect(lambda idx: title_changed(parent))

	positions = ['Select', 'top left', 'top center', 'top right',
	'bottom left', 'bottom center', 'bottom right']
	parent.gb_position_cb.addItems(positions)
	parent.gb_position_cb.currentIndexChanged.connect(lambda idx: title_changed(parent))

	parent.gb_title_pad_left_sb.valueChanged.connect(lambda value: title_changed(parent))
	parent.gb_title_pad_right_sb.valueChanged.connect(lambda value: title_changed(parent))


######### QGroupBox Stylesheet #########

def create_stylesheet(parent):
	style = False

	# QGroupBox normal pseudo-state
	if parent.gb_n_style:
		style = 'QGroupBox {\n'

		# color
		if parent.gb_n_fgc_var:
			style += f'\tcolor: {parent.gb_n_fgc_var};\n'
		if parent.gb_n_bgc_var:
			style += f'\tbackground-color: {parent.gb_n_bgc_var};\n'

		# font
		if parent.gb_font_family:
			style += f'\tfont-family: {parent.gb_font_family};\n'
		if parent.gb_font_size:
			style += f'\tfont-size: {parent.gb_font_size}pt;\n'
		if parent.gb_font_weight:
			style += f'\tfont-weight: {parent.gb_font_weight};\n'

		# size
		if parent.gb_min_width_sb.value() > 0:
			style += f'\tmin-width: {parent.gb_min_width_sb.value()}px;\n'
		if parent.gb_max_width_sb.value() > 0:
			style += f'\tmax-width: {parent.gb_max_width_sb.value()}px;\n'
		if parent.gb_min_height_sb.value() > 0:
			style += f'\tmin-height: {parent.gb_min_height_sb.value()}px;\n'
		if parent.gb_max_height_sb.value() > 0:
			style += f'\tmax-height: {parent.gb_max_height_sb.value()}px;\n'

		# padding 
		if parent.gb_padding_all_sb.value() > 0:
			style += f'\tpadding: {parent.gb_padding_all_sb.value()};\n'
		elif parent.gb_padding_all_sb.value() == 0:
			if parent.gb_padding_top_sb.value() > 0:
				style += f'\tpadding-top: {parent.gb_padding_top_sb.value()};\n'
			if parent.gb_padding_right_sb.value() > 0:
				style += f'\tpadding-right: {parent.gb_padding_right_sb.value()};\n'
			if parent.gb_padding_bottom_sb.value() > 0:
				style += f'\tpadding-bottom: {parent.gb_padding_bottom_sb.value()};\n'
			if parent.gb_padding_left_sb.value() > 0:
				style += f'\tpadding-left: {parent.gb_padding_left_sb.value()};\n'

		# border
		if parent.gb_n_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.gb_n_bdt_cb.currentText()};\n'
			if parent.gb_n_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.gb_n_bdw_sb.value()}px;\n'
			if parent.gb_n_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.gb_n_bdr_sb.value()}px;\n'
		if parent.gb_n_bdc_var:
			style += f'\tborder-color: {parent.gb_n_bdc_var};\n'

		# margin
		if parent.gb_margin_all_sb.value() > 0:
			style += f'\tmargin: {parent.gb_margin_all_sb.value()};\n'
		elif parent.gb_margin_all_sb.value() == 0:
			if parent.gb_margin_top_sb.value() > 0:
				style += f'\tmargin-top: {parent.gb_margin_top_sb.value()};\n'
			if parent.gb_margin_right_sb.value() > 0:
				style += f'\tmargin-right: {parent.gb_margin_right_sb.value()};\n'
			if parent.gb_margin_bottom_sb.value() > 0:
				style += f'\tmargin-bottom: {parent.gb_margin_bottom_sb.value()};\n'
			if parent.gb_margin_left_sb.value() > 0:
				style += f'\tmargin-left: {parent.gb_margin_left_sb.value()};\n'

		style += '}\n' # End of QGroupBox normal pseudo-state

	# QGroupBox title
	if parent.gb_title_style:
		if style: # style is not False
			style += '\nQGroupBox::title {\n'
		else:
			style = '\nQGroupBox::title {\n'

		# Origin
		if parent.gb_origin_cb.currentText() != 'Select':
			style += f'subcontrol-origin: {parent.gb_origin_cb.currentText()};\n'

		# Position
		if parent.gb_position_cb.currentText() != 'Select':
			style += f'subcontrol-position: {parent.gb_position_cb.currentText()};\n'

		# Padding
		if parent.gb_title_pad_left_sb.value() > 0:
			style += f'\tpadding-left: {parent.gb_title_pad_left_sb.value()};\n'
		if parent.gb_title_pad_right_sb.value() > 0:
			style += f'\tpadding-right: {parent.gb_title_pad_right_sb.value()};\n'

		style += '}\n' # End of QGroupBox title


	# QGroupBox hover pseudo-state
	if parent.gb_h_style:
		if style: # style is not False
			style += '\nQGroupBox:hover {\n'
		else:
			style = '\nQGroupBox:hover {\n'

		# color
		if parent.gb_h_fgc_var:
			style += f'\tcolor: {parent.gb_h_fgc_var};\n'
		if parent.gb_h_bgc_var:
			style += f'\tbackground-color: {parent.gb_h_bgc_var};\n'

		# border
		if parent.gb_h_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.gb_h_bdt_cb.currentText()};\n'
			if parent.gb_h_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.gb_h_bdw_sb.value()}px;\n'
			if parent.gb_h_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.gb_h_bdr_sb.value()}px;\n'
		if parent.gb_h_bdc_var:
			style += f'\tborder-color: {parent.gb_h_bdc_var};\n'

		style += '}\n' # End of QGroupBox hover pseudo-state

	# QGroupBox pressed pseudo-state
	if parent.gb_p_style:
		if style: # style is not False
			style += '\nQGroupBox:pressed {\n'
		else:
			style = '\nQGroupBox:pressed {\n'

		# color
		if parent.gb_p_fgc_var:
			style += f'\tcolor: {parent.gb_p_fgc_var};\n'
		if parent.gb_p_bgc_var:
			style += f'\tbackground-color: {parent.gb_p_bgc_var};\n'

		# border
		if parent.gb_p_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.gb_p_bdt_cb.currentText()};\n'
			if parent.gb_p_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.gb_p_bdw_sb.value()}px;\n'
			if parent.gb_p_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.gb_p_bdr_sb.value()}px;\n'
		if parent.gb_p_bdc_var:
			style += f'\tborder-color: {parent.gb_p_bdc_var};\n'

		style += '}\n' # End of QGroupBox pressed pseudo-state

	# QGroupBox checked pseudo-state
	if parent.gb_c_style:
		if style: # style is not False
			style += '\nQGroupBox:checked {\n'
		else:
			style = '\nQGroupBox:checked {\n'

		# color
		if parent.gb_c_fgc_var:
			style += f'\tcolor: {parent.gb_c_fgc_var};\n'
		if parent.gb_c_bgc_var:
			style += f'\tbackground-color: {parent.gb_c_bgc_var};\n'

		# border
		if parent.gb_c_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.gb_c_bdt_cb.currentText()};\n'
			if parent.gb_c_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.gb_c_bdw_sb.value()}px;\n'
			if parent.gb_c_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.gb_c_bdr_sb.value()}px;\n'
		if parent.gb_c_bdc_var:
			style += f'\tborder-color: {parent.gb_c_bdc_var};\n'

		style += '}\n' # End of QGroupBox checked pseudo-state

	# QGroupBox disabled pseudo-state
	if parent.gb_d_style:
		if style: # style is not False
			style += '\n\nQGroupBox:disabled {\n'
		else:
			style = '\n\nQGroupBox:disabled {\n'

		# color
		if parent.gb_d_fgc_var:
			style += f'\tcolor: {parent.gb_d_fgc_var};\n'
		if parent.gb_d_bgc_var:
			style += f'\tbackground-color: {parent.gb_d_bgc_var};\n'

		# border
		if parent.gb_d_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.gb_d_bdt_cb.currentText()};\n'
			if parent.gb_d_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.gb_d_bdw_sb.value()}px;\n'
			if parent.gb_d_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.gb_d_bdr_sb.value()}px;\n'
		if parent.gb_d_bdc_var:
			style += f'\tborder-color: {parent.gb_d_bdc_var};\n'

		style += '}\n' # End of QGroupBox disabled pseudo-state

	# QGroupBox build and apply the stylesheet
	parent.gb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.gb_stylesheet.appendPlainText(line)

		parent.gb_n.setStyleSheet(style)
		parent.gb_c.setStyleSheet(style)
		parent.gb_d.setStyleSheet(style)

def border_changed(parent):
	if parent.sender().currentText() != 'Select':
		state = parent.sender().objectName().split('_')[1]
		setattr(parent, f'gb_{state}_style', True)

def size_changed(parent): # size, padding and margin are only for normal state
	if parent.sender().value() > 0:
		parent.gb_n_style = True

def title_changed(parent):
	sender = parent.sender()
	if isinstance(sender, QComboBox):
		if parent.sender().currentText() != 'Select':
			parent.gb_title_style = True
	elif isinstance(sender, QSpinBox):
		if parent.sender().value() > 0:
			parent.gb_title_style = True

def clear_stylesheet(parent):
	parent.gb_stylesheet.clear()
	parent.gb_n_style = False
	parent.gb_title_style = False

	for state in STATES: # color dialog connections
		# set all the variables to False
		setattr(parent, f'gb_{state}_fgc_var', False)
		setattr(parent, f'gb_{state}_bgc_var', False)
		setattr(parent, f'gb_{state}_bdc_var', False)
		setattr(parent, f'gb_{state}_style', False)

		# clear all the colors
		getattr(parent, f'gb_{state}_fgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'gb_{state}_bgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'gb_{state}_bdc_lb').setStyleSheet('background-color: none;')

		# set spin boxes to 0
		getattr(parent, f'gb_{state}_bdr_sb').setValue(0)
		getattr(parent, f'gb_{state}_bdw_sb').setValue(0)

	# set the font variables to False
	parent.gb_font_family = False
	parent.gb_font_size = False
	parent.gb_font_weight = False
	parent.gb_font_style = False
	parent.gb_font_italic = False

	# set Size spin boxes to 0
	for item in SIZE:
		getattr(parent, f'gb_{item}_sb').setValue(0)
	for item in PADDING:
		getattr(parent, f'gb_{item}_sb').setValue(0)
	for item in MARGIN:
		getattr(parent, f'gb_{item}_sb').setValue(0)


