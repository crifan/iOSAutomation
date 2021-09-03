# Functon: Crifan's bs=BeautifulSoup common functions
# Author: Crifan Li
# Update: 20200603

import copy

################################################################################
# Config
################################################################################

################################################################################
# BeautifulSoup Function
################################################################################

def generateFullScreenSoupAttrDict(curScreenX, curScreenY):
    """Generate for common used full screen soup attribute dict value
        for later Beautifulsoup find elememt use
    """
    curFullScreenSoupAttrDict = {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % curScreenX, "height":"%s" % curScreenY}
    return curFullScreenSoupAttrDict


# def generateCommonPopupItemChainList(screenWidth, screenHeight, itemValue):
#     commonItemChainList = [
#         {
#             "tag": "XCUIElementTypeWindow",
#             "attrs": {"visible":"true", "enabled":"true", "width": "%s" % screenWidth, "height": "%s" % screenHeight}
#         },
#         {
#             "tag": "XCUIElementTypeButton",
#             "attrs": {"visible":"true", "enabled":"true", "width": "%s" % screenWidth, "height": "%s" % screenHeight}
#         },
#         {
#             "tag": "XCUIElementTypeStaticText",
#             "attrs": {"visible":"true", "enabled":"true", "value": itemValue}
#         },
#     ]
#     return commonItemChainList

def generateCommonPopupItemChainList(
        screenWidth,
        screenHeight,
        firstLevelTag="XCUIElementTypeWindow",
        # firstLevelAttrs=None,
        secondLevelTag="XCUIElementTypeButton",
        # secondLevelAttrs=None,
        thirdLevelTag="XCUIElementTypeStaticText",
        thirdLevelValue=None,
        thirdLevelName=None,
    ):
    """Generate common used chain list of parameter for later soup find use
    """
    CommonAttrs_VisibleEnabled = {"visible":"true", "enabled":"true"}
    # CommonAttrs_VisibleEnabledFullWidthFullHeight = {"visible":"true", "enabled":"true", "width": "%s" % self.X, "height": "%s" % self.totalY}
    CommonAttrs_VisibleEnabledFullWidthFullHeight = copy.deepcopy(CommonAttrs_VisibleEnabled)
    CommonAttrs_VisibleEnabledFullWidthFullHeight["width"] = screenWidth
    CommonAttrs_VisibleEnabledFullWidthFullHeight["height"] = screenHeight

    # if not firstLevelAttrs:
    #     firstLevelAttrs = CommonAttrs_VisibleEnabledFullWidthFullHeight
    
    # if not secondLevelAttrs:
    #     secondLevelAttrs = CommonAttrs_VisibleEnabledFullWidthFullHeight

    commonItemChainList = [
        {
            "tag": firstLevelTag,
            # "attrs": firstLevelAttrs
            "attrs": CommonAttrs_VisibleEnabledFullWidthFullHeight
        },
        {
            "tag": secondLevelTag,
            # "attrs": secondLevelAttrs
            "attrs": CommonAttrs_VisibleEnabledFullWidthFullHeight
        },
    ]
    thirdItemAttrs = copy.deepcopy(CommonAttrs_VisibleEnabled)
    if thirdLevelValue:
        thirdItemAttrs["value"] = thirdLevelValue
    if thirdLevelName:
        thirdItemAttrs["name"] = thirdLevelName
    thirdItemDict =  {
        "tag": thirdLevelTag,
        "attrs": thirdItemAttrs
    }
    commonItemChainList.append(thirdItemDict)
    return commonItemChainList

def isContainSpecificSoup(soupList, elementName, isSizeValidCallback, matchNum=1):
    """
        判断BeautifulSoup的soup的list中，是否包含符合条件的特定的元素：
            只匹配指定个数的元素才视为找到了
            元素名相同
            面积大小是否符合条件
    Args:
        elementName (str): element name
        isSizeValidCallback (function): callback function to check whether element size(width * height) is valid or not
        matchNum (int): sould only matched specific number consider as valid
    Returns:
        bool
    Raises:
    """
    isFound = False

    matchedSoupList = []

    for eachSoup in soupList:
        # if hasattr(eachSoup, "tag"):
        if hasattr(eachSoup, "name"):
            # curSoupTag = eachSoup.tag
            curSoupTag = eachSoup.name
            if curSoupTag == elementName:
                if hasattr(eachSoup, "attrs"):
                    soupAttr = eachSoup.attrs
                    soupWidth = int(soupAttr["width"])
                    soupHeight = int(soupAttr["height"])
                    curSoupSize = soupWidth * soupHeight # 326 * 270
                    isSizeValid = isSizeValidCallback(curSoupSize)
                    if isSizeValid:
                        matchedSoupList.append(eachSoup)

    matchedSoupNum = len(matchedSoupList)
    if matchNum == 0:
        isFound = True
    else:
        if matchedSoupNum == matchNum:
            isFound = True

    return isFound
