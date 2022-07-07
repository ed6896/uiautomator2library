# -*- coding:utf-8 -*-
import threading

import uiautomator2 as u2
from time import sleep


class Actions:
    _instance_lock = threading.Lock()

    def __init__(self):
        self.device = None

    def __new__(cls):
        if not hasattr(Actions, "_instance"):
            with Actions._instance_lock:
                if not hasattr(Actions, "_instance"):
                    Actions._instance = object.__new__(cls)
        return Actions._instance

    def connect_device(self, serial_url=None):
        """
        Connect to phone device
        :param serial_url: device serial or WiFi url, default connect by usb
        :return:

        Example:
            | Connect Device  |
            or
            | Connect Device  | serial
            or
            | Connect Device  | 192.168.1.100
            or
            | Connect Device  | http://192.168.1.100
        """
        if self.device is None:
            self.device = u2.connect(serial_url)


class UiActions(Actions):
    def __init__(self):
        super(UiActions, self).__init__()

    def clear_element_text_by_locator(self, *args, **kwargs):
        """
        clear UiObject text
        :param args: Only include timeout/UiObject, default timeout is 10 seconds
        :param kwargs: locator dict
        :return:

        Example:
            | Clear element Text By Locator  | UiObject
            or
            | Clear element Text By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | Clear element Text By Locator  | 3 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | Clear element Text By Locator  | 3 | &{locator}
        """
        if len(args) == 1 and isinstance(args[0], u2.UiObject) and not kwargs:
            args[0].clear_text()
        elif len(args) == 1 and isinstance(args[0], int) and kwargs:
            self.device(**kwargs).clear_text(timeout=args[0])
        elif not args and kwargs:
            self.device(**kwargs).clear_text(timeout=10)
        else:
            raise TypeError("clear_ui_text() wrong number or type of argument")

    def click_element_by_locator(self, *args, **kwargs):
        """
        click UiObject on page
        :param args: Only include timeout/UiObject, default timeout is 10 seconds
        :param kwargs: locator dict
        :return:

        Example:
            | Click Element By Locator  | UiObject
            or
            | Click Element By Locator  | UiObject | 3
            or
            | Click Element By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | Click Element By Locator  | 3 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | Click Element By Locator  | 3 | &{locator}
        """
        if len(args) == 1 and isinstance(args[0], u2.UiObject):
            args[0].click_exists(timeout=10)
        elif len(args) == 1 and isinstance(args[0], int) and kwargs:
            self.device(**kwargs).click_exists(timeout=args[0])
        elif len(args) == 2 and not kwargs:
            element = None
            sleep_time = None
            for arg in args:
                if isinstance(arg, u2.UiObject):
                    element = arg
                elif isinstance(arg, int):
                    sleep_time = arg
                else:
                    raise TypeError("click_ui() wrong number or type of argument")
            element.click_exists(timeout=sleep_time)
        elif not args and kwargs:
            return self.device(**kwargs).click_exists(timeout=10)
        else:
            raise TypeError(f"click_ui() wrong number or type of argument")

    def element_is_existed_by_locator(self, *args, **kwargs) -> bool:
        """
        If UiObject is show on page, return True, else return False
        :param args: Only include sleep-time/UiObject, sleep-time is sleep before return status
        :param kwargs: locator dict
        :return:

        Example:
            | ${variable} | Element Is Existed By Locator  | UiObject
            or
            | ${variable} | Element Is Existed By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Element Is Existed By Locator  | 3 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Element Is Existed By Locator  | 3 | &{locator}
        """
        if len(args) == 1 and isinstance(args[0], u2.UiObject):
            return args[0].exists()
        elif len(args) == 1 and isinstance(args[0], int) and kwargs:
            sleep(args[0])
            return self.device(**kwargs).exists()
        elif len(args) == 2 and not kwargs:
            element = None
            sleep_time = None
            for arg in args:
                if isinstance(arg, u2.UiObject):
                    element = arg
                elif isinstance(arg, int):
                    sleep_time = arg
                else:
                    raise TypeError("ui_is_existed() wrong number or type of argument")
            sleep(sleep_time)
            return element.exists()
        elif not args and kwargs:
            return self.device(**kwargs).exists()
        else:
            raise TypeError(f"ui_is_existed() wrong number or type of argument")

    def find_element_by_locator(self, timeout=10, **kwargs):
        """
        If UiObject is show on page, return UiObject
        :param timeout: Only include timeout type, default timeout is 10 seconds
        :param kwargs: locator dict
        :return:

        Example:
            | ${variable} | Find Element By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Find Element By Locator  | 3 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{variable}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Find Element By Locator  | 3 | &{locator}
        """
        self.device(**kwargs).must_wait(timeout=timeout)
        return self.device(**kwargs)

    @staticmethod
    def find_element_by_locator_with_direction(ui: u2.UiObject, direction, **kwargs):
        """
        Find UiObject by direction and locator with specified origin UiObject
        :param ui: specified origin UiObject
        :param direction: left,right,up,down
        :param kwargs: locator dict
        :return: UiObject

        Example:
            | ${variable} | Find Element By Locator With Direction | UiObject | left | resourceId=com.example.test:id/username   | className=android.widget.EditText
            &{variable}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Find Element By Locator With Direction  |  UiObject | left | &{locator}
        """
        assert direction in ["left", "right", "up", "down"]
        if direction == "left":
            return ui.left(**kwargs)
        elif direction == "right":
            return ui.right(**kwargs)
        elif direction == "up":
            return ui.up(**kwargs)
        else:
            return ui.down(**kwargs)

    def find_element_child_by_locator(self, *args, **kwargs):
        """
        Find child UiObject with child locator under the specified UiObject
        :param args: sleep-time/parent UiObjects, no default sleep-time
        :param kwargs: locator dict
        :return:
            1. if only one of the parent UiObject and kwargs locator is input，
            return list of all child UiObjects
            2. if both parent UiObject and kwargs are input,
            return the specified UiObject with kwargs locator under parent UiObject

        Example:
            | ${variable} | Find Element Child By Locator  | UiObject
            or
            | ${variable} | Find Element Child By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Find Element Child By Locator  | UiObject | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Find Element Child By Locator  | 3 | UiObject | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Find Element Child By Locator  | UiObject | &{locator}
        """
        if len(args) == 1 and isinstance(args[0], u2.UiObject):
            if kwargs:
                return args[0].child(**kwargs)
            else:
                return args[0].child()
        elif len(args) == 1 and isinstance(args[0], int) and kwargs:
            sleep(args[0])
            return self.device(**kwargs).child()
        elif len(args) == 2:
            element = None
            sleep_time = None
            for arg in args:
                if isinstance(arg, u2.UiObject):
                    element = arg
                elif isinstance(arg, int):
                    sleep_time = arg
                else:
                    raise TypeError("find_child_ui() wrong number or type of argument")
            sleep(sleep_time)
            if kwargs:
                return element.child(**kwargs)
            else:
                return element.child()
        elif not args and kwargs:
            return self.device(**kwargs).child()
        else:
            raise TypeError("find_child_ui() wrong number or type of argument")

    @staticmethod
    def find_element_child_by_locator_with_description(parent: u2.UiObject, txt, **kwargs) -> u2.UiObject:
        """
        Find child UiObject by description and locator
        :param parent: parent UiObject
        :param txt: the description of child UiObject
        :param kwargs: the locator dict of child UiObject
        :return: child UiObject

        Example:
            | ${variable} | Find Element Child By Locator With Description  | parent | description
            or
            | ${variable} | Find Element Child By Locator With Description  | parent | description | resourceId=com.example.test:id/username
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Find Element Child By Locator With Description  | parent | description | &{locator}
        """

        kwargs["allow_scroll_search"] = True
        return parent.child_by_description(txt, **kwargs)

    @staticmethod
    def find_element_child_by_locator_with_index(parent: u2.UiObject, index: int, **kwargs) -> u2.UiObject:
        """
        Find child UiObject by instance index and locator
        :param parent: parent UiObject
        :param index: the instance index of child UiObject
        :param kwargs: the locator dict of child UiObject
        :return: child UiObject

        Example:
            | ${variable} | Find Element Child By Locator With Index  | parent | 1
            or
            | ${variable} | Find Element Child By Locator With Index  | parent | 1 | resourceId=com.example.test:id/username
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Find Element Child By Locator With Index  | parent | 1 | &{locator}
        """
        return parent.child_by_instance(index, **kwargs)

    @staticmethod
    def find_element_child_by_locator_with_text(parent: u2.UiObject, txt, **kwargs) -> u2.UiObject:
        """
        Find child UiObject by text and locator
        :param parent: parent UiObject
        :param txt: the text of child UiObject
        :param kwargs: the locator dict of child UiObject
        :return: child UiObject

        Example:
            | ${variable} | Find Element Child By Locator With Text  | parent | text
            or
            | ${variable} | Find Element Child By Locator With Text  | parent | text | resourceId=com.example.test:id/username
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Find Element Child By Locator With Text  | parent | text | &{locator}
        """

        kwargs["allow_scroll_search"] = True
        return parent.child_by_text(txt, **kwargs)

    @staticmethod
    def find_element_sibling_by_locator(ui: u2.UiObject, **kwargs) -> u2.UiObject:
        """
        Find sibling UiObject by locator
        :param ui: UiObject
        :param kwargs: the locator dict of sibling UiObject
        :return: sibling UiObject

        Example:
            | ${ui_object} | Find Element By Locator | resourceId=com.example.test:id/login

            | ${variable} | Find Element Sibling By Locator  | ${ui_object} | resourceId=com.example.test:id/username
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Find Element Sibling By Locator  | ${ui_object} | &{locator}
        """
        return ui.sibling(**kwargs)

    def get_element_attribute_by_locator(self, *args, **kwargs):
        """
        Gets UiObject info dict or attribute value
        :param args: Only include timeout/UiObject and attribute string, default timeout is 10 seconds,
            attribute: bounds, childCount, className, contentDescription, packageName,
                resourceName, text, visibleBounds, checkable, checked, clickable, enabled, focusable,
                focused, longClickable, scrollable, selected
        :param kwargs: locator dict
        :return:
            1. if attribute is none, return UiObject info dict
            2. if attribute is not none, return UiObject attribute value

        Example:
            | ${variable} | Get Element Attribute By Locator  | UiObject
            or
            | ${variable} | Get Element Attribute By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Get Element Attribute By Locator  | 3 | packageName | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Get Element Attribute By Locator  | 3 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Get Element Attribute By Locator  | 3 | packageName | &{locator}

        """
        attribute = ["bounds", "childCount", "className", "contentDescription", "packageName", "resourceName", "text",
                     "visibleBounds", "checkable", "checked", "clickable", "enabled", "focusable", "focused",
                     "longClickable", "scrollable", "selected"]
        if len(args) == 1 and isinstance(args[0], int) and kwargs:
            sleep(args[0])
            return self.device(**kwargs).info
        elif len(args) == 1 and isinstance(args[0], str) and kwargs:
            assert args[0] in attribute
            return self.device(**kwargs).info[args[0]]
        elif 4 > len(args) > 1 and not kwargs:
            element = None
            timeout = None
            attribute_str = None
            for arg in args:
                if isinstance(arg, u2.UiObject):
                    element = arg
                elif isinstance(arg, int):
                    timeout = arg
                elif isinstance(arg, str):
                    attribute_str = arg
                else:
                    raise TypeError("get_ui_info_or_attribute() wrong number or arguments or type")
            if element:
                if attribute_str:
                    assert attribute_str in attribute
                if timeout:
                    sleep(timeout)
                return element.info[attribute_str] if attribute_str else element.info
            else:
                raise TypeError("get_ui_info_or_attribute() wrong number or arguments or type")
        elif not args and kwargs:
            return self.device(**kwargs).info
        else:
            raise TypeError("get_ui_info_or_attribute() wrong number or arguments or type")

    def get_element_text_by_locator(self, *args, **kwargs):
        """
        Gets the text of the UiObject
        :param args: Only include timeout/UiObject, default timeout is 10 seconds
        :param kwargs: locator dict
        :return: text string

        Example:
            | ${variable} | Get Element Text By Locator  | UiObject
            or
            | ${variable} | Get Element Text By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Get Element Text By Locator  | 3 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Get Element Text By Locator  | 3 | &{locator}
        """
        if len(args) == 1 and isinstance(args[0], u2.UiObject):
            return args[0].get_text(timeout=10)
        elif len(args) == 1 and isinstance(args[0], int) and kwargs:
            return self.device(**kwargs).get_text(timeout=10)
        elif len(args) == 2 and not kwargs:
            element = None
            timeout = None
            for arg in args:
                if isinstance(arg, u2.UiObject):
                    element = arg
                elif isinstance(arg, int):
                    timeout = arg
                else:
                    raise TypeError("get_ui_text() wrong number or arguments or type")
            return element.get_text(timeout=timeout)
        elif not args and kwargs:
            return self.device(**kwargs).get_text(timeout=10)
        else:
            raise TypeError(f"get_ui_text() wrong number or arguments or type")

    def get_elements_count_by_locator(self, timeout=10, **kwargs) -> int:
        """
        Gets the count of the UiObjects
        :param timeout: default timeout is 10 seconds
        :param kwargs: locator dict
        :return: int

        Example:
            | ${variable} | Get Elements Count By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | ${variable} | Get Elements Count By Locator  | 3 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | ${variable} | Get Elements Count By Locator  | 3 | &{locator}
        """
        ui_object = self.find_element_by_locator(timeout, **kwargs)
        return len(ui_object)

    def long_click_element_by_locator(self, duration=1, **kwargs):
        """
        Long click UiObjects
        :param duration: long click time, default timeout is 1 seconds
        :param kwargs: locator dict
        :return:

        Example:
            | Long Click Element By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            | Long Click Element By Locator  | 2 | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | Long Click Element By Locator  | 2 | &{locator}
        """
        self.device(**kwargs).long_click(duration=duration)

    def scroll_backward(self):
        """
        Slide the interface vertically downward
        :return:

        Example:
            | Scroll Backward
        """
        return self.device(scrollable=True).scroll.backward()

    def scroll_forward(self):
        """
        Slide the interface vertically upward
        :return:

        Example:
            | Scroll Forward
        """
        return self.device(scrollable=True).scroll.forward()

    def scroll_to_beginning(self):
        """
        Slide the interface to the top
        :return:

        Example:
            | Scroll To Beginning
        """
        self.device(scrollable=True).scroll.toBeginning()

    def scroll_to_end(self):
        """
        Slide the interface to the end
        :return:

        Example:
            | Scroll To End
        """
        self.device(scrollable=True).scroll.toEnd()

    def scroll_to_text(self, text):
        """
        Slide the interface vertically upward to text
        :param text:
        :return:
        Example:
            | Scroll To Text        | content         |
        """
        return self.device(scrollable=True).scroll.to(text=text)

    def set_element_text_by_locator(self, *args, **kwargs):
        """
        Set text to UiObject, if you want to clear text, please use Clear Ui Text keyword
        :param args: Only include text/UiObject, default timeout is 5 seconds
        :param kwargs: locator dict
        :return: int

        Example:
            | Set Element Text By Locator  | UiObject |  text
            or
            | Set Element Text By Locator  | text | resourceId=com.example.test:id/username   | className=android.widget.EditText
            or
            &{locator}        resourceId=com.example.test:id/username    className=android.widget.EditText
            | Set Element Text By Locator  | text | &{locator}
        """
        if len(args) == 1 and not isinstance(args[0], u2.UiObject) and kwargs:
            self.device(**kwargs).set_text(str(args[0]), timeout=5)
        elif len(args) == 2 and not kwargs:
            text = None
            element = None
            for arg in args:
                if isinstance(arg, u2.UiObject):
                    element = arg
                else:
                    text = str(arg)
            if element:
                element.set_text(text, timeout=5)
            else:
                raise TypeError("set_text_to_ui() wrong number or arguments or type")
        else:
            raise TypeError("set_text_to_ui() wrong number or arguments or type")

    def wait_element_visible_by_locator(self, timeout=10, **kwargs) -> bool:
        """
        Wait the locator show on page
        :param timeout: default 10 second
        :param kwargs:
        :return:

        Example:
            | ${variable} | Wait Element Visible By Locator  | resourceId=com.example.test:id/username
            or
            | ${variable} | Wait Element Visible By Locator  | 5 | resourceId=com.example.test:id/username
        """
        if self.device(**kwargs).wait(timeout=timeout):
            return True
        else:
            raise TimeoutError

    def wait_element_invisible_by_locator(self, timeout=10, **kwargs) -> bool:
        """
        Wait the locator disappear on page
        :param timeout: default 10 second
        :param kwargs:
        :return:

        Example:
            | ${variable} | Wait Element Invisible By Locator  | resourceId=com.example.test:id/username
            or
            | ${variable} | Wait Element Invisible By Locator  | 5 | resourceId=com.example.test:id/username
        """
        if self.device(**kwargs).wait_gone(timeout=timeout):
            return True
        else:
            raise TimeoutError


class DeviceActions(Actions):

    def __init__(self):
        super(DeviceActions, self).__init__()

    def dev_app_clear(self, package):
        """
        Clear the application data based on the package name
        :param package: application package name
        :return:

        Example:
            | Dev App Clear | package name
        """
        self.device.app_clear(package)

    def dev_app_info(self, package):
        """
        Gets the application information based on the package name
        :param package: application package name
        :return: information dict
            {
                "mainActivity": "com.github.uiautomator.MainActivity",
                "label": "ATX",
                "versionName": "1.1.7",
                "versionCode": 1001007,
                "size":1760809
            }

        Example:
            | &{variable} | Dev App Info | package name
        """
        return self.device.app_info(package)

    def dev_app_install(self, data):
        """
        Install the application based on data
        :param data: can be file path or url or file object
        :return:

        Example:
            | Dev App Install | package name
        """
        self.device.app_install(data)

    def dev_app_start(self, package):
        """
        Launch the application based on the package name, and stop it before start application
        :param package: application package name
        :return:

        Example:
            | Dev App Start | package name
        """
        self.device.app_start(package_name=package, wait=True, stop=True)

    def dev_app_stop(self, package):
        """
        Stop the application based on the package name
        :param package: application package name
        :return:

        Example:
            | Dev App Stop | package name
        """
        self.device.app_stop(package)

    def dev_app_uninstall(self, package):
        """
        Uninstall the application based on the package name
        :param package: application package name
        :return:

        Example:
            | Dev App Uninstall | package name
        """
        self.device.app_uninstall(package)

    def dev_click_screen(self, x, y):
        """
        Click position
        :param x:
        :param y:
        :return:

        Example:
            | Dev Click Screen | x | y
        """
        self.device.click(x, y)

    def dev_current_app(self) -> dict:
        """
        Gets the current application information
        :return: dict(package, activity, pid?)

        Example:
            | &{variable} | Dev Current App
        """
        return self.device.app_current()

    def dev_double_click_screen(self, x, y):
        """
        Double click position
        :param x:
        :param y:
        :return:

        Example:
            | Dev Double Click Screen | x | y
        """
        self.device.double_click(x, y)

    def dev_get_device_info(self):
        """
        Gets device and system information
        :return: information dict

        Example:
            | &{variable} | Dev Get Device Info
        """
        return self.device.dev_info

    def dev_get_page_text(self) -> list:
        """
        Gets all texts on the page
        :return: text list

        Example:
            | @{variable} | Dev Get Page Text
        """
        return [ele.text for ele in self.device.xpath('//android.widget.TextView').all()]

    def dev_get_toast_message(self) -> str or bool:
        """
        Gets toast message
        :return:

        Example:
            | ${variable} | Dev Get Toast Message
        """
        return self.device.toast.get_message()

    def dev_get_window_size(self):
        """
        Gets window size
        :return: size tuple

        Example:
            | ${variable} | Dev Get Window Size
        """
        return self.device.window_size()

    def dev_long_click_screen(self, x, y, duration: float = 1):
        """
        Long click position
        :param x:
        :param y:
        :param duration: long click time, default is 1 second
        :return:

        Example:
            | Dev Long Click Screen | x | y
            or
            | Dev Long Click Screen | x | y | 2
        """
        self.device.long_click(x, y, duration)

    def dev_press_key(self, key):
        """
        Simulate press key via name or key code. Supported key name includes:
            home, back, left, right, up, down, center, menu, search, enter,
            delete(or del), recent(recent apps), volume_up, volume_down,
            volume_mute, camera, power.
        :param key: hardware button
        :return:

        Example:
            | Dev Press Key | home
        """
        assert key in ["home", "back", "left", "right", "up", "down", "center", "menu", "search", "enter",
                       "delete", "del", "recent", "volume_up", "volume_down", "volume_mute", "camera", "power"]
        return self.device.press(key)

    def dev_screenshot(self, filename):
        """
        Save screenshot to filename
        :param filename: file path and name
        :return:

        Example:
            | Dev Screenshot | C:\\Users\\screenshot.png
        """
        return self.device.screenshot(filename)

    def dev_scroll_to_deep_end(self):
        """
        need test
        At the end of the scroll page, if the list loads the content, the load is scrolled until the last record
        :return:

        Example:
            | Dev Scroll To Deep End |
        """
        a_txt = []
        while True:
            self.device(scrollable=False).scroll.toEnd()
            sleep(3)
            b_txt = self.dev_get_page_text()
            if len(list(set(b_txt).difference(set(a_txt)))) == 0:
                break
            else:
                a_txt = b_txt

    def dev_show_float_window(self):
        """
        Display suspension window to improve the stability of uiAutomator running
        :return:

        Example:
            | Dev Show Float Window
        """
        self.device.show_float_window()

    def dev_swipe_screen(self, fx, fy, tx, ty, steps=55):
        """
        Swipe screen
        :param fx: from position
        :param fy: from position
        :param tx: to position
        :param ty: to position
        :param steps: 1 steps is about 5ms, default 55*5ms
        :return:

        Example:
            | Dev Swipe Screen | 600 | 800 | 600 | 80 | 30
        """
        self.device.swipe(fx, fy, tx, ty, steps=steps)

    def dev_turn_screen(self, status):
        """
        Turn screen
        :param status: True is on, false is off
        :return:

        Example:
            | Dev Turn Screen | True
        """
        if status:
            self.device.screen_on()
        else:
            self.device.screen_off()

    def dev_wait_activity(self, activity) -> bool:
        """
        Wait activity show on screen
        :param activity: activity name
        :return: raise TimeoutError

        Example:
            | Dev Wait Activity | com.android.activity.DemoActivity
        """
        if self.device.wait_activity(activity):
            return True
        else:
            raise TimeoutError


class XpathActions(Actions):
    def __init__(self):
        super(XpathActions, self).__init__()

    def click_element_by_xpath(self, xpath, timeout=10):
        """
        Click element by xpath
        :param xpath: xpath string or XMLElement instance.
        :param timeout: default is 10 second, if xpath is XMLElement, timeout will be ignore
        :return:

        Example
            | Click Element By Xpath | xmlElement
            or
            | Click Element By Xpath | //*[@resource-id="com.android.demo:id/login"]
            or
            | Click Element By Xpath | //*[@resource-id="com.android.demo:id/login"] | 5
        """
        if isinstance(xpath, u2.xpath.XMLElement):
            xpath.click()
        else:
            self.find_element_by_xpath(xpath, timeout=timeout).click()

    def long_click_element_by_xpath(self, xpath, timeout=10):
        """
        Long click element by xpath
        :param xpath: xpath string or XMLElement instance.
        :param timeout: default is 10 second, if xpath is XMLElement, timeout will be ignore
        :return:

        Example
            | Long Click Element By Xpath | xmlElement
            or
            | Long Click Element By Xpath | //*[@resource-id="com.android.demo:id/login"]
            or
            | Long Click Element By Xpath | //*[@resource-id="com.android.demo:id/login"] | 5
        """
        if isinstance(xpath, u2.xpath.XMLElement):
            xpath.long_click()
        else:
            self.find_element_by_xpath(xpath, timeout=timeout).long_click()

    def element_is_existed_by_xpath(self, xpath, timeout=10):
        """
        Gets the xpath element status of the display
        :param xpath: xpath string
        :param timeout: default is 10 second
        :return:

        Example
            | ${variable} | Element Is Existed By Xpath | //*[@resource-id="com.android.demo:id/login"]
            or
            | ${variable} | Element Is Existed By Xpath | //*[@resource-id="com.android.demo:id/login"] | 5
        """
        if self.find_element_by_xpath(xpath, timeout=timeout):
            return self.device.xpath(xpath).exists

    def find_element_by_xpath(self, xpath, timeout=10):
        """
        Find element by xpath
        :param xpath: xpath string
        :param timeout: default is 10 second
        :return: XMLElement

        Example
            | ${variable} | Find Element By Xpath | //*[@resource-id="com.android.demo:id/login"]
            or
            | ${variable} | Find Element By Xpath | //*[@resource-id="com.android.demo:id/login"] | 5
        """
        return self.device.xpath(xpath).get(timeout=timeout)

    def find_elements_by_xpath(self, xpath, timeout=10):
        """
        Find all elements with same xpath
        :param xpath: xpath string
        :param timeout: default is 10 second
        :return: XMLElement list

        Example
            | @{variable} | Find Elements By Xpath | //*[@resource-id="com.android.demo:id/login"]
            or
            | @{variable} | Find Elements By Xpath | //*[@resource-id="com.android.demo:id/login"] | 5
        """
        if self.find_element_by_xpath(xpath, timeout=timeout):
            return self.device.xpath(xpath).all()

    def find_parent_element_by_xpath(self, xpath, timeout=10):
        """
        Find parent XMLElement
        :param xpath: xpath string or XMLElement instance.
        :param timeout: default is 10 second, if xpath is XMLElement, timeout will be ignore
        :return: XMLElement

        Example
            | @{variable} | Find Parent Element By Xpath | xmlElement
            or
            | @{variable} | Find Parent Element By Xpath | //*[@resource-id="com.android.demo:id/login"]
            or
            | @{variable} | Find Parent Element By Xpath | //*[@resource-id="com.android.demo:id/login"] | 5
        """
        if isinstance(xpath, u2.xpath.XMLElement):
            return xpath.parent()
        else:
            element = self.find_element_by_xpath(xpath, timeout=timeout)
            return element.parent()

    def get_element_attribute_by_xpath(self, xpath, attribute=None, timeout=10):
        """
        Gets UiObject info dict or attribute value
        :param xpath: xpath string or XMLElement instance.
        :param attribute: text,focusable,enabled,focused,scrollable,selected,className,bounds,
            contentDescription,longClickable,packageName,resourceName,resourceId,childCount
        :param timeout: default is 10 second, if xpath is XMLElement, timeout will be ignore
        :return:
            1. if attribute is none, return info dict
            2. if attribute is not none, return attribute value

        Example:
            | ${variable} | Get Element Attribute By Xpath  | xmlElement
            or
            | ${variable} | Get Element Attribute By Xpath  | xmlElement | text
            or
            | ${variable} | Get Element Attribute By Xpath  | //*[@resource-id="com.android.demo:id/login"]
            or
            | ${variable} | Get Element Attribute By Xpath  | //*[@resource-id="com.android.demo:id/login"] | text   | 3
            or
            &{locator}        //*[@resource-id="com.android.demo:id/login"]
            | ${variable} | Get Element Attribute By Xpath  | 3 | packageName | &{locator}
        """

        if isinstance(xpath, u2.xpath.XMLElement):
            element = xpath
        else:
            element = self.find_element_by_xpath(xpath, timeout=timeout)
        if attribute:
            assert attribute in ["text", "focusable", "enabled", "focused", "scrollable", "selected", "className",
                                 "bounds", "contentDescription", "longClickable", "packageName", "resourceName",
                                 "resourceId", "childCount"]
            return element.info[attribute]
        else:
            return element.info

    def get_element_text_by_xpath(self, xpath, timeout=10):
        """
        Gets element text by xpath
        :param xpath: xpath string or XMLElement instance.
        :param timeout: default is 10 second, if xpath is XMLElement, timeout will be ignore
        :return:

        Example
            | ${variable} | Get Element Text By Xpath | xmlElement
            or
            | ${variable} | Get Element Text By Xpath | //*[@resource-id="com.android.demo:id/login"]
            or
            | ${variable} | Get Element Text By Xpath | //*[@resource-id="com.android.demo:id/login"] | 5
        """
        if isinstance(xpath, u2.xpath.XMLElement):
            return xpath.text()
        else:
            if self.find_element_by_xpath(xpath, timeout=timeout):
                return self.device.xpath(xpath).get_text()

    def set_element_text_by_xpath(self, xpath, text, timeout=10):
        """
        Sets element text by xpath
        :param xpath: xpath string
        :param text:
        :param timeout: default is 10 second
        :return:

        Example
            | Set Element Text By Xpath | //*[@resource-id="com.android.demo:id/login"] | text
            or
            | Set Element Text By Xpath | //*[@resource-id="com.android.demo:id/login"] | text | 5
        """
        if self.find_element_by_xpath(xpath, timeout=timeout):
            self.device.xpath(xpath).set_text(text)

    def wait_element_visible_by_xpath(self, xpath, timeout=10):
        """
        :param xpath: xpath string
        :param timeout: default is 10 second
        :return:

        Example
            | Wait Element Visible By Xpath | //*[@resource-id="com.android.demo:id/login"] | text
            or
            | Wait Element Visible By Xpath | //*[@resource-id="com.android.demo:id/login"] | text | 5
        """
        if self.device.xpath(xpath).wait(timeout):
            return True
        else:
            raise TimeoutError

    def wait_element_invisible_by_xpath(self, xpath, timeout=10):
        """
        :param xpath: xpath string
        :param timeout: default is 10 second
        :return:

        Example
            | Wait Element Invisible By Xpath | //*[@resource-id="com.android.demo:id/login"] | text
            or
            | Wait Element Invisible By Xpath | //*[@resource-id="com.android.demo:id/login"] | text | 5
        """
        if self.device.xpath(xpath).wait_gone(timeout):
            return True
        else:
            raise TimeoutError


class Driver(UiActions, DeviceActions, XpathActions):
    pass
