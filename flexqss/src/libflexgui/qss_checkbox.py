from functools import partial

STATES = ['n', 'h', 'p', 'c', 'd']
SIZE = ['min_width', 'max_width', 'min_height', 'max_height']
PADDING = ['padding_all', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left']
MARGIN = ['margin_all', 'margin_top', 'margin_right', 'margin_bottom', 'margin_left']

def startup(parent):
	parent.cb_stylesheet.setTabStopDistance(20.0)

	parent.cb_apply_style.clicked.connect(partial(create_stylesheet, parent))
	parent.cb_clear_style.clicked.connect(partial(clear_stylesheet, parent))

	# QCheckBox
	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']

	for state in STATES: # color dialog connections
		getattr(parent, f'cb_{state}_fgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'cb_{state}_fgc_var', False)
		getattr(parent, f'cb_{state}_bgc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'cb_{state}_bgc_var', False)
		getattr(parent, f'cb_{state}_bdt_cb').addItems(border_types)
		getattr(parent, f'cb_{state}_bdt_cb').currentIndexChanged.connect(lambda idx: border_changed(parent))
		getattr(parent, f'cb_{state}_bdc_pb').clicked.connect(parent.color_dialog)
		setattr(parent, f'cb_{state}_bdc_var', False)
		setattr(parent, f'cb_{state}_style', False)

	for item in SIZE:
		getattr(parent, f'cb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in PADDING:
		getattr(parent, f'cb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))
	for item in MARGIN:
		getattr(parent, f'cb_{item}_sb').valueChanged.connect(lambda value: size_changed(parent))

	parent.cb_font_picker.clicked.connect(parent.font_dialog)
	parent.cb_font_family = False
	parent.cb_font_size = False
	parent.cb_font_weight = False
	parent.cb_font_style = False
	parent.cb_font_italic = False


######### QCheckBox Stylesheet #########

def create_stylesheet(parent):
	style = False

	# QCheckBox normal pseudo-state
	if parent.cb_n_style:
		style = 'QCheckBox {\n'

		# color
		if parent.cb_n_fgc_var:
			style += f'\tcolor: {parent.cb_n_fgc_var};\n'
		if parent.cb_n_bgc_var:
			style += f'\tbackground-color: {parent.cb_n_bgc_var};\n'

		# font
		if parent.cb_font_family:
			style += f'\tfont-family: {parent.cb_font_family};\n'
		if parent.cb_font_size:
			style += f'\tfont-size: {parent.cb_font_size}pt;\n'
		if parent.cb_font_weight:
			style += f'\tfont-weight: {parent.cb_font_weight};\n'

		# size
		if parent.cb_min_width_sb.value() > 0:
			style += f'\tmin-width: {parent.cb_min_width_sb.value()}px;\n'
		if parent.cb_max_width_sb.value() > 0:
			style += f'\tmax-width: {parent.cb_max_width_sb.value()}px;\n'
		if parent.cb_min_height_sb.value() > 0:
			style += f'\tmin-height: {parent.cb_min_height_sb.value()}px;\n'
		if parent.cb_max_height_sb.value() > 0:
			style += f'\tmax-height: {parent.cb_max_height_sb.value()}px;\n'

		# padding 
		if parent.cb_padding_all_sb.value() > 0:
			style += f'\tpadding: {parent.cb_padding_all_sb.value()};\n'
		elif parent.cb_padding_all_sb.value() == 0:
			if parent.cb_padding_top_sb.value() > 0:
				style += f'\tpadding-top: {parent.cb_padding_top_sb.value()};\n'
			if parent.cb_padding_right_sb.value() > 0:
				style += f'\tpadding-right: {parent.cb_padding_right_sb.value()};\n'
			if parent.cb_padding_bottom_sb.value() > 0:
				style += f'\tpadding-bottom: {parent.cb_padding_bottom_sb.value()};\n'
			if parent.cb_padding_left_sb.value() > 0:
				style += f'\tpadding-left: {parent.cb_padding_left_sb.value()};\n'

		# border
		if parent.cb_n_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.cb_n_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.cb_n_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.cb_n_bdr_sb.value()}px;\n'
		if parent.cb_n_bdc_var:
			style += f'\tborder-color: {parent.cb_n_bdc_var};\n'

		# margin
		if parent.cb_margin_all_sb.value() > 0:
			style += f'\tmargin: {parent.cb_margin_all_sb.value()};\n'
		elif parent.cb_margin_all_sb.value() == 0:
			if parent.cb_margin_top_sb.value() > 0:
				style += f'\tmargin-top: {parent.cb_margin_top_sb.value()};\n'
			if parent.cb_margin_right_sb.value() > 0:
				style += f'\tmargin-right: {parent.cb_margin_right_sb.value()};\n'
			if parent.cb_margin_bottom_sb.value() > 0:
				style += f'\tmargin-bottom: {parent.cb_margin_bottom_sb.value()};\n'
			if parent.cb_margin_left_sb.value() > 0:
				style += f'\tmargin-left: {parent.cb_margin_left_sb.value()};\n'

		style += '}' # End of QCheckBox normal pseudo-state

	# QCheckBox hover pseudo-state
	if parent.cb_h_style:
		if style: # style is not False
			style += '\n\nQCheckBox:hover {\n'
		else:
			style = '\n\nQCheckBox:hover {\n'

		# color
		if parent.cb_h_fgc_var:
			style += f'\tcolor: {parent.cb_h_fgc_var};\n'
		if parent.cb_h_bgc_var:
			style += f'\tbackground-color: {parent.cb_h_bgc_var};\n'

		# border
		if parent.cb_h_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.cb_h_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.cb_h_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.cb_h_bdr_sb.value()}px;\n'
		if parent.cb_h_bdc_var:
			style += f'\tborder-color: {parent.cb_h_bdc_var};\n'

		style += '}' # End of QCheckBox hover pseudo-state

	# QCheckBox pressed pseudo-state
	if parent.cb_p_style:
		if style: # style is not False
			style += '\n\nQCheckBox:pressed {\n'
		else:
			style = '\n\nQCheckBox:pressed {\n'

		# color
		if parent.cb_p_fgc_var:
			style += f'\tcolor: {parent.cb_p_fgc_var};\n'
		if parent.cb_p_bgc_var:
			style += f'\tbackground-color: {parent.cb_p_bgc_var};\n'

		# border
		if parent.cb_p_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.cb_p_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.cb_p_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.cb_p_bdr_sb.value()}px;\n'
		if parent.cb_p_bdc_var:
			style += f'\tborder-color: {parent.cb_p_bdc_var};\n'

		style += '}' # End of QCheckBox pressed pseudo-state

	# QCheckBox checked pseudo-state
	if parent.cb_c_style:
		if style: # style is not False
			style += '\n\nQCheckBox:checked {\n'
		else:
			style = '\n\nQCheckBox:checked {\n'

		# color
		if parent.cb_c_fgc_var:
			style += f'\tcolor: {parent.cb_c_fgc_var};\n'
		if parent.cb_c_bgc_var:
			style += f'\tbackground-color: {parent.cb_c_bgc_var};\n'

		# border
		if parent.cb_c_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.cb_c_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.cb_c_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.cb_c_bdr_sb.value()}px;\n'
		if parent.cb_c_bdc_var:
			style += f'\tborder-color: {parent.cb_c_bdc_var};\n'

		style += '}' # End of QCheckBox checked pseudo-state

	# QCheckBox disabled pseudo-state
	if parent.cb_d_style:
		if style: # style is not False
			style += '\n\nQCheckBox:disabled {\n'
		else:
			style = '\n\nQCheckBox:disabled {\n'

		# color
		if parent.cb_d_fgc_var:
			style += f'\tcolor: {parent.cb_d_fgc_var};\n'
		if parent.cb_d_bgc_var:
			style += f'\tbackground-color: {parent.cb_d_bgc_var};\n'

		# border
		if parent.cb_d_bdt_cb.currentText() != 'Select':
			style += f'\tborder-style: {parent.cb_d_bdt_cb.currentText()};\n'
			style += f'\tborder-width: {parent.cb_d_bdw_sb.value()}px;\n'
			style += f'\tborder-radius: {parent.cb_d_bdr_sb.value()}px;\n'
		if parent.cb_d_bdc_var:
			style += f'\tborder-color: {parent.cb_d_bdc_var};\n'

		style += '}' # End of QCheckBox disabled pseudo-state


	# QCheckBox build and apply the stylesheet
	parent.cb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.cb_stylesheet.appendPlainText(line)

		parent.cb_n.setStyleSheet(style)
		parent.cb_c.setStyleSheet(style)
		parent.cb_d.setStyleSheet(style)

def border_changed(parent):
	if parent.sender().currentText() != 'Select':
		state = parent.sender().objectName().split('_')[1]
		setattr(parent, f'cb_{state}_style', True)

def size_changed(parent): # size, padding and margin are only for normal state
	if parent.sender().value() > 0:
		parent.cb_n_style = True

def clear_stylesheet(parent):

	parent.cb_n_style = False

	for state in STATES: # color dialog connections
		# set all the variables to False
		setattr(parent, f'cb_{state}_fgc_var', False)
		setattr(parent, f'cb_{state}_bgc_var', False)
		setattr(parent, f'cb_{state}_bdc_var', False)
		setattr(parent, f'cb_{state}_style', False)

		# clear all the colors
		getattr(parent, f'cb_{state}_fgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'cb_{state}_bgc_lb').setStyleSheet('background-color: none;')
		getattr(parent, f'cb_{state}_bdc_lb').setStyleSheet('background-color: none;')

		# set spin boxes to 0
		getattr(parent, f'cb_{state}_bdr_sb').setValue(0)
		getattr(parent, f'cb_{state}_bdw_sb').setValue(0)

	# set the font variables to False
	parent.cb_font_family = False
	parent.cb_font_size = False
	parent.cb_font_weight = False
	parent.cb_font_style = False
	parent.cb_font_italic = False

	# set Size spin boxes to 0
	for item in SIZE:
		getattr(parent, f'cb_{item}_sb').setValue(0)
	for item in PADDING:
		getattr(parent, f'cb_{item}_sb').setValue(0)
	for item in MARGIN:
		getattr(parent, f'cb_{item}_sb').setValue(0)


