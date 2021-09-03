# Function: facebook-wda test
# Author: Crifan Li
# Update: 20200412

import os
import time
import enum
import re
import copy
import sys
import logging

import wda
from wda import BatteryState, ApplicationState

from lxml import etree

sys.path.append("libs")
from libs import crifanLogging
from libs import utils
from libs import crifanWda
from libs import appCrawlerCommon

from libs.crifanWda import debugSaveScreenshot, debugSaveSource

################################################################################
# Const
################################################################################

PublicAccount_DongKaKongJian = "gh_cfcfcee032cc"


################################################################################
# Config
################################################################################

# ScreenX = 375
# ScreenY = 667
ScreenX = 414
ScreenY = 736

################################################################################
# Global Variable
################################################################################

gServerUrl = None
gWdaClient = None
gCurSession = None

# com.netease.cloudmusic - 网易云音乐 876
# gCurAppId = "com.netease.cloudmusic"
# com.360buy.jdmobile - 京东 7.3.6
# gCurAppId = "com.360buy.jdmobile"
# com.suiyi.foodshop1 - 食行生鲜 4911
# gCurAppId = "com.suiyi.foodshop1"
# com.tencent.xin - 微信 6.7.4.44
# gCurAppId = "com.tencent.xin"

gCurAppId = None

# gCurDatetimeStr = None

################################################################################
# Util Function
################################################################################

################################################################################
# Main
################################################################################

def testWdaBasicFunction():
    wdaStatus = gWdaClient.status()
    logging.debug("wdaStatus=%s", wdaStatus)

    osInfo = wdaStatus["os"]
    logging.debug("osInfo=%s", osInfo)
    osName = osInfo["name"]
    osVersion = osInfo["version"]
    osStr = "%s%s" % (osName, osVersion)
    logging.debug("osStr=%s", osStr)

    iosInfo = wdaStatus["ios"]
    logging.debug("iosInfo=%s", iosInfo)
    deviceIp = iosInfo["ip"]
    logging.debug("deviceIp=%s", deviceIp)

    # # curDeviceName = deviceIp
    # curDeviceName = "%s_%s" % (osStr, gCurDatetimeStr) # 'iOS12.4.5_20200221_143208'
    # logging.debug("curDeviceName=%s", curDeviceName)

    # # Wait WDA ready
    # gWdaClient.wait_ready(timeout=300) # 等待300s，默认120s

    # # Press home button
    # gWdaClient.home()

    # # Hit healthcheck
    # gWdaClient.healthcheck()

    # # Get page source
    # sourceFilename = "%s_source" % curDeviceName
    # xmlFilename = "%s.xml" % sourceFilename # 'iOS12.4.5_20200221_143208_source.xml'
    # curPageXml = gWdaClient.source() # format XML
    # logging.debug("curPageXml=%s", curPageXml)
    # utils.saveTextToFile(xmlFilename, curPageXml)

    # jsonFilename = "%s.json" % sourceFilename
    # curPageJson = gWdaClient.source(accessible=True) # default false, format JSON
    # logging.debug("curPageJson=%s", curPageJson)
    # utils.saveJsonToFile(jsonFilename, curPageJson)

    # screenShotFilename = "iOS_simulator_screen"
    # screenShotFilename = "iOS_screen_iphone6"
    # screenShotFilename = "%s_screen" % curDeviceName

    # pngFilename = "%s.png" % screenShotFilename
    # curScreenObj = gWdaClient.screenshot(png_filename=pngFilename)
    # logging.debug("curScreenObj=%s", curScreenObj)

    # # convert to PIL.Image and then save as jpg
    # jpgFilename = "%s.jpg" % screenShotFilename
    # curScreenObj.save(jpgFilename) # Good

    # curApp = gWdaClient.app_current()
    # logging.debug("curApp=%s", curApp)
    # curApp={'processArguments': {'env': {}, 'args': []}, 'name': '', 'pid': 15235, 'bundleId': 'com.apple.springboard'}

def testAppState():
    global gCurAppId
    curAppWithSession = gWdaClient.app_current()
    logging.debug("curAppWithSession=%s", curAppWithSession)

    curAppStateWithoutSession = gWdaClient.app_state(gCurAppId)
    curAppStateValueWithoutSession = curAppStateWithoutSession[0]
    logging.debug("curAppStateValueWithoutSession=%s", curAppStateValueWithoutSession)
    curStateEnum = ApplicationState(curAppStateValueWithoutSession)
    logging.debug("curStateEnum=%s", curStateEnum)

def testAppDeviceInfo(curSession):
    global gWdaClient, gCurAppId

    curAppState = curSession.app_state(gCurAppId)
    # logging.debug("curAppState=%s", curAppState)
    # -> 发生异常: TypeError, not all arguments converted during string formatting
    # curAppStateValue = curAppState["value"]
    # -> 发生异常: TypeError, tuple indices must be integers or slices, not str
    # curAppStateValue = curAppState["value"]
    """
    {
        "value" : 4,
        "sessionId" : "5BBD460B-F420-461D-A5E3-244A74CDF5CE"
    }
    """
    curAppStateValue = curAppState[0]
    logging.debug("curAppStateValue=%s", curAppStateValue)
    curStateEnum = ApplicationState(curAppStateValue)
    logging.debug("curStateEnum=%s", curStateEnum)

    # screenInfo = curSession.screen_info()
    screenInfo = gWdaClient.screen_info()
    logging.debug("screenInfo=%s", screenInfo)

    # windowInfo = curSession.window_info()
    windowInfo = gWdaClient.window_info()
    logging.debug("windowInfo=%s", windowInfo)

    deviceInfo = curSession.device_info()
    logging.debug("deviceInfo=%s", deviceInfo)

    curAppList = curSession.app_list()
    logging.debug("curAppList=%s", curAppList)

def testLaunchApp(curSession):
    testCount = 10
    while testCount > 0:
        debugSaveSource()
        testCount -= 1

    foundNameMusic = curSession(name='音乐')
    logging.debug("foundNameMusic=%s", foundNameMusic)
    founNameContainsMusic = curSession(nameContains='音乐')
    logging.debug("founNameContainsMusic=%s", founNameContainsMusic)
    foundLabelMusic = curSession(label='音乐')
    logging.debug("foundLabelMusic=%s", foundLabelMusic)

    founNameContainsJd = curSession(nameContains='京东超市')
    logging.debug("founNameContainsJd=%s", founNameContainsJd)

    founNameContainsMaxShop = curSession(nameContains='Max商城')
    logging.debug("founNameContainsMaxShop=%s", founNameContainsMaxShop)

def testDeviceManage():
    respValue = gWdaClient.matchTouchID()
    logging.info("respValue=%s", respValue)

def testRectPredicteSearch(curSession):
    # debugSaveScreenshot(curScale=3)
    # debugSaveSource()

    # query = {'enabled': 'true', 'height': '56', 'label': '信用卡', 'name': '信用卡', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'width': '183', 'x': '48', 'y': '680'}
    # <XCUIElementTypeButton type="XCUIElementTypeButton" name="通讯录" label="通讯录" enabled="true" visible="true" x="106" y="681" width="99" height="55"/>
    # query = {'label': '通讯录', 'name': '通讯录', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'enabled': 'true', 'x': '106', 'y': '681', 'width': '99', 'height': '55'}
    # query = {'label': '通讯录', 'name': '通讯录', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'enabled': 'true', 'x': '106', 'y': '681', 'width': '100', 'height': '60'}
    # query = {'label': '通讯录', 'name': '通讯录', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'enabled': 'true', 'x': '106', 'y': '681'}
    # query = {'label': '通讯录', 'name': '通讯录', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'enabled': 'true', "rect": {'x': '106', 'y': '681'}}
    # query = {'label': '通讯录', 'name': '通讯录', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'enabled': 'true', "rect": {'x': 106, 'y': 681, 'width': 100, 'height': 60}}
    query = {'label': '通讯录', 'name': '通讯录', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'enabled': 'true', "rect": {'x': 106, 'y': 681, 'width': 99, 'height': 55}}
    isFound, respInfo = crifanWda.findElement(curSession, query=query)
    logging.debug("isFound=%s, respInfo=%s", isFound, respInfo)

def testWdaAttributeValue(curSession):
    """
        AppStore 详情页 正在下载：
            <XCUIElementTypeButton type="XCUIElementTypeButton" value="18%" name="正在下载" label="正在下载" enabled="true" visible="true" x="154" y="308" width="74" height="30"/>
    """
    isDownloading = False
    curProgress = ""
    while True:
        parentCellClassChain = "/XCUIElementTypeCell[`rect.x = 0 AND rect.width = %d`]" % ScreenX
        downloadingButtonQuery = {"type":"XCUIElementTypeButton", "name": "正在下载", "enabled": "true"}
        downloadingButtonQuery["parent_class_chains"] = [ parentCellClassChain ]
        isfound, respInfo = crifanWda.findElement(curSession, query=downloadingButtonQuery, timeout=0.1)
        if isfound:
            isDownloading = isfound
            curElement = respInfo
            curValue = curElement.value # always get null
            if curValue is not None:
                curProgress = curValue
                break

    return isDownloading, curProgress

def testWdaElementName(curSession):
    """
        AppStore 详情页 不折叠输入法 带金额的购买按钮 ¥1.00：
            <XCUIElementTypeCollectionView type="XCUIElementTypeCollectionView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="-672" width="414" height="736"/>
                <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="64" width="414" height="211">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" value="不折叠输入法" name="插图" label="插图" enabled="true" visible="true" x="20" y="64" width="118" height="118"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="不折叠输入法" name="不折叠输入法" label="不折叠输入法" enabled="true" visible="true" x="154" y="71" width="134" height="27"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="JUNJIE HUANG" name="JUNJIE HUANG" label="JUNJIE HUANG" enabled="true" visible="false" x="154" y="101" width="108" height="19"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="新版发文不再一行的小键盘" name="新版发文不再一行的小键盘" label="新版发文不再一行的小键盘" enabled="true" visible="true" x="154" y="101" width="184" height="19"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="¥1.00" label="¥1.00" enabled="true" visible="true" x="154" y="152" width="74" height="30"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="App 内购买项目" name="App 内购买项目" label="App 内购买项目" enabled="true" visible="true" x="234" y="152" width="62" height="30"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="366" y="154" width="28" height="28"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" name="三颗星, 793个评分, 3, 工具, 4+, 年龄" label="三颗星, 793个评分, 3, 工具, 4+, 年龄" enabled="true" visible="true" x="20" y="202" width="374" height="50"/>
                </XCUIElementTypeCell>
    """
    parentCellClassChain = "/XCUIElementTypeCell[`rect.x = 0 AND rect.width = %d`]" % ScreenX
    moneyButtonQuery = {"type":"XCUIElementTypeButton", "nameContains": "¥", "enabled": "true"}
    moneyButtonQuery["parent_class_chains"] = [ parentCellClassChain ]
    foundMoneyButton, respInfo = crifanWda.findElement(curSession, query=moneyButtonQuery, timeout=0.1)
    if foundMoneyButton:
        curElement = respInfo
        curName = curElement.name
        # curName = curElement.text
        if curName is not None:
            moneyButtonName = curName

def testWdaElementClearText(curSession):
    """
        测试删除已有文本值
    """

    """
        <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="269" width="414" height="46">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="269" width="414" height="1"/>
            <XCUIElementTypeTextField type="XCUIElementTypeTextField" value="192.168.31.46" name="服务器" label="服务器" enabled="true" visible="true" x="92" y="281" width="294" height="21"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="15" y="313" width="305" height="1"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="20" y="313" width="394" height="2"/>
        </XCUIElementTypeCell>
    """
    parentCellClassChain = "/XCUIElementTypeCell[`rect.x = 0 AND rect.width = %d`]" % ScreenX
    serverFieldQuery = {"type":"XCUIElementTypeTextField", "name": "服务器", "enabled": "true"}
    serverFieldQuery["parent_class_chains"] = [ parentCellClassChain ]
    foundServer, respInfo = crifanWda.findElement(curSession, query=serverFieldQuery, timeout=0.1)
    if foundServer:
        curElement = respInfo
        # curElement.click()
        # curElement.clear_text()
        # curElement.tap_hold(2.0)
        backspaceChar = '\b'
        maxDeleteNum = 50
        curElement.set_text(maxDeleteNum * backspaceChar)
        # click 全选
        debugSaveScreenshot(curScale=curSession.scale)
        debugSaveSource()


def wdaTest():
    global gServerUrl, gWdaClient, gCurSession, gCurAppId

    appCrawlerCommon.wdaCommonInit()
    gWdaClient = crifanWda.gWdaClient
    gServerUrl = crifanWda.gServerUrl
    gCurAppId = crifanWda.gCurAppId
    gCurSession = crifanWda.gCurSession
    curSession = gCurSession

    # testDeviceManage()

    # testAppState()

    isDebugScreenAndSource = False
    isDebugScreenAndSource = True

    if isDebugScreenAndSource:
        while True:
            debugSaveScreenshot(curScale=curSession.scale)
            debugSaveSource()
            print("----------")

    # testRectPredicteSearch(curSession)

    # testWdaBasicFunction()
    # testAppDeviceInfo(curSession)
    # testLaunchApp(curSession)

    # testWdaAttributeValue(curSession)

    # testWdaElementName(curSession)

    # testWdaElementClearText(curSession)

if __name__ == "__main__":
    wdaTest()