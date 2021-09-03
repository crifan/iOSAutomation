# Functon: debug iOS app 斑马AI课 cases
# Author: Crifan Li
# Update: 20200601

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
gCurAppId = None

################################################################################
# Main
################################################################################

def debugBanMaPopupCommonCancel(curSession):
    foundAndProcessedPopup = False
    curPageXml = crifanWda.getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        斑马AI课 弹框 该音频为专属音频 取消：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="414" height="736"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="20" width="414" height="716"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="30" y="178" width="354" height="380">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" name="ZBEFMAlertImage" enabled="true" visible="false" x="93" y="198" width="228" height="184"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="该音频为专属音频，仅对英语S2系统课用户开放" name="该音频为专属音频，仅对英语S2系统课用户开放" label="该音频为专属音频，仅对英语S2系统课用户开放" enabled="true" visible="true" x="57" y="395" width="300" height="43"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="查看课程详情" label="查看课程详情" enabled="true" visible="true" x="79" y="454" width="256" height="44"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="191" y="510" width="32" height="30"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeWindow>
    """
    commonCancelChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            # "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"取消"}
        },
    ]
    commonCancelSoup = utils.bsChainFind(soup, commonCancelChainList)
    if commonCancelSoup:
        appCrawlerCommon.clickCenterPosition(curSession, commonCancelSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def wdaDebugCommon():
    global gServerUrl, gWdaClient, gCurSession, gCurAppId

    appCrawlerCommon.wdaCommonInit()
    gWdaClient = crifanWda.gWdaClient
    gServerUrl = crifanWda.gServerUrl
    gCurAppId = crifanWda.gCurAppId
    gCurSession = crifanWda.gCurSession

    curSession = gCurSession

    debugBanMaPopupCommonCancel(curSession)

    pass

if __name__ == "__main__":
    wdaDebugCommon()