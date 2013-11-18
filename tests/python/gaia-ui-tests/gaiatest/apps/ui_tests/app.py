# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.marionette import Actions

from marionette.by import By
from gaiatest.apps.base import Base


UI_TESTS = "UI Tests"


class UiTests(Base):

    _ui_page_locator = (By.CSS_SELECTOR, 'a[href="#UI"]')
    _api_page_locator = (By.CSS_SELECTOR, 'a[href="#API"]')
    _hw_page_locator = (By.CSS_SELECTOR, 'a[href="#HW"]')
    _mozId_tests_button_locator = (By.LINK_TEXT, 'navigator.mozId')
    _app_identity_frame = (By.CSS_SELECTOR, 'iframe[src*="identity"]')
    _app_std_request_button_locator = (By.ID, 't-request')
    _app_logout_button_locator = (By.ID, 't-logout')

    _app_ready_event = (By.CSS_SELECTOR, 'li.ready')
    _app_login_event = (By.CSS_SELECTOR, 'li.login')
    _app_logout_event = (By.CSS_SELECTOR, 'li.logout')
    _app_login_assertion_text = (By.CSS_SELECTOR, 'li.login div.assertion')
    _keyboard_locator = (By.LINK_TEXT, 'Keyboard')
    _contextmenu_locator = (By.LINK_TEXT, 'Contextmenu')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.name = UI_TESTS

    def launch(self):
        Base.launch(self, launch_timeout=120000)

    def launch_standard_sign_in(self):
        self.switch_to_mozId_frame()
        self.tap_standard_button()
        from gaiatest.apps.persona.app import Persona
        return Persona(self.marionette)

    def switch_to_mozId_frame(self):
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._app_identity_frame))

    def get_assertion(self):
        # Gets the last assertion in the event stream list, use logout event to make sure
        # we're done getting assertions
        return self.marionette.find_elements(*self._app_login_assertion_text)[-1].text

    def tap_ui_button(self):
        self.wait_for_element_displayed(*self._ui_page_locator)
        self.marionette.find_element(*self._ui_page_locator).tap()

    def tap_api_button(self):
        self.wait_for_element_displayed(*self._api_page_locator)
        self.marionette.find_element(*self._api_page_locator).tap()

    def tap_hw_button(self):
        self.wait_for_element_displayed(*self._hw_page_locator)
        self.marionette.find_element(*self._hw_page_locator).tap()

    def tap_standard_button(self):
        self.wait_for_element_displayed(*self._app_std_request_button_locator)
        self.marionette.find_element(*self._app_std_request_button_locator).tap()

    def tap_mozId_button(self):
        self.wait_for_element_displayed(*self._mozId_tests_button_locator, timeout=120)
        # Hack to make the identity button visible from underneath the toolbar
        mozId_button = self.marionette.find_element(*self._mozId_tests_button_locator)
        self.marionette.execute_script('arguments[0].scrollIntoView(false);', [mozId_button])
        mozId_button.tap()

    def tap_logout_button(self):
        self.wait_for_element_displayed(*self._app_logout_button_locator)
        self.marionette.find_element(*self._app_logout_button_locator).tap()

    def wait_for_logout_event(self):
        self.wait_for_element_displayed(*self._app_logout_event)

    def wait_for_ready_event(self):
        self.wait_for_element_displayed(*self._app_ready_event)

    def wait_for_login_event(self):
        self.wait_for_element_displayed(*self._app_login_event)

    def tap_keyboard_option(self):
        self.wait_for_element_displayed(*self._keyboard_locator, timeout=120)
        # Hack to make the keyboard button visible from underneath the toolbar
        keyboard_button = self.marionette.find_element(*self._keyboard_locator)
        self.marionette.execute_script('arguments[0].scrollIntoView(false);', [keyboard_button])
        keyboard_button.tap()

    def tap_contextmenu_option(self):
        self.wait_for_element_displayed(*self._contextmenu_locator, timeout=120)
        self.marionette.find_element(*self._contextmenu_locator).tap()
        self.switch_to_contextmenu_page_frame()
        return ContextmenuPage(self.marionette)

    def switch_to_keyboard_page_frame(self):
        keyboard_page_iframe = self.marionette.find_element(By.CSS_SELECTOR, "#test-iframe[src*='keyboard']")
        self.marionette.switch_to_frame(keyboard_page_iframe)
        return KeyboardPage(self.marionette)

    def switch_to_contextmenu_page_frame(self):
        contextmenu_page_iframe = self.marionette.find_element(By.CSS_SELECTOR, "#test-iframe[src*='contextmenu']")
        self.marionette.switch_to_frame(contextmenu_page_iframe)


class KeyboardPage(Base):

    _number_input_locator = (By.CSS_SELECTOR, 'input[type="number"]')
    _text_input_locator = (By.CSS_SELECTOR, 'input[type="text"]')
    _url_input_locator = (By.CSS_SELECTOR, 'input[type="url"]')

    def tap_number_input(self):
        self.marionette.find_element(*self._number_input_locator).tap()
        from gaiatest.apps.keyboard.app import Keyboard
        return Keyboard(self.marionette)

    @property
    def number_input(self):
        return self.marionette.find_element(*self._number_input_locator).get_attribute('value')

    def tap_text_input(self):
        self.marionette.find_element(*self._text_input_locator).tap()
        from gaiatest.apps.keyboard.app import Keyboard
        return Keyboard(self.marionette)

    @property
    def text_input(self):
        return self.marionette.find_element(*self._text_input_locator).get_attribute('value')

    def tap_url_input(self):
        self.marionette.find_element(*self._url_input_locator).tap()
        from gaiatest.apps.keyboard.app import Keyboard
        return Keyboard(self.marionette)

    @property
    def url_input(self):
        return self.marionette.find_element(*self._url_input_locator).get_attribute('value')


class ContextmenuPage(Base):

    _contextmenu_body_locator = (By.CSS_SELECTOR, "body > section")

    def long_press_contextmenu_body(self):
        self.wait_for_condition(lambda m: m.find_element(*self._contextmenu_body_locator).is_displayed())
        contextmenu_body = self.marionette.find_element(*self._contextmenu_body_locator)
        Actions(self.marionette).press(contextmenu_body).wait(1).release().perform()

        from gaiatest.apps.system.regions.activities import Activities
        return Activities(self.marionette)