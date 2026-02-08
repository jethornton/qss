from functools import partial

STATES = ['n', 'h', 'p', 'c', 'd']
SIZE = ['min_width', 'max_width', 'min_height', 'max_height']
PADDING = ['padding_all', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left']
MARGIN = ['margin_all', 'margin_top', 'margin_right', 'margin_bottom', 'margin_left']

def startup(parent):
	parent.tb_stylesheet.setTabStopDistance(20.0)

	parent.tb_apply_style.clicked.connect(partial(create_stylesheet, parent))
	parent.tb_clear_style.clicked.connect(partial(clear_stylesheet, parent))

	# QToolButton
	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']

	for state in STATES: # color dialog connections
		getattr(parent, f'tb_{state}_fgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'tb_{state}_fgc_var', False)
		getattr(parent, f'tb_{state}_bgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'tb_{state}_bgc_var', False)
		getattr(parent, f'tb_{state}_bdt_cb').addItems(border_types)
		getattr(parent, f'tb_{state}_bdt_cb').currentIndexChanged.connect(lambda idx: border_changed(parent))
		getattr(parent, f'tb_{state}_bdc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'tb_{state}_bdc_var', False)
		setattr(parent, f'tb_{state}_style', False)

	for item in SIZE:
		getattr(parent, f'tb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in PADDING:
		getattr(parent, f'tb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in MARGIN:
		getattr(parent, f'tb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))

	parent.tb_font_picker.clicked.connect(parent.font_dialog)
	parent.tb_font_family = False
	parent.tb_font_size = False
	parent.tb_font_weight = False
	parent.tb_font_style = False
	parent.tb_font_italic = False


######### QToolButton Stylesheet #########

def create_stylesheet(parent):
	style = False

	# QToolButton normal pseudo-state
	if parent.tb_n_style:
		style = 'QToolButton {\n'

		# color
		if parent.tb_n_fgc_var:
			style += f'\tcolor: {parent.tb_n_fgc_var};\n'
		if parent.tb_n_bgc_var:
			style += f'\tbackground-color: {parent.tb_n_bgc_var};\n'

		# font
		if parent.tb_font_family:
			style += f'\tfont-family: {parent.tb_font_family};\n'
		if parent.tb_font_size:
			style += f'\tfont-size: {parent.tb_font_size}pt;\n'
		if parent.tb_font_weight:
			style += f'\tfont-weight: {parent.tb_font_weight};\n'

		# size
		if parent.tb_min_width_sb.value() > 0:
			style += f'\tmin-width: {parent.tb_min_width_sb.value()}px;\n'
		if parent.tb_max_width_sb.value() > 0:
			style += f'\tmax-width: {parent.tb_max_width_sb.value()}px;\n'
		if parent.tb_min_height_sb.value() > 0:
			style += f'\tmin-height: {parent.tb_min_height_sb.value()}px;\n'
		if parent.tb_max_height_sb.value() > 0:
			style += f'\tmax-height: {parent.tb_max_height_sb.value()}px;\n'

		# padding 
		if parent.tb_padding_all_sb.value() > 0:
			style += f'\tpadding: {parent.tb_padding_all_sb.value()};\n'
		elif parent.tb_padding_all_sb.value() == 0:
			if parent.tb_padding_top_sb.value() > 0:
				style += f'\tpadding-top: {parent.tb_padding_top_sb.value()};\n'
			if parent.tb_padding_right_sb.value() > 0:
				style += f'\tpadding-right: {parent.tb_padding_right_sb.value()};\n'
			if parent.tb_padding_bottom_sb.value() > 0:
				style += f'\tpadding-bottom: {parent.tb_padding_bottom_sb.value()};\n'
			if parent.tb_padding_left_sb.value() > 0:
				style += f'\tpadding-left: {parent.tb_padding_left_sb.value()};\n'

		# border
		if parent.tb_n_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.tb_n_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.tb_n_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.tb_n_bdr_sb.value()}px;\n'
		if parent.tb_n_bdc_var:
			style += f'\tborder-color: {parent.tb_n_bdc_var};\n'

		# margin
		if parent.tb_margin_all_sb.value() > 0:
			style += f'\tmargin: {parent.tb_margin_all_sb.value()};\n'
		elif parent.tb_margin_all_sb.value() == 0:
			if parent.tb_margin_top_sb.value() > 0:
				style += f'\tmargin-top: {parent.tb_margin_top_sb.value()};\n'
			if parent.tb_margin_right_sb.value() > 0:
				style += f'\tmargin-right: {parent.tb_margin_right_sb.value()};\n'
			if parent.tb_margin_bottom_sb.value() > 0:
				style += f'\tmargin-bottom: {parent.tb_margin_bottom_sb.value()};\n'
			if parent.tb_margin_left_sb.value() > 0:
				style += f'\tmargin-left: {parent.tb_margin_left_sb.value()};\n'

		style += '}' # End of QToolButton normal pseudo-state

	# QToolButton hover pseudo-state
	if parent.tb_h_style:
		if style: # style is not False
			style += '\n\nQToolButton:hover {\n'
		else:
			style = '\n\nQToolButton:hover {\n'

		# color
		if parent.tb_h_fgc_var:
			style += f'\tcolor: {parent.tb_h_fgc_var};\n'
		if parent.tb_h_bgc_var:
			style += f'\tbackground-color: {parent.tb_h_bgc_var};\n'

		# border
		if parent.tb_h_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.tb_h_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.tb_h_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.tb_h_bdr_sb.value()}px;\n'
		if parent.tb_h_bdc_var:
			style += f'\tborder-color: {parent.tb_h_bdc_var};\n'

		style += '}' # End of QToolButton hover pseudo-state

	# QToolButton pressed pseudo-state
	if parent.tb_p_style:
		if style: # style is not False
			style += '\n\nQToolButton:pressed {\n'
		else:
			style = '\n\nQToolButton:pressed {\n'

		# color
		if parent.tb_p_fgc_var:
			style += f'\tcolor: {parent.tb_p_fgc_var};\n'
		if parent.tb_p_bgc_var:
			style += f'\tbackground-color: {parent.tb_p_bgc_var};\n'

		# border
		if parent.tb_p_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.tb_p_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.tb_p_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.tb_p_bdr_sb.value()}px;\n'
		if parent.tb_p_bdc_var:
			style += f'\tborder-color: {parent.tb_p_bdc_var};\n'

		style += '}' # End of QToolButton pressed pseudo-state

	# QToolButton checked pseudo-state
	if parent.tb_c_style:
		if style: # style is not False
			style += '\n\nQToolButton:checked {\n'
		else:
			style = '\n\nQToolButton:checked {\n'

		# color
		if parent.tb_c_fgc_var:
			style += f'\tcolor: {parent.tb_c_fgc_var};\n'
		if parent.tb_c_bgc_var:
			style += f'\tbackground-color: {parent.tb_c_bgc_var};\n'

		# border
		if parent.tb_c_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.tb_c_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.tb_c_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.tb_c_bdr_sb.value()}px;\n'
		if parent.tb_c_bdc_var:
			style += f'\tborder-color: {parent.tb_c_bdc_var};\n'

		style += '}' # End of QToolButton checked pseudo-state

	# QToolButton disabled pseudo-state
	if parent.tb_d_style:
		if style: # style is not False
			style += '\n\nQToolButton:disabled {\n'
		else:
			style = '\n\nQToolButton:disabled {\n'

		# color
		if parent.tb_d_fgc_var:
			style += f'\tcolor: {parent.tb_d_fgc_var};\n'
		if parent.tb_d_bgc_var:
			style += f'\tbackground-color: {parent.tb_d_bgc_var};\n'

		# border
		if parent.tb_d_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.tb_d_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.tb_d_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.tb_d_bdr_sb.value()}px;\n'
		if parent.tb_d_bdc_var:
			style += f'\tborder-color: {parent.tb_d_bdc_var};\n'

		style += '}' # End of QToolButton disabled pseudo-state


	# QToolButton build and apply the stylesheet
	parent.tb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.tb_stylesheet.appendPlainText(line)

		parent.tb_n.setStyleSheet(style)
		parent.tb_c.setStyleSheet(style)
		parent.tb_d.setStyleSheet(style)

def border_changed(parent):
	if parent.sender().currentText() != 'Select':
		state = parent.sender().objectName().split('_')[1]
		setattr(parent, f'tb_{state}_style', True)

def size_changed(parent): # size, padding and margin are only for normal state
	if parent.sender().value() > 0:
		parent.tb_n_style = True

def clear_stylesheet(parent):

	parent.tb_n_style = False

	for state in STATES: # color dialog connections
		# set all the variables to False
		setattr(parent, f'tb_{state}_fgc_var', False)
		setattr(parent, f'tb_{state}_bgc_var', False)
		setattr(parent, f'tb_{state}_bdc_var', False)
		setattr(parent, f'tb_{state}_style', False)

		# clear all the colors
		getattr(parent, f'tb_{state}_fgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'tb_{state}_bgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'tb_{state}_bdc_lb').setStyleSheet('background-color: none;')

		# set spin boxes to 0
		getattr(parent, f'tb_{state}_bdr_sb').setValue(0)
		getattr(parent, f'tb_{state}_bdw_sb').setValue(0)

	# set the font variables to False
	parent.tb_font_family = False
	parent.tb_font_size = False
	parent.tb_font_weight = False
	parent.tb_font_style = False
	parent.tb_font_italic = False

	# set Size spin boxes to 0
	for item in SIZE:
		getattr(parent, f'tb_{item}_sb').setValue(0)
	for item in PADDING:
		getattr(parent, f'tb_{item}_sb').setValue(0)
	for item in MARGIN:
		getattr(parent, f'tb_{item}_sb').setValue(0)


