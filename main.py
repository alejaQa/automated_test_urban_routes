from time import sleep

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from data import strings


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    result_button = (By.XPATH, f'//button[text()= "{strings["pedirTaxi"]}"]')
    auto_type_div = (By.XPATH, f'//div[@class="tariff-picker shown"]')

    comfort_button = (By.XPATH,
                      f'//img[@src="/static/media/kids.075fd8d4.svg"]')
    comfort_card = (By.XPATH, '//div[@class="tcard active"]')

    cellphone_button = (By.XPATH,
                        f'//div[@class="form"]//div[@class="np-button"]//div[contains(text(), "{strings["numeroTelefono"]}")]')

    add_phone_modal_phone_input = (By.ID, 'phone')
    add_phone_modal_confirmation_input = (By.ID, 'code')

    add_phone_modal_next_button = (By.XPATH,
                                   f'//div[@class="buttons"]//button[@type="submit" and contains(text(), "{strings["siguiente"]}")]')
    add_phone_modal_confirmation_button = (By.XPATH,
                                           f'//div[@class="modal"]//div[@class="section active"]//form//button[contains(text(), "{strings["confirmar"]}")]')

    payment_method_button = (By.XPATH,
                             f'//div[@class="pp-button filled"]//div[contains(text(), "{strings["metodoPago"]}")]')

    add_payment_method_button = (By.XPATH, f'//img[@src="/static/media/card.411e0152.svg"]')

    add_payment_method_number_input = (By.ID, 'number')
    add_payment_method_code_input = (By.XPATH, '//input[@id="code" and @class="card-input"]')

    add_payment_method_confirmation_button = (By.XPATH,
                                              f'//div[@class="pp-buttons"]//button[@type="submit" and contains(text(), "{strings["agregar"]}")]')

    add_payment_method_added_card = (By.XPATH, f'//div[@class="pp-row"]//div[contains(text(), "{strings["tarjeta"]}")]')

    add_comment_input = (By.ID, 'comment')

    delivery_request_combox = (By.XPATH,
                               f'//div[@class="reqs-head" and contains(text(), "{strings["requisitosPedidos"]}")]')

    delivery_request_blanket_scarves_checkbox = (By.XPATH,
                                                 f'//div[contains(text(), "{strings["mantaypanuelos"]}")]/following-sibling::div//span[@class="slider round"]')

    delivery_request_blanket_scarves_input = (
        By.XPATH,
        f'//div[contains(text(), "{strings["mantaypanuelos"]}")]/following-sibling::div//input[@type="checkbox"]'
    )

    ice_cream_add_plus_button = (By.XPATH, '//div[@class="counter"]//div[@class="counter-plus"]')
    ice_cream_counter_label = (By.XPATH, '//div[@class="counter"]//div[@class="counter-value"]')

    request_a_taxi_request_button = (By.XPATH,
                                     f'//button[@class="smart-button"]//span[contains(text(), "{strings["pedirTaxi"]}")]')

    request_a_taxi_seeking_taxi_modal = (By.XPATH, f'//div[contains(text(), "{strings["buscarAutomovil"]}")]')

    request_a_taxi_seeking_taxi_driver_modal = (By.XPATH, f'//div[contains(text(), "{strings["conductorLLegaraEn"]}")]')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.add_phone_modal_phone_input)
        ).send_keys(phone_number)

    def set_confirmation_code(self, code):
        self.driver.find_element(*self.add_phone_modal_confirmation_input).send_keys(code)

    def set_payment_method_number(self, payment_method_number):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.add_payment_method_number_input)
        ).send_keys(payment_method_number)

    def set_payment_method_code(self, payment_method_code):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.add_payment_method_code_input)
        ).send_keys(payment_method_code)

    def set_add_comment_input(self, comment):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.add_comment_input)
        ).send_keys(comment)

    def click_add_phone_modal_next_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.add_phone_modal_next_button)
        ).click()

    def click_add_phone_modal_confirmation_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.add_phone_modal_confirmation_button)
        )
        self.driver.find_element(*self.add_phone_modal_confirmation_button).click()

    def click_result_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.result_button)
        ).click()

    def click_comfort_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.comfort_button)
        ).click()

    def click_cellphone_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.cellphone_button)
        ).click()

    def click_payment_method_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.payment_method_button)
        ).click()

    def click_add_payment_method_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.add_payment_method_button)
        ).click()

    def click_add_payment_method_confirmation_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.add_payment_method_confirmation_button)
        ).click()

    def click_delivery_request_combo_box(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.delivery_request_combox)
        ).click()

    def click_delivery_request_blanket_scarves_checkbox(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.delivery_request_blanket_scarves_checkbox)
        ).click()

    def click_ice_cream_add_plus_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.ice_cream_add_plus_button)
        ).click()

    def click_request_a_taxi_request_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.request_a_taxi_request_button)
        ).click()

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_result_button(self):
        return self.driver.find_element(*self.result_button)

    def get_auto_type_div(self):
        return self.driver.find_element(*self.auto_type_div)

    def get_comfort_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.comfort_button)
        )

    def get_comfort_card(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.comfort_card)
        )

    def get_add_payment_code_input(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.add_payment_method_code_input)
        )

    def get_add_payment_method_confirmation_button(self):
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(self.add_payment_method_confirmation_button)
        )

    def get_payment_method_add_payment_method_added_card(self):
        return WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(self.add_payment_method_added_card)
        )

    def set_addresses(self, from_address, to_address):
        self.set_to(to_address)
        self.set_from(from_address)

    def get_payment_method_code(self, payment_method_code):
        return WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located(self.add_payment_method_code_input)
        )

    def get_delivery_request_blanket_scarves_checkbox(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_located_selection_state_to_be(self.delivery_request_blanket_scarves_input, True)
        )
        return self.driver.find_element(*self.delivery_request_blanket_scarves_checkbox)

    def get_ice_cream_counter_label(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.ice_cream_counter_label)
        )

    def get_request_a_taxi_seeking_taxi_modal(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.request_a_taxi_seeking_taxi_modal)
        )

    def get_request_a_taxi_seeking_taxi_driver_modal(self):
        return WebDriverWait(self.driver, 31).until(
            EC.presence_of_element_located(self.request_a_taxi_seeking_taxi_driver_modal)
        )


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 5)

    def open_routes_page(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        # wait until input is present before interacting
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
        return routes_page

    def select_comfort_type(self):
        routes_page = self.open_routes_page()
        routes_page.set_addresses(data.address_from, data.address_to)
        routes_page.click_result_button()
        routes_page.click_comfort_button()

        return routes_page

    def add_a_phone_number(self, routes_page):
        # open add modal
        routes_page.click_cellphone_button()
        # Fill phone number
        routes_page.set_phone_number(data.phone_number)
        # Click next button
        routes_page.click_add_phone_modal_next_button()
        # getCode
        code = retrieve_phone_code(self.driver)
        print(f'response code -> {code}')
        # insert code
        routes_page.set_confirmation_code(code)
        # click confirmation code
        routes_page.click_add_phone_modal_confirmation_button()

    def request_a_taxi_(self, routes_page):
        # Add a number
        self.add_a_phone_number(routes_page)
        # Add a message
        routes_page.set_add_comment_input(data.message_for_driver)
        # Request a taxi
        routes_page.click_request_a_taxi_request_button()

    def test_set_route(self):
        routes_page = self.open_routes_page()
        routes_page.set_addresses(data.address_from, data.address_to)

        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_button(self):
        routes_page = self.select_comfort_type()
        comfort_card = routes_page.get_comfort_card()
        assert 'active' in comfort_card.get_attribute('class')

    def test_add_phone_number(self):
        routes_page = self.select_comfort_type()
        self.add_a_phone_number(routes_page)

        confirmation_input = self.driver.find_element(By.CSS_SELECTOR, ".np-button.filled")
        border = confirmation_input.value_of_css_property("border")

        assert 'rgb(86, 184, 159)' in border

    def test_add_payment_method_button(self):
        routes_page = self.select_comfort_type()
        # open add a payment method
        routes_page.click_payment_method_button()
        # open add card modal
        routes_page.click_add_payment_method_button()
        # set card number
        routes_page.set_payment_method_number(data.card_number)
        # set code
        routes_page.set_payment_method_code(data.card_code)
        # tab user
        add_payment_code_input = routes_page.get_add_payment_code_input()
        add_payment_code_input.send_keys(Keys.TAB)
        # click confirmation modal
        routes_page.click_add_payment_method_confirmation_button()
        # get card like "tarjeta"
        title_card = routes_page.get_payment_method_add_payment_method_added_card()
        assert strings['tarjeta'] in title_card.text

    def test_add_a_comment(self):
        routes_page = self.select_comfort_type()
        routes_page.set_add_comment_input(data.message_for_driver)
        comment_input = routes_page.get_add_payment_code_input()

        # rgb(0,126,255)

        assert comment_input.text in data.message_for_driver

    def test_request_blankets_and_scarves(self):
        routes_page = self.select_comfort_type()
        # routes_page.click_delivery_request_combo_box()
        # click on checkbox
        routes_page.click_delivery_request_blanket_scarves_checkbox()
        # verify background color
        check_box = routes_page.get_delivery_request_blanket_scarves_checkbox()
        sleep(1)
        background_color = check_box.value_of_css_property("background-color")
        # .switch - input: checked +.slider
        print(f'response code -> {background_color.strip()}')
        assert '0, 126, 255' in background_color.strip()

    def test_add_2_ice_cream(self):
        routes_page = self.select_comfort_type()
        # click twice
        routes_page.click_ice_cream_add_plus_button()
        routes_page.click_ice_cream_add_plus_button()

        # get counter value
        counter_label = routes_page.get_ice_cream_counter_label()
        assert '2' == counter_label.text

    def test_request_a_taxi(self):
        routes_page = self.select_comfort_type()
        # Add a number
        self.add_a_phone_number(routes_page)
        # Add a message
        routes_page.set_add_comment_input(data.message_for_driver)
        # Request a taxi
        routes_page.click_request_a_taxi_request_button()
        # shown modal
        seeking_taxi_modal = routes_page.get_request_a_taxi_seeking_taxi_modal()

        print(f'response seek taxi -> {seeking_taxi_modal.text}')
        assert strings['buscarAutomovil'] in seeking_taxi_modal.text

    def test_shown_driver_info(self):
        routes_page = self.select_comfort_type()
        self.request_a_taxi_(routes_page)
        # shown modal
        driver_info_modal = routes_page.get_request_a_taxi_seeking_taxi_driver_modal()

        print(f'response seek taxi -> {driver_info_modal.text}')
        assert strings['conductorLLegaraEn'] in driver_info_modal.text


@classmethod
def teardown_class(cls):
    cls.driver.quit()
