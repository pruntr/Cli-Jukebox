from ChromeDriver import create_driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import os
import pickle
from time import sleep
import sys
# TODO:


class Player:

    def __init__(self):
        self.actions = None
        # self.display = Display(visible=0, size=(1080, 1920))
        # self.display.start()
        self.driver = create_driver()
        self.driver.maximize_window()
        self.driver.minimize_window()
        self.driver.get("https://youtube.com")
        self.url = "https://youtube.com"
        #these are for future hoped changes
        self.has_playlist = False
        # self.has_cookies = self.check_credentials()
        # Close loaded extension tab
        if(len(self.driver.window_handles) > 1):
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()
        # Switch focus to first tab
        self.driver.switch_to.window(self.driver.window_handles[0])


    def search(self, song):
        """
        Search and play given song on YouTube.
        :param (str) song: Song name to be searched
        :return:
        """

        song = "+".join(song.split(' '))
        driver = self.driver
        driver.implicitly_wait(10)
        self.url = "https://www.youtube.com/results?search_query="+song
        driver.maximize_window()
        driver.minimize_window()
        driver.get(self.url)
        driver.find_element(By.ID, "search-icon-legacy").click()
        driver.find_element(By.CLASS_NAME, "style-scope ytd-video-renderer").click()
        self.has_playlist = self.lookup_playlist()
        return True

    def get_song_title(self):
        """
        Get currently playing song's title.
        :return (str): Current song title
        """

        info = self.driver.find_element(By.XPATH, r'//*[@id="container"]/h1/yt-formatted-string').text
        return info

    def lookup_playlist(self):
        """
        Checks if there is any associated playlist for the current song.
        :return:
        """
        try:
            self.driver.find_element(By.CLASS_NAME, "style-scope ytd-compact-radio-renderer").click()
            return True
        except NoSuchElementException:
            return False
        

    def get_playlist(self):
        """
        Get next 5 songs from playlist
        :return (dict): Next 5 songs from associated playlist else None
        """
        if not self.has_playlist:
            return False

        next5 = {}
        for i in range(2,7):
            link = self.driver.find_element(By.XPATH,
                r'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div['
                r'2]/div/ytd-playlist-panel-renderer/div/div[2]/ytd-playlist-panel-video-renderer['
                + str(i) + r']/a').get_attribute('href')
            title = self.driver.find_element(By.XPATH,
                r'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div['
                r'2]/div/ytd-playlist-panel-renderer/div/div[2]/ytd-playlist-panel-video-renderer['
                + str(i) + r']/a/div/div[2]/h4/span').text
            next5[link] = title
        return next5

    def action(self, key_signal):
        """
        Control YouTube webplayer
        :param (str) key_signal: Key combination string
        :return:
        """

        self.actions = ActionChains(self.driver)
        self.actions.send_keys(key_signal)
        self.actions.perform()
        self.actions = None

    def next(self):
        """
        Play next song
        :return:
        """
        key_signal = Keys.LEFT_SHIFT + 'N'
        self.action(key_signal)
        sys.stdout.flush()

    def prev(self):
        """
        Play previous song
        :return:
        """
        key_signal = Keys.LEFT_SHIFT + 'P'
        self.action(key_signal)

    def play_pause(self):
        """
        Toggle play state
        :return:
        """
        key_signal = 'k'
        self.action(key_signal)

    def volume_up(self):
        """
        Volume up
        :return:
        """
        key_signal = Keys.ARROW_UP
        self.action(key_signal)

    def volume_down(self):
        """
        Volume down
        :return:
        """
        key_signal = Keys.ARROW_DOWN
        self.action(key_signal)

    def mute(self):
        """
        Mute player
        :return:
        """
        key_signal = 'm'
        self.action(key_signal)

    def forward(self):
        """
        Seek 5 seconds forward
        :return:
        """
        key_signal = Keys.ARROW_RIGHT
        self.action(key_signal)

    def backward(self):
        """
        Seek 5 seconds back
        :return:
        """
        key_signal = Keys.ARROW_LEFT
        self.action(key_signal)

    def quit(self):
        """
        Quits application
        :return:
        """
        # self.display.stop()
        self.driver.quit()
        return

