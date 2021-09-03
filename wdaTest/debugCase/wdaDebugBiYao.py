# Functon: debug iOS app 必要 many cases
# Author: Crifan Li
# Update: 20200601


# def debugBiYaoPopupUpperRightColseButton(curSession):
def debugPopupNameContainColseButton(curSession):
    """
        必要 红包 弹框 右上角 name中有close
        必要 验证码登录 弹框 左上角 name中有close
    """
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        必要 弹框 右上角关闭按钮 name中有close：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="414" height="736"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="44" y="150" width="327" height="436">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="rights close white" label="rights close white" enabled="true" visible="true" x="338" y="150" width="32" height="32"/>
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="44" y="199" width="326" height="387">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="01 : 58 : 31 . 6 后过期" name="01 : 58 : 31 . 6 后过期" label="01 : 58 : 31 . 6 后过期" enabled="true" visible="true" x="137" y="476" width="140" height="18"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="137" y="495" width="140" height="2"/>
                    </XCUIElementTypeImage>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>

        必要 验证码登录页 左上角 关闭 按钮 name中含close：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="login close" label="login close" enabled="true" visible="true" x="10" y="20" width="44" height="44"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="293" y="20" width="111" height="44">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="密码登录" label="密码登录" enabled="true" visible="true" x="293" y="20" width="111" height="44"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
    """
    closeP = re.compile("close")
    # rights close white
    # login close
    closeChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": closeP}
        },
    ]
    closeSoup = utils.bsChainFind(soup, closeChainList)
    if closeSoup:
        # clickCenterPosition(curSession, closeSoup.attrs) # seems not work: click other place ?
        # foundAndProcessedPopup = True

        # # change to wda element query then click by element
        # curButtonName = closeSoup.attrs["name"]
        # # rights close white
        # # login close
        # closeButtonQuery = {"type":"XCUIElementTypeButton", "enabled":"true", "name": curButtonName}
        # foundAndClicked = findAndClickElement(curSession, closeButtonQuery)
        # foundAndProcessedPopup = foundAndClicked
        foundAndProcessedPopup = findAndClickButtonElementBySoup(curSession, closeSoup)

    return foundAndProcessedPopup

def debugBiYaoBackButton(curSession):
    """必要 左上角 返回 name中有back """
    back_iOS(curSession)


def debugPopupPossibleCloseButton(curSession):
    """
        必要 弹框 首单限时福利 右上角 关闭按钮
            特殊：但是内部无有效识别内容，比如name中包含close这类条件
            暂时只能特殊但通用处理：
                window -> other -> button
                    且 button的 w和h基本一致，后者差距小于w和h最大值的10%
                    以及 w和h都在一定（普通关闭按钮的大小）范围，比如 20-60

        必要 我的 蒙层弹框 首次使用引导页：
            基于上面逻辑：
                window->other->button
                button条件不变
            基础上，底层判断逻辑是：
                next的sibling后面，有且只有一个button，且有name
                    且按钮宽高大小在合理范围，比如普通按钮的大小，算作为 30x30 < 按钮面积 < 100x100
                        意思是：引导页往往伴随着一个普通大小的按钮，供用户点击
        
        必要 弹框 推荐开通以下授权 关闭按钮在弹框下面：
            和前面逻辑略有不同
                Application -> window -> Other
            button条件不变
            其他条件类似于第一个，但是是 prev的sibling 是个Other元素，且面积是弹框类大小
    """
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        必要 弹框 首单限时福利 右上角 关闭按钮：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            。。。
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="339" y="122" width="31" height="32"/>
                    <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="44" y="174" width="326" height="388"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeWindow>
        
        必要 我的 蒙层弹框 首次使用引导页：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                。。。
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="208"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="392" width="414" height="344"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="101" y="406" width="296" height="186">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="101" y="406" width="296" height="186"/>
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="236" y="441" width="25" height="25"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="367" y="459" width="25" height="25"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="发现新功能" name="发现新功能" label="发现新功能" enabled="true" visible="true" x="114" y="468" width="88" height="18"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="必要地震预警通知功能（测试版）上线！ 曾提前61秒成功为成都预警四川长宁地震的成都高新减灾研究所与必要战略合作，为您的安全保驾护航！" name="必要地震预警通知功能（测试版）上线！ 曾提前61秒成功为成都预警四川长宁地震的成都高新减灾研究所与必要战略合作，为您的安全保驾护航！" label="必要地震预警通知功能（测试版）上线！ 曾提前61秒成功为成都预警四川长宁地震的成都高新减灾研究所与必要战略合作，为您的安全保驾护航！" enabled="true" visible="true" x="114" y="488" width="278" height="51"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="开启预警" label="开启预警" enabled="true" visible="true" x="316" y="547" width="67" height="32"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
        
        必要 弹框 推荐开通以下授权 关闭按钮在弹框下面：：
            <XCUIElementTypeApplication type="XCUIElementTypeApplication" name="必要" label="必要" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    。。。
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="44" y="233" width="326" height="270">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="推荐开通以下授权" name="推荐开通以下授权" label="推荐开通以下授权" enabled="true" visible="true" x="53" y="257" width="308" height="24"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="86" y="324" width="242" height="58">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="85" y="324" width="244" height="58">
                                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="85" y="331" width="45" height="45"/>
                                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="定位" name="定位" label="定位" enabled="true" visible="true" x="140" y="324" width="33" height="19"/>
                                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="开启定位通知将在推荐、配送等方面为您提供更精准服务。" name="开启定位通知将在推荐、配送等方面为您提供更精准服务。" label="开启定位通知将在推荐、配送等方面为您提供更精准服务。" enabled="true" visible="true" x="140" y="353" width="189" height="29"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="开启" label="开启" enabled="true" visible="true" x="69" y="429" width="276" height="50"/>
                    </XCUIElementTypeOther>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="191" y="538" width="32" height="31"/>
    """
    # noNameP = re.compile("???")
    noNameP = False
    possibleCloseChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": noNameP}
        },
    ]
    possibleCloseSoup = utils.bsChainFind(soup, possibleCloseChainList)

    isCloseUnderPopup = False
    if not possibleCloseSoup:
        # 尝试找 是否是 关闭按钮在弹框下面的 弹框
        closeUnderPopupChainList = [
            {
                "tag": "XCUIElementTypeApplication",
                "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
            },
            {
                "tag": "XCUIElementTypeWindow",
                "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
            },
            {
                "tag": "XCUIElementTypeButton",
                "attrs": {"enabled":"true", "visible":"true", "name": noNameP}
            },
        ]
        possibleCloseSoup = utils.bsChainFind(soup, closeUnderPopupChainList)
        if possibleCloseSoup:
            isCloseUnderPopup = True

    if possibleCloseSoup:
        isValidSize = False
        isAlmostSameWH = False
        # isNexSiblingImage = False
        # isImageSizeValid = False

        isPossibleClose = True

        if isPossibleClose:
            # check is match close button rule or not
            soupAttrDict = possibleCloseSoup.attrs # {'enabled': 'true', 'height': '32', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'width': '31', 'x': '339', 'y': '122'}
            logging.debug("possibleCloseSoup soupAttrDict=%s", soupAttrDict)
            # x = int(soupAttrDict["x"])
            # y = int(soupAttrDict["y"])
            width = int(soupAttrDict["width"])
            height = int(soupAttrDict["height"])
            # ButtonMinWH = 20
            # ButtonMinWH = 30
            ButtonMinWH = 25
            ButtonMaxWH = 60
            isValidWidth = ButtonMinWH  <= width  <= ButtonMaxWH
            isValidHeight = ButtonMinWH <= height <= ButtonMaxWH
            isValidSize = isValidWidth and isValidHeight

            isPossibleClose = isValidSize

        if isPossibleClose:
            isAlmostSameWH = False
            isSameWH = width == height
            if isSameWH:
                isAlmostSameWH = isSameWH
            else:
                maxWH = max(width, height)
                diffWH = abs(width - height)
                MaxAllowDiffRatio = 0.1
                curDiffRatio = diffWH / maxWH
                isValidDiff = curDiffRatio <= MaxAllowDiffRatio
                isAlmostSameWH = isValidDiff

            isPossibleClose = isAlmostSameWH

        if isPossibleClose:
            # check next sibling is large Image
            # nextSiblingeSoup = possibleCloseSoup.next_sibling # '\n'
            nextSiblingSoupGenerator = possibleCloseSoup.next_siblings
            nextSiblingSoupList = list(nextSiblingSoupGenerator)

            def isPopupWindowSize(curSize):
                FullScreenSize = ScreenX * ScreenY
                curSizeRatio = curSize / FullScreenSize # 0.289
                PopupWindowSizeMinRatio = 0.25
                # PopupWindowSizeMaxRatio = 0.9
                PopupWindowSizeMaxRatio = 0.8
                # isSizeValid = curSizeRatio >= MinPopupWindowSizeRatio
                # is popup like window, size should large enough, but should not full screen
                isSizeValid = PopupWindowSizeMinRatio <= curSizeRatio <= PopupWindowSizeMaxRatio
                return isSizeValid

            hasLargeImage = isContainSpecificSoup(nextSiblingSoupList, "XCUIElementTypeImage", isPopupWindowSize)
            isPossibleClose = hasLargeImage

            if not isPossibleClose:
                def isNormalButton(curSize):
                    NormalButtonSizeMin = 30*30
                    NormalButtonSizeMax = 100*100
                    isNormalSize = NormalButtonSizeMin <= curSize <= NormalButtonSizeMax
                    return isNormalSize

                hasNormalButton = isContainSpecificSoup(nextSiblingSoupList, "XCUIElementTypeButton", isNormalButton)
                isPossibleClose = hasNormalButton

            if not isPossibleClose:
                if isCloseUnderPopup:
                    # prevSiblingSoupGenerator = possibleCloseSoup.previous_siblings
                    # prevPrevSiblingSoupList = list(prevSiblingSoupGenerator)
                    # hasLargeOther = isContainSpecificSoup(prevPrevSiblingSoupList, "XCUIElementTypeOther", isPopupWindowSize)
                    prevSiblingSoup = possibleCloseSoup.previous_sibling # '\n'
                    if prevSiblingSoup:
                        prevPrevSiblingSoup = prevSiblingSoup.previous_sibling # XCUIElementTypeOther
                        prevPrevSiblingSoupList = [ prevPrevSiblingSoup ]
                        hasLargeOther = isContainSpecificSoup(prevPrevSiblingSoupList, "XCUIElementTypeOther", isPopupWindowSize)
                        isPossibleClose = hasLargeOther

            # NextSiblingImage = "XCUIElementTypeImage"
            # nextFirstImgeSoup = None
            # for eachNextSiblingSoup in nextSiblingSoupList:
            #     # if hasattr(eachNextSiblingSoup, "tag"):
            #     if hasattr(eachNextSiblingSoup, "name"):
            #         # curSiblingTag = eachNextSiblingSoup.tag
            #         curSiblingTag = eachNextSiblingSoup.name
            #         if curSiblingTag == NextSiblingImage:
            #             nextFirstImgeSoup = eachNextSiblingSoup
            #             break
            # # if hasattr(nextSiblingeSoup, "tag"):
            # #     nextSiblingTag = nextSiblingeSoup.tag
            # #     isNexSiblingImage = nextSiblingTag == NextSiblingImage
            # # else:
            # #     isNexSiblingImage = False
            # isNexSiblingImage = bool(nextFirstImgeSoup)
            # isPossibleClose = isNexSiblingImage
            # if isPossibleClose:
            #     # if hasattr(nextSiblingeSoup, "attrs"):
            #     if hasattr(nextFirstImgeSoup, "attrs"):
            #         # imageAttr = nextSiblingeSoup.attrs
            #         imageAttr = nextFirstImgeSoup.attrs
            #         imageWidth = int(imageAttr["width"])
            #         imageHeight = int(imageAttr["height"])
            #         curImgSize = imageWidth * imageHeight
            #         FullScreenSize = ScreenX * ScreenY
            #         curImageRatio = curImgSize / FullScreenSize
            #         MinPopupWindowSizeRatio = 0.25
            #         # image is popup image, size should large enough
            #         isImageSizeValid = curImageRatio >= MinPopupWindowSizeRatio
            #     else:
            #         isImageSizeValid = False
            #     isPossibleClose = isImageSizeValid

        # logging.debug("isValidSize=%s, isAlmostSameWH=%s, isNexSiblingImage=%s, isImageSizeValid=%s, isPossibleClose=%s",
        #     isValidSize, isAlmostSameWH, isNexSiblingImage, isImageSizeValid, isPossibleClose)

        if isPossibleClose:
            foundAndProcessedPopup = findAndClickButtonElementBySoup(curSession, possibleCloseSoup)

    return foundAndProcessedPopup

def debugBiYaoPopupCoverGuide(curSession):
    debugPopupPossibleCloseButton(curSession)

def debugBiYaoPopupCloseUnderPopup(curSession):
    debugPopupPossibleCloseButton(curSession)


def debugBiYaoPopupSovereignHasRead(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        必要 弹框 朕已阅：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="44" y="156" width="326" height="424">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="抢福利活动说明" name="抢福利活动说明" label="抢福利活动说明" enabled="true" visible="true" x="149" y="165" width="117" height="20"/>
                    <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="抢福利活动全新上线啦！！！&#10;当您获得特权金、参团卡、全民拼卡、返现卡、金币等资产后，请您尽快使用，很可能会被好友抢走哦！&#10;本期重磅推出&lt;保护罩&gt;道具卡！您的资产可受到保护不被抢走,快去使用金币在每日签到页兑换吧！！&#10;新玩法需要用户更新APP，如果您更新APP后，仍然无法参与活动，有可能APP正在发版中，请您等待。" enabled="true" visible="true" x="66" y="204" width="282" height="292"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="朕已阅" label="朕已阅" enabled="true" visible="true" x="82" y="513" width="250" height="50"/>
                </XCUIElementTypeImage>
            </XCUIElementTypeOther>
    """
    hasReadChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeImage",
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": "朕已阅"}
        },
    ]
    hasReadCloseSoup = utils.bsChainFind(soup, hasReadChainList)
    if hasReadCloseSoup:
        clickCenterPosition(curSession, hasReadCloseSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup


def debugBiYaoTabMineBackToMain(curSession):
    """
        当进入start back to main page
        去判断
        当app 是必要
        且顶部是：热门 价格 全部分类 visible=true时
        则此时处于 我的 页面，但是向下滚动后的页面
        然后去 向上滚动，直到：
        能找到visible=true的 设置
        即可视为 返回了main了。
    """
    ScreenX = 414
    ScreenY = 736

    SwipDuration = 0.1
    swipeBounds = utils.getSwipeBounds("SwipeUp", ScreenX, ScreenY, headY=64) # [207, 248, 207, 552]

    # curPageXml = getPageSource(gWdaClient)
    # soup = utils.xmlToSoup(curPageXml)

    """
        当 我的 向下滚动后，顶部始终显示 热门 价格 全部分类 时：
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="平台服务" label="平台服务" enabled="true" visible="false" x="286" y="-393" width="49" height="50"/>
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="设置" label="设置" enabled="true" visible="false" x="347" y="-393" width="50" height="50"/>
    """
    # foundInvisiblePlatformService = soup.find(
    #     'XCUIElementTypeButton',
    #     attrs={"type": "XCUIElementTypeButton", "name": "平台服务", "enabled":"true", "visible":"false"},
    # )
    # foundInvisibleSetting = soup.find(
    #     'XCUIElementTypeButton',
    #     attrs={"type": "XCUIElementTypeButton", "name": "设置", "enabled":"true", "visible":"false"},
    # )
    # isPageScrolledDown = bool(foundInvisiblePlatformService) and bool(foundInvisibleSetting)

    PlatformServiceQuery = {"type":"XCUIElementTypeButton", "name":"平台服务", "enabled":"true"}
    SettingQuery = {"type":"XCUIElementTypeButton", "name":"设置", "enabled":"true"}

    isFoundPlatformService, platformServiceElement = findElement(curSession, PlatformServiceQuery, timeout=0.1)
    isFoundSetting, settingElement = findElement(curSession, SettingQuery, timeout=0.1)
    isPageScrolledDown = False
    if isFoundPlatformService and isFoundSetting:
        isPlatformServiceInvisible = not platformServiceElement.visible
        isSettingInvisible = not settingElement.visible
        isPageScrolledDown = isPlatformServiceInvisible and isSettingInvisible

    if isPageScrolledDown:
        while True:
            curSession.swipe(swipeBounds[0], swipeBounds[1], swipeBounds[2], swipeBounds[3], SwipDuration)

            # curPageXml = getPageSource(gWdaClient)
            # soup = utils.xmlToSoup(curPageXml)
            """
                当 我的 刚进入 顶部时：
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="平台服务" label="平台服务" enabled="true" visible="true" x="286" y="37" width="49" height="50"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="设置" label="设置" enabled="true" visible="true" x="347" y="37" width="50" height="50"/>
            """
            # foundVisiblePlatformService = soup.find(
            #     'XCUIElementTypeButton',
            #     attrs={"type": "XCUIElementTypeButton", "name": "平台服务", "enabled":"true", "visible":"true"},
            # )
            # foundVisibleSetting = soup.find(
            #     'XCUIElementTypeButton',
            #     attrs={"type": "XCUIElementTypeButton", "name": "设置", "enabled":"true", "visible":"true"},
            # )
            # isPageInTop = bool(foundVisiblePlatformService) and bool(foundVisibleSetting)

            isFoundPlatformService, platformServiceElement = findElement(curSession, PlatformServiceQuery, timeout=0.1)
            isFoundSetting, settingElement = findElement(curSession, SettingQuery, timeout=0.1)
            isPageInTop = False
            if isFoundPlatformService and isFoundSetting:
                isPlatformServiceVisible = platformServiceElement.visible
                isSettingVisible = settingElement.visible
                isPageInTop = isPlatformServiceVisible and isSettingVisible

            if isPageInTop:
                break

    return

def wdaDebugBiYao():

    # debugBiYaoPopupUpperRightColseButton(curSession)

    # debugBiYaoBackButton(curSession)

    # debugPopupNameContainColseButton(curSession)

    # debugPopupPossibleCloseButton(curSession)

    # debugBiYaoPopupCoverGuide(curSession)
    # debugBiYaoPopupCloseUnderPopup(curSession)

    # debugBiYaoPopupSovereignHasRead(curSession)

    # debugBiYaoTabMineBackToMain(curSession)
    pass

if __name__ == "__main__":
    wdaDebugJdFinance()