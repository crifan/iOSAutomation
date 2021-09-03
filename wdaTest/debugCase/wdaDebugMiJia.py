# Functon: debug iOS app 斑马AI课 cases
# Author: Crifan Li
# Update: 20200601

import re

import sys
import os
CurrentFile = os.path.abspath(__file__) 
CurrentFolder = os.path.dirname(CurrentFile)
ParentFolder = os.path.dirname(CurrentFolder)
ParentParentFolder = os.path.dirname(ParentFolder)
sys.path.append(CurrentFolder)
sys.path.append(ParentFolder)
sys.path.append(ParentParentFolder)

from libs import crifanLogging

from libs import utils
from libs import crifanWda
from libs import appCrawlerCommon
from libs import crifanBeautifulsoup

################################################################################
# Config
################################################################################

ScreenX = 414
ScreenY = 736

################################################################################
# Global Variable
################################################################################

gServerUrl = None
gWdaClient = None
gCurSession = None
gCurAppId = None

gFullScreenAttrDict = None

################################################################################
# Main
################################################################################

def debugMiJiaPopupLocationChooseSave(curSession):
    foundAndProcessedPopup = False
    curPageXml = crifanWda.getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        米家 弹框 地区选择 保存：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">

                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="414" height="88">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="10" y="64" width="394" height="36">
                                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="10" y="64" width="394" height="36"/>
                                <XCUIElementTypeSearchField type="XCUIElementTypeSearchField" name="搜索" label="搜索" enabled="true" visible="true" x="18" y="64" width="378" height="36"/>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="110" width="414" height="10"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="选择你的使用国家或地区" name="选择你的使用国家或地区" label="选择你的使用国家或地区" enabled="true" visible="true" x="22" y="120" width="368" height="32"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="22" y="151" width="392" height="1"/>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="0" y="152" width="414" height="450">

                        </XCUIElementTypeTable>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" value="1" name="checkbox unchecked" label="checkbox unchecked" enabled="true" visible="true" x="91" y="626" width="20" height="20"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="我已阅读 用户协议和隐私政策" label="我已阅读 用户协议和隐私政策" enabled="true" visible="true" x="119" y="622" width="176" height="28"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="保存" label="保存" enabled="true" visible="true" x="24" y="672" width="366" height="42"/>
                    </XCUIElementTypeOther>
    """
    FullScreenSoupAttrDict = crifanBeautifulsoup.generateFullScreenSoupAttrDict(ScreenX, ScreenY)
    commonSaveChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": FullScreenSoupAttrDict
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": FullScreenSoupAttrDict
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"保存"}
        },
    ]
    commonSaveSoup = utils.bsChainFind(soup, commonSaveChainList)
    if commonSaveSoup:
        appCrawlerCommon.clickCenterPosition(curSession, commonSaveSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

# def debugCommonPopupAccessContactOK(curSession):
def iOSProcessCommonAlertOk(curSession):
    foundAndProcessedPopup = False
    curPageXml = crifanWda.getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        恒易贷 弹框 想访问您的通讯录 好：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="“恒易贷”想访问您的通讯录" label="“恒易贷”想访问您的通讯录" enabled="true" visible="true" x="72" y="298" width="270" height="141">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="298" width="270" height="141">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="298" width="270" height="141">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="298" width="270" height="141">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="298" width="270" height="141"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="298" width="270" height="141">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="298" width="270" height="141"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="298" width="270" height="141"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="298" width="270" height="141">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="298" width="270" height="96">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="298" width="270" height="96">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="“恒易贷”想访问您的通讯录" name="“恒易贷”想访问您的通讯录" label="“恒易贷”想访问您的通讯录" enabled="true" visible="true" x="88" y="317" width="238" height="21"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="恒易贷需要获取您的通讯录信息，以提供更精准的服务" name="恒易贷需要获取您的通讯录信息，以提供更精准的服务" label="恒易贷需要获取您的通讯录信息，以提供更精准的服务" enabled="true" visible="true" x="88" y="341" width="238" height="33"/>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="1">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="394" width="270" height="1"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="1"/>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="135" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="不允许" label="不允许" enabled="true" visible="true" x="72" y="394" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="394" width="1" height="45">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="207" y="394" width="1" height="45"/>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="394" width="1" height="45"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="394" width="135" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="好" label="好" enabled="true" visible="true" x="207" y="394" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>
        
        米家 弹框 想访问您的家庭数据 好：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="“米家”想访问您的家庭数据" label="“米家”想访问您的家庭数据" enabled="true" visible="true" x="72" y="290" width="270" height="157">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="290" width="270" height="157">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="290" width="270" height="157">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="290" width="270" height="157">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="290" width="270" height="157"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="290" width="270" height="157">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="290" width="270" height="157"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="290" width="270" height="157"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="290" width="270" height="157">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="290" width="270" height="112">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="290" width="270" height="112">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="“米家”想访问您的家庭数据" name="“米家”想访问您的家庭数据" label="“米家”想访问您的家庭数据" enabled="true" visible="true" x="88" y="309" width="238" height="21"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="HomeKit权限将用于通过“米家App”来访问并控制已接入HomeKit的设备。请点击“好”，授权米家使用该权限。" name="HomeKit权限将用于通过“米家App”来访问并控制已接入HomeKit的设备。请点击“好”，授权米家使用该权限。" label="HomeKit权限将用于通过“米家App”来访问并控制已接入HomeKit的设备。请点击“好”，授权米家使用该权限。" enabled="true" visible="true" x="88" y="333" width="238" height="49"/>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="402" width="270" height="1">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="402" width="270" height="1"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="402" width="270" height="1"/>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="402" width="270" height="45">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="402" width="270" height="45">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="402" width="270" height="45">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="402" width="135" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="不允许" label="不允许" enabled="true" visible="true" x="72" y="402" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="402" width="1" height="45">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="207" y="402" width="1" height="45"/>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="402" width="1" height="45"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="402" width="135" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="好" label="好" enabled="true" visible="true" x="207" y="402" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>
    """
    accessYourP = re.compile("想访问您的") # “恒易贷”想访问您的通讯录, “米家”想访问您的家庭数据"
    okChainList = [
        {
            "tag": "XCUIElementTypeAlert",
            "attrs": {"enabled":"true", "visible":"true", "name": accessYourP}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"好"}
        },
    ]
    okSoup = utils.bsChainFind(soup, okChainList)
    if okSoup:
        foundAndProcessedPopup = crifanWda.findAndClickButtonElementBySoup(curSession, okSoup)

    return foundAndProcessedPopup

def debugMiJiaCommonConfirmButton(curSession):
    """
        other下面other下的button name="确定"
    """
    foundAndProcessedPopup = False
    curPageXml = crifanWda.getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        米家 弹框 米家隐私政策 确定：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="41" y="243" width="332" height="250">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="米家隐私政策" name="米家隐私政策" label="米家隐私政策" enabled="true" visible="true" x="49" y="263" width="316" height="16"/>
                    <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="我们的隐私政策已于2018年4月28日更新，将会于2018年5月25日生效。我们对隐私政策进行了详细修订，从该日期开始，这一隐私政策能够提供有关我们如何管理你在使用所有米家产品和服务时透露的个人信息的隐私详情，特定的米家产品或服务提供独立的隐私政策除外。&#10;请花一些时间熟悉我们的隐私权惯例，如果你有任何问题，请告诉我们。&#10;&#10; 米家隐私政策 " enabled="true" visible="true" x="49" y="283" width="316" height="145"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="41" y="442" width="332" height="1"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="41" y="443" width="166" height="50"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="206" y="443" width="2" height="50"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="207" y="443" width="166" height="50"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    FullScreenAttrDict = crifanBeautifulsoup.generateFullScreenSoupAttrDict(ScreenX, ScreenY)
    confirmChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": FullScreenAttrDict
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"确定"}
        },
    ]
    confirmSoup = utils.bsChainFind(soup, confirmChainList)
    if confirmSoup:
        appCrawlerCommon.clickCenterPosition(curSession, confirmSoup.attrs)
        foundAndProcessedPopup = True

    return foundAndProcessedPopup

def debugMiJiaImmediatelyExperience(curSession):
    """
        弹框 other->other-button name=立即体验
    """

    """
        米家 弹框 立即体验：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" name="sort_guide_icon" enabled="true" visible="false" x="54" y="115" width="306" height="310"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="设备排序全新升级" name="设备排序全新升级" label="设备排序全新升级" enabled="true" visible="true" x="111" y="426" width="192" height="34"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="1.新增快速置顶，排序操作更方便 2.顶部排序固定，不会被随意打乱" name="1.新增快速置顶，排序操作更方便 2.顶部排序固定，不会被随意打乱" label="1.新增快速置顶，排序操作更方便 2.顶部排序固定，不会被随意打乱" enabled="true" visible="true" x="95" y="468" width="224" height="42"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="立即体验" label="立即体验" enabled="true" visible="true" x="24" y="657" width="366" height="43"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    immediatelyExperienceChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": gFullScreenAttrDict
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": gFullScreenAttrDict
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"立即体验"}
        },
    ]
    foundAndProcessedPopup = crifanWda.findAndClickCenterPosition(curSession, immediatelyExperienceChainList)
    return foundAndProcessedPopup

def wdaDebugCommon():
    global gServerUrl, gWdaClient, gCurSession, gCurAppId, gFullScreenAttrDict

    gFullScreenAttrDict = crifanBeautifulsoup.generateFullScreenSoupAttrDict(ScreenX, ScreenY)

    appCrawlerCommon.wdaCommonInit()
    gWdaClient = crifanWda.gWdaClient
    gServerUrl = crifanWda.gServerUrl
    gCurAppId = crifanWda.gCurAppId
    gCurSession = crifanWda.gCurSession

    curSession = gCurSession

    # debugMiJiaPopupLocationChooseSave(curSession)

    # iOSProcessCommonAlertOk(curSession)

    # debugMiJiaCommonConfirmButton(curSession)

    debugMiJiaImmediatelyExperience(curSession)

    pass

if __name__ == "__main__":
    wdaDebugCommon()