# Functon: debug iOS weixin many cases
# Author: Crifan Li
# Update: 20200601

import logging
sys.path.append("libs")
from libs import crifanLogging
from libs import utils

# ScreenX = 375
# ScreenY = 667
ScreenX = 414
ScreenY = 736

global gWdaClient


def debugBack(curSession):
    global gWdaClient
    # iOS: NO phisical back button

    isFoundAndClicked = False

    # case 1: 导航栏下的按钮： 关闭、 返回
    if not isFoundAndClicked:
        # try emulate click left up corner back or close button to back to previous page
        """
            <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="通讯录" enabled="true" visible="true" x="0" y="20" width="375" height="44">
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="关闭" label="关闭" enabled="true" visible="true" x="16" y="20" width="40" height="44"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="187" y="24" width="1" height="36"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="319" y="20" width="40" height="44"/>
            </XCUIElementTypeNavigationBar>
        """

        """
            <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="动卡空间" enabled="true" visible="true" x="0" y="20" width="414" height="44">
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="返回" label="返回" enabled="true" visible="true" x="20" y="20" width="30" height="44"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" name="动卡空间," label="动卡空间," enabled="true" visible="true" x="206" y="24" width="2" height="36"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="聊天详情" label="聊天详情" enabled="true" visible="true" x="354" y="20" width="40" height="44"/>
            </XCUIElementTypeNavigationBar>
        """

        parentNaviBarClassChain = "/XCUIElementTypeNavigationBar[`rect.width = %d`]" % ScreenX
        # BackTypeButtonList = ["关闭", "返回"]
        BackTypeButtonList = ["返回", "关闭"]
        for eachBackButton in BackTypeButtonList:
            backBtnQuery = {"type":"XCUIElementTypeButton", "name": eachBackButton, "label": eachBackButton, "enabled": "true"}
            backBtnQuery["parent_class_chains"] = [parentNaviBarClassChain]
            isFoundBack, respInfo = findElement(curSession, query=backBtnQuery)
            if isFoundBack:
                backElement = respInfo
                clickOk = clickElement(curSession, backElement)
                isFoundAndClicked = clickOk

                if isFoundAndClicked:
                    break

    # case 3: full screen image, click any position to back
    if not isFoundAndClicked:
        # debugSaveScreenshot(curScale=2)
        # debugSaveSource()

        isFoundFullScreenImage = False
        curPageXml = getPageSource(gWdaClient)
        soup = utils.xmlToSoup(curPageXml)
        FullScreenImageText = "关闭"
        foundFullScreenImage = soup.find(
            'XCUIElementTypeImage',
            attrs={"type": "XCUIElementTypeImage", "name": FullScreenImageText, "label": FullScreenImageText},
        )
        logging.debug("foundFullScreenImage=%s", foundFullScreenImage)
        if foundFullScreenImage:
            imageParent = foundFullScreenImage.parent
            if imageParent:
                ParentName = "XCUIElementTypeScrollView"
                isNameMatch = imageParent.name == ParentName
                curAttrib = imageParent.attrs
                x = int(curAttrib["x"])
                y = int(curAttrib["y"])
                width = int(curAttrib["width"])
                height = int(curAttrib["height"])
                isBoundsMatch = (x == 0) and (y ==0) and (width == ScreenX) and (height == ScreenY)
                isParentMatch = isNameMatch and isBoundsMatch
                if isParentMatch:
                    imageParentParent = imageParent.parent
                    if imageParentParent:
                        ParentParentName = "XCUIElementTypeScrollView"
                        isNameMatch = imageParentParent.name == ParentParentName
                        curAttrib = imageParentParent.attrs
                        height = int(curAttrib["height"])
                        isHeightMatch = height == ScreenY
                        isParentParentMatch  = isNameMatch and isHeightMatch

                        isFoundFullScreenImage = isParentParentMatch

        if isFoundFullScreenImage:
            screenCenterX = int(ScreenX / 2)
            screenCenterY = int(ScreenY / 2)
            curSession.click(screenCenterX, screenCenterY)
            isFoundAndClicked = True

    return isFoundAndClicked

def getWeixinSecondMenuParentElement_iOS(curPageXml):
    """get second menu parent element
        XCUIElementTypeScrollView's parent's parent, should be XCUIElementTypeButton
    """
    secondMenuParentElement = None

    soup = utils.xmlToSoup(curPageXml)
    foundScrollView = soup.find(
        'XCUIElementTypeScrollView',
        attrs={"type": "XCUIElementTypeScrollView", "enabled": "true", "visible": "true"},
    )
    if foundScrollView:
        scrollViewParent = foundScrollView.parent
        if scrollViewParent:
            scrollViewParentParent = scrollViewParent.parent
            if scrollViewParentParent:
                scrollViewParentParentPrevSibling = scrollViewParentParent.previous_sibling
                if scrollViewParentParentPrevSibling:
                    scrollViewParentParentPrevPrevSibling = scrollViewParentParentPrevSibling.previous_sibling
                    if scrollViewParentParentPrevPrevSibling:
                        curNodeName = scrollViewParentParentPrevPrevSibling.name
                        XCUIElementTypeButton = "XCUIElementTypeButton"
                        if curNodeName == XCUIElementTypeButton:
                            secondMenuParentElement = scrollViewParentParentPrevPrevSibling
                    else:
                        logging.debug("no second menu for scroll view parent parent previous's previous sibling is empty")
                else:
                    logging.debug("no second menu for scroll view parent parent previous sibling is empty")
            else:
                logging.debug("no second menu for not found scroll view parent parent")
        else:
            logging.debug("no second menu for not found scroll view parent")
    else:
        logging.debug("no second menu for not found scroll view")

    return secondMenuParentElement


def getWeixinSecondMenuElementList_iOS(curSession):
    global gWdaClient

    # secondMenuSoupNodeList = []
    secondMenuElementList = []
    subMenuSoupNodeList = []
    secondMenuParentElement = None

    curPageXml = getPageSource(gWdaClient)
    secondMenuParentElement = getWeixinSecondMenuParentElement_iOS(curPageXml)
    if secondMenuParentElement:
        if not subMenuSoupNodeList:
            """
            three button:
                <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="622">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="0" y="0" width="375" height="622"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="69" y="461" width="122" height="150">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="69" y="461" width="52" height="150"/>
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="120" y="461" width="19" height="150"/>
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="138" y="461" width="53" height="150"/>
                        <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="69" y="470" width="122" height="126">
                            <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="69" y="470" width="122" height="40">
                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="兴业 信用卡" label="兴业 信用卡" enabled="true" visible="true" x="69" y="470" width="122" height="40"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="84" y="509" width="107" height="1"/>
                            </XCUIElementTypeCell>
                            <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="69" y="510" width="122" height="3">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="84" y="512" width="107" height="1"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="89" y="510" width="82" height="1"/>
                            </XCUIElementTypeCell>
                            <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="69" y="513" width="122" height="40">
                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="交通 信用卡" label="交通 信用卡" enabled="true" visible="true" x="69" y="513" width="122" height="40"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="84" y="552" width="107" height="1"/>
                            </XCUIElementTypeCell>
                            <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="69" y="553" width="122" height="3">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="84" y="555" width="107" height="1"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="89" y="553" width="82" height="1"/>
                            </XCUIElementTypeCell>
                            <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="69" y="556" width="122" height="40">
                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="平安 信用卡" label="平安 信用卡" enabled="true" visible="true" x="69" y="556" width="122" height="40"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="84" y="595" width="107" height="1"/>
                            </XCUIElementTypeCell>
                        </XCUIElementTypeTable>
                    </XCUIElementTypeOther>
                </XCUIElementTypeButton>
            """
            foundTable = secondMenuParentElement.find("XCUIElementTypeTable")
            if foundTable:
                subMenuSoupNodeList = foundTable.find_all("XCUIElementTypeButton", attrs={"type":"XCUIElementTypeButton", "enabled":"true"})

        if not subMenuSoupNodeList:
            """
            XCUIElementTypeButton's XCUIElementTypeStaticText:
                <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="414" height="691">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="兴业 信用卡" name="兴业 信用卡" label="兴业 信用卡" enabled="true" visible="true" x="99" y="593" width="81" height="18"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="交通 信用卡" name="交通 信用卡" label="交通 信用卡" enabled="true" visible="true" x="99" y="636" width="81" height="18"/>
                </XCUIElementTypeButton>
            """
            notEmptyP = re.compile(".+")
            subMenuSoupNodeList = secondMenuParentElement.find_all("XCUIElementTypeStaticText",
                attrs={"type": "XCUIElementTypeStaticText", "value": notEmptyP})

        if subMenuSoupNodeList:
            # secondMenuSoupNodeList = subMenuSoupNodeList
    
            # convert to Element for later calc MD5
            # for eachSoupNode in secondMenuSoupNodeList:
            for eachSoupNode in subMenuSoupNodeList:
                curTag = eachSoupNode.name
                curAttrib = eachSoupNode.attrs

                # xml XMLElement 
                # curQuery = curAttrib
                # foundElement = self.findElement(query=curQuery)

                # lxml etree.Element
                curLxmlElement = etree.Element(curTag, attrib=curAttrib)
                logging.info("curLxmlElement=%s", curLxmlElement)
                secondMenuElementList.append(curLxmlElement)

    # return secondMenuSoupNodeList
    return secondMenuElementList, secondMenuParentElement


def debugSecondLevelMenu(curSession):
    debugSaveScreenshot(curScale=curSession.scale)
    debugSaveSource()

    getWeixinSecondMenuElementList_iOS(curSession)

def debugBack_PublicAccounSearchPage(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    global gWdaClient

    ScreenX = 414
    ScreenY = 736

    isFoundAndClicked = False

    backQueryList = []

    parentNaviBarClassChain = "/XCUIElementTypeNavigationBar[`rect.width = %d`]" % ScreenX

    # case 1: 左上角 导航栏 返回
    """
        <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="动卡空间" enabled="true" visible="true" x="0" y="20" width="414" height="44">
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="返回" label="返回" enabled="true" visible="true" x="20" y="20" width="30" height="44"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="动卡空间," label="动卡空间," enabled="true" visible="true" x="206" y="24" width="2" height="36"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="聊天详情" label="聊天详情" enabled="true" visible="true" x="354" y="20" width="40" height="44"/>
        </XCUIElementTypeNavigationBar>
    """
    NaviBarReturnText = "返回"
    returnButtonQuery = {"type":"XCUIElementTypeButton", "name": NaviBarReturnText, "label": NaviBarReturnText, "enabled": "true"}
    returnButtonQuery["parent_class_chains"] = [ parentNaviBarClassChain ]
    backQueryList.append(returnButtonQuery)

    # case 2: 左上角 导航栏 关闭
    """
        <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="通讯录" enabled="true" visible="true" x="0" y="20" width="375" height="44">
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="关闭" label="关闭" enabled="true" visible="true" x="16" y="20" width="40" height="44"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="187" y="24" width="1" height="36"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="319" y="20" width="40" height="44"/>
        </XCUIElementTypeNavigationBar>
    """
    NaviBarCloseText = "关闭"
    closeButtonQuery = {"type":"XCUIElementTypeButton", "name": NaviBarCloseText, "label": NaviBarCloseText, "enabled": "true"}
    closeButtonQuery["parent_class_chains"] = [ parentNaviBarClassChain ]
    backQueryList.append(closeButtonQuery)

    # case 3: 公众号搜索页的左上角的返回
    """
        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="0" y="0" width="414" height="70">
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="返回" label="返回" enabled="true" visible="true" x="0" y="20" width="33" height="50"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="33" y="20" width="381" height="56">
                ...
            </XCUIElementTypeOther>
        </XCUIElementTypeImage>
    """
    SearchReturnName = "返回"
    parentImageClassChain = "/XCUIElementTypeImage[`rect.width = %d`]" % ScreenX
    searchReturnQuery = {"type":"XCUIElementTypeButton", "name": SearchReturnName, "label": SearchReturnName, "enabled": "true"}
    searchReturnQuery["parent_class_chains"] = [ parentImageClassChain ]
    backQueryList.append(searchReturnQuery)

    # case 4: 全屏显示的图片 full screen image, click any position to back
    """
        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="-10" y="0" width="395" height="667">
            <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeImage type="XCUIElementTypeImage" name="关闭" label="关闭" enabled="true" visible="true" x="0" y="127" width="375" height="412"/>
            </XCUIElementTypeScrollView>
        </XCUIElementTypeScrollView>

        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="-10" y="0" width="395" height="667">
            <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeImage type="XCUIElementTypeImage" name="关闭" label="关闭" enabled="true" visible="true" x="0" y="17" width="375" height="632"/>
            </XCUIElementTypeScrollView>
        </XCUIElementTypeScrollView>

        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="-10" y="0" width="434" height="736">
            <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeImage type="XCUIElementTypeImage" name="关闭" label="关闭" enabled="true" visible="true" x="0" y="140" width="414" height="455"/>
            </XCUIElementTypeScrollView>
        </XCUIElementTypeScrollView>
    """
    FullScreenImageText = "关闭"
    parentParentScrollClassChain = "/XCUIElementTypeScrollView[`rect.height = %d`]" % ScreenY
    parentScrollClassChain = "/XCUIElementTypeScrollView[`rect.width = %d AND rect.height = %d`]" % (ScreenX, ScreenY)
    fullScreenImageQuery = {"type":"XCUIElementTypeImage", "name": FullScreenImageText, "label": FullScreenImageText, "enabled": "true"}
    fullScreenImageQuery["parent_class_chains"] = [ parentParentScrollClassChain, parentScrollClassChain ]
    backQueryList.append(fullScreenImageQuery)

    # find and click
    for eachBackQuery in backQueryList:
        isCurFound, respInfo = findElement(curSession, query=eachBackQuery)
        logging.debug("eachBackQuery=%s -> isCurFound=%s", eachBackQuery, isCurFound)
        if isCurFound:
            curElement = respInfo
            clickOk = clickElement(curSession, curElement)
            isFoundAndClicked = clickOk

            if isFoundAndClicked:
                break

    return isFoundAndClicked

def debugDisplayed(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    """
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="16" y="707" width="382" height="54">
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="同车人员最高10万元/人乘车意外保障（最多限6人）" name="同车人员最高10万元/人乘车意外保障（最多限6人）" label="同车人员最高10万元/人乘车意外保障（最多限6人）" enabled="true" visible="true" x="16" y="709" width="382" height="49"/>
        </XCUIElementTypeOther>
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="16" y="761" width="382" height="54">
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="车上所有人员（含驾驶员）最高4000元/人驾乘意外医疗保障" name="车上所有人员（含驾驶员）最高4000元/人驾乘意外医疗保障" label="车上所有人员（含驾驶员）最高4000元/人驾乘意外医疗保障" enabled="true" visible="false" x="16" y="763" width="382" height="49"/>
        </XCUIElementTypeOther>
    """
    # visibleTrueQuery = {"type": "XCUIElementTypeOther", "visible": "true", "x": "16", "y": "707", "width":"382", "height":"54"}
    visibleTrueQuery = {"type": "XCUIElementTypeOther", "x": "16", "y": "707", "width":"382", "height":"54"}
    isFound, respInfo = findElement(curSession, query=visibleTrueQuery)
    logging.debug("isFound=%s, respInfo=%s", isFound, respInfo)


def debugWeixinExceptionNextStep(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()
    global gWdaClient

    foundAndClicked = False

    scrollViewClassChain = "/XCUIElementTypeScrollView[`rect.width = %d AND rect.height = %d`]" % (ScreenX, ScreenY)

    ButtonLabelNextStep = "下一步"
    ButtonLabelIntoWeixin = "进入微信"

    # nextStepButtonQuery = {"type":"XCUIElementTypeButton", "label": "下一步", "enabled": "true"}
    # nextStepButtonQuery["parent_class_chains"] = [scrollViewClassChain]

    # intoWeixinButtonQuery = {"type":"XCUIElementTypeButton", "label": "进入微信", "enabled": "true"}
    # intoWeixinButtonQuery["parent_class_chains"] = [scrollViewClassChain]

    """
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="147" y="106" width="120" height="120"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="当前检测出微信连续异常，你可以尝试以下方法修复：" name="当前检测出微信连续异常，你可以尝试以下方法修复：" label="当前检测出微信连续异常，你可以尝试以下方法修复：" enabled="true" visible="true" x="18" y="262" width="378" height="39"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="下一步" label="下一步" enabled="true" visible="true" x="18" y="319" width="378" height="47">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="下一步" name="下一步" label="下一步" enabled="true" visible="true" x="179" y="331" width="56" height="23"/>
                </XCUIElementTypeButton>
            </XCUIElementTypeScrollView>
        </XCUIElementTypeOther>
    """
    # continousExceptionQuery = {"type":"XCUIElementTypeStaticText", "value": "当前检测出微信连续异常，你可以尝试以下方法修复：", "enabled": "true"}
    # continousExceptionQuery["parent_class_chains"] = [scrollViewClassChain]
    # isFoundContinousException, respInfo = findElement(curSession, query=continousExceptionQuery, timeout=0.5)
    # if isFoundContinousException:
    #     isFoundNextStep, respInfo = findElement(curSession, query=nextStepButtonQuery)
    #     if isFoundNextStep:
    #         nextStepElement = respInfo
    #         foundAndClicked = clickElement(curSession, nextStepElement)

    """
        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="147" y="106" width="120" height="120"/>
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="建议你重启手机，避免微信启动异常" name="建议你重启手机，避免微信启动异常" label="建议你重启手机，避免微信启动异常" enabled="true" visible="true" x="18" y="262" width="378" height="15"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="重启手机" label="重启手机" enabled="true" visible="true" x="18" y="285" width="378" height="47">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="重启手机" name="重启手机" label="重启手机" enabled="true" visible="true" x="170" y="297" width="74" height="23"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="不重启手机，进入下一步" name="不重启手机，进入下一步" label="不重启手机，进入下一步" enabled="true" visible="true" x="18" y="356" width="378" height="15"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="下一步" label="下一步" enabled="true" visible="true" x="18" y="379" width="378" height="47">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="下一步" name="下一步" label="下一步" enabled="true" visible="true" x="179" y="391" width="56" height="23"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="垂直滚动条, 1页" label="垂直滚动条, 1页" enabled="true" visible="true" x="381" y="64" width="30" height="672"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="水平滚动条, 1页" label="水平滚动条, 1页" enabled="true" visible="true" x="0" y="703" width="414" height="30"/>
        </XCUIElementTypeScrollView>
    """
    # # if not foundAndClicked:
    # rebootWeixinQuery = {"type":"XCUIElementTypeStaticText", "value": "建议你重启手机，避免微信启动异常", "enabled": "true"}
    # rebootWeixinQuery["parent_class_chains"] = [scrollViewClassChain]
    # isFoundRebootWeixin, respInfo = findElement(curSession, query=rebootWeixinQuery, timeout=0.5)
    # if isFoundRebootWeixin:
    #     isFoundNextStep, respInfo = findElement(curSession, query=nextStepButtonQuery)
    #     if isFoundNextStep:
    #         nextStepElement = respInfo
    #         foundAndClicked = clickElement(curSession, nextStepElement)
    
    """
        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="414" height="243">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="115" y="94" width="184" height="183"/>
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="115" y="94" width="184" height="183"/>
            </XCUIElementTypeOther>
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="清理缓存会清理你的手机本地缓存文件，但不会清理你的消息数据，使用后需要重新登录微信" name="清理缓存会清理你的手机本地缓存文件，但不会清理你的消息数据，使用后需要重新登录微信" label="清理缓存会清理你的手机本地缓存文件，但不会清理你的消息数据，使用后需要重新登录微信" enabled="true" visible="true" x="18" y="330" width="378" height="29"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="清理缓存" label="清理缓存" enabled="true" visible="true" x="18" y="367" width="378" height="47">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="清理缓存" name="清理缓存" label="清理缓存" enabled="true" visible="true" x="170" y="379" width="74" height="23"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="不清理缓存，进入下一步" name="不清理缓存，进入下一步" label="不清理缓存，进入下一步" enabled="true" visible="true" x="18" y="438" width="378" height="15"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="下一步" label="下一步" enabled="true" visible="true" x="18" y="461" width="378" height="47">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="下一步" name="下一步" label="下一步" enabled="true" visible="true" x="179" y="473" width="56" height="23"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="垂直滚动条, 1页" label="垂直滚动条, 1页" enabled="true" visible="true" x="381" y="64" width="30" height="672"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="水平滚动条, 1页" label="水平滚动条, 1页" enabled="true" visible="true" x="0" y="703" width="414" height="30"/>
        </XCUIElementTypeScrollView>
    """
    # # if not foundAndClicked:
    # clearCacheQuery = {"type":"XCUIElementTypeStaticText", "value": "清理缓存会清理你的手机本地缓存文件，但不会清理你的消息数据，使用后需要重新登录微信", "enabled": "true"}
    # clearCacheQuery["parent_class_chains"] = [scrollViewClassChain]
    # isFoundClearCache, respInfo = findElement(curSession, query=clearCacheQuery, timeout=0.5)
    # if isFoundClearCache:
    #     isFoundNextStep, respInfo = findElement(curSession, query=nextStepButtonQuery)
    #     if isFoundNextStep:
    #         nextStepElement = respInfo
    #         foundAndClicked = clickElement(curSession, nextStepElement)
    
    """
        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="147" y="106" width="120" height="120"/>
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="如果问题还没解决，你可以上传手机日志文件，协助技术人员解决问题。所上传的文件不会包含聊天记录等私人内容，且不会被对外传播" name="如果问题还没解决，你可以上传手机日志文件，协助技术人员解决问题。所上传的文件不会包含聊天记录等私人内容，且不会被对外传播" label="如果问题还没解决，你可以上传手机日志文件，协助技术人员解决问题。所上传的文件不会包含聊天记录等私人内容，且不会被对外传播" enabled="true" visible="true" x="18" y="262" width="378" height="29"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="上传文件" label="上传文件" enabled="true" visible="true" x="18" y="298" width="378" height="47">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="上传文件" name="上传文件" label="上传文件" enabled="true" visible="true" x="170" y="310" width="74" height="23"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="显示上传文件列表" label="显示上传文件列表" enabled="true" visible="true" x="17" y="353" width="100" height="15">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="显示上传文件列表" name="显示上传文件列表" label="显示上传文件列表" enabled="true" visible="true" x="17" y="352" width="100" height="16"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="不上传文件，进入下一步" name="不上传文件，进入下一步" label="不上传文件，进入下一步" enabled="true" visible="true" x="18" y="391" width="378" height="15"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="下一步" label="下一步" enabled="true" visible="true" x="18" y="413" width="378" height="47">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="下一步" name="下一步" label="下一步" enabled="true" visible="true" x="179" y="425" width="56" height="23"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="垂直滚动条, 1页" label="垂直滚动条, 1页" enabled="true" visible="true" x="381" y="64" width="30" height="672"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="水平滚动条, 1页" label="水平滚动条, 1页" enabled="true" visible="true" x="0" y="703" width="414" height="30"/>
        </XCUIElementTypeScrollView>
    """

    """
        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="147" y="106" width="120" height="120"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="147" y="106" width="120" height="120"/>
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="如果使用过程中还出现问题，建议你重启手机，更新系统，或者联系我们的客服人员。 当前设备标识：7a3e060db5c52291******" name="如果使用过程中还出现问题，建议你重启手机，更新系统，或者联系我们的客服人员。 当前设备标识：7a3e060db5c52291******" label="如果使用过程中还出现问题，建议你重启手机，更新系统，或者联系我们的客服人员。 当前设备标识：7a3e060db5c52291******" enabled="true" visible="true" x="18" y="262" width="378" height="58"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="进入微信" label="进入微信" enabled="true" visible="true" x="18" y="338" width="378" height="47">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="进入微信" name="进入微信" label="进入微信" enabled="true" visible="true" x="170" y="350" width="74" height="23"/>
            </XCUIElementTypeButton>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="垂直滚动条, 1页" label="垂直滚动条, 1页" enabled="true" visible="true" x="381" y="64" width="30" height="672"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" value="0%" name="水平滚动条, 1页" label="水平滚动条, 1页" enabled="true" visible="true" x="0" y="703" width="414" height="30"/>
        </XCUIElementTypeScrollView>
    """

    EachStepNoticeList = [
        ("当前检测出微信连续异常，你可以尝试以下方法修复：", ButtonLabelNextStep),
        ("建议你重启手机，避免微信启动异常", ButtonLabelNextStep),
        ("清理缓存会清理你的手机本地缓存文件，但不会清理你的消息数据，使用后需要重新登录微信", ButtonLabelNextStep),
        ("如果问题还没解决，你可以上传手机日志文件，协助技术人员解决问题。所上传的文件不会包含聊天记录等私人内容，且不会被对外传播", ButtonLabelNextStep),
        ("如果使用过程中还出现问题，建议你重启手机，更新系统，或者联系我们的客服人员。", ButtonLabelIntoWeixin),
    ]
    for (curStepNotice, buttonLabel) in EachStepNoticeList:
        # curNoticeQuery = {"type":"XCUIElementTypeStaticText", "value": curStepNotice, "enabled": "true"}
        # curNoticeQuery = {"type":"XCUIElementTypeStaticText", "value_part": curStepNotice, "enabled": "true"}
        curNoticeQuery = {"type":"XCUIElementTypeStaticText", "valueContains": curStepNotice, "enabled": "true"}
        curNoticeQuery["parent_class_chains"] = [scrollViewClassChain]
        isFoundCurNotice, respInfo = findElement(curSession, query=curNoticeQuery, timeout=0.5)
        if isFoundCurNotice:
            # isFoundNextStep, respInfo = findElement(curSession, query=nextStepButtonQuery)
            # isFoundButton, respInfo = findElement(curSession, query=buttonQuery)
            buttonQuery = {"type":"XCUIElementTypeButton", "label": buttonLabel, "enabled": "true"}
            buttonQuery["parent_class_chains"] = [scrollViewClassChain]
            isFoundButton, respInfo = findElement(curSession, query=buttonQuery)
            if isFoundButton:
                buttonElement = respInfo
                clickOk = clickElement(curSession, buttonElement)
                if clickOk:
                    foundAndClicked = clickOk

    return foundAndClicked


def isInWeixin(curSession):
    tabBarClassChain = "/XCUIElementTypeTabBar[`rect.width = %d`]" % ScreenX

    """
        <XCUIElementTypeTabBar type="XCUIElementTypeTabBar" enabled="true" visible="true" x="0" y="680" width="414" height="56">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="680" width="414" height="56">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="680" width="414" height="56">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="680" width="414" height="56"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="680" width="414" height="56"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="680" width="414" height="56"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
            <XCUIElementTypeButton type="XCUIElementTypeButton" value="2" name="微信" label="微信" enabled="true" visible="true" x="2" y="681" width="100" height="55"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="通讯录" label="通讯录" enabled="true" visible="true" x="106" y="681" width="99" height="55"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" value="未读" name="发现" label="发现" enabled="true" visible="true" x="209" y="681" width="100" height="55"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="我" label="我" enabled="true" visible="true" x="313" y="681" width="99" height="55"/>
        </XCUIElementTypeTabBar>
    """
    weixinTabQuery = {"type":"XCUIElementTypeButton", "name": "微信", "label": "微信", "enabled": "true"}
    weixinTabQuery["parent_class_chains"] = [ tabBarClassChain ]
    isFoundWeixin, respInfo = crifanWda.findElement(curSession, query=weixinTabQuery, timeout=0.2)
    inWeixin = isFoundWeixin
    return inWeixin

def debugMakesureIntoWeixin(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    global gWdaClient

    maxRetryNum = 3

    beInWeixin = isInWeixin(curSession)

    while (not beInWeixin) and (maxRetryNum > 0):
        beInWeixin = isInWeixin(curSession)
        if not beInWeixin:
            # try process for exception
            foundAndProcessedException = debugWeixinExceptionNextStep(curSession)
            if foundAndProcessedException:
                beInWeixin = isInWeixin(curSession)

        maxRetryNum -= 1

    return beInWeixin


def debugPopupCertificate(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    # alertText = gWdaClient.alert.text
    # curAlert = curSession.alert
    # alertText = curAlert.text
    # logging.debug("alertText=%s", alertText)
    # alertButtons = curAlert.buttons()
    # logging.debug("alertButtons=%s", alertButtons)

    global gWdaClient

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    """
        <XCUIElementTypeButton type="XCUIElementTypeButton" name="网络出错，轻触屏幕重新加载:-1202" label="网络出错，轻触屏幕重新加载:-1202" enabled="true" visible="true" x="0" y="64" width="414" height="672">
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="网络出错，轻触屏幕重新加载:-1202" name="网络出错，轻触屏幕重新加载:-1202" label="网络出错，轻触屏幕重新加载:-1202" enabled="true" visible="true" x="0" y="264" width="414" height="40"/>
        </XCUIElementTypeButton>
    """
    netErrTouchReloadP = re.compile("网络出错，轻触屏幕重新加载")
    foundTouchReload = soup.find(
        "XCUIElementTypeButton",
        attrs={"visible":"true", "name": netErrTouchReloadP, "enabled":"true"}
    )
    if foundTouchReload:
        curAttrDict = foundTouchReload.attrs
        clickCenterPosition(curSession, curAttrDict)

    """
        <XCUIElementTypeButton type="XCUIElementTypeButton" name="网络出错，轻触屏幕重新加载:-1202" label="网络出错，轻触屏幕重新加载:-1202" enabled="true" visible="false" x="0" y="64" width="414" height="672">
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="网络出错，轻触屏幕重新加载:-1202" name="网络出错，轻触屏幕重新加载:-1202" label="网络出错，轻触屏幕重新加载:-1202" enabled="true" visible="false" x="0" y="264" width="414" height="40"/>
        </XCUIElementTypeButton>

        <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="安全警告" name="安全警告" label="安全警告" enabled="true" visible="true" x="71" y="286" width="272" height="19"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="mp.weixin.qq.com 该网站的安全证书存在问题，可选择“继续”在浏览器中访问。" name="mp.weixin.qq.com 该网站的安全证书存在问题，可选择“继续”在浏览器中访问。" label="mp.weixin.qq.com 该网站的安全证书存在问题，可选择“继续”在浏览器中访问。" enabled="true" visible="true" x="71" y="320" width="272" height="74"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="取消" name="取消" label="取消" enabled="true" visible="true" x="109" y="443" width="36" height="22"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="继续" name="继续" label="继续" enabled="true" visible="true" x="269" y="443" width="36" height="22"/>
                </XCUIElementTypeButton>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        </XCUIElementTypeWindow>
    """
    # foundWindowList = soup.find_all(
    #     "XCUIElementTypeWindow",
    #     attrs={"visible":"true", "enabled":"true"}
    # )
    # if foundWindowList:
    #     for eachWindowSoup in foundWindowList:
    #         foundButtonList = eachWindowSoup.find_all(
    #             "XCUIElementTypeButton",
    #             attrs={"visible":"true", "enabled":"true"}
    #         )
    #         if foundButtonList:
    #             for eachButtonSoup in foundButtonList:
    #                 foundSecurityWarning = eachButtonSoup.find(
    #                     "XCUIElementTypeStaticText",
    #                     attrs={"visible":"true", "enabled":"true", "value":"安全警告"}
    #                 )

    #                 certificateProblemP = re.compile("该网站的安全证书存在问题")
    #                 foundCertProblem = eachButtonSoup.find(
    #                     "XCUIElementTypeStaticText",
    #                     attrs={"visible":"true", "enabled":"true", "value":certificateProblemP}
    #                 )
    #                 if foundSecurityWarning and foundCertProblem:
    #                     foundCancel = eachButtonSoup.find(
    #                         "XCUIElementTypeStaticText",
    #                         attrs={"visible":"true", "enabled":"true", "value":"取消"}
    #                     )
    #                     if foundCancel:
    #                         curAttrDict = foundCancel.attrs
    #                         clickCenterPosition(curSession, curAttrDict)
    #                         break

    foundAndProcessed = False

    securityWarningChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value":"安全警告"}
        },
    ]
    securityWarningSoup = utils.bsChainFind(soup, securityWarningChainList)
    if securityWarningSoup:
        parentButtonSoup = securityWarningSoup.parent
        if parentButtonSoup:
            certificateProblemP = re.compile("该网站的安全证书存在问题")
            foundCertProblem = parentButtonSoup.find(
                "XCUIElementTypeStaticText",
                attrs={"visible":"true", "enabled":"true", "value":certificateProblemP}
            )
            if foundCertProblem:
                foundCancel = parentButtonSoup.find(
                    "XCUIElementTypeStaticText",
                    attrs={"visible":"true", "enabled":"true", "value":"取消"}
                )
                if foundCancel:
                    clickCenterPosition(curSession, foundCancel.attrs)
                    foundAndProcessed = True

    return foundAndProcessed


def debugPopupJumpThirdApp(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    ScreenX = 414
    ScreenY = 736
    
    foundAndProcessedPopup = False
    
    """
        <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" enabled="true" visible="false" x="47" y="288" width="0" height="0"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="可能离开微信，打开第三方应用" name="可能离开微信，打开第三方应用" label="可能离开微信，打开第三方应用" enabled="true" visible="true" x="71" y="331" width="272" height="18"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="取消" name="取消" label="取消" enabled="true" visible="true" x="109" y="409" width="36" height="22"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="继续" name="继续" label="继续" enabled="true" visible="true" x="269" y="409" width="36" height="22"/>
                        </XCUIElementTypeButton>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        </XCUIElementTypeWindow>
    """
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    # foundWindowList = soup.find_all(
    #     "XCUIElementTypeWindow",
    #     attrs={"visible":"true", "enabled":"true", "width": ScreenX, "height": ScreenY}
    # )
    # if foundWindowList:
    #     for eachWindowSoup in foundWindowList:
    #         if foundAndProcessedPopup:
    #             break

    #         foundButtonList = eachWindowSoup.find_all(
    #             "XCUIElementTypeButton",
    #             attrs={"visible":"true", "enabled":"true", "width": ScreenX, "height": ScreenY}
    #         )
    #         if foundButtonList:
    #             for eachButtonSoup in foundButtonList:
    #                 if foundAndProcessedPopup:
    #                     break

    #             foundLeaveWeixin = eachButtonSoup.find(
    #                 "XCUIElementTypeStaticText",
    #                 attrs={"visible":"true", "enabled":"true", "value":"可能离开微信，打开第三方应用"}
    #             )
    #             if foundLeaveWeixin:
    #                 foundCancel = eachButtonSoup.find(
    #                     "XCUIElementTypeStaticText",
    #                     attrs={"visible":"true", "enabled":"true", "value":"取消"}
    #                 )
    #                 if foundCancel:
    #                     clickCenterPosition(curSession, foundCancel.attrs)
    #                     foundAndProcessedPopup = True
    #                     break
    leaveWeixinChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value":"可能离开微信，打开第三方应用"}
        },
    ]
    foundLeaveWeixin = utils.bsChainFind(soup, leaveWeixinChainList)
    if foundLeaveWeixin:
        parentButtonSoup = foundLeaveWeixin.parent
        if parentButtonSoup:
            foundCancel = parentButtonSoup.find(
                "XCUIElementTypeStaticText",
                attrs={"visible":"true", "enabled":"true", "value":"取消"}
            )
            if foundCancel:
                clickCenterPosition(curSession, foundCancel.attrs)
                foundAndProcessedPopup = True

    return foundAndProcessedPopup


def debugPopupWeixinLogin(curSession):
    global gWdaClient

    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    ScreenX = 414
    ScreenY = 736

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    """
        <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="236" width="310" height="263">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微信登录" name="微信登录" label="微信登录" enabled="true" visible="true" x="83" y="251" width="248" height="18"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="285" width="310" height="1"/>
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="189" y="306" width="36" height="35"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微店消息助手申请获得以下权限:" name="微店消息助手申请获得以下权限:" label="微店消息助手申请获得以下权限:" enabled="true" visible="true" x="82" y="356" width="231" height="19"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="82" y="390" width="250" height="1"/>
                    <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="82" y="391" width="250" height="62">
                        <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="82" y="391" width="250" height="47">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="82" y="406" width="15" height="14"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="获得你的公开信息（昵称、头像、地区及性别）" name="获得你的公开信息（昵称、头像、地区及性别）" label="获得你的公开信息（昵称、头像、地区及性别）" enabled="true" visible="true" x="101" y="405" width="230" height="34"/>
                        </XCUIElementTypeCell>
                    </XCUIElementTypeTable>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="52" y="454" width="310" height="1"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="拒绝" label="拒绝" enabled="true" visible="true" x="52" y="454" width="155" height="45">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="拒绝" name="拒绝" label="拒绝" enabled="true" visible="true" x="112" y="466" width="35" height="21"/>
                    </XCUIElementTypeButton>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="207" y="454" width="1" height="45"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="允许" label="允许" enabled="true" visible="true" x="207" y="454" width="155" height="45">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="允许" name="允许" label="允许" enabled="true" visible="true" x="267" y="466" width="35" height="21"/>
                    </XCUIElementTypeButton>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        </XCUIElementTypeWindow>
    """

    foundAndProcessedPopup = False

    # foundWindowList = soup.find_all(
    #     "XCUIElementTypeWindow",
    #     attrs={"visible":"true", "enabled":"true"}
    # )
    # if foundWindowList:
    #     for eachWindowSoup in foundWindowList:
    #         if foundAndProcessedPopup:
    #             break

    #         foundOtherList = eachWindowSoup.find_all(
    #             "XCUIElementTypeOther",
    #             attrs={"visible":"true", "enabled":"true"}
    #         )
    #         if foundOtherList:
    #             for eachOtherSoup in foundOtherList:
    #                 if foundAndProcessedPopup:
    #                     break

    #                 foundWeixinLogin = eachOtherSoup.find(
    #                     "XCUIElementTypeStaticText",
    #                     attrs={"visible":"true", "enabled":"true", "value":"微信登录"}
    #                 )

    #                 foundTable = eachOtherSoup.find(
    #                     "XCUIElementTypeTable",
    #                     attrs={"visible":"true", "enabled":"true"}
    #                 )

    #                 if foundWeixinLogin and foundTable:
    #                     foundAllowButton = eachOtherSoup.find(
    #                         "XCUIElementTypeButton",
    #                         attrs={"visible":"true", "enabled":"true", "label":"允许"}
    #                     )
    #                     if foundAllowButton:
    #                         curAttrDict = foundAllowButton.attrs
    #                         clickCenterPosition(curSession, curAttrDict)
    #                         foundAndProcessedPopup = True
    #                         break

    weixinLoginChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value":"微信登录"}
        },
    ]
    foundWeixinLogin = utils.bsChainFind(soup, weixinLoginChainList)

    tableChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeTable",
            "attrs": {"visible":"true", "enabled":"true"}
        },
    ]
    foundTable = utils.bsChainFind(soup, tableChainList)

    if foundWeixinLogin and foundTable:
        parentOtherSoup = foundWeixinLogin.parent
        if parentOtherSoup:
            foundAllowButton = parentOtherSoup.find(
                "XCUIElementTypeButton",
                attrs={"visible":"true", "enabled":"true", "label":"允许"}
            )
            if foundAllowButton:
                clickCenterPosition(curSession, foundAllowButton.attrs)
                foundAndProcessedPopup = True

    return foundAndProcessedPopup

def debugElementVisible(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    # <XCUIElementTypeButton type="XCUIElementTypeButton" name="进入公众号" label="进入公众号" enabled="true" visible="false" x="0" y="177" width="82" height="20">
    intoAccountQuery = {"name": "进入公众号", "type": "XCUIElementTypeButton", "visible": "false"} # support and found -> expected
    # intoAccountQuery = {"name": "进入公众号", "type": "XCUIElementTypeButton", "visible": "true"} # support and not found -> expected
    isFoundIntoAccount, respInfo = findElement(curSession, query=intoAccountQuery, timeout=1.0)
    logging.info("isFoundIntoAccount=%s, respInfo=%s", isFoundIntoAccount, respInfo)

    # <XCUIElementTypeButton type="XCUIElementTypeButton" name="关注公众号" label="关注公众号" enabled="true" visible="true" x="166" y="177" width="82" height="20">
    focusAccountQuery = {"name": "关注公众号", "type": "XCUIElementTypeButton", "visible": "true"}  # support and found -> expected
    # focusAccountQuery = {"name": "关注公众号", "type": "XCUIElementTypeButton", "visible": "false"}  # support and not found -> expected
    isFoundFocusAccount, respInfo = findElement(curSession, query=focusAccountQuery, timeout=1.0)
    logging.info("isFoundFocusAccount=%s, respInfo=%s", isFoundFocusAccount, respInfo)


def debugPopupGetInfoFail(curSession):
    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    # ScreenX = 414
    # ScreenY = 736
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    """
        微信：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            。。。
                <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="获取信息失败" name="获取信息失败" label="获取信息失败" enabled="true" visible="true" x="71" y="309" width="272" height="21"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="取消" name="取消" label="取消" enabled="true" visible="true" x="109" y="419" width="36" height="22"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="确定" name="确定" label="确定" enabled="true" visible="true" x="269" y="419" width="36" height="22"/>
                </XCUIElementTypeButton>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="87" height="32">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="88" height="32">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="320" y="24" width="44" height="32"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="关闭" label="关闭" enabled="true" visible="true" x="363" y="24" width="45" height="32"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            。。。
            </XCUIElementTypeWindow>
        
        小程序：
            <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="32" y="251" width="311" height="165">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="32" y="251" width="311" height="165"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="获取信息失败" name="获取信息失败" label="获取信息失败" enabled="true" visible="true" x="52" y="276" width="271" height="21"/>
                    <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="是否重新加载页面" enabled="true" visible="true" x="121" y="311" width="133" height="35"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="32" y="365" width="156" height="51"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="187" y="365" width="156" height="51"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeButton>
    """

    foundAndProcessed = False

    getInfoFailChainList = generateCommonPopupItemChainList(ScreenX, ScreenY, thirdLevelValue="获取信息失败")
    getInfoFailSoup = utils.bsChainFind(soup, getInfoFailChainList)
    if getInfoFailSoup:
        parentButtonOrOtherSoup = getInfoFailSoup.parent
        if parentButtonOrOtherSoup:
            # 微信 弹框 获取信息失败
            foundConfirm = parentButtonOrOtherSoup.find(
                "XCUIElementTypeStaticText",
                attrs={"visible":"true", "enabled":"true", "value": "确定"}
            )

            if not foundConfirm:
                # 小程序 弹框 获取信息失败
                foundConfirm = parentButtonOrOtherSoup.find(
                    "XCUIElementTypeButton",
                    attrs={"visible":"true", "enabled":"true", "name": "确定"}
                )

            if foundConfirm:
                clickCenterPosition(curSession, foundConfirm.attrs)
                foundAndProcessed = True

    return foundAndProcessed

def debugMiniprogramBack(curSession):
    """
        小程序 左上角 返回 + 右上角 关闭：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="64">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="15" y="20" width="30" height="44">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="返回" label="返回" enabled="true" visible="true" x="15" y="20" width="30" height="44"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="个人信息" name="个人信息" label="个人信息" enabled="true" visible="true" x="152" y="30" width="71" height="20"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="280" y="24" width="88" height="32">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="280" y="24" width="44" height="32"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="关闭" label="关闭" enabled="true" visible="true" x="324" y="24" width="44" height="32"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>

        右上角 同心圆 关闭：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="387" y="-189" width="12" height="12">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="387" y="-189" width="12" height="12">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="" name="" label="" enabled="true" visible="false" x="387" y="-189" width="12" height="12"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>

            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="87" height="32">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="88" height="32">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="320" y="24" width="44" height="32"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="关闭" label="关闭" enabled="true" visible="true" x="363" y="24" width="45" height="32"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    MiniprogramBackButtonText = "返回"
    parentParentOtherClassChain = "/XCUIElementTypeOther[`enabled = 1 AND visible = 1 AND rect.width = %d`]" % ScreenX
    parentOtherClassChain = "/XCUIElementTypeOther[`enabled = 1 AND visible = 1`]"
    miniprogramCloseButtonQuery = {"type": "XCUIElementTypeButton", "name": MiniprogramBackButtonText, "label": MiniprogramBackButtonText, "enabled":"true", "visible":"true"}
    miniprogramCloseButtonQuery["parent_class_chains"] = [ parentParentOtherClassChain, parentOtherClassChain ]
    # isFound, respInfo = findElement(curSession, miniprogramCloseButtonQuery)
    # print("isFound=%s, respInfo=%s" % (isFound, respInfo))
    foundAndClickedBack = findAndClickElement(curSession, miniprogramCloseButtonQuery, enableDebug=True)
    print("foundAndClickedBack=%s" % foundAndClickedBack)

    backButtonQuery = {"type": "XCUIElementTypeStaticText", "width":"12", "height":"12"}
    closeButtonQuery = {"type": "XCUIElementTypeButton", "name":"关闭", "label":"关闭", "enabled":"true", "visible":"true"}
    foundAndClickedClose = findAndClickElement(curSession, closeButtonQuery, enableDebug=True)
    print("foundAndClickedClose=%s" % foundAndClickedClose)


def debugMiniprogamPopupAuthority(curSession):
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    """
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="315" width="375" height="352">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="20" y="335" width="24" height="25"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="优理氏UNES官方旗舰店" name="优理氏UNES官方旗舰店" label="优理氏UNES官方旗舰店" enabled="true" visible="true" x="49" y="338" width="163" height="19"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="申请" name="申请" label="申请" enabled="true" visible="true" x="217" y="338" width="31" height="19"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="获取你的昵称、头像、地区及性别" name="获取你的昵称、头像、地区及性别" label="获取你的昵称、头像、地区及性别" enabled="true" visible="true" x="20" y="383" width="260" height="25"/>
                <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="20" y="423" width="335" height="65">
                    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="20" y="423" width="335" height="65">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="20" y="423" width="335" height="65"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="20" y="423" width="335" height="1"/>
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="20" y="435" width="40" height="41"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="20" y="486" width="335" height="1"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="斐波测试2" name="斐波测试2" label="斐波测试2" enabled="true" visible="false" x="72" y="435" width="291" height="22"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微信个人信息" name="微信个人信息" label="微信个人信息" enabled="true" visible="false" x="72" y="460" width="291" height="18"/>
                        <XCUIElementTypeImage type="XCUIElementTypeImage" name="icon_selected" enabled="true" visible="false" x="335" y="445" width="20" height="21"/>
                    </XCUIElementTypeCell>
                </XCUIElementTypeTable>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="使用其他头像和昵称" label="使用其他头像和昵称" enabled="true" visible="true" x="20" y="503" width="138" height="18"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="59" y="561" width="121" height="40"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="允许" label="允许" enabled="true" visible="true" x="195" y="561" width="121" height="40"/>
            </XCUIElementTypeOther>
        </XCUIElementTypeOther>
    """
    foundAndProcessedPopup = False

    # weixinPersonInfoChainList = generateCommonPopupItemChainList(
    #     ScreenX,
    #     ScreenY,
    #     firstLevelTag="XCUIElementTypeTable",
    #     firstLevelAttrs={"enabled":"true", "visible":"true"},
    #     secondLevelTag="XCUIElementTypeCell",
    #     secondLevelAttrs={"enabled":"true", "visible":"true"},
    #     thirdLevelTag="XCUIElementTypeStaticText",
    #     thirdLevelValue="微信个人信息"
    # )
    weixinPersonInfoChainList = [
        {
            "tag": "XCUIElementTypeTable",
            "attrs": {"visible":"true", "enabled":"true"}
        },
        {
            "tag": "XCUIElementTypeCell",
            "attrs": {"visible":"true", "enabled":"true"}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            # "attrs": {"visible":"true", "enabled":"true", "value":"微信个人信息"}
            "attrs": {"visible":"false", "enabled":"true", "value":"微信个人信息"}
        },
    ]
    foundWeixinLogin = utils.bsChainFind(soup, weixinPersonInfoChainList)
    if foundWeixinLogin:
        # allowChainList = generateCommonPopupItemChainList(
        #     ScreenX,
        #     ScreenY,
        #     firstLevelTag="XCUIElementTypeOther",
        #     secondLevelTag="XCUIElementTypeCell",
        #     secondLevelAttrs={"enabled":"true", "visible":"true", "width": ScreenX},
        #     thirdLevelTag="XCUIElementTypeButton",
        #     thirdLevelName="允许"
        # )
        # foundAllow = utils.bsChainFind(soup, allowChainList)
        parentCell = foundWeixinLogin.parent
        parentParentTable = parentCell.parent
        parentParentParentOther = parentParentTable.parent
        foundAllow = parentParentParentOther.find(
            "XCUIElementTypeButton",
            attrs={"visible":"true", "enabled":"true", "name": "允许"}
        )
        if foundAllow:
            clickCenterPosition(curSession, foundAllow.attrs)
            foundAndProcessedPopup = True

    return foundAndProcessedPopup



def debugMiniprogamPopupGetContactInfo(curSession):
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="429" width="375" height="238">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="20" y="449" width="24" height="25"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="优理氏UNES官方旗舰店" name="优理氏UNES官方旗舰店" label="优理氏UNES官方旗舰店" enabled="true" visible="true" x="49" y="452" width="163" height="19"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="申请" name="申请" label="申请" enabled="true" visible="true" x="217" y="452" width="31" height="19"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="获取你的通讯地址" name="获取你的通讯地址" label="获取你的通讯地址" enabled="true" visible="true" x="20" y="497" width="139" height="25"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="拒绝" label="拒绝" enabled="true" visible="true" x="59" y="561" width="121" height="40"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="允许" label="允许" enabled="true" visible="true" x="195" y="561" width="121" height="40"/>
            </XCUIElementTypeOther>
        </XCUIElementTypeOther>
    """
    getYourP = re.compile("获取你的\S+") # 获取你的通讯地址， 获取你的昵称、头像、地区及性别
    # getYourChainList = generateCommonPopupItemChainList(
    #     ScreenX,
    #     ScreenY,
    #     firstLevelTag="XCUIElementTypeOther",
    #     secondLevelTag="XCUIElementTypeOther",
    #     thirdLevelValue=getYourP,
    # )
    getYourChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true", "x":"0", "width": ScreenX}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true", "x":"0", "width": ScreenX}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"enabled":"true", "value": getYourP}
        },
    ]
    getYourSoup = utils.bsChainFind(soup, getYourChainList)
    if getYourSoup:
        parentOther = getYourSoup.parent
        foundAllow = parentOther.find(
            "XCUIElementTypeButton",
            attrs={"visible":"true", "enabled":"true", "name": "允许"}
        )
        if foundAllow:
            clickCenterPosition(curSession, foundAllow.attrs)
            foundAndProcessedPopup = True
    
    return foundAndProcessedPopup


def debugMiniprogamPopupDisclaimer(curSession):
    foundAndProcessedPopup = False
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="375" height="667">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="27" y="208" width="321" height="251">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="27" y="208" width="321" height="251"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="免责声明" name="免责声明" label="免责声明" enabled="true" visible="true" x="51" y="240" width="273" height="21"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="本服务由第三方提供，获取你的微信收货地址信息。相关服务和责任由该第三方承担，如有问题请咨询该公司客服。" name="本服务由第三方提供，获取你的微信收货地址信息。相关服务和责任由该第三方承担，如有问题请咨询该公司客服。" label="本服务由第三方提供，获取你的微信收货地址信息。相关服务和责任由该第三方承担，如有问题请咨询该公司客服。" enabled="true" visible="true" x="51" y="277" width="273" height="94"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="知道了" label="知道了" enabled="true" visible="true" x="27" y="403" width="321" height="56"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeButton>
            </XCUIElementTypeOther>
        </XCUIElementTypeWindow>
    """
    # disclaimerChainList = generateCommonPopupItemChainList(ScreenX, ScreenY, thirdLevelValue="免责声明")
    disclaimerChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": {"visible":"true", "enabled":"true", "width": ScreenX, "height": ScreenY}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"visible":"true", "enabled":"true", "width": ScreenX, "height": ScreenY}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value": "免责声明"}
        },
    ]
    disclaimerSoup = utils.bsChainFind(soup, disclaimerChainList)
    if disclaimerSoup:
        parentOtherSoup = disclaimerSoup.parent
        if parentOtherSoup:
            foundIKnow = parentOtherSoup.find(
                "XCUIElementTypeButton",
                attrs={"visible":"true", "enabled":"true", "name":"知道了"}
            )
            if foundIKnow:
                clickCenterPosition(curSession, foundIKnow.attrs)
                foundAndProcessedPopup = True

    return foundAndProcessedPopup


def debugAccountSearchResultNoAccountName(curSession):
    """Find weixin public account zh-CN name element for public account search result no show account name

    Args:
        soup (soup): soup of current page xml
    Returns:
        public account zhcn element
    Raises:
    """
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    zhcnAccountName = ""

    foundFocused = soup.find(
        'XCUIElementTypeStaticText',
        attrs={"value": "已关注", "type": "XCUIElementTypeStaticText", "enabled":"true", "visible":"true"},
    )
    if foundFocused:
        parentOtherSoup = foundFocused.parent
        parentParentOtherSoup = parentOtherSoup.parent
        parentParentParentOtherSoup = parentParentOtherSoup.parent # 搜一搜

        otherSoupList = parentParentParentOtherSoup.find_all(
            'XCUIElementTypeOther',
            attrs={"type": "XCUIElementTypeOther", "enabled":"true", "visible":"true"},
        )
        if otherSoupList:
            otherSoupCount = len(otherSoupList)
            if otherSoupCount >= 2:
                firstOtherSoup = otherSoupList[0]
                if hasattr(firstOtherSoup, "attrs"):
                    firstOtherName = firstOtherSoup.attrs.get("name")
                    if firstOtherName == "公众号":
                        secondOtherSoup = otherSoupList[1]
                        if hasattr(secondOtherSoup, "attrs"):
                            secondOtherName = secondOtherSoup.attrs.get("name")
                            secondOtherValue = secondOtherSoup.attrs.get("value")
                            isNoName = not secondOtherName
                            isNoValue = not secondOtherValue
                            if isNoName and isNoValue:
                                # find and merge all text
                                allTextSoupList = secondOtherSoup.find_all(
                                    'XCUIElementTypeStaticText',
                                    attrs={"type": "XCUIElementTypeStaticText", "enabled":"true", "visible":"true"},
                                )
                                for eachTextSoup in allTextSoupList:
                                    curValue = eachTextSoup.attrs.get("value")
                                    zhcnAccountName += curValue
    # '优理氏UNES官方'
    return zhcnAccountName


def debugSettingsAllowUseLocation(curSession):
    """
        设置 使用我的地理位置：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="设置" enabled="true" visible="true" x="0" y="20" width="375" height="44">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="返回" label="返回" enabled="true" visible="true" x="10" y="20" width="30" height="44"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="设置" name="设置" label="设置" enabled="true" visible="true" x="187" y="24" width="1" height="36"/>
                </XCUIElementTypeNavigationBar>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="375" height="64"/>
                            <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="允许&quot;贝德玛会员中心&quot;" name="允许&quot;贝德玛会员中心&quot;" label="允许&quot;贝德玛会员中心&quot;" enabled="true" visible="true" x="15" y="88" width="345" height="17"/>
                                <XCUIElementTypeCell type="XCUIElementTypeCell" value="0" enabled="true" visible="true" x="0" y="115" width="375" height="44">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="115" width="375" height="1"/>
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="158" width="375" height="1"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="使用我的地理位置" name="使用我的地理位置" label="使用我的地理位置" enabled="true" visible="true" x="15" y="126" width="139" height="22"/>
                                    <XCUIElementTypeSwitch type="XCUIElementTypeSwitch" value="0" name="使用我的地理位置" label="使用我的地理位置" enabled="true" visible="true" x="309" y="122" width="51" height="31"/>
                                </XCUIElementTypeCell>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="159" width="375" height="1219"/>
                            </XCUIElementTypeTable>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    ScreenX = 375
    ScreenY = 667

    useLocationSwitchQuery = {"type": "XCUIElementTypeSwitch", "name": "使用我的地理位置", "enabled":"true"}
    parentCellClassChain = "/XCUIElementTypeCell[`enabled = 1 AND rect.width = %d`]" % ScreenX
    useLocationSwitchQuery["parent_class_chains"] = [ parentCellClassChain ]
    foundAndClickeUseLocation = findAndClickElement(curSession, useLocationSwitchQuery, enableDebug=True)
    print("foundAndClickeUseLocation=%s" % foundAndClickeUseLocation)
    if foundAndClickeUseLocation:
        parentNaviBarClassChain = '/XCUIElementTypeNavigationBar[`enabled = 1 AND name="设置"`]'
        backButtonQuery = {"type": "XCUIElementTypeButton", "name": "返回", "enabled":"true"}
        backButtonQuery["parent_class_chains"] = parentNaviBarClassChain
        foundAndClickeBack = findAndClickElement(curSession, backButtonQuery, enableDebug=True)
        print("foundAndClickeBack=%s" % foundAndClickeBack)


def debugUnfollowSingleAccount(curSession):
    ScreenX = 375
    ScreenY = 667
    SwipDuration = 0.3

    SwipeLeftBounds = [round(ScreenX*0.9), ScreenY//2, round(ScreenX*0.1), ScreenY//2] # [338, 333, 38, 333]

    accountName = "贝德玛Bioderma"
    accountQuery = {"type": "XCUIElementTypeStaticText", "name": accountName, "enabled":"true"}
    isFound, visibleAccountElement = findElement(curSession, accountQuery)
    if isFound:
        isVisible = visibleAccountElement
        if isVisible:
            curRect = visibleAccountElement.bounds
            rectCenter = curRect.center
            centerY = rectCenter[1]
            elementY = centerY
            # curSwipeLeftBounds = [round(ScreenX*0.9), elementY//2, round(ScreenX*0.1), elementY//2]
            # curSwipeLeftBounds = [int(round(ScreenX*0.9)), elementY//2, int(round(ScreenX*0.1)), elementY//2]
            # curSwipeLeftBounds = [int(round(ScreenX*0.9)), int(elementY//2), int(round(ScreenX*0.1)), int(elementY//2)]
            curSwipeLeftBounds = [int(round(ScreenX*0.9)), int(centerY), int(round(ScreenX*0.1)), int(centerY)]
            # SwipeDirectionBounds = SwipeLeftBounds
            SwipeDirectionBounds = curSwipeLeftBounds

            curSession.swipe(SwipeDirectionBounds[0], SwipeDirectionBounds[1], SwipeDirectionBounds[2], SwipeDirectionBounds[3], SwipDuration)
            """
                左滑后 取消关注：
                <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="142" width="375" height="65">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消关注" label="取消关注" enabled="true" visible="false" x="375" y="142" width="117" height="65"/>
            """
            unfollowButtonQuery = {"type": "XCUIElementTypeButton", "name": "取消关注", "enabled":"true"}
            isFound, unfollowButtonElement = findElement(curSession, unfollowButtonQuery)
            if isFound:
                clickOk = clickElement(curSession, unfollowButtonElement)
                if clickOk:
                    """
                        取消关注 弹框：
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="561" width="375" height="106">
                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消关注" label="取消关注" enabled="true" visible="true" x="0" y="561" width="375" height="50"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="611" width="375" height="6"/>
                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="0" y="617" width="375" height="50"/>
                        </XCUIElementTypeOther>
                    """
                    unfollowPopupQuery = {"type": "XCUIElementTypeButton", "name": "取消关注", "enabled":"true"}
                    isFound, unfollowPopupElement = findElement(curSession, unfollowPopupQuery)
                    if isFound:
                        clickOk = clickElement(curSession, unfollowPopupElement)
                        if clickOk:
                            debugSaveScreenshot(curScale=curSession.scale)
                            debugSaveSource()

def debugPublicAccountPage_swipeToTop(curSession):
    isFoundTop = False

    MaxRetryNum = 10

    ScreenX = 375
    ScreenY = 667
    SwipDuration = 0.3

    middleX = int(ScreenX / 2)
    middleY = int(ScreenY / 2)
    startY = int(middleY - middleY/2)
    endY = int(middleY + middleY/2)

    SwipeUpBounds = [middleX, startY, middleX, endY]

    """
        公众号列表页 顶部 搜索 可见：
            <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="0" y="64" width="375" height="56"/>
                <XCUIElementTypeSearchField type="XCUIElementTypeSearchField" name="搜索" label="搜索" enabled="true" visible="true" x="8" y="74" width="359" height="36"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" name="c" enabled="true" visible="true" x="0" y="120" width="375" height="22">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" name="c" label="c" enabled="true" visible="true" x="10" y="120" width="10" height="22"/>
                </XCUIElementTypeOther>
        
        公众号列表页 中间 搜索 不可见：
            <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="0" y="-448" width="375" height="57"/>
                <XCUIElementTypeSearchField type="XCUIElementTypeSearchField" name="搜索" label="搜索" enabled="true" visible="false" x="8" y="-438" width="359" height="37"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="-327" width="375" height="23">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="-327" width="375" height="23"/>
                </XCUIElementTypeOther>
    """
    curRetryNum = MaxRetryNum
    searchFieldQuery = {"type": "XCUIElementTypeSearchField", "name": "搜索", "enabled":"true"}
    while curRetryNum > 0:
        isFound, searchFieldElement = findElement(curSession, searchFieldQuery)
        if isFound:
            isVisible = searchFieldElement.visible
            if isVisible:
                isFoundTop = True
                break

        curSession.swipe(SwipeUpBounds[0], SwipeUpBounds[1], SwipeUpBounds[2], SwipeUpBounds[3], SwipDuration)

        curRetryNum -= 1

    return isFoundTop

def debugSwipeUntilFound(curSession):
    """
        公众号列表页 中间 xxx个公众号 不可见：
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="17个公众号" name="17个公众号" label="17个公众号" enabled="true" visible="false" x="0" y="992" width="375" height="21"/>

        公众号列表页 底部 xxx个公众号 可见：
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="17个公众号" name="17个公众号" label="17个公众号" enabled="true" visible="true" x="0" y="632" width="375" height="20"/>
    """

    ScreenX = 375
    ScreenY = 667

    middleX = int(ScreenX / 2)
    middleY = int(ScreenY / 2)
    upHalfY = int(middleY - middleY/2)
    downHalfY = int(middleY + middleY/2)

    SwipeUpBounds = [middleX, upHalfY, middleX, downHalfY]
    swipeDownBounds = [middleX, downHalfY, middleX, upHalfY]

    searchFieldQuery = {"type": "XCUIElementTypeSearchField", "name": "搜索", "enabled":"true"}
    foundSearchFieldElement = SwipeUntilFound_iOS(curSession, searchFieldQuery, SwipeUpBounds)
    if foundSearchFieldElement:
        print("foundSearchFieldElement")

    someNumberAccountQuery =  {"type": "XCUIElementTypeStaticText", "valueContains": "个公众号", "enabled":"true"}
    foundSomeNumberAccountElement = SwipeUntilFound_iOS(curSession, someNumberAccountQuery, swipeDownBounds)
    if foundSomeNumberAccountElement:
        print("foundSomeNumberAccountElement")

def debugUnfollowCrashPartVisible(curSession):
    ScreenX = 375
    ScreenY = 667

    SwipDuration = 0.1

    middleX = int(ScreenX / 2)
    middleY = int(ScreenY / 2)
    upHalfY = int(middleY - middleY/2)
    downHalfY = int(middleY + middleY/2)

    """
    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="642" width="375" height="66">
        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="水光针" name="水光针" label="水光针" enabled="true" visible="true" x="70" y="666" width="46" height="18"/>
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="10" y="650" width="50" height="50">
            <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="10" y="650" width="50" height="50"/>
            <XCUIElementTypeImage type="XCUIElementTypeImage" name="头像" label="头像" enabled="true" visible="true" x="13" y="653" width="44" height="44"/>
        </XCUIElementTypeOther>
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="15" y="707" width="360" height="1"/>
        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="水光针" name="水光针" label="水光针" enabled="true" visible="true" x="70" y="666" width="46" height="18"/>
    </XCUIElementTypeCell>
    """
    accountNameQuery = {"type":"XCUIElementTypeStaticText", "name":"水光针", "enabled":"true"}
    isFound, foundElement = findElement(curSession, accountNameQuery)
    if isFound:
        isVisible = foundElement.visible
        if isVisible:
            # # for debug
            # # isVisible = foundElement.visible
            # curRect = foundElement.bounds
            # rectCenter = curRect.center
            # curX0 = curRect.x0
            # curX1 = curRect.x1
            # curY0 = curRect.y0
            # curY1 = curRect.y1
            # curCenterX = curRect.centerX
            # curCenterY = curRect.centerY

            # if y1 exceed screen height -> only part visible -> swipe to fullly visible
            curRect = foundElement.bounds
            # y0 = curRect.y
            height = curRect.height
            # y1 = y0 + height
            y1 = curRect.y1
            isPartVisible = y1 > ScreenY
            if isPartVisible:
                scrollUpDistance = int(2 * height) # swipe double height makesure fully visible
                toY = middleY - scrollUpDistance
                swipeBounds = [middleX, middleY, middleX, toY]
                curSession.swipe(swipeBounds[0], swipeBounds[1], swipeBounds[2], swipeBounds[3], SwipDuration)

                isFound, foundElement = findElement(curSession, accountNameQuery)
                if isFound:
                    isVisible = foundElement.visible
                    if isVisible:
                        curRect = foundElement.bounds
                        y1 = curRect.y1
                        isStillPartVisible = y1 > ScreenY
                        print("isStillPartVisible=%s" % isStillPartVisible)

# def SwipeUntilFound_iOS(curSession, elementQuery, swipeBounds):
def SwipeUntilFound_iOS(curSession, elementQuery, swipeDirectoin, maxEndPosition):
    """
        一直滑动，直到找到某个可见的元素
        举例：
            向上滚动直到顶部-》找到visible=true的 搜索
            向下滚动直到底部-》找到visible=true的 xxx个公众号
    """
    ScreenX = 375
    ScreenY = 667

    # middleX = int(ScreenX / 2)
    # middleY = int(ScreenY / 2)

    headY = utils.calcHeadY(curSession) # 64
    # BottomY = ScreenY

    # swipeStartX = middleX
    # swipeVerticalRange = int(ScreenY // 4)
    # vertialTopY = int(headY + swipeVerticalRange) # 248
    # vertialBottomY = int(BottomY - swipeVerticalRange) # 478.4

    # SwipeUpBounds = [swipeStartX, vertialTopY, swipeStartX, vertialBottomY]
    # SwipeDownBounds = [swipeStartX, vertialBottomY, swipeStartX, vertialTopY]
    # # SwipeLeftBounds = [int(round(ScreenX * 0.9)), middleY, int(round(ScreenX * 0.1)), middleY]

    # SwipeBoundsDict = {
    #     "SwipeUp": SwipeUpBounds,
    #     "SwipeDown": SwipeDownBounds,
    #     # "SwipeLeft": SwipeLeftBounds,
    # }
    # swipeBounds = SwipeBoundsDict[swipeDirectoin]

    utils.getSwipeBounds(swipeDirectoin, ScreenX, ScreenY, headY=headY)

    visibleElement = None

    # SwipDuration = 0.3
    SwipDuration = 0.1
    MaxRetryNum = 10

    curRetryNum = MaxRetryNum
    while curRetryNum > 0:
        isFound, foundElement = findElement(curSession, elementQuery)
        if isFound:
            isVisible = foundElement.visible
            if isVisible:
                visibleElement = foundElement
                break

        curSession.swipe(swipeBounds[0], swipeBounds[1], swipeBounds[2], swipeBounds[3], SwipDuration)
        # time.sleep(0.1)

        curRetryNum -= 1

    if foundElement:
        # if end of x or y, exceed screen left/right/top/bottom
        #   -> only part visible
        #       -> swipe to fullly visible
        isExceed = False
        minorSwipeBounds = None
        curRect = foundElement.bounds
        # swipe double height makesure fully visible
        virticalMinorScrollLength = int(2 * curRect.height)
        # swipe single height enough to make it fully visible
        #   -> but if run without debug, swipe not work !
        # virticalMinorScrollLength = int(curRect.height)
        if swipeDirectoin == "SwipeUp":
            curMinY = curRect.y0
            # minPossible = headY
            possibleMinY = maxEndPosition
            isExceed = curMinY < possibleMinY
            toY = middleY + virticalMinorScrollLength
            minorSwipeBounds = [middleX, middleY, middleX, toY]
        elif swipeDirectoin == "SwipeDown":
            curMaxY = curRect.y1
            # maxPossible = ScreenY
            possibleMaxY = maxEndPosition
            isExceed = curMaxY > possibleMaxY
            toY = middleY - virticalMinorScrollLength
            minorSwipeBounds = [middleX, middleY, middleX, toY]
        elif swipeDirectoin == "SwipeLeft":
            # TODO: add support SwipeLeft in future if necessary
            logging.warning("TODO: add support SwipeLeft in future if necessary")

        isPartVisible = isExceed
        if isPartVisible:
            curSession.swipe(minorSwipeBounds[0], minorSwipeBounds[1], minorSwipeBounds[2], minorSwipeBounds[3], SwipDuration)
            # time.sleep(0.1)

    return foundElement

def debugScrollPartVisible(curSession):
    # searchFieldQuery = {"type": "XCUIElementTypeSearchField", "name": "搜索", "enabled":"true"}
    # searchFieldElement = SwipeUntilFound_iOS(curSession, searchFieldQuery, "SwipeUp")
    """
        公众号列表 顶部 部分显示 二更：
            <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="48" width="375" height="66">
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="二更" name="二更" label="二更" enabled="true" visible="true" x="70" y="72" width="31" height="18"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="113" width="375" height="1"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="10" y="56" width="50" height="50">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="10" y="56" width="50" height="50"/>
                    <XCUIElementTypeImage type="XCUIElementTypeImage" name="头像" label="头像" enabled="true" visible="true" x="13" y="59" width="44" height="44"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="二更" name="二更" label="二更" enabled="true" visible="true" x="70" y="72" width="31" height="18"/>
            </XCUIElementTypeCell>
    """
    ScreenX = 375
    ScreenY = 667

    headY = calcHeadY(curSession) # 64
    floatUpperLeterHeight = 0
    floatUpperLetterElement = findFloatUpperLetter(curSession)
    if floatUpperLetterElement:
        curRect = floatUpperLetterElement.bounds
        floatUpperLeterHeight = curRect.height # 22
    minHeadY = headY + floatUpperLeterHeight # 86

    debugSaveScreenshot(curScale=curSession.scale)
    topPartVisibleAccountName = "二更"
    topPartVisibleAccountQuery = {"value" : topPartVisibleAccountName, "type":"XCUIElementTypeStaticText"}
    topPartVisibleAccountElement = SwipeUntilFound_iOS(curSession, topPartVisibleAccountQuery, "SwipeUp", minHeadY)
    debugSaveScreenshot(curScale=curSession.scale)

    debugSaveScreenshot(curScale=curSession.scale)
    bottomPartVisibleAccountName = "水光针"
    bottomPartVisibleAccountQuery = {"value" : bottomPartVisibleAccountName, "type":"XCUIElementTypeStaticText"}
    bottomPartVisibleAccountElement = SwipeUntilFound_iOS(curSession, bottomPartVisibleAccountQuery, "SwipeDown", ScreenY)
    debugSaveScreenshot(curScale=curSession.scale)

def findFloatUpperLetter(curSession):
    """
        寻找 微信公众号列表页中 上下滚动后的 顶部浮动的大写字母横条的元素
    """
    ScreenX = 375
    ScreenY = 667
    """
        <XCUIElementTypeOther type="XCUIElementTypeOther" name="D" enabled="true" visible="true" x="0" y="64" width="375" height="22">
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="D" label="D" enabled="true" visible="true" x="10" y="64" width="12" height="22"/>
        </XCUIElementTypeOther>

        <XCUIElementTypeOther type="XCUIElementTypeOther" name="E" enabled="true" visible="true" x="0" y="64" width="375" height="22">
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="E" name="E" label="E" enabled="true" visible="true" x="10" y="64" width="10" height="22"/>
        </XCUIElementTypeOther>

        <XCUIElementTypeOther type="XCUIElementTypeOther" name="J" enabled="true" visible="true" x="0" y="64" width="375" height="22">
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="J" name="J" label="J" enabled="true" visible="true" x="10" y="64" width="9" height="22"/>
        </XCUIElementTypeOther>
    """
    floatUpperLetterElement = None
    # floatUpperLetterQuery = {"type":"XCUIElementTypeStaticText", "valueMatches":"^[A-Z]$"}
    # isFound, foundElement = findElement(curSession, floatUpperLetterQuery)
    floatUpperLetterQuery = {"type":"XCUIElementTypeOther", "nameMatches":"^[A-Z]$", "enabled":"true", "x":"0", "width": "%s" % ScreenX}
    isFound, foundElement = findElement(curSession, floatUpperLetterQuery)
    if isFound:
        isVisible = foundElement.visible
        if isVisible:
            floatUpperLetterElement = foundElement
    
    return floatUpperLetterElement

def debugElementQueryRegex(curSession):
    floatUpperLetterElement = findFloatUpperLetter(curSession)
    if floatUpperLetterElement:
        curRect = floatUpperLetterElement.bounds
        floatUpperLeterHeight = curRect.height
        print("floatUpperLeterHeight=%s" % floatUpperLeterHeight)

def debugMiniprogramPopWarningNotAuthorized(curSession):
    """
        微信-小程序 弹框 警告 尚未进行授权：
            <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="32" y="240" width="311" height="187">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="32" y="240" width="311" height="187"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="警告" name="警告" label="警告" enabled="true" visible="true" x="52" y="265" width="271" height="21"/>
                    <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="尚未进行授权，请点击确定跳转到授权页面进行授权。" enabled="true" visible="true" x="60" y="300" width="255" height="57"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="32" y="376" width="156" height="51"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="187" y="376" width="156" height="51"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeButton>
    """
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False

    warningChainList = [
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true"}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value":"警告"}
        },
    ]
    warningSoup = utils.bsChainFind(soup, warningChainList)
    if warningSoup:
        parentOtherSoup = warningSoup.parent
        confirmSoup = parentOtherSoup.find(
            "XCUIElementTypeButton",
            attrs={"visible":"true", "enabled":"true", "name": "确定"}
        )
        if confirmSoup:
            clickCenterPosition(curSession, confirmSoup.attrs)
            foundAndProcessedPopup = True

    return foundAndProcessedPopup

def debugWillOpenNonOfficialPage(curSession):
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False

    """
        将要访问 非有赞官方网页，请确认是否继续访问
        <XCUIElementTypeWebView type="XCUIElementTypeWebView" enabled="true" visible="true" x="0" y="64" width="375" height="603">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="375" height="603">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="0" height="0">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="0" height="0">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="375" height="603">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="375" height="603">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="150" y="234" width="75" height="24">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="将要访问" name="将要访问" label="将要访问" enabled="true" visible="true" x="150" y="234" width="75" height="23"/>
                                </XCUIElementTypeOther>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="30" y="268" width="315" height="44">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="http://weixintx.haoduoke.cn/mobile/new_shop?appId=wx63d48daf039fe35c" name="http://weixintx.haoduoke.cn/mobile/new_shop?appId=wx63d48daf039fe35c" label="http://weixintx.haoduoke.cn/mobile/new_shop?appId=wx63d48daf039fe35c" enabled="true" visible="true" x="37" y="270" width="301" height="40"/>
                                </XCUIElementTypeOther>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="58" y="322" width="258" height="22">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="非有赞官方网页，请确认是否继续访问。" name="非有赞官方网页，请确认是否继续访问。" label="非有赞官方网页，请确认是否继续访问。" enabled="true" visible="true" x="58" y="324" width="259" height="18"/>
                                </XCUIElementTypeOther>
                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="继续访问" label="继续访问" enabled="true" visible="true" x="20" y="384" width="335" height="50"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="160" y="632" width="74" height="15">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="有赞安全中心" name="有赞安全中心" label="有赞安全中心" enabled="true" visible="true" x="160" y="632" width="74" height="15"/>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        </XCUIElementTypeWebView>
    """
    willOpenChainList = [
        {
            "tag": "XCUIElementTypeWebView",
            "attrs": {"visible":"true", "enabled":"true", "x":"0", "width": "%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true", "x":"0", "width": "%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value":"将要访问"}
        },
    ]
    willOpenSoup = utils.bsChainFind(soup, willOpenChainList)
    if willOpenSoup:
        parentOtherSoup = willOpenSoup.parent
        parentParentOtherSoup = parentOtherSoup.parent
        if parentParentOtherSoup:
            continueOpenSoup = parentParentOtherSoup.find(
                "XCUIElementTypeButton",
                attrs={"visible":"true", "enabled":"true", "name": "继续访问"}
            )
            if continueOpenSoup:
                clickCenterPosition(curSession, continueOpenSoup.attrs)
                foundAndProcessedPopup = True

    return foundAndProcessedPopup

def debugWeixinPublicAccountSearchNotFound(curSession):
    """
        公众号搜索页 搜索不到 gh_d98c3fcb63e0 公众号：
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="70" width="375" height="597">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" name="搜一搜" label="搜一搜" enabled="true" visible="false" x="0" y="70" width="375" height="1881">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="359" height="23">
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="52" height="23"/>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="16" y="133" width="60" height="60"/>
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="343" y="132" width="16" height="16"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="130" width="271" height="23">
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="sumru" name="sumru" label="sumru" enabled="true" visible="true" x="88" y="130" width="49" height="22"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="gh" name="gh" label="gh" enabled="true" visible="true" x="136" y="130" width="20" height="22"/>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="155" width="271" height="21">
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="趣人趣事" name="趣人趣事" label="趣人趣事" enabled="true" visible="true" x="88" y="156" width="62" height="19"/>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="16" y="224" width="60" height="60"/>
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="343" y="223" width="16" height="16"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="221" width="271" height="23">
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="GH" name="GH" label="GH" enabled="true" visible="true" x="88" y="221" width="25" height="22"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="5DanceStudio" name="5DanceStudio" label="5DanceStudio" enabled="true" visible="true" x="112" y="221" width="109" height="22"/>
                        </XCUIElementTypeOther>
    """
    pass


# def findWeixinPublicAccountZhcnSoup(soup, curAccountId):
def findWeixinPublicAccountZhcnFullName(soup, curAccountId):
    """Find weixin public account element's zh-CN full name

    Args:
        soup (soup): soup of current page xml
    Returns:
        public account zh-CN full name
    Raises:
    """
    # accountZhcnTextSoup = None
    accountZhcnFullName = ""

    """
        搜索结果中文名节点是Text
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="搜一搜" label="搜一搜" enabled="true" visible="true" x="0" y="70" width="414" height="666">
                <XCUIElementTypeOther type="XCUIElementTypeOther" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="398" height="23">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" value="2" enabled="true" visible="true" x="16" y="83" width="52" height="23">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="52" height="22"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="16" y="129" width="60" height="60"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="126" width="310" height="23">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="动卡空间" name="动卡空间" label="动卡空间" enabled="true" visible="true" x="88" y="126" width="70" height="22"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="151" width="310" height="21">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="分享用卡活动，传播正能量" name="分享用卡活动，传播正能量" label="分享用卡活动，传播正能量" enabled="true" visible="true" x="88" y="152" width="184" height="19"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="178" width="266" height="20">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微信号：" name="微信号：" label="微信号：" enabled="true" visible="true" x="88" y="178" width="58" height="19"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="gh_cfcfcee032cc" name="gh_cfcfcee032cc" label="gh_cfcfcee032cc" enabled="true" visible="true" x="145" y="178" width="112" height="19"/>
                </XCUIElementTypeOther>
        
        搜索结果中文名节点是Other，其下是多个Text节点：
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="搜一搜" label="搜一搜" enabled="true" visible="true" x="0" y="70" width="375" height="600">
                <XCUIElementTypeOther type="XCUIElementTypeOther" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="359" height="23">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="52" height="23"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="16" y="129" width="60" height="60"/>
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="343" y="128" width="16" height="16"/>
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="324" y="128" width="16" height="16"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="126" width="271" height="23">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="牛尔" name="牛尔" label="牛尔" enabled="true" visible="true" x="88" y="126" width="35" height="22"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="Tmall" name="Tmall" label="Tmall" enabled="true" visible="true" x="122" y="126" width="41" height="22"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="旗舰店" name="旗舰店" label="旗舰店" enabled="true" visible="true" x="162" y="126" width="53" height="22"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="151" width="271" height="21">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="牛尔亲研天猫官方旗舰店" name="牛尔亲研天猫官方旗舰店" label="牛尔亲研天猫官方旗舰店" enabled="true" visible="true" x="88" y="152" width="169" height="19"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="178" width="271" height="19">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微信号：" name="微信号：" label="微信号：" enabled="true" visible="true" x="88" y="178" width="58" height="18"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="niuer-tmall" name="niuer-tmall" label="niuer-tmall" enabled="true" visible="true" x="145" y="178" width="70" height="18"/>
                </XCUIElementTypeOther>
        
        公众号中文名全部是绿色的：
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="搜一搜" label="搜一搜" enabled="true" visible="true" x="0" y="70" width="414" height="666">
                <XCUIElementTypeOther type="XCUIElementTypeOther" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="398" height="23">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" value="2" enabled="true" visible="true" x="16" y="83" width="52" height="23">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="2" name="公众号" label="公众号" enabled="true" visible="true" x="16" y="83" width="52" height="22"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="16" y="129" width="60" height="60"/>
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="382" y="128" width="16" height="16"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="126" width="310" height="23">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="limi里美" name="limi里美" label="limi里美" enabled="true" visible="true" x="88" y="126" width="61" height="22"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="151" width="310" height="21">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="真实好成分，呵护少女肌。" name="真实好成分，呵护少女肌。" label="真实好成分，呵护少女肌。" enabled="true" visible="true" x="88" y="152" width="184" height="19"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="88" y="178" width="310" height="19">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微信号：" name="微信号：" label="微信号：" enabled="true" visible="true" x="88" y="178" width="58" height="18"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="limi_official" name="limi_official" label="limi_official" enabled="true" visible="true" x="145" y="178" width="72" height="18"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="0" height="0"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="237" width="414" height="25">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="没有更多的搜索结果" name="没有更多的搜索结果" label="没有更多的搜索结果" enabled="true" visible="true" x="133" y="239" width="148" height="20"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    foundAccountId = soup.find(
        'XCUIElementTypeStaticText',
        attrs={"value": curAccountId, "name": curAccountId, "type": "XCUIElementTypeStaticText"},
    )
    logging.debug("foundAccountId=%s", foundAccountId)
    # foundAccountId=<XCUIElementTypeStaticText enabled="true" height="18" label="gh_cfcfcee032cc" name="gh_cfcfcee032cc" type="XCUIElementTypeStaticText" value="gh_cfcfcee032cc" visible="true" width="112" x="145" y="178"/>
    if foundAccountId:
        idParent = foundAccountId.parent
        logging.debug("idParent=%s", idParent)
        if idParent:
            # method 1: two prev.prev
            # # idParentPrev = idParent.previous_sibling
            # idParentPrev = idParent.previous_sibling.previous_sibling
            # accountDescNode = idParentPrev
            # logging.info("accountDescNode=%s", accountDescNode) # '\n'
            # if accountDescNode:
            #     # accountZhcnNode = accountDescNode.previous_sibling
            #     accountZhcnNode = accountDescNode.previous_sibling.previous_sibling
            #     logging.info("accountZhcnNode=%s", accountZhcnNode)

            # # method 2: siblings[-2] of XCUIElementTypeOther
            # idParentPrevSiblingList = idParent.previous_siblings

            # accountDescNode = None
            # accountZhcnNode = None

            # TypeOther = "XCUIElementTypeOther"
            # typeOtherNodeCurIdx = 0
            # AccountDescNodeIdx = 1
            # AccountZhcnNodeIdx = 2

            # for eachPrevSiblingNode in idParentPrevSiblingList:
            #     curNodeName = eachPrevSiblingNode.name
            #     isTypeOtherNode = curNodeName == TypeOther
            #     if isTypeOtherNode:
            #         typeOtherNodeCurIdx += 1

            #         if AccountDescNodeIdx == typeOtherNodeCurIdx:
            #             accountDescNode = eachPrevSiblingNode
            #         elif AccountZhcnNodeIdx == typeOtherNodeCurIdx:
            #             accountZhcnNode = eachPrevSiblingNode
                
            #     hasFoundAll = accountDescNode and accountZhcnNode
            #     if hasFoundAll:
            #         break
            
            # logging.info("accountDescNode=%s", accountDescNode)
            # logging.info("accountZhcnNode=%s", accountZhcnNode)

            # if accountZhcnNode:
            #     accountZhcnTextSoup = accountZhcnNode.find(
            #         'XCUIElementTypeStaticText',
            #         attrs={ "type": "XCUIElementTypeStaticText"},
            #     )

            # method 3: parent'parent is 搜一搜, direct child 2nd XCUIElementTypeOther of enabled="true" visible="true"
            idParentParent = idParent.parent
            if idParentParent:
                otherSoupList = idParentParent.find_all(
                    "XCUIElementTypeOther",
                    attrs={"type": "XCUIElementTypeOther", "enabled":"true", "visible":"true"},
                    recursive=False,
                )
                if otherSoupList and (len(otherSoupList) >= 2):
                    firstOtherSoup = otherSoupList[0]
                    if firstOtherSoup.attrs["name"] == "公众号":
                        secondOtherSoup = otherSoupList[1]
                        zhcnNameSoupList = secondOtherSoup.find_all(
                            "XCUIElementTypeStaticText",
                            attrs={"type": "XCUIElementTypeStaticText", "enabled":"true", "visible":"true"},
                        )
                        if zhcnNameSoupList:
                            for eachTextSoup in zhcnNameSoupList:
                                curPartName = eachTextSoup.attrs.get("value")
                                accountZhcnFullName += curPartName

    # return accountZhcnTextSoup
    return accountZhcnFullName

def debugPublicAccountZhcnFullName(curSession):
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    # curAccountId = "niuer-tmall"
    curAccountId = "limi_official"

    accountZhcnFullName = findWeixinPublicAccountZhcnFullName(soup, curAccountId)
    print("accountZhcnFullName=%s" % accountZhcnFullName)


def testWeixinPublicAccount(curSession):
    # curScreenFile = debugSaveScreenshot(curScale=curSession.scale)

    # <XCUIElementTypeButton type="XCUIElementTypeButton" name="通讯录" label="通讯录" enabled="true" visible="true" x="96" y="619" width="90" height="48"/>
    # contactQuery = {"nameContains": "通讯录"}
    contactQuery = {"name": "通讯录"}
    foundAndClickedContact = findAndClickElement(curSession, contactQuery)
    if not foundAndClickedContact:
        logging.error("Not found and/or clicked for %s", contactQuery)
        return

    # <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="285" width="375" height="55">
    #   <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="公众号" name="公众号" label="公众号" enabled="true" visible="false" x="56" y="285" width="49" height="55"/>
    publickAccountQuery = {"name": "公众号"}
    foundAndClickedAccount = findAndClickElement(curSession, publickAccountQuery)
    if not foundAndClickedAccount:
        logging.error("Not found and/or clicked for %s", publickAccountQuery)
        return

    # debugSaveScreenshot(curScale=curSession.scale)

    # <XCUIElementTypeButton type="XCUIElementTypeButton" name="添加" label="添加" enabled="true" visible="true" x="317" y="20" width="58" height="44"/>
    addQuery = {"name": "添加"}
    foundAndClickedAdd = findAndClickElement(curSession, addQuery)
    if not foundAndClickedAdd:
        logging.error("Not found and/or clicked for %s", addQuery)
        return

    # debugSaveScreenshot(curScale=curSession.scale)
    # debugSaveSource()

    # time.sleep(0.5)

    # <XCUIElementTypeSearchField type="XCUIElementTypeSearchField" name="搜索" label="搜索" enabled="true" visible="true" x="41" y="24" width="280" height="36"/>
    searchInputQuery = {"name": "搜索"}
    isFoundSearchInput, respInfo = findElement(curSession, searchInputQuery)
    if not isFoundSearchInput:
        logging.error("Not found element for %s", searchInputQuery)
        return

    searchFieldElement = respInfo
    curAccountId = PublicAccount_DongKaKongJian
    searchFieldElement.set_text(curAccountId)
    logging.info("set text %s to %s", curAccountId, searchFieldElement)

    debugSaveScreenshot(curScale=curSession.scale)
    debugSaveSource()

    # <XCUIElementTypeButton type="XCUIElementTypeButton" name="Search" label="Search" enabled="true" visible="true" x="281" y="620" width="94" height="47"/>
    searchButtonQuery = {"name": "Search"}
    foundAndClickedDoSearch = findAndClickElement(curSession, searchButtonQuery)
    if not foundAndClickedDoSearch:
        logging.error("Not found and/or clicked for %s", searchButtonQuery)
        return

    debugSaveScreenshot(curScale=curSession.scale)
    debugSaveSource()

    curPageXml = getPageSource(gWdaClient)
    # <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="gh_cfcfcee032cc" name="gh_cfcfcee032cc" label="gh_cfcfcee032cc" enabled="true" visible="true" x="145" y="178" width="112" height="18"/>
    soup = utils.xmlToSoup(curPageXml)
    accountZhcnTextSoup = findWeixinPublicAccountZhcnSoup(soup, curAccountId)
    logging.info("curAccountId=%s -> accountZhcnTextSoup=%s", curAccountId, accountZhcnTextSoup)
    # <XCUIElementTypeStaticText enabled="true" height="22" label="动卡空间" name="动卡空间" type="XCUIElementTypeStaticText" value="动卡空间" visible="true" width="70" x="88" y="126"/>
    if not accountZhcnTextSoup:
        logging.error("Not found public account zhcn text soup node")
        return

    accountZhcnName = accountZhcnTextSoup["name"]
    accountZhcnLabel = accountZhcnTextSoup["label"]
    logging.info("accountZhcnName=%s, accountZhcnLabel=%s", accountZhcnName, accountZhcnLabel)
    # accountZhcnName=动卡空间, accountZhcnLabel=动卡空间
    accountZhcnTextQuery = {"name": accountZhcnName, "label": accountZhcnLabel}
    foundAnClickedAccountZhcnName = findAndClickElement(curSession, query=accountZhcnTextQuery)
    if not foundAnClickedAccountZhcnName:
        logging.error("Not found and clicked public account zhcn name element for %s", accountZhcnTextQuery)
        return

    """
        <XCUIElementTypeButton type="XCUIElementTypeButton" name="进入公众号" label="进入公众号" enabled="true" visible="false" x="0" y="256" width="87" height="34">
            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="进入公众号" name="进入公众号" label="进入公众号" enabled="true" visible="false" x="0" y="263" width="87" height="21"/>
        </XCUIElementTypeButton>
    """
    intoAccountQuery = {"name": "进入公众号", "type": "XCUIElementTypeButton", "visible": "true"}
    isFoundIntoAccount, respInfo = findElement(curSession, query=intoAccountQuery, timeout=1.0)
    logging.info("isFoundIntoAccount=%s, respInfo=%s", isFoundIntoAccount, respInfo)
    if isFoundIntoAccount:
        intoAccountElement = respInfo
        clickElement(curSession, intoAccountElement)
        # respInfo = None
    else:
        # <XCUIElementTypeButton type="XCUIElementTypeButton" name="关注公众号" label="关注公众号" enabled="true" visible="true" x="144" y="256" width="87" height="34"/>
        focusAccountQuery = {"name": "关注公众号", "type": "XCUIElementTypeButton", "visible": "true"}
        foundAndClickedFocus = findAndClickElement(curSession, query=focusAccountQuery, timeout=1.0)
        logging.info("foundAndClickedFocus=%s", foundAndClickedFocus)

    debugSaveScreenshot(curScale=curSession.scale)
    debugSaveSource()

def debugMiniprogramPopupGetYours(curSession):
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False

    """
        小程序 弹框 需要获取你的地理位置：
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="375" height="667"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="375" height="667"/>
                <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="&quot;贝德玛会员中心&quot; 需要获取你的地理位置" label="&quot;贝德玛会员中心&quot; 需要获取你的地理位置" enabled="true" visible="true" x="52" y="270" width="271" height="127">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="270" width="271" height="127">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="270" width="271" height="127">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="52" y="270" width="271" height="127">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="52" y="270" width="271" height="127"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="52" y="270" width="271" height="127">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="52" y="270" width="271" height="127"/>
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="52" y="270" width="271" height="127"/>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="270" width="271" height="127">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="270" width="271" height="83">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="270" width="271" height="83">
                                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="&quot;贝德玛会员中心&quot; 需要获取你的地理位置" name="&quot;贝德玛会员中心&quot; 需要获取你的地理位置" label="&quot;贝德玛会员中心&quot; 需要获取你的地理位置" enabled="true" visible="true" x="68" y="290" width="239" height="43"/>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="352" width="271" height="1">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="52" y="352" width="271" height="1"/>
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="352" width="271" height="1"/>
                                </XCUIElementTypeOther>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="353" width="271" height="44">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="353" width="271" height="44">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="353" width="271" height="44">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="52" y="353" width="136" height="44">
                                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="不允许" label="不允许" enabled="true" visible="true" x="52" y="353" width="136" height="44"/>
                                            </XCUIElementTypeOther>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="187" y="353" width="1" height="44">
                                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="187" y="353" width="1" height="44"/>
                                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="187" y="353" width="1" height="44"/>
                                            </XCUIElementTypeOther>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="188" y="353" width="135" height="44">
                                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="允许" label="允许" enabled="true" visible="true" x="188" y="353" width="135" height="44"/>
                                            </XCUIElementTypeOther>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeAlert>
            </XCUIElementTypeOther>
        </XCUIElementTypeOther>
    """
    getYoursP = re.compile("需要获取你的") # "贝德玛会员中心" 需要获取你的地理位置
    getYoursAlertSoup = soup.find(
        'XCUIElementTypeAlert',
        attrs={"name": getYoursP, "type": "XCUIElementTypeAlert", "enabled":"true", "visible":"true"},
    )
    if getYoursAlertSoup:
        allowSoup = getYoursAlertSoup.find(
            "XCUIElementTypeButton",
            attrs={"type": "XCUIElementTypeButton", "visible":"true", "enabled":"true", "name":"允许"}
        )
        if allowSoup:
            clickCenterPosition(curSession, allowSoup.attrs)
            foundAndProcessedPopup = True

    return foundAndProcessedPopup

def debugMissAndNotLocateMainMenu(curSession):
    """
        公众号 聊天页 底部主菜单：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="617" width="375" height="50">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="0" y="617" width="375" height="50"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="切换到文本输入" label="切换到文本输入" enabled="true" visible="true" x="0" y="617" width="44" height="50"/>
                <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="44" y="617" width="331" height="50">
                    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="44" y="617" width="111" height="50">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="牛尔天猫" label="牛尔天猫" enabled="true" visible="true" x="44" y="617" width="111" height="49"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="59" y="666" width="96" height="1"/>
                    </XCUIElementTypeCell>
                    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="154" y="617" width="111" height="50">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="会员福利" label="会员福利" enabled="true" visible="true" x="154" y="617" width="111" height="49"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="169" y="666" width="96" height="1"/>
                    </XCUIElementTypeCell>
                    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="264" y="617" width="112" height="50">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="店铺热卖" label="店铺热卖" enabled="true" visible="true" x="264" y="617" width="112" height="49"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="279" y="666" width="97" height="1"/>
                    </XCUIElementTypeCell>
                </XCUIElementTypeScrollView>
            </XCUIElementTypeOther>
    """
    pass

def debugPopupDoSomeFail(curSession):
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    """
        微信：
            获取信息失败：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            。。。
                <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="获取信息失败" name="获取信息失败" label="获取信息失败" enabled="true" visible="true" x="71" y="309" width="272" height="21"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="取消" name="取消" label="取消" enabled="true" visible="true" x="109" y="419" width="36" height="22"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="确定" name="确定" label="确定" enabled="true" visible="true" x="269" y="419" width="36" height="22"/>
                </XCUIElementTypeButton>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="87" height="32">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="88" height="32">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="320" y="24" width="44" height="32"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="关闭" label="关闭" enabled="true" visible="true" x="363" y="24" width="45" height="32"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            。。。
            </XCUIElementTypeWindow>

            微信登录失败：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="32" y="247" width="311" height="173">
                            <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="32" y="247" width="311" height="173"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微信登录失败" name="微信登录失败" label="微信登录失败" enabled="true" visible="true" x="52" y="272" width="271" height="22"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="此公众号并没有这些scope的权限，错误码:10005" name="此公众号并没有这些scope的权限，错误码:10005" label="此公众号并没有这些scope的权限，错误码:10005" enabled="true" visible="true" x="59" y="309" width="257" height="40"/>
                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="32" y="370" width="311" height="50"/>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeButton>
                </XCUIElementTypeOther>
            </XCUIElementTypeWindow>

        小程序：
            获取信息失败：
            <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="32" y="251" width="311" height="165">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="32" y="251" width="311" height="165"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="获取信息失败" name="获取信息失败" label="获取信息失败" enabled="true" visible="true" x="52" y="276" width="271" height="21"/>
                    <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="是否重新加载页面" enabled="true" visible="true" x="121" y="311" width="133" height="35"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="32" y="365" width="156" height="51"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="187" y="365" width="156" height="51"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeButton>
    """
    foundAndProcessed = False

    doSomeFailP = re.compile("\S+失败$") # 获取信息失败, 微信登录失败
    doSomeFailChainList = generateCommonPopupItemChainList(ScreenX, ScreenY, thirdLevelValue=doSomeFailP)
    doSomeFailSoup = utils.bsChainFind(soup, doSomeFailChainList)
    if doSomeFailSoup:
        parentButtonOrOtherSoup = doSomeFailSoup.parent
        if parentButtonOrOtherSoup:
            # 微信 弹框：获取信息失败
            foundConfirm = parentButtonOrOtherSoup.find(
                "XCUIElementTypeStaticText",
                attrs={"visible":"true", "enabled":"true", "value": "确定"}
            )

            if not foundConfirm:
                # 小程序 弹框：获取信息失败
                # 微信 弹框：微信登录失败
                foundConfirm = parentButtonOrOtherSoup.find(
                    "XCUIElementTypeButton",
                    attrs={"visible":"true", "enabled":"true", "name": "确定"}
                )

            if foundConfirm:
                clickCenterPosition(curSession, foundConfirm.attrs)
                foundAndProcessed = True

    return foundAndProcessed

def debugWeixinPopupAuthorizeLocation(curSession):
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False

    """
        微信 弹框 是否授权当前位置：
            <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="32" y="240" width="311" height="187">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="32" y="240" width="311" height="187"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="是否授权当前位置" name="是否授权当前位置" label="是否授权当前位置" enabled="true" visible="true" x="52" y="265" width="271" height="21"/>
                    <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="需要获取您的地理位置，请确认授权，否则无法获取专柜导航" enabled="true" visible="true" x="67" y="300" width="241" height="57"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="32" y="376" width="156" height="51"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="187" y="376" width="156" height="51"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeButton>
    """
    authorizeLocationChainList = [
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"visible":"true", "enabled":"true", "width": "%s" % ScreenX, "height": "%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true"}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value":"是否授权当前位置"}
        },
    ]
    authorizeLocationSoup = utils.bsChainFind(soup, authorizeLocationChainList)
    if authorizeLocationSoup:
        parentOtherSoup = authorizeLocationSoup.parent
        confirmSoup = parentOtherSoup.find("XCUIElementTypeButton", attrs={"visible":"true", "enabled":"true", "name": "确定"})
        if confirmSoup:
            clickCenterPosition(curSession, confirmSoup.attrs)
            foundAndProcessedPopup = True

    return foundAndProcessedPopup

def debugWeixinPopupLoginFail(curSession):
    foundAndProcessedPopup = False
    ScreenX = 375
    ScreenY = 667

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)

    """
        <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="375" height="667">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="0" y="0" width="375" height="667">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="32" y="247" width="311" height="173">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="32" y="247" width="311" height="173"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="微信登录失败" name="微信登录失败" label="微信登录失败" enabled="true" visible="true" x="52" y="272" width="271" height="22"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="此公众号并没有这些scope的权限，错误码:10005" name="此公众号并没有这些scope的权限，错误码:10005" label="此公众号并没有这些scope的权限，错误码:10005" enabled="true" visible="true" x="59" y="309" width="257" height="40"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="32" y="370" width="311" height="50"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeButton>
            </XCUIElementTypeOther>
        </XCUIElementTypeWindow>
    """
    getInfoFailChainList = generateCommonPopupItemChainList(ScreenX, ScreenY, thirdLevelValue="微信登录失败")


def isPublicAccountFocusOrIntoPage_iOS(page):
    """Check whether current page is Weixin Public focus or enter into page"""
    isPublicAccountFocusOrInto = False

    soup = utils.xmlToSoup(page)
    foundNaviBar = soup.find(
        'XCUIElementTypeNavigationBar',
        attrs={"type":"XCUIElementTypeNavigationBar", "enabled":"true"},
    )
    if foundNaviBar:
        foundTypeOther = foundNaviBar.find("XCUIElementTypeOther",
            attrs={"type": "XCUIElementTypeOther", "enabled":"true"}
        )
        logging.info("foundTypeOther=%s", foundTypeOther)

    return isPublicAccountFocusOrInto

def testWeixinPublickAccountFocusPage(curSession):
    global gWdaClient
    curPageXml = getPageSource(gWdaClient)
    isPublicAccountFocusOrInto = isPublicAccountFocusOrIntoPage_iOS(curPageXml)


def wdaDebugWeixin():
    # testWeixinPublicAccount(curSession)

    # testWeixinPublickAccountFocusPage(curSession)

    # debugBack(curSession)

    # debugSecondLevelMenu(curSession)

    # debugBack_PublicAccounSearchPage(curSession)

    # debugDisplayed(curSession)

    # debugWeixinExceptionNextStep(curSession)
    
    # debugMakesureIntoWeixin(curSession)

    # debugPopupCertificate(curSession)

    # debugPopupJumpThirdApp(curSession)

    # debugPopupWeixinLogin(curSession)

    # debugElementVisible(curSession)

    # debugPopupGetInfoFail(curSession)

    # debugMiniprogramBack(curSession)

    # debugMiniprogamPopupAuthority(curSession)

    # debugMiniprogamPopupGetContactInfo(curSession)

    # debugMiniprogamPopupDisclaimer(curSession)

    # debugMissAndNotLocateMainMenu(curSession)

    # debugWeixinPopupLoginFail(curSession)
    # debugPopupDoSomeFail(curSession)

    # debugMiniprogramPopupGetYours(curSession)

    # debugWeixinPopupAuthorizeLocation(curSession)

    # debugAccountSearchResultNoAccountName(curSession)

    # debugSettingsAllowUseLocation(curSession)

    # debugUnfollowSingleAccount(curSession)

    # debugPublicAccountPage_swipeToTop(curSession)

    # debugSwipeUntilFound(curSession)

    # debugNotFoundElement(curSession)

    # debugUnfollowCrashPartVisible(curSession)

    # debugCalcHeadY(curSession)

    # debugElementQueryRegex(curSession)

    # debugScrollPartVisible(curSession)

    # debugMiniprogramPopWarningNotAuthorized(curSession)

    # debugWillOpenNonOfficialPage(curSession)

    # debugWeixinPublicAccountSearchNotFound(curSession)

    # debugPublicAccountZhcnFullName(curSession)

    pass


if __name__ == "__main__":
    wdaDebugWeixin()
