# importing required libraries
from base64 import urlsafe_b64decode, urlsafe_b64encode
import colorsys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
try:
    from PyQt5.QtWebEngineWidgets import *
except:
    from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from robin_stocks import robinhood as rh
import os
from os import popen as cmd
import sys
from time import sleep as delay
from codecs import encode, decode
import sys
try:
	def alert(text):
		print(text)
	if __name__ != "__main__":
		exit()
	else:
		pass
	directory = str(os.getcwd()).replace("\\", "/")
	source = directory + "/options.html"

	def hex_to_rgb(color):
		h = str(color).lstrip('#')
		output = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
		return  output

	def find_all(string, case):
		position = 0
		lp = []
		for s in string:
			if ord(s) == ord(case):
				lp.append(position)
			position += 1
		return lp
	try:
		saved_li = open(directory + "/saved_pw.txt", "w+")
	except:
		saved_li = None
	def login(username = None, password = None):
		try:
			if saved_li != None:
				saved_li.write(str(username) + "\n" + str(password))
			else:
				while True:
					username = input("USERNAME:\t")
					if username == "":
						continue
					else:
						pass
					password = input("PASSWORD:\t")
					if password == "":
						continue
					else:
						pass
					break
		except:
			while True:
				username = input("USERNAME:\t")
				if username == "":
					pass
				else:
					continue
				password = input("PASSWORD:\t")
				if password == "":
					pass
				else:
					continue
				break
		rh.login(username = username, password = password, expiresIn = 86400, scope = "internal", mfa_code=None, pickle_name="")

	def update(ticker = None):
		global title
		title = ticker.upper()
		while True:
			try:
				if saved_li != None:
					read = saved_li.read()
					if read == "":
						username = input("USERNAME:\t")
						password = input("PASSWORD:\t")
						saved_li.write(username + "\n" + password)
					else:
						lines = read.splitlines()
						username = lines[0]
						password = lines[1]
				else:
					login()
					break
				login(username = username, password = password)
				break
			except Exception as e:
				print(e)
				alert("A Robinhood account is needed to activate this web browser. Go to https://robinhood.com/ to set up an account.")
				while True:
					delay(1)
		style = """
	table {
	font-family: arial, sans-serif;
	border-collapse: collapse;
	width: 100%;
	}

	td, th {
	border: 1px solid #dddddd;
	text-align: left;
	padding: 8px;
	}

	tr:nth-child(even) {
	background-color: #dddddd;
	}
	tr:hover {background-color: #D6EEEE;}
	body {
	position: relative;
	background-attachment: absolute;
	background-color: rgba(50, 255, 50);
	font-family: sans-serif;
	}
	.block {
	border: 0.1em solid #b1b1b1;
	border-radius: 1em 1em 1em 1em;
	padding: 1em;
	margin-left: 1em;
	margin-right: 1em;
	margin-top: 1em;
	margin-bottom: 1em;
	background-color: rgba(50, 50, 50, 0.75);
	color: #b1ffb1;
	width: 20em;
	height: 20em;
	}
	h1 {
	font-size: 3em;
	color: #ffffff;
	}
	h2 {
	font-size: 2em;
	color: #ffffff;
	}
	h3 {
	font-size: 1em;
	color: #ffffff;
	}
	#scroll {
	position: scroll;
	}

	.text {
	background-color: rgb(50, 255, 50);
	border-radius: 0.1em 0.1em 0.1em 0.1em;
		position: relative;
		text-align: center;
		top: 0%; 
		right: 0%;
		transform: translate(0%,-0%);
		text-transform: uppercase;
		font-family: verdana;
		font-size: 7em;
		font-weight: 700;
		color: #ffffff;
		text-shadow: 1px 1px 1px #919191,
			1px 2px 1px #919191,
			1px 3px 1px #919191,
			1px 4px 1px #919191,
			1px 5px 1px #919191,
			1px 6px 1px #919191,
			1px 7px 1px #919191,
			1px 8px 1px #919191,
			1px 9px 1px #919191,
			1px 10px 1px #919191,
		1px 18px 6px rgba(16,16,16,0.4),
		1px 22px 10px rgba(16,16,16,0.2),
		1px 25px 35px rgba(16,16,16,0.2),
		1px 30px 60px rgba(16,16,16,0.4);
	}
	"""
		hexs = find_all(style, "#")
		for h in hexs:
			try:
				case = style[h:h+7]
				rgb = "rgb" + str(hex_to_rgb(case)) + ""
				style = style.replace(case, rgb)
			except:
				style = style.replace(case, case)
		while True:
			try:
				if ticker == None:
					ticker = str(input("TICKER:\t")).upper()
				historicals = rh.get_stock_historicals([ticker], interval='hour', span='day', bounds='regular', info=None)
				if historicals == [None]:
					return "error"
				else:
					break
			except:
				pass
		options = rh.options.find_tradable_options(ticker, expirationDate=None, strikePrice=None, optionType=None, info=None)
		text = ""
		for option in options:
			text += """<tr>\n"""
			for attr in option:
				if ("expiration_date" in attr) or ("strike_price" in attr) or ("state" in attr):
					text += """<td onclick="alert('""" + str(attr) + """:\t""" + str(option[attr]) + """')">""" + str(option[attr]) + """</td>\n"""
			text += "</tr>\n"
				
		file = open(source.replace("options", str(title)), "w")
		script = """
		"""
		file.writelines("""
	<html>
	<head>
	<title>
	{TITLE}
	</title>
	</head>
	<body>
	<div>
	<h1>
	<div class = 'text'>
	{TICKER}
	</div>
	</h1>
	</div>
	<div id = 'scroll'>
	<table id="sortMe" class="table">
	<tr>
	<th>
	Expiration Date
	</th>
	<th>
	State
	</th>
	<th>
	Strike Price
	</th>
	</tr>
	{OPTIONS}
	</table>
	</div>
	</body>
	<script type="text/javascript" language="JavaScript">
	{SCRIPT}
	</script>
	<style>
	{STYLE}
	</style>
	</html>
	""".format(TITLE = title, TICKER = str(ticker).upper(), OPTIONS = text, SCRIPT = script, STYLE = style))
	update(ticker = "CCL")

	# main window

	class MainWindow(QMainWindow):

		# constructor
		def __init__(self, *args, **kwargs):
			super(MainWindow, self).__init__(*args, **kwargs)
			self.title = "SecureWeb"

			# creating a tab widget
			self.tabs = QTabWidget()

			# making document mode true
			self.tabs.setDocumentMode(True)

			# adding action when double clicked
			self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

			# adding action when tab is changed
			self.tabs.currentChanged.connect(self.current_tab_changed)

			# making tabs closeable
			self.tabs.setTabsClosable(True)

			# adding action when tab close is requested
			self.tabs.tabCloseRequested.connect(self.close_current_tab)

			# making tabs as central widget
			self.setCentralWidget(self.tabs)

			# creating a status bar
			self.status = QStatusBar()

			# setting status bar to the main window
			self.setStatusBar(self.status)

			# creating a tool bar for navigation
			navtb = QToolBar("Navigation")

			# adding tool bar tot he main window
			self.addToolBar(navtb)

			# creating back action
			back_btn = QAction(chr(27), self)

			# setting status tip
			back_btn.setStatusTip("Back to previous page")

			# adding action to back button
			# making current tab to go back
			back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

			# adding this to the navigation tool bar
			navtb.addAction(back_btn)

			# similarly adding next button
			next_btn = QAction(chr(26), self)
			next_btn.setStatusTip("Forward to next page")
			next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
			navtb.addAction(next_btn)

			# similarly adding reload button
			reload_btn = QAction(chr(128259), self)
			reload_btn.setStatusTip("Reload page")
			reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
			navtb.addAction(reload_btn)

			# creating home action
			home_btn = QAction("Home", self)
			home_btn.setStatusTip("Go home")

			# adding action to home button
			home_btn.triggered.connect(self.navigate_home)
			navtb.addAction(home_btn)

			# similarly adding reload button
			reload_btn = QAction("+", self)
			reload_btn.setStatusTip("New Tab")
			reload_btn.triggered.connect(lambda: self.add_new_tab())
			navtb.addAction(reload_btn)

			# adding a separator
			navtb.addSeparator()

			# creating a line edit widget for URL
			self.urlbar = QLineEdit()

			# adding action to line edit when return key is pressed
			self.urlbar.returnPressed.connect(self.navigate_to_url)

			# adding line edit to tool bar
			navtb.addWidget(self.urlbar)

			# similarly adding stop action
			stop_btn = QAction("Stop", self)
			stop_btn.setStatusTip("Stop loading current page")
			stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
			navtb.addAction(stop_btn)

			# similarly adding full screen action
			fs_btn = QAction("\U000026F6", self)
			fs_btn.setStatusTip("Toggle fullscreen")
			fs_btn.triggered.connect(lambda:
						self.toggleFullScreen()
						)
			navtb.addAction(fs_btn)

			# creating first tab
			self.add_new_tab(QUrl("file:" + source.replace("options", str(title))), 'Homepage')

			# showing all the components
			self.show()

			# setting window title
			self.setWindowTitle("SecureWeb")

			
		def toggleFullScreen(self):
			if self.isFullScreen() == True:
				self.showNormal()
			elif self.isFullScreen() == False:
				self.showFullScreen()
		def run_js(self, script):
			browser = QWebEngineView()
			page = browser.page()
			page.runJavaScript(script)

		# method for adding new tab
		def add_new_tab(self, qurl = None, label ="Blank"):
			try:
				# if url is blank
				# if qurl is None:
				# creating a google url
				qurl = QUrl("file:" + source.replace("options", str(title)))
				# creating a QWebEngineView objec
				browser = QWebEngineView()
				browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
				# setting url to browser
				browser.setUrl(qurl)
			except:
				pass
			# setting url to browser
			browser.setUrl(qurl)

			# setting tab index
			i = self.tabs.addTab(browser, label)
			self.tabs.setCurrentIndex(i)

			# adding action to the browser when url is changed
			# update the url
			browser.urlChanged.connect(lambda qurl, browser = browser:
									self.update_urlbar(qurl, browser))

			# adding action to the browser when loading is finished
			# set the tab title
			browser.loadFinished.connect(lambda _, i = i, browser = browser:
										self.tabs.setTabText(i, browser.page().title()))
			browser.page().fullScreenRequested.connect(lambda request, browser=browser: self.handle_fullscreen_requested(request, browser))

		def handle_fullscreen_requested(self, request, browser):
			request.accept()
			if request.toggleOn():
				self.showFullScreen()
				try:
					self.tabs.tabBar().hide()
				except:
					pass
				try:
					self.statusBar().hide()
				except:
					pass
				try:
					self.navtb.hide()
				except:
					pass
			else:
				self.showNormal()
				try:
					self.tabs.tabBar().show()
				except:
					pass
				try:
					self.statusBar().show()
				except:
					pass
				try:
					self.navtb.show()
				except:
					pass

		# when double clicked is pressed on tabs
		def tab_open_doubleclick(self, i):

			# checking index i.e
			# No tab under the click
			if i == -1:
				# creating a new tab
				self.add_new_tab()

		# when tab is changed
		def current_tab_changed(self, i):

			# get the curl
			qurl = self.tabs.currentWidget().url()

			# update the url
			self.update_urlbar(qurl, self.tabs.currentWidget())

			# update the title
			self.update_title(self.tabs.currentWidget())

		# when tab is closed
		def close_current_tab(self, i):

			# if there is only one tab
			if self.tabs.count() < 2:
				# do nothing
				return

			# else remove the tab
			self.tabs.removeTab(i)

		# method for updating the title
		def update_title(self, browser):

			# if signal is not from the current tab
			if browser != self.tabs.currentWidget():
				# do nothing
				return

			# get the page title
			title = self.tabs.currentWidget().page().title()

			# set the window title
			self.setWindowTitle("% s - SecureWeb" % title)

		# action to go to home
		def navigate_home(self):

			# go to google
			self.tabs.currentWidget().setUrl(QUrl("file:" + source.replace("options", str(title))))

		# method for navigate to url
		def navigate_to_url(self):

			# get the line edit text
			# convert it to QUrl object
			q = QUrl(self.urlbar.text())


			# set the url
			if "." in self.urlbar.text():
				# if scheme is blank
				if q.scheme() == "":
					# set scheme
					q.setScheme("http")
				self.tabs.currentWidget().setUrl(q)
			else:
				up = update(ticker = self.urlbar.text())
				if up == "error":
						search = QUrl("http://www.google.com/search?q=" + str(q.toString()))
						self.tabs.currentWidget().setUrl(search)
				else:
					try:
						self.tabs.currentWidget().setUrl(QUrl("file:" + source.replace("options", str(title))))
					except Exception as e:
						print(e)
							
		# method to update the url
		def update_urlbar(self, q, browser = None):

			# If this signal is not from the current tab, ignore
			if browser != self.tabs.currentWidget():

				return

			# set text to the url bar
			self.urlbar.setText(q.toString())

			# set cursor position
			self.urlbar.setCursorPosition(0)
	# creating a PyQt5 application
	app = QApplication(sys.argv)
	clipboard = app.clipboard()

	# setting name to the application
	app.setApplicationName("SecureWeb")
	app.setApplicationDisplayName("SecureWeb")
	app.setApplicationVersion("1.0")
	app.setDesktopFileName("SecureWeb")

	desktop = app.desktop()

	"""for d in dir(desktop):
			if "set".upper() in d.upper():
					print("desktop.{d}".format(d=d))"""

	desktop.setShortcutEnabled(True)
	desktop.setShortcutAutoRepeat(True)
	desktop.setUpdatesEnabled(True)
	app.setWheelScrollLines(4)

	# creating MainWindow object
	window = MainWindow()
	#window.showFullScreen()
	window.setShortcutEnabled(True)
	window.showMaximized()
	window.unifiedTitleAndToolBarOnMac()
	window.setAnimated(True)

	app.installTranslator(QTranslator(window))
	cursor = window.cursor()
	#get cursor position
	def get_cursor_pos():
			hotspot = cursor.hotSpot()
			x = getattr(hotspot, "x")
			y = getattr(hotspot, "y")
			return (x(), y())

	#window settings
	window.setDockNestingEnabled(True)
	window.setAutoFillBackground(True)
	window.setDocumentMode(True)
	window.setAcceptDrops(True)
	window.setAnimated(True)
	window.setVisible(True)
	window.blockSignals(False)

	#app settings
	app.blockSignals(False)
	app.setAutoSipEnabled(True)
	app.sync()
	icon = QIcon("C:\\Users\\4kenn\\OneDrive\\Desktop\\SecureWeb\\SecureWeb.jpg")
	app.setWindowIcon(icon)
	app.desktopSettingsAware()
	app.setSetuidAllowed(True)
	app.setFont(QFont("Calibri Light", 9, 1, False))
	app.setAutoSipEnabled(True)
	screens = app.screens()
	for screen in screens:
			orientation = screen.orientation()
	a, b = pow(2, 32, mod=255), 2147483647
	spectrum = min(a, b)
	app.setColorSpec(spectrum)
	app.setQuitLockEnabled(False)
	app.setQuitOnLastWindowClosed(True)
	app.setDesktopSettingsAware(True)
	class dialog(QMainWindow):
		def __init__(self, title, text):
			"""super().__init__()
			dlg = QMessageBox(self)
			dlg.setWindowTitle(title)
			dlg.setText(text)
			button = dlg.exec()"""
			return 0

	def about():
			return app.aboutQt()

	style = str("""



	/*
	* The MIT License (MIT)
	*
	* Copyright (c) <2013-2014> <Colin Duquesnoy>
	* Copyright (c) <2017> <Michell Stuttgart>
	*
	* Permission is hereby granted, free of charge, to any person obtaining a copy
	* of this software and associated documentation files (the "Software"), to deal
	* in the Software without restriction, including without limitation the rights
	* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	* copies of the Software, and to permit persons to whom the Software is
	* furnished to do so, subject to the following conditions:

	* The above copyright notice and this permission notice shall be included in
	* all copies or substantial portions of the Software.

	* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	* THE SOFTWARE.
	*/
	QToolTip
	{
		border: 1px solid black;
		background-color: #D1DBCB;
		padding: 1px;
		border-radius: 3px;
		opacity: 100;
	}

	QWidget
	{
		color: #b1b1b1;
		background-color: #323232;
		selection-background-color:#323232;
		selection-color: black;
		background-clip: border;
		border-image: none;
		border: 0px transparent black;
		outline: 0;
	}

	QWidget:item:hover
	{
		background-color: #D1DBCB;
		color: black;
	}

	QWidget:item:selected
	{
		background-color: #D1DBCB;
		border: 0px
	}

	QCheckBox
	{
		spacing: 5px;
		outline: none;
		color: #eff0f1;
		margin-bottom: 2px;
	}

	QCheckBox:disabled
	{
		color: #76797C;
	}

	QCheckBox::indicator,QGroupBox::indicator
	{
		width: 18px;
		height: 18px;
	}

	QGroupBox::indicator
	{
		margin-left: 2px;
	}

	QCheckBox::indicator:unchecked
	{
		image: url(:/qss_icons/rc/checkbox_unchecked.png);
	}

	QCheckBox::indicator:unchecked:hover,
	QCheckBox::indicator:unchecked:focus,
	QCheckBox::indicator:unchecked:pressed,
	QGroupBox::indicator:unchecked:hover,
	QGroupBox::indicator:unchecked:focus,
	QGroupBox::indicator:unchecked:pressed
	{
	border: none;
		image: url(:/qss_icons/rc/checkbox_unchecked_focus.png);
	}

	QCheckBox::indicator:checked
	{
		image: url(:/qss_icons/rc/checkbox_checked.png);
	}

	QCheckBox::indicator:checked:hover,
	QCheckBox::indicator:checked:focus,
	QCheckBox::indicator:checked:pressed,
	QGroupBox::indicator:checked:hover,
	QGroupBox::indicator:checked:focus,
	QGroupBox::indicator:checked:pressed
	{
		border: none;
		image: url(:/qss_icons/rc/checkbox_checked_focus.png);
	}


	QCheckBox::indicator:indeterminate
	{
		image: url(:/qss_icons/rc/checkbox_indeterminate.png);
	}

	QCheckBox::indicator:indeterminate:focus,
	QCheckBox::indicator:indeterminate:hover,
	QCheckBox::indicator:indeterminate:pressed
	{
		image: url(:/qss_icons/rc/checkbox_indeterminate_focus.png);
	}

	QCheckBox::indicator:checked:disabled,
	QGroupBox::indicator:checked:disabled
	{
		image: url(:/qss_icons/rc/checkbox_checked_disabled.png);
	}

	QCheckBox::indicator:unchecked:disabled,
	QGroupBox::indicator:unchecked:disabled
	{
		image: url(:/qss_icons/rc/checkbox_unchecked_disabled.png);
	}

	QRadioButton
	{
		spacing: 5px;
		outline: none;
		color: #eff0f1;
		margin-bottom: 2px;
	}

	QRadioButton:disabled
	{
		color: #76797C;
	}
	QRadioButton::indicator
	{
		width: 21px;
		height: 21px;
	}

	QRadioButton::indicator:unchecked
	{
		image: url(:/qss_icons/rc/radio_unchecked.png);
	}


	QRadioButton::indicator:unchecked:hover,
	QRadioButton::indicator:unchecked:focus,
	QRadioButton::indicator:unchecked:pressed
	{
		border: none;
		outline: none;
		image: url(:/qss_icons/rc/radio_unchecked_focus.png);
	}

	QRadioButton::indicator:checked
	{
		border: none;
		outline: none;
		image: url(:/qss_icons/rc/radio_checked.png);
	}

	QRadioButton::indicator:checked:hover,
	QRadioButton::indicator:checked:focus,
	QRadioButton::indicator:checked:pressed
	{
		border: none;
		outline: none;
		image: url(:/qss_icons/rc/radio_checked_focus.png);
	}

	QRadioButton::indicator:checked:disabled
	{
		outline: none;
		image: url(:/qss_icons/rc/radio_checked_disabled.png);
	}

	QRadioButton::indicator:unchecked:disabled
	{
		image: url(:/qss_icons/rc/radio_unchecked_disabled.png);
	}


	QMenuBar
	{
		background-color: #323232;
		color: #D1DBCB;
	}

	QMenuBar::item
	{
		background-color: #323232;
		background: transparent;
		/* padding: 2px 20px 2px 20px; */
	}

	QMenuBar::item:selected
	{
		background: transparent;
		/* border: 1px solid #76797C; */
	}

	QMenuBar::item:pressed
	{
		border: 0px solid #76797C;
		background-color: #D1DBCB;
		color: #000;
		margin-bottom:-1px;
		padding-bottom:1px;
	}

	QMenu
	{
		background-color: #323232;
		/* border: 1px solid #76797C; */
		color: #eff0f1;
		/*margin: 2px; */
	}

	QMenu::icon
	{
		/*margin: 5px;*/
	}

	QMenu::item
	{
		padding: 2px 30px 2px 30px;
		/*margin-left: 5px;*/
		border: 1px solid transparent; /* reserve space for selection border */
	}

	QMenu::item:selected
	{
		color: #000000;
	}

	QMenu::separator {
		height: 2px;
		background: #D1DBCB;
		margin-left: 10px;
		margin-right: 5px;
	}

	QMenu::indicator {
		width: 18px;
		height: 18px;
	}

	/* non-exclusive indicator = check box style indicator
	(see QActionGroup::setExclusive) */
	QMenu::indicator:non-exclusive:unchecked {
		image: url(:/qss_icons/rc/checkbox_unchecked.png);
	}

	QMenu::indicator:non-exclusive:unchecked:selected {
		image: url(:/qss_icons/rc/checkbox_unchecked_disabled.png);
	}

	QMenu::indicator:non-exclusive:checked {
		image: url(:/qss_icons/rc/checkbox_checked.png);
	}

	QMenu::indicator:non-exclusive:checked:selected {
		image: url(:/qss_icons/rc/checkbox_checked_disabled.png);
	}

	/* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
	QMenu::indicator:exclusive:unchecked {
		image: url(:/qss_icons/rc/radio_unchecked.png);
	}

	QMenu::indicator:exclusive:unchecked:selected {
		image: url(:/qss_icons/rc/radio_unchecked_disabled.png);
	}

	QMenu::indicator:exclusive:checked {
		image: url(:/qss_icons/rc/radio_checked.png);
	}

	QMenu::indicator:exclusive:checked:selected {
		image: url(:/qss_icons/rc/radio_checked_disabled.png);
	}

	QMenu::right-arrow {
		margin: 5px;
		image: url(:/qss_icons/rc/right_arrow.png)
	}


	QWidget:disabled
	{
		color: #454545;
		background-color: #323232;
	}

	QAbstractItemView
	{
		alternate-background-color: #323232;
		color: #eff0f1;
		border: 1px solid 3A3939;
		border-radius: 2px;
	}

	QWidget:focus, QMenuBar:focus,QToolBar:focus,QScrollAreaViewer:focus
	{
		/* border: 2px solid #D1DBCB; */
	}

	QTabWidget:focus, QCheckBox:focus, QRadioButton:focus, QSlider:focus
	{
		border: none;
	}

	QLineEdit
	{
		background-color: #1e1e1e;
		selection-background-color: #D1DBCB;
		selection-color: black;
		padding: 5px;
		border-style: solid;
		border: 1px solid #76797C;
		border-radius: 2px;
		color: #eff0f1;
	}

	QGroupBox {
		border:1px solid #76797C;
		border-radius: 2px;
		margin-top: 20px;
	}

	QGroupBox::title {
		subcontrol-origin: margin;
		subcontrol-position: top center;
		padding-left: 10px;
		padding-right: 10px;
		padding-top: 10px;
	}

	QAbstractScrollArea
	{
		border-radius: 0px;
		border: 0px solid #76797C;
		background-color: transparent;
	}

	QScrollBar:horizontal
	{
		height: 15px;
		margin: 3px 15px 3px 15px;
		border: 1px transparent #2A2929;
		border-radius: 4px;
		background-color: #2A2929;
	}

	QScrollBar::handle:horizontal
	{
		background-color: #605F5F;
		min-width: 5px;
		border-radius: 4px;
	}

	QScrollBar::add-line:horizontal
	{
		margin: 0px 3px 0px 3px;
		border-image: url(:/qss_icons/rc/right_arrow_disabled.png);
		width: 10px;
		height: 10px;
		subcontrol-position: right;
		subcontrol-origin: margin;
	}

	QScrollBar::sub-line:horizontal
	{
		margin: 0px 3px 0px 3px;
		border-image: url(:/qss_icons/rc/left_arrow_disabled.png);
		height: 10px;
		width: 10px;
		subcontrol-position: left;
		subcontrol-origin: margin;
	}

	QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
	{
		border-image: url(:/qss_icons/rc/right_arrow.png);
		height: 10px;
		width: 10px;
		subcontrol-position: right;
		subcontrol-origin: margin;
	}


	QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
	{
		border-image: url(:/qss_icons/rc/left_arrow.png);
		height: 10px;
		width: 10px;
		subcontrol-position: left;
		subcontrol-origin: margin;
	}

	QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
	{
		background: none;
	}


	QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
	{
		background: none;
	}

	QScrollBar:vertical
	{
		background-color: #2A2929;
		width: 15px;
		margin: 15px 3px 15px 3px;
		border: 1px transparent #2A2929;
		border-radius: 4px;
	}

	QScrollBar::handle:vertical
	{
		background-color: #605F5F;
		min-height: 5px;
		border-radius: 4px;
	}

	QScrollBar::sub-line:vertical
	{
		margin: 3px 0px 3px 0px;
		border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
		height: 10px;
		width: 10px;
		subcontrol-position: top;
		subcontrol-origin: margin;
	}

	QScrollBar::add-line:vertical
	{
		margin: 3px 0px 3px 0px;
		border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
		height: 10px;
		width: 10px;
		subcontrol-position: bottom;
		subcontrol-origin: margin;
	}

	QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
	{

		border-image: url(:/qss_icons/rc/up_arrow.png);
		height: 10px;
		width: 10px;
		subcontrol-position: top;
		subcontrol-origin: margin;
	}


	QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
	{
		border-image: url(:/qss_icons/rc/down_arrow.png);
		height: 10px;
		width: 10px;
		subcontrol-position: bottom;
		subcontrol-origin: margin;
	}

	QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
	{
		background: none;
	}


	QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
	{
		background: none;
	}

	QTextEdit
	{
		background-color: #1e1e1e;
		color: #eff0f1;
		border: 1px solid #76797C;
	}

	QPlainTextEdit
	{
		background-color: #1e1e1e;;
		color: #eff0f1;
		border-radius: 2px;
		border: 1px solid #76797C;
	}

	QHeaderView::section
	{
		background-color: #76797C;
		color: #eff0f1;
		padding: 5px;
		border: 1px solid #76797C;
	}

	QSizeGrip {
		image: url(:/qss_icons/rc/sizegrip.png);
		width: 12px;
		height: 12px;
	}


	QMainWindow::separator
	{
		background-color: #323232;
		color: white;
		padding-left: 4px;
		spacing: 2px;
		border: 1px dashed #76797C;
	}

	QMainWindow::separator:hover
	{

		background-color: #787876;
		color: white;
		padding-left: 4px;
		border: 1px solid #76797C;
		spacing: 2px;
	}


	QMenu::separator
	{
		height: 1px;
		background-color: #76797C;
		color: white;
		padding-left: 4px;
		margin-left: 10px;
		margin-right: 5px;
	}

	QFrame
	{
		border-radius: 0px;
		/*border: 1px solid #76797C;*/
	}


	QFrame[frameShape="0"]
	{
		border-radius: 0px;
		border: 0px transparent #76797C;
	}

	QStackedWidget
	{
		border: 1px transparent black;
	}

	QToolBar {
		border: 0px transparent #393838;
		background: 0px solid #323232;
		font-weight: bold;
	}

	QToolBar::handle:horizontal {
		image: url(:/qss_icons/rc/Hmovetoolbar.png);
	}
	QToolBar::handle:vertical {
		image: url(:/qss_icons/rc/Vmovetoolbar.png);
	}
	QToolBar::separator:horizontal {
		image: url(:/qss_icons/rc/Hsepartoolbar.png);
	}
	QToolBar::separator:vertical {
		image: url(:/qss_icons/rc/Vsepartoolbar.png);
	}
	QToolButton#qt_toolbar_ext_button {
		background: #58595a
	}

	QPushButton
	{
		color: #eff0f1;
		background-color: #323232;
		border-width: 1px;
		border-color: #76797C;
		border-style: solid;
		padding: 5px;
		border-radius: 0px;
		outline: none;
	}

	QPushButton:disabled
	{
		background-color: #323232;
		border-width: 1px;
		border-color: #454545;
		border-style: solid;
		padding-top: 5px;
		padding-bottom: 5px;
		padding-left: 10px;
		padding-right: 10px;
		border-radius: 2px;
		color: #454545;
	}

	QPushButton:focus {
		background-color: #D1DBCB;
		color: black;
	}

	QPushButton:pressed
	{
		color: black;
		background-color: #D1DBCB;
		padding-top: -15px;
		padding-bottom: -17px;
	}

	QComboBox
	{
		selection-background-color: #D1DBCB;
		background-color: #31363B;
		border-style: solid;
		border: 1px solid #76797C;
		border-radius: 2px;
		padding: 5px;
		min-width: 75px;
	}

	QPushButton:checked{
		background-color: #76797C;
		border-color: #6A6969;
	}

	QComboBox:hover,QPushButton:hover,QAbstractSpinBox:hover,QLineEdit:hover,QTextEdit:hover,QPlainTextEdit:hover,QAbstractView:hover,QTreeView:hover
	{
		border: 1px solid #D1DBCB;
	}

	QComboBox:on
	{
		padding-top: 0px;
		padding-left: 4px;
		selection-background-color: #4a4a4a;
	}

	QComboBox QAbstractItemView
	{
		background-color: #1e1e1e;
		border-radius: 2px;
		border: 1px solid #76797C;
		selection-background-color: #D1DBCB;
	}

	QComboBox::drop-down
	{
		subcontrol-origin: padding;
		subcontrol-position: top right;
		width: 15px;

		border-left-width: 0px;
		border-left-color: darkgray;
		border-left-style: solid;
		border-top-right-radius: 3px;
		border-bottom-right-radius: 3px;
	}

	QComboBox::down-arrow
	{
		image: url(:/qss_icons/rc/down_arrow_disabled.png);
	}

	QComboBox::down-arrow:on, QComboBox::down-arrow:hover,
	QComboBox::down-arrow:focus
	{
		image: url(:/qss_icons/rc/down_arrow.png);
	}

	QAbstractSpinBox {
		padding: 2px;
		margin: 2px;
		background-color: #1e1e1e;
		color: #eff0f1;
		border-radius: 0px;
		min-width: 75px;
		selection-background-color: #D1DBCB;
		selection-color: black;
	}

	QAbstractSpinBox:up-button
	{
		background-color: transparent;
		subcontrol-origin: border;
		subcontrol-position: center right;
	}

	QAbstractSpinBox:down-button
	{
		background-color: transparent;
		subcontrol-origin: border;
		subcontrol-position: center left;
	}

	QAbstractSpinBox::up-arrow,QAbstractSpinBox::up-arrow:disabled,QAbstractSpinBox::up-arrow:off {
		image: url(:/qss_icons/rc/up_arrow_disabled.png);
		width: 10px;
		height: 10px;
	}
	QAbstractSpinBox::up-arrow:hover
	{
		image: url(:/qss_icons/rc/up_arrow.png);
	}


	QAbstractSpinBox::down-arrow,QAbstractSpinBox::down-arrow:disabled,QAbstractSpinBox::down-arrow:off
	{
		image: url(:/qss_icons/rc/down_arrow_disabled.png);
		width: 10px;
		height: 10px;
	}
	QAbstractSpinBox::down-arrow:hover
	{
		image: url(:/qss_icons/rc/down_arrow.png);
	}


	QLabel
	{
		border: 0px solid black;
		margin-left: 2px;
		margin-right: 2px;
		color: #D1DBCB;
		text-align: center;
	}

	QTabWidget{
		border: 0px transparent black;
	}

	QTabWidget::pane {
		border: 1px solid #76797C;
		padding: 5px;
		margin: 0px;
		text-align: center;
	}

	QTabWidget::tab-bar {
		text-align: center;
		left: 5px; /* move to the right by 5px */
		border-radius: 1em;
	}

	QTabBar
	{
		qproperty-drawBase: 0;
		border-radius: 30px;
	}

	QTabBar::focus
	{
		border: 0px transparent black;
		color: black;
	}

	QTabBar::hover
	{
		border: 0px transparent black;
		color: black;
	}

	QTabBar::close-button  {
		image: url(:/qss_icons/rc/close.png);
		background: transparent;
	}

	QTabBar::close-button:hover
	{
		image: url(:/qss_icons/rc/close-hover.png);
		background: transparent;
	}

	QTabBar::close-button:pressed {
		image: url(:/qss_icons/rc/close-pressed.png);
		background: transparent;
	}

	/* TOP TABS */
	QTabBar::tab:top {
		color: #eff0f1;
		border: 1px solid #76797C;
		border-bottom: 1px transparent black;
		background-color: #323232;
		padding: 5px;
		min-width: 10px;
		max-width: 250px;
		border-top-left-radius: 5px;
		border-top-right-radius: 5px;
		text-align: left;
	}

	QTabBar::tab:top:!selected
	{
		color: #eff0f1;
		background-color: #54575B;
		border: 1px solid #76797C;
		border-bottom: 1px transparent black;
		border-top-left-radius: 2px;
		border-top-right-radius: 2px;
	}

	QTabBar::tab:top:!selected:hover {
		background-color: #D1DBCB;
		color: black;
	}

	/* BOTTOM TABS */
	QTabBar::tab:bottom {
		color: #eff0f1;
		border: 1px solid #76797C;
		border-top: 1px transparent black;
		background-color: #323232;
		padding: 5px;
		border-bottom-left-radius: 2px;
		border-bottom-right-radius: 2px;
		min-width: 50px;
	}

	QTabBar::tab:bottom:!selected
	{
		color: #eff0f1;
		background-color: #54575B;
		border: 1px solid #76797C;
		border-top: 1px transparent black;
		border-bottom-left-radius: 2px;
		border-bottom-right-radius: 2px;
	}

	QTabBar::tab:bottom:!selected:hover {
		background-color: #D1DBCB;
		color: black;
	}

	/* LEFT TABS */
	QTabBar::tab:left {
		color: #eff0f1;
		border: 1px solid #76797C;
		border-left: 1px transparent black;
		background-color: #323232;
		padding: 5px;
		border-top-right-radius: 2px;
		border-bottom-right-radius: 2px;
		min-height: 50px;
	}

	QTabBar::tab:left:!selected
	{
		color: #eff0f1;
		background-color: #54575B;
		border: 1px solid #76797C;
		border-left: 1px transparent black;
		border-top-right-radius: 2px;
		border-bottom-right-radius: 2px;
	}

	QTabBar::tab:left:!selected:hover {
		background-color: #D1DBCB;
		color: black;
	}


	/* RIGHT TABS */
	QTabBar::tab:right {
		color: #eff0f1;
		border: 1px solid #76797C;
		border-right: 1px transparent black;
		background-color: #323232;
		padding: 5px;
		border-top-left-radius: 2px;
		border-bottom-left-radius: 2px;
		min-height: 50px;
	}

	QTabBar::tab:right:!selected
	{
		color: #eff0f1;
		background-color: #54575B;
		border: 1px solid #76797C;
		border-right: 1px transparent black;
		border-top-left-radius: 2px;
		border-bottom-left-radius: 2px;
	}

	QTabBar::tab:right:!selected:hover {
		background-color: #D1DBCB;
		color: black;
	}

	QTabBar QToolButton::right-arrow:enabled {
		image: url(:/qss_icons/rc/right_arrow.png);
	}

	QTabBar QToolButton::left-arrow:enabled {
		image: url(:/qss_icons/rc/left_arrow.png);
	}

	QTabBar QToolButton::right-arrow:disabled {
		image: url(:/qss_icons/rc/right_arrow_disabled.png);
	}

	QTabBar QToolButton::left-arrow:disabled {
		image: url(:/qss_icons/rc/left_arrow_disabled.png);
	}


	QDockWidget {
		background: #323232;
		border: 1px solid #403F3F;
		titlebar-close-icon: url(:/qss_icons/rc/close.png);
		titlebar-normal-icon: url(:/qss_icons/rc/undock.png);
	}

	QDockWidget::close-button, QDockWidget::float-button {
		border: 1px solid transparent;
		border-radius: 2px;
		background: transparent;
	}

	QDockWidget::close-button:hover, QDockWidget::float-button:hover {
		background: rgba(255, 255, 255, 10);
	}

	QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
		padding: 1px -1px -1px 1px;
		background: rgba(255, 255, 255, 10);
	}

	QTreeView, QListView
	{
		border: 1px solid #76797C;
		background-color: #1e1e1e;
	}

	QTreeView:branch:selected, QTreeView:branch:hover
	{
		background: url(:/qss_icons/rc/transparent.png);
	}

	QTreeView::branch:has-siblings:!adjoins-item {
		border-image: url(:/qss_icons/rc/transparent.png);
	}

	QTreeView::branch:has-siblings:adjoins-item {
		border-image: url(:/qss_icons/rc/transparent.png);
	}

	QTreeView::branch:!has-children:!has-siblings:adjoins-item {
		border-image: url(:/qss_icons/rc/transparent.png);
	}

	QTreeView::branch:has-children:!has-siblings:closed,
	QTreeView::branch:closed:has-children:has-siblings {
		image: url(:/qss_icons/rc/branch_closed.png);
	}

	QTreeView::branch:open:has-children:!has-siblings,
	QTreeView::branch:open:has-children:has-siblings  {
		image: url(:/qss_icons/rc/branch_open.png);
	}

	QTreeView::branch:has-children:!has-siblings:closed:hover,
	QTreeView::branch:closed:has-children:has-siblings:hover {
		image: url(:/qss_icons/rc/branch_closed-on.png);
		}

	QTreeView::branch:open:has-children:!has-siblings:hover,
	QTreeView::branch:open:has-children:has-siblings:hover  {
		image: url(:/qss_icons/rc/branch_open-on.png);
		}

	QListView::item:!selected:hover, QTreeView::item:!selected:hover  {
		background: #848383;
		outline: 0;
		color: #eff0f1;
	}

	QListView::item:selected:hover, QTreeView::item:selected:hover  {
		background: #D1DBCB;
	}

	QSlider::groove:horizontal {
		border: 1px solid #565a5e;
		height: 4px;
		background: #565a5e;
		margin: 0px;
		border-radius: 2px;
	}

	QSlider::handle:horizontal {
		background: #D1DBCB;
		border: 1px solid #999999;
		width: 10px;
		height: 10px;
		margin: -5px 0;
	}

	QSlider::add-page:qlineargradient {
		background: #595858;
		border-top-right-radius: 5px;
		border-bottom-right-radius: 5px;
		border-top-left-radius: 0px;
		border-bottom-left-radius: 0px;
	}

	QSlider::sub-page::qlineargradient:horizontal {
		background:  #D1DBCB;
		border-top-right-radius: 0px;
		border-bottom-right-radius: 0px;
		border-top-left-radius: 5px;
		border-bottom-left-radius: 5px;
	}

	QSlider::groove:vertical {
		border: 1px solid #565a5e;
		width: 4px;
		background: #565a5e;
		margin: 0px;
		border-radius: 3px;
	}

	QSlider::handle:vertical {
		background: #D1DBCB;
		border: 1px solid #999999;
		width: 10px;
		height: 10px;
		margin: 0 -5px;
	}

	QToolButton {
		color: #D1DBCB;
		background-color: transparent;
		border: 0px transparent #76797C;
		border-radius: 0px;
		padding: 1px;
		margin-right: 5px;
	}

	QToolButton[popupMode="1"] { /* only for MenuButtonPopup */
	padding-right: 20px; /* make way for the popup button */
	border: 1px #76797C;
	border-radius: 0px;
	}

	QToolButton[popupMode="2"] { /* only for InstantPopup */
	padding-right: 10px; /* make way for the popup button */
	border: 0px #76797C;
	}


	QToolButton:hover, QToolButton::menu-button:hover {
		background-color: transparent;
		border: 1px solid #D1DBCB;
		padding: 2px;
	}

	QToolButton:checked, QToolButton:pressed,
			QToolButton::menu-button:pressed {
		color: black;
		background-color: #D1DBCB;
		border: 0px solid #D1DBCB;
		padding: 2px;
	}

	/* the subcontrol below is used only in the InstantPopup or DelayedPopup mode */
	QToolButton::menu-indicator {
		image: url(:/qss_icons/rc/down_arrow.png);
		top: -7px; left: -2px; /* shift it a bit */
	}

	/* the subcontrols below are used only in the MenuButtonPopup mode */
	QToolButton::menu-button {
		border: 1px transparent #76797C;
		border-top-right-radius: 6px;
		border-bottom-right-radius: 6px;
		/* 16px width + 4px for border = 20px allocated above */
		width: 16px;
		outline: none;
	}

	QToolButton::menu-arrow {
		image: url(:/qss_icons/rc/down_arrow.png);
	}

	QToolButton::menu-arrow:open {
		border: 1px solid #76797C;
	}

	QPushButton::menu-indicator  {
		subcontrol-origin: padding;
		subcontrol-position: bottom right;
		left: 8px;
	}

	QTableView
	{
		border: 1px solid #76797C;
		gridline-color: #323232;
		background-color: #1e1e1e;
	}


	QTableView, QHeaderView
	{
		border-radius: 0px;
	}

	QTableView::item:pressed, QListView::item:pressed, QTreeView::item:pressed  {
		background: #D1DBCB;
		color: black;
	}

	QTableView::item:selected:active, QTreeView::item:selected:active, QListView::item:selected:active  {
		background: #D1DBCB;
		color: black;
	}

	QHeaderView
	{
		background-color: #323232;
		border: 1px transparent;
		border-radius: 0px;
		margin: 0px;
		padding: 0px;

	}

	QHeaderView::section  {
		background-color: #323232;
		color: #eff0f1;
		padding: 5px;
		border: 1px solid #76797C;
		border-radius: 0px;
		text-align: center;
	}

	QHeaderView::section::vertical::first, QHeaderView::section::vertical::only-one
	{
		border-top: 1px solid #76797C;
	}

	QHeaderView::section::vertical
	{
		border-top: transparent;
	}

	QHeaderView::section::horizontal::first, QHeaderView::section::horizontal::only-one
	{
		border-left: 1px solid #76797C;
	}

	QHeaderView::section::horizontal
	{
		border-left: transparent;
	}


	QHeaderView::section:checked
	{
		color: white;
		background-color: #848383;
	}

	/* style the sort indicator */
	QHeaderView::down-arrow {
		image: url(:/qss_icons/rc/down_arrow.png);
	}

	QHeaderView::up-arrow {
		image: url(:/qss_icons/rc/up_arrow.png);
	}


	QTableCornerButton::section {
		background-color: #323232;
		border: 1px transparent #76797C;
		border-radius: 0px;
	}

	QToolBox  {
		padding: 5px;
		border: 1px transparent black;
	}

	QToolBox::tab {
		color: #eff0f1;
		background-color: #323232;
		border: 1px solid #76797C;
		border-bottom: 1px transparent #323232;
		border-top-left-radius: 5px;
		border-top-right-radius: 5px;
	}

	QToolBox::tab:selected { /* italicize selected tabs */
		font: italic;
		background-color: #323232;
		border-color: #D1DBCB;
	}

	QStatusBar::item {
		border: 0px transparent dark;
		margin: 0px;
		border: 0px;
	}


	QFrame[height="3"], QFrame[width="3"] {
		background-color: #76797C;
	}


	QSplitter::handle {
		border: 1px dashed #76797C;
	}

	QSplitter::handle:hover {
		background-color: #787876;
		border: 1px solid #76797C;
	}

	QSplitter::handle:horizontal {
		width: 1px;
	}

	QSplitter::handle:vertical {
		height: 1px;
	}

	QProgressBar {
		border: 1px solid #76797C;
		border-radius: 5px;
		text-align: center;
	}

	QProgressBar::chunk {
		background-color: #D1DBCB;
	}

	QDateEdit
	{
		selection-background-color: #D1DBCB;
		border-style: solid;
		border: 1px solid #CEE343;
		border-radius: 2px;
		padding: 1px;
		min-width: 75px;
	}

	QDateEdit:on
	{
		padding-top: 3px;
		padding-left: 4px;
		selection-background-color: #4a4a4a;
	}

	QDateEdit QAbstractItemView
	{
		background-color: #1e1e1e;
		border-radius: 2px;
		border: 1px solid #3375A3;
		selection-background-color: #D1DBCB;
	}

	QDateEdit::drop-down
	{
		subcontrol-origin: padding;
		subcontrol-position: top right;
		width: 15px;
		border-left-width: 0px;
		border-left-color: darkgray;
		border-left-style: solid;
		border-top-right-radius: 3px;
		border-bottom-right-radius: 3px;
	}

	QDateEdit::down-arrow
	{
		image: url(:/qss_icons/rc/down_arrow_disabled.png);
	}

	QDateEdit::down-arrow:on, QDateEdit::down-arrow:hover,
	QDateEdit::down-arrow:focus
	{
		image: url(:/qss_icons/rc/down_arrow.png);
	}

	""")
	hexs = find_all(style, "#")
	for h in hexs:
		try:
			case = style[h:h+7]
			rgb = "rgb" + str(hex_to_rgb(case)) + ""
		except:
			pass
	#window.setStyleSheet(style)
	app.setStyleSheet(style)

	def welcome():
			title = "WELCOME"
			text = """Welcome to SecureWeb v0.1, the most secure browser by today's standards. This is a startup browser based on the PyQt5 module for Python 3.10. If you have any questions, comments, concerns, or want to provide feedback, feel free to reach out to me. My email is kdtechhouse@gmail.com."""
			return dialog(title, text).show()
	#welcome()

	def error(err):
			print(str(err))
			while True:
				delay(1)
	# loop
	try:
		while app.exec():
			delay(1)
		app.removeTranslator(QTranslator(window))
	except Exception as e:
		error(e)
except Exception as exc:
	print(exc)
	while True:
		delay(1)
