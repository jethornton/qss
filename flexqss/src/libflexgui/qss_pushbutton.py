from functools import partial

STATES = ['n', 'h', 'p', 'c', 'd']
SIZE = ['min_width', 'max_width', 'min_height', 'max_height']
PADDING = ['padding_all', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left']
MARGIN = ['margin_all', 'margin_top', 'margin_right', 'margin_bottom', 'margin_left']

def startup(parent):
	parent.pb_stylesheet.setTabStopDistance(20.0)

	parent.pb_apply_style.clicked.connect(partial(create_stylesheet, parent))
	parent.pb_clear_style.clicked.connect(partial(clear_stylesheet, parent))

	# QPushButton
	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']

	for state in STATES: # color dialog connections
		getattr(parent, f'pb_{state}_fgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'pb_{state}_fgc_var', False)
		getattr(parent, f'pb_{state}_bgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'pb_{state}_bgc_var', False)
		getattr(parent, f'pb_{state}_bdt_cb').addItems(border_types)
		getattr(parent, f'pb_{state}_bdt_cb').currentIndexChanged.connect(lambda idx: border_changed(parent))
		getattr(parent, f'pb_{state}_bdc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'pb_{state}_bdc_var', False)
		setattr(parent, f'pb_{state}_style', False)

	for item in SIZE:
		getattr(parent, f'pb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in PADDING:
		getattr(parent, f'pb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in MARGIN:
		getattr(parent, f'pb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))

	parent.pb_font_picker.clicked.connect(parent.font_dialog)
	parent.pb_font_family = False
	parent.pb_font_size = False
	parent.pb_font_weight = False
	parent.pb_font_style = False
	parent.pb_font_italic = False


######### QPushButton Stylesheet #########

def create_stylesheet(parent):
	style = False

	# QPushButton normal pseudo-state
	if parent.pb_n_style:
		style = 'QPushButton {\n'

		# color
		if parent.pb_n_fgc_var:
			style += f'\tcolor: {parent.pb_n_fgc_var};\n'
		if parent.pb_n_bgc_var:
			style += f'\tbackground-color: {parent.pb_n_bgc_var};\n'

		# font
		if parent.pb_font_family:
			style += f'\tfont-family: {parent.pb_font_family};\n'
		if parent.pb_font_size:
			style += f'\tfont-size: {parent.pb_font_size}pt;\n'
		if parent.pb_font_weight:
			style += f'\tfont-weight: {parent.pb_font_weight};\n'

		# size
		if parent.pb_min_width_sb.value() > 0:
			style += f'\tmin-width: {parent.pb_min_width_sb.value()}px;\n'
		if parent.pb_max_width_sb.value() > 0:
			style += f'\tmax-width: {parent.pb_max_width_sb.value()}px;\n'
		if parent.pb_min_height_sb.value() > 0:
			style += f'\tmin-height: {parent.pb_min_height_sb.value()}px;\n'
		if parent.pb_max_height_sb.value() > 0:
			style += f'\tmax-height: {parent.pb_max_height_sb.value()}px;\n'

		# padding 
		if parent.pb_padding_all_sb.value() > 0:
			style += f'\tpadding: {parent.pb_padding_all_sb.value()};\n'
		elif parent.pb_padding_all_sb.value() == 0:
			if parent.pb_padding_top_sb.value() > 0:
				style += f'\tpadding-top: {parent.pb_padding_top_sb.value()};\n'
			if parent.pb_padding_right_sb.value() > 0:
				style += f'\tpadding-right: {parent.pb_padding_right_sb.value()};\n'
			if parent.pb_padding_bottom_sb.value() > 0:
				style += f'\tpadding-bottom: {parent.pb_padding_bottom_sb.value()};\n'
			if parent.pb_padding_left_sb.value() > 0:
				style += f'\tpadding-left: {parent.pb_padding_left_sb.value()};\n'

		# border
		if parent.pb_n_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.pb_n_bdt_cb.currentText()};\n'
			if parent.pb_n_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.pb_n_bdw_sb.value()}px;\n'
			if parent.pb_n_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.pb_n_bdr_sb.value()}px;\n'
		if parent.pb_n_bdc_var:
			style += f'\tborder-color: {parent.pb_n_bdc_var};\n'

		# margin
		if parent.pb_margin_all_sb.value() > 0:
			style += f'\tmargin: {parent.pb_margin_all_sb.value()};\n'
		elif parent.pb_margin_all_sb.value() == 0:
			if parent.pb_margin_top_sb.value() > 0:
				style += f'\tmargin-top: {parent.pb_margin_top_sb.value()};\n'
			if parent.pb_margin_right_sb.value() > 0:
				style += f'\tmargin-right: {parent.pb_margin_right_sb.value()};\n'
			if parent.pb_margin_bottom_sb.value() > 0:
				style += f'\tmargin-bottom: {parent.pb_margin_bottom_sb.value()};\n'
			if parent.pb_margin_left_sb.value() > 0:
				style += f'\tmargin-left: {parent.pb_margin_left_sb.value()};\n'

		style += '}' # End of QPushButton normal pseudo-state

	# QPushButton hover pseudo-state
	if parent.pb_h_style:
		if style: # style is not False
			style += '\n\nQPushButton:hover {\n'
		else:
			style = '\n\nQPushButton:hover {\n'

		# color
		if parent.pb_h_fgc_var:
			style += f'\tcolor: {parent.pb_h_fgc_var};\n'
		if parent.pb_h_bgc_var:
			style += f'\tbackground-color: {parent.pb_h_bgc_var};\n'

		# border
		if parent.pb_h_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.pb_h_bdt_cb.currentText()};\n'
			if parent.pb_h_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.pb_h_bdw_sb.value()}px;\n'
			if parent.pb_h_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.pb_h_bdr_sb.value()}px;\n'
		if parent.pb_h_bdc_var:
			style += f'\tborder-color: {parent.pb_h_bdc_var};\n'

		style += '}' # End of QPushButton hover pseudo-state

	# QPushButton pressed pseudo-state
	if parent.pb_p_style:
		if style: # style is not False
			style += '\n\nQPushButton:pressed {\n'
		else:
			style = '\n\nQPushButton:pressed {\n'

		# color
		if parent.pb_p_fgc_var:
			style += f'\tcolor: {parent.pb_p_fgc_var};\n'
		if parent.pb_p_bgc_var:
			style += f'\tbackground-color: {parent.pb_p_bgc_var};\n'

		# border
		if parent.pb_p_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.pb_p_bdt_cb.currentText()};\n'
			if parent.pb_p_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.pb_p_bdw_sb.value()}px;\n'
			if parent.pb_p_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.pb_p_bdr_sb.value()}px;\n'
		if parent.pb_p_bdc_var:
			style += f'\tborder-color: {parent.pb_p_bdc_var};\n'

		style += '}' # End of QPushButton pressed pseudo-state

	# QPushButton checked pseudo-state
	if parent.pb_c_style:
		if style: # style is not False
			style += '\n\nQPushButton:checked {\n'
		else:
			style = '\n\nQPushButton:checked {\n'

		# color
		if parent.pb_c_fgc_var:
			style += f'\tcolor: {parent.pb_c_fgc_var};\n'
		if parent.pb_c_bgc_var:
			style += f'\tbackground-color: {parent.pb_c_bgc_var};\n'

		# border
		if parent.pb_c_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.pb_c_bdt_cb.currentText()};\n'
			if parent.pb_c_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.pb_c_bdw_sb.value()}px;\n'
			if parent.pb_c_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.pb_c_bdr_sb.value()}px;\n'
		if parent.pb_c_bdc_var:
			style += f'\tborder-color: {parent.pb_c_bdc_var};\n'

		style += '}' # End of QPushButton checked pseudo-state

	# QPushButton disabled pseudo-state
	if parent.pb_d_style:
		if style: # style is not False
			style += '\n\nQPushButton:disabled {\n'
		else:
			style = '\n\nQPushButton:disabled {\n'

		# color
		if parent.pb_d_fgc_var:
			style += f'\tcolor: {parent.pb_d_fgc_var};\n'
		if parent.pb_d_bgc_var:
			style += f'\tbackground-color: {parent.pb_d_bgc_var};\n'

		# border
		if parent.pb_d_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.pb_d_bdt_cb.currentText()};\n'
			if parent.pb_d_bdw_sb.value() > 0:
				style += f'\tborder-width: {parent.pb_d_bdw_sb.value()}px;\n'
			if parent.pb_d_bdr_sb.value() > 0:
				style += f'\tborder-radius: {parent.pb_d_bdr_sb.value()}px;\n'
		if parent.pb_d_bdc_var:
			style += f'\tborder-color: {parent.pb_d_bdc_var};\n'

		style += '}' # End of QPushButton disabled pseudo-state


	# QPushButton build and apply the stylesheet
	parent.pb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.pb_stylesheet.appendPlainText(line)

		parent.pb_n.setStyleSheet(style)
		parent.pb_c.setStyleSheet(style)
		parent.pb_d.setStyleSheet(style)

def border_changed(parent):
	if parent.sender().currentText() != 'Select':
		state = parent.sender().objectName().split('_')[1]
		setattr(parent, f'pb_{state}_style', True)

def size_changed(parent): # size, padding and margin are only for normal state
	if parent.sender().value() > 0:
		parent.pb_n_style = True

def clear_stylesheet(parent):
	parent.pb_stylesheet.clear()
	parent.pb_n_style = False

	for state in STATES: # color dialog connections
		# set all the variables to False
		setattr(parent, f'pb_{state}_fgc_var', False)
		setattr(parent, f'pb_{state}_bgc_var', False)
		setattr(parent, f'pb_{state}_bdc_var', False)
		setattr(parent, f'pb_{state}_style', False)

		# clear all the colors
		getattr(parent, f'pb_{state}_fgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'pb_{state}_bgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'pb_{state}_bdc_lb').setStyleSheet('background-color: none;')

		# set spin boxes to 0
		getattr(parent, f'pb_{state}_bdr_sb').setValue(0)
		getattr(parent, f'pb_{state}_bdw_sb').setValue(0)

	# set the font variables to False
	parent.pb_font_family = False
	parent.pb_font_size = False
	parent.pb_font_weight = False
	parent.pb_font_style = False
	parent.pb_font_italic = False

	# set Size spin boxes to 0
	for item in SIZE:
		getattr(parent, f'pb_{item}_sb').setValue(0)
	for item in PADDING:
		getattr(parent, f'pb_{item}_sb').setValue(0)
	for item in MARGIN:
		getattr(parent, f'pb_{item}_sb').setValue(0)


