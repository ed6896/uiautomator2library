# -*- coding:utf-8 -*-


"""
param locator **kwargs: key=value
key: text,textContains,textMatches,textStartsWith,
        className,classNameMatches,
        description,descriptionContains,descriptionMatches,descriptionStartsWith,
        checkable,checked,
        clickable,longClickable,
        scrollable,enabled,focusable,focused,selected,
        packageName,packageNameMatches,
        resourceId,resourceIdMatches,
        index,instance
e.g:
    ui = UiActions()
    ui.connect_device()
    ui.find_element_by_locator(textContains="test")

    or use this in RobotFramework
    | Connect Device | 192.168.1.100
    | ${variable} | Find Element By Locator  | resourceId=com.example.test:id/username   | className=android.widget.EditText

"""
from __future__ import absolute_import
from .u2keywords import DeviceActions
from .u2keywords import UiActions
from .u2keywords import XpathActions


class Mobile(DeviceActions, UiActions, XpathActions):
    """ Mobile object """

    def __init__(self):
        super(Mobile, self).__init__()


class Uiautomator2Library(Mobile):
    """
    robotframework-uiautomatorlibrary is an Android device testing library for Robot Framework.

    It uses uiautomator2 - Python wrapper for Android uiautomator2 tool (https://pypi.org/project/uiautomator2) internally.

    *Before running tests*

    You can use `Set Serial` to specify which device to perform the test.

    *Identify UI object*

    If the UI object can be identified just by one selector, you can use librarykeywords to manipulate the object directly.

    For example:

    | Swipe Left | description=Settings |                | # swipe the UI object left by description          |
    | Swipe Left | description=Settings | clickable=True | # swipe the UI object left by description and text |

    If the UI object is in other or UI object (other layout or something else), you can always get the object layer by layer.

    For example:

    | ${some_parent_object} | Get Object | className=android.widget.FrameLayout |
    | ${some_child_object}  | Get Child  | ${some_parent_object}                | text=ShownTextOnChildObject |

    *Selectors*

    If the librarykeywords argument expects _**selectors_, the following parameters are supported. (more details https://github.com/xiaocong/uiautomator#selector):

    - text, textContains, textMatches, textStartsWith
    - className, classNameMatches
    - description, descriptionContains, descriptionMatches, descriptionStartsWith
    - checkable, checked, clickable, longClickable
    - scrollable, enabled,focusable, focused, selected
    - packageName, packageNameMatches
    - resourceId, resourceIdMatches
    - index, instance

    p.s. These parameters are case sensitive.

    *Input*

    The librarykeywords Type allows you to type in languages other than English.

    You have to :

    1. Install MyIME.apk (in support folder) to device.

    2. Set MyIME as your input method editor in the setting.

    *Operations without UI*

    If you want to use keywords with *[Test Agent]* tag.

    You have to install TestAgent.apk (in support folder) to device.
    """
    # ROBOT_LIBRARY_VERSION = '0.1'
    # ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # ROBOT_EXIT_ON_FAILURE = True

    # def __init__(self):
    #     """
    #     """
    #     Mobile.__init__(self)
