# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.



from selenium import webdriver
from selenium.test.selenium.webdriver.common import select_element_handling_tests
from selenium.test.selenium.webdriver.common.webserver import SimpleWebServer
from selenium.test.selenium.webdriver.common.network import get_lan_ip

def setup_module(module):
    
    webserver = SimpleWebServer(host=get_lan_ip())
    webserver.start()
    FirefoxSelectElementHandlingTests.webserver = webserver
    FirefoxSelectElementHandlingTests.driver = webdriver.Firefox()


class FirefoxSelectElementHandlingTests(select_element_handling_tests.SelectElementHandlingTests):
    pass


def teardown_module(module):
    try:
        FirefoxSelectElementHandlingTests.driver.quit()
    except AttributeError:
        pass
    try:
        FirefoxSelectElementHandlingTests.webserver.stop()
    except AttributeError:
        pass
    
