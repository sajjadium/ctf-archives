from selenium/standalone-chrome:3.141.59

USER seluser

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /tmp \
    && sudo dpkg -i /tmp/google-chrome-stable_current_amd64.deb \
    && rm /opt/selenium/chromedriver-94.0.4606.61 /tmp/google-chrome-stable_current_amd64.deb \
    && CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
    && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
    && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
    && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
    && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-94.0.4606.61

COPY ./flag /flag
