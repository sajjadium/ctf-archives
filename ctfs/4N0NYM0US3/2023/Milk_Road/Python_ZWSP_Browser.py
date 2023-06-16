# Importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import webbrowser

# Creating main window class
class MainWindow(QMainWindow):
    # Constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Creating a QWebEngineView
        self.browser = QWebEngineView()

        # Setting default browser url as google
        self.browser.setUrl(QUrl("http://google.com"))

        # Adding action when url gets changed
        self.browser.urlChanged.connect(self.update_urlbar)

        # Adding action when loading is finished
        self.browser.loadFinished.connect(self.update_title)

        # Set this browser as central widget or main window
        self.setCentralWidget(self.browser)

        # Creating a status bar object
        self.status = QStatusBar()

        # Adding status bar to the main window
        self.setStatusBar(self.status)

        # Creating QToolBar for navigation
        navtb = QToolBar("Navigation")

        # Adding this tool bar to the main window
        self.addToolBar(navtb)

        # Adding actions to the tool bar
        # Creating an action for back
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # Connect the loadProgress signal to check for content process termination
        self.browser.loadProgress.connect(self.check_content_process_termination)

        self.browser.loadFinished.connect(self.inject_javascript)

        self.content_process_terminated = False  # Track whether content process termination has been handled

        self.show()

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - ZWSP Browser" % title)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def inject_javascript(self):
        script = """
        let bodyText = document.body.innerText;
        let zeroWidthCharacters = ['\u200B', '\u200C', '\u200D', '\uFEFF'];
        let foundSequences = [];

        for (let char of zeroWidthCharacters) {
            if (bodyText.includes(char)) {
                let sequence = "";
                for (let i = 0; i < bodyText.length; i++) {
                    if (zeroWidthCharacters.includes(bodyText[i])) {
                        sequence += bodyText[i];
                    } else {
                        if (sequence) {
                            foundSequences.push(sequence);
                            sequence = "";
                        }
                    }
                }
                break;
            }
        }

        foundSequences;
        """

        self.browser.page().runJavaScript(script, self.handle_result)

    def handle_result(self, result):
        if result:
            for sequence in result:
                self.decode_zero_width_chars(sequence)
        else:
            print("No zero-width characters detected.")

    def decode_zero_width_chars(self, sequence):
        binary_mapping = {'\u200B': '0', '\u200C': '1'}

        binary_sequence = ''.join([binary_mapping[char] for char in sequence if char in binary_mapping])

        # Split the binary sequence into 8-bit segments
        binary_segments = [binary_sequence[i:i+8] for i in range(0, len(binary_sequence), 8)]

        # Convert each 8-bit segment to its ASCII character representation
        decoded_message = ''.join([chr(int(segment, 2)) for segment in binary_segments])

        # Get the original HTML file name without extension
        original_filename = os.path.splitext(self.browser.url().fileName())[0]
        # Append "decoded_" to the original filename
        decoded_filename = "d3c0d3d_" + original_filename + ".html"

        # Save the decoded message to a new HTML file
        with open(decoded_filename, "w") as file:
            file.write(decoded_message)

        # Open the new HTML file in the Python web browser
        local_url = QUrl.fromLocalFile(os.path.abspath(decoded_filename))
        self.browser.load(local_url)

    def check_content_process_termination(self, progress):
        # Check if progress reaches 100% but loadFinished signal is not emitted
        if progress == 100 and not self.content_process_terminated:
            # Reload the page if the content process terminates
            self.browser.reload()

            # Optional: Show a message or perform any additional action when content process terminates
            print("Content process terminated.")
            self.content_process_terminated = True

# Creating a PyQt5 application
app = QApplication(sys.argv)

# Setting name to the application
app.setApplicationName("ZWSP Browser")

# Creating a main window object
window = MainWindow()

# Start the event loop
sys.exit(app.exec_())
