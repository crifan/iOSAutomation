

def debugTuHuSwipeLeftGuideToMain(curSession):
    """
        途虎养车 左滑引导页 1页/3页：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" name="guide0" enabled="true" visible="true" x="0" y="0" width="414" height="736"/>
                    </XCUIElementTypeScrollView>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" value="1" name="loading sign nonsel" label="loading sign nonsel" enabled="true" visible="true" x="177" y="630" width="10" height="10"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="loading sign nonsel" label="loading sign nonsel" enabled="true" visible="true" x="202" y="630" width="10" height="10"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="loading sign nonsel" label="loading sign nonsel" enabled="true" visible="true" x="227" y="630" width="10" height="10"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        
        途虎养车 左滑引导页 2页/3页：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" name="guide1" enabled="true" visible="true" x="0" y="0" width="414" height="736"/>
                    </XCUIElementTypeScrollView>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="loading sign nonsel" label="loading sign nonsel" enabled="true" visible="true" x="177" y="630" width="10" height="10"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" value="1" name="loading sign nonsel" label="loading sign nonsel" enabled="true" visible="true" x="202" y="630" width="10" height="10"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="loading sign nonsel" label="loading sign nonsel" enabled="true" visible="true" x="227" y="630" width="10" height="10"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        
        途虎养车 左滑引导页 3页/3页 立即进入：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" name="guide2" enabled="true" visible="true" x="0" y="0" width="414" height="736"/>
                    </XCUIElementTypeScrollView>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="loading btn" label="loading btn" enabled="true" visible="true" x="141" y="628" width="132" height="30"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    # GuideText = "guide"
    # parentScrollViewClassChain = "/XCUIElementTypeScrollView[`rect.x = 0 AND rect.y = 0 AND rect.width = %d AND rect.height = %d`]" % (ScreenX, ScreenY)
    # guideImgeQuery = {"type":"XCUIElementTypeImage", "nameContains": GuideText, "enabled": "true", "x":"0", "y":"0", "width": "%s" % ScreenX, "height":"%s" % ScreenY}
    # guideImgeQuery["parent_class_chains"] = [ parentScrollViewClassChain ]
    # isFound, guideImgeElement = findElement(curSession, guideImgeQuery, timeout=0.1)
    # if isFound:
    #     # foundAndClicked = clickElement(curSession, guideImgeElement)
    #     swipeLeft(curSession)

    foundAndSwipeGuideToMain = False
    FullScreenSoupAttrDict = generateFullScreenSoupAttrDict()

    guideP = re.compile("guide") # guide0, guide1, guide2
    guideImageChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {**FullScreenSoupAttrDict},
        },
        {
            "tag": "XCUIElementTypeScrollView",
            "attrs": {**FullScreenSoupAttrDict},
        },
        {
            "tag": "XCUIElementTypeImage",
            "attrs": {"name": guideP, **FullScreenSoupAttrDict}
        },
    ]

    while True:
        curPageXml = getPageSource(gWdaClient)
        soup = utils.xmlToSoup(curPageXml)

        guideImageSoup = utils.bsChainFind(soup, guideImageChainList)
        if not guideImageSoup:
            break

        parentScrollViewSoup = guideImageSoup.parent
        if not parentScrollViewSoup:
            break

        validButtonSoupList = []

        nextSiblingList = parentScrollViewSoup.next_siblings
        for eachNextSiblingSoup in nextSiblingList:
            if hasattr(eachNextSiblingSoup, "attrs"):
                soupAttrDict = eachNextSiblingSoup.attrs # {'enabled': 'true', 'height': '30', 'label': 'loading btn', 'name': 'loading btn', 'type': 'XCUIElementTypeButton', 'visible': 'true', 'width': '132', 'x': '141', 'y': '628'}
                soupType = soupAttrDict.get("type") # 'XCUIElementTypeButton'
                soupName = soupAttrDict.get("name") # 'loading btn'
                soupVisible = soupAttrDict.get("visible") # 'true'
                isButton = soupType == "XCUIElementTypeButton"
                # isLoadingName = bool(re.search(soupName, "loading"))
                isLoadingName = bool(re.search("loading", soupName))
                isVisible = soupVisible == "true"
                isValid = isButton and isLoadingName and isVisible
                if isValid:
                    validButtonSoupList.append(eachNextSiblingSoup)

        if validButtonSoupList:
            validButtonNum = len(validButtonSoupList)
            if validButtonNum == 1:
                # end page, click button, into main page
                lastPageButtonSoup = validButtonSoupList[0]
                clickCenterPosition(curSession, lastPageButtonSoup.attrs)
                foundAndSwipeGuideToMain = True
                break
            elif validButtonNum > 1:
                # not end, should continue to swipe left
                swipeLeft(curSession)
                logging.info("Swipe left for guide page")

    return foundAndSwipeGuideToMain

def debugTuHuPopupChooseCity(curSession):
    """
        途虎养车 弹框 选择城市 无法获取源码内容：
        <?xml version="1.0" encoding="UTF-8"?>
        <XCUIElementTypeAny type="XCUIElementTypeAny" name="途虎养车" label="途虎养车" enabled="true" visible="true" x="0" y="0" width="414" height="736"/>
    """
    pass

def debugTuHuPopupUnderCloseButton(curSession):
    """
        弹框 关闭按钮在弹框下面的 尤其是 name=""
    """
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        途虎养车 弹框 关闭按钮在下面 新人618全品类消费券：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                            <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="72" y="190" width="270" height="356"/>
                            <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="true" x="72" y="190" width="270" height="356"/>
                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="" label="" enabled="true" visible="true" x="187" y="589" width="40" height="41"/>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeWindow>
    """
    specialChar = ""
    underCloseChainList = [
        {
            "tag": "XCUIElementTypeWindow",
            "attrs": FullScreenSoupAttrDict,
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": FullScreenSoupAttrDict,
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": specialChar}
        },
    ]
    underCloseSoup = utils.bsChainFind(soup, underCloseChainList)
    if underCloseSoup:
        clickCenterPosition(curSession, underCloseSoup.attrs)
        foundAndProcessedPopup = True
    
    return foundAndProcessedPopup

def wdaDebugTuHu():
    # debugTuHuSwipeLeftGuideToMain(curSession)

    # debugTuHuPopupChooseCity(curSession)

    # debugTuHuPopupUnderCloseButton(curSession)

    pass


if __name__ == "__main__":
    wdaDebugTuHu()