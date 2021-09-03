# Functon: debug iOS app 京东金融 many cases
# Author: Crifan Li
# Update: 20200601


def debugJdFinanceRightUpperJumpOver(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 登录页 右上角 跳过：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" enabled="true" visible="false" x="65" y="20" width="284" height="44"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="跳过" label="跳过" enabled="true" visible="true" x="344" y="29" width="55" height="26"/>
                    </XCUIElementTypeOther>
    """
    jumpOverChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"跳过"}
        },
    ]
    jumpOverSoup = utils.bsChainFind(soup, jumpOverChainList)
    if jumpOverSoup:
        clickCenterPosition(curSession, jumpOverSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugJdFinanceRightUpperClose(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 登录页 弹框 右上角 关闭按钮：
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" enabled="true" visible="false" x="65" y="20" width="284" height="44"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="com icon black close u" label="com icon black close u" enabled="true" visible="true" x="370" y="20" width="44" height="44"/>
                    </XCUIElementTypeOther>
    """
    containCloseP = re.compile("close") # com icon black close u
    closeChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": containCloseP}
        },
    ]
    closeSoup = utils.bsChainFind(soup, closeChainList)
    if closeSoup:
        clickCenterPosition(curSession, closeSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugJdFinanceFullScreenImage(curSession):
    back_iOS(curSession)

def debugJdFinanceNetworkNotStableRetry(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
    京东金融 页面 网络不稳定 请点击重试：
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="com icon black backup u" label="com icon black backup u" enabled="true" visible="true" x="0" y="20" width="44" height="44"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" enabled="true" visible="false" x="65" y="20" width="284" height="44"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="comunity top report@3x" label="comunity top report@3x" enabled="true" visible="true" x="326" y="20" width="44" height="44"/>
                    </XCUIElementTypeOther>
                    <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="0" y="64" width="414" height="673">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="414" height="1"/>
                        <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="64" width="414" height="629">
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="网络不稳定,请点击重试" name="网络不稳定,请点击重试" label="网络不稳定,请点击重试" enabled="true" visible="true" x="16" y="322" width="382" height="21"/>
                            <XCUIElementTypeImage type="XCUIElementTypeImage" name="icon_network-instability" enabled="true" visible="false" x="132" y="152" width="150" height="151"/>
                        </XCUIElementTypeCell>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="692" width="414" height="1"/>
                    </XCUIElementTypeTable>
                </XCUIElementTypeOther>
    """
    networkNotStableChainList = [
        {
            "tag": "XCUIElementTypeTable",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeCell",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"enabled":"true", "visible":"true", "value": "网络不稳定,请点击重试"}
        },
    ]
    networkNotStableSoup = utils.bsChainFind(soup, networkNotStableChainList)
    if networkNotStableSoup:
        clickCenterPosition(curSession, networkNotStableSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugJdFinanceNetworkNotStableRefresh(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 页面 网络不稳定 刷新试试：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="414" height="623">
                <XCUIElementTypeTable type="XCUIElementTypeTable" name="空列表" label="空列表" enabled="true" visible="false" x="0" y="64" width="414" height="623"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="414" height="623">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" name="com_network_err" enabled="true" visible="false" x="152" y="164" width="110" height="110"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="网络不稳定" name="网络不稳定" label="网络不稳定" enabled="true" visible="true" x="0" y="287" width="414" height="17"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="刷新试试" label="刷新试试" enabled="true" visible="true" x="147" y="323" width="120" height="41"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    tryRefreshChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": "刷新试试"}
        },
    ]
    tryRefreshSoup = utils.bsChainFind(soup, tryRefreshChainList)
    if tryRefreshSoup:
        clickCenterPosition(curSession, tryRefreshSoup.attrs)
        foundAndProcessedPopup = True

        # # Special: above click by position not work
        # # so change to wda query element then click
        # tryRefreshButtonQuery = {"type":"XCUIElementTypeButton", "enabled":"true", "name": "刷新试试"}
        # foundAndClicked = findAndClickElement(curSession, tryRefreshButtonQuery)
        # foundAndProcessedPopup = foundAndClicked

    return foundAndProcessedPopup

def debugJdFinanceHiIAmMaxAlertClose(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
    京东金融 tab2财富 弹框 我是Max alertClose：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                。。。
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="jr fianncing alertClose@3x" label="jr fianncing alertClose@3x" enabled="true" visible="true" x="327" y="132" width="26" height="25"/>
    """
    alertCloseP = re.compile("alertClose")
    alertCloseChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": alertCloseP}
        },
    ]
    alertCloseSoup = utils.bsChainFind(soup, alertCloseChainList)
    if alertCloseSoup:
        clickCenterPosition(curSession, alertCloseSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugJdFinancePopupUpperRightCommonClose(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 登录页 弹框 右上角 关闭按钮：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" enabled="true" visible="false" x="65" y="20" width="284" height="44"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="com icon black close u" label="com icon black close u" enabled="true" visible="true" x="370" y="20" width="44" height="44"/>
                </XCUIElementTypeOther>

        京东金融 tab2财富 弹框 我是Max alertClose：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                。。。
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="jr fianncing alertClose@3x" label="jr fianncing alertClose@3x" enabled="true" visible="true" x="327" y="132" width="26" height="25"/>
    """
    commonCloseP = re.compile("close", flags=re.I) # alertClose, close
    commonCloseChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            # "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name": commonCloseP}
        },
    ]
    commonCloseSoup = utils.bsChainFind(soup, commonCloseChainList)
    if commonCloseSoup:
        clickCenterPosition(curSession, commonCloseSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugJdFinanceSystemAbnormalRetryRefresh(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 异常页面 系统正在开小差，请稍后再试 再刷新下：
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="系统正在开小差，请稍后再试 再刷新下" label="系统正在开小差，请稍后再试 再刷新下" enabled="true" visible="true" x="0" y="64" width="414" height="672">
                <XCUIElementTypeOther type="XCUIElementTypeOther" name="系统正在开小差，请稍后再试 再刷新下" label="系统正在开小差，请稍后再试 再刷新下" enabled="true" visible="true" x="0" y="64" width="414" height="672">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" name="系统正在开小差，请稍后再试" label="系统正在开小差，请稍后再试" enabled="true" visible="true" x="114" y="240" width="186" height="136">
                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="true" x="152" y="240" width="110" height="111"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="系统正在开小差，请稍后再试" name="系统正在开小差，请稍后再试" label="系统正在开小差，请稍后再试" enabled="true" visible="true" x="114" y="360" width="186" height="16"/>
                    </XCUIElementTypeOther>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" name="再刷新下" label="再刷新下" enabled="true" visible="true" x="147" y="375" width="120" height="61">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" name="再刷新下" label="再刷新下" enabled="true" visible="true" x="147" y="395" width="120" height="41"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    retryRefreshChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "name": "再刷新下"}
        },
    ]
    retryRefreshSoup = utils.bsChainFind(soup, retryRefreshChainList)
    if retryRefreshSoup:
        clickCenterPosition(curSession, retryRefreshSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugJdFinanceServerBusyLaterRetry(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 异常页面 服务器繁忙，请稍后重试
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="com icon backup u" label="com icon backup u" enabled="true" visible="true" x="0" y="20" width="44" height="44"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" enabled="true" visible="false" x="80" y="64" width="254" height="24"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="64" width="414" height="672">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" name="network_err_dog" enabled="true" visible="false" x="152" y="164" width="110" height="110"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="服务器繁忙，请稍后重试" name="服务器繁忙，请稍后重试" label="服务器繁忙，请稍后重试" enabled="true" visible="true" x="0" y="304" width="414" height="17"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="686" width="414" height="50">
                    <XCUIElementTypeCollectionView type="XCUIElementTypeCollectionView" enabled="true" visible="false" x="0" y="686" width="414" height="50"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" enabled="true" visible="false" x="0" y="686" width="414" height="50"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" enabled="true" visible="false" x="16" y="701" width="382" height="20"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    busyRetryChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"enabled":"true", "visible":"true", "value": "服务器繁忙，请稍后重试"}
        },
    ]
    busyRetrySoup = utils.bsChainFind(soup, busyRetryChainList)
    if busyRetrySoup:
        # find back button
        parentOtherSoup = busyRetrySoup.parent
        parentParentOtherSoup = parentOtherSoup.parent
        if parentParentOtherSoup:
            backupP = re.compile("backup") # "com icon backup u"
            backupSoup = parentParentOtherSoup.find(
                "XCUIElementTypeButton",
                attrs={"visible":"true", "enabled":"true", "name": backupP}
            )
            if backupSoup:
                clickCenterPosition(curSession, backupSoup.attrs)
                foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugJdFinanceGiveupRegister(curSession):
    ScreenX = 414
    ScreenY = 736
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False
    """
        京东金融 弹框 是否放弃注册？
        <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="是否放弃注册？" label="是否放弃注册？" enabled="true" visible="true" x="72" y="316" width="270" height="105">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="316" width="270" height="105">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="316" width="270" height="105">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="316" width="270" height="105">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="316" width="270" height="105"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="316" width="270" height="105">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="316" width="270" height="105"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="316" width="270" height="105"/>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="316" width="270" height="105">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="316" width="270" height="60">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="316" width="270" height="60">
                                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="是否放弃注册？" name="是否放弃注册？" label="是否放弃注册？" enabled="true" visible="true" x="88" y="335" width="238" height="21"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="376" width="270" height="1">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="376" width="270" height="1"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="376" width="270" height="1"/>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="376" width="270" height="45">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="376" width="270" height="45">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="376" width="270" height="45">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="376" width="135" height="45">
                                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="放弃" label="放弃" enabled="true" visible="true" x="72" y="376" width="135" height="45"/>
                                    </XCUIElementTypeOther>
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="1" height="45">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="207" y="376" width="1" height="45"/>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="1" height="45"/>
                                    </XCUIElementTypeOther>
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="135" height="45">
                                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="继续注册" label="继续注册" enabled="true" visible="true" x="207" y="376" width="135" height="45"/>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        </XCUIElementTypeAlert>
    """
    giveupChainList = [
        {
            "tag": "XCUIElementTypeAlert",
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"放弃"}
        },
    ]
    alertGiveupSoup = utils.bsChainFind(soup, giveupChainList)
    if alertGiveupSoup:
        clickCenterPosition(curSession, alertGiveupSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

# def debugJdFinancePopupIKnow(curSession):
def debugCommonPopupIKnow(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 弹框 我知道了：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="67" y="189" width="280" height="358">
                    <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="true" x="67" y="217" width="280" height="280">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="权限调用说明" name="权限调用说明" label="权限调用说明" enabled="true" visible="true" x="77" y="217" width="260" height="21"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" name="在提供服务过程中，我们可能需要调用您的以下重要设备权限，我们将在首次调用时逐项询问您是否允许使用该权限。您可以在我们询问时开启相关权限，也可以在设备系统“设置”里管理相关权限：&#10;1、相机、相册权限：向您提供扫一扫、头像设置、客服、评论或分享、人脸等图像识别服务时，您可以通过开通相机权限和/或相册权限以便进行实时拍摄和图片/视频上传。&#10;2、位置权限：基于您当前位置为您自动定位商家网点（银行、加油站等）、推荐周边服务及优惠、提供限定销售区域的金融服务时，您可以通过开启位置权限以便查看或获取当前所在区域的服务。&#10;3、通讯录权限：向您提供手机充值、转账、还款服务时，您可以选择直接从通讯录中选择并导入选定的特定联系人信息。&#10;4、日历权限：向您提供早起打卡提醒服务时，您可以通过开启日历权限便捷管理您的自定义事项、设定重要事项提醒。&#10;5、麦克风权限：向您提供语音搜索或语音客服服务时，您可以开启麦克风权限点击语音按钮进行录音，以便我们收集您的语音内容并进行必要的处理。&#10;6、面容 ID权限：向您提供面容 ID支付、面容 ID解锁服务时，您可以开启面容 ID权限并在您的设备上完成面容 ID验证，以便我们接收使用验证结果。&#10;7、蓝牙权限：向您提供手环服务时，您可以开启蓝牙权限搜索周边设备，以便您的手环能够与京东金融APP建立正常连接。&#10;&#10;更多权限信息说明，请点击查看完整版《京东金融隐私政策》。&#10;&#10;" label="在提供服务过程中，我们可能需要调用您的以下重要设备权限，我们将在首次调用时逐项询问您是否允许使用该权限。您可以在我们询问时开启相关权限，也可以在设备系统“设置”里管理相关权限：&#10;1、相机、相册权限：向您提供扫一扫、头像设置、客服、评论或分享、人脸等图像识别服务时，您可以通过开通相机权限和/或相册权限以便进行实时拍摄和图片/视频上传。&#10;2、位置权限：基于您当前位置为您自动定位商家网点（银行、加油站等）、推荐周边服务及优惠、提供限定销售区域的金融服务时，您可以通过开启位置权限以便查看或获取当前所在区域的服务。&#10;3、通讯录权限：向您提供手机充值、转账、还款服务时，您可以选择直接从通讯录中选择并导入选定的特定联系人信息。&#10;4、日历权限：向您提供早起打卡提醒服务时，您可以通过开启日历权限便捷管理您的自定义事项、设定重要事项提醒。&#10;5、麦克风权限：向您提供语音搜索或语音客服服务时，您可以开启麦克风权限点击语音按钮进行录音，以便我们收集您的语音内容并进行必要的处理。&#10;6、面容 ID权限：向您提供面容 ID支付、面容 ID解锁服务时，您可以开启面容 ID权限并在您的设备上完成面容 ID验证，以便我们接收使用验证结果。&#10;7、蓝牙权限：向您提供手环服务时，您可以开启蓝牙权限搜索周边设备，以便您的手环能够与京东金融APP建立正常连接。&#10;&#10;更多权限信息说明，请点击查看完整版《京东金融隐私政策》。&#10;&#10;" enabled="true" visible="true" x="77" y="257" width="261" height="888"/>
                    </XCUIElementTypeScrollView>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="67" y="497" width="280" height="1"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="我知道了" label="我知道了" enabled="true" visible="true" x="67" y="497" width="280" height="50"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        
        恒易贷 权限获取说明 我知道了：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="37" y="151" width="340" height="434">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="权限获取说明" name="权限获取说明" label="权限获取说明" enabled="true" visible="true" x="158" y="171" width="98" height="20"/>
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="为了给您提供优质的服务，在您借款过程中，恒易贷需要您授权开启以下权限：" name="为了给您提供优质的服务，在您借款过程中，恒易贷需要您授权开启以下权限：" label="为了给您提供优质的服务，在您借款过程中，恒易贷需要您授权开启以下权限：" enabled="true" visible="true" x="62" y="196" width="290" height="33"/>
                    <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="62" y="246" width="290" height="274">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="62" y="246" width="290" height="1"/>
                        <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="62" y="246" width="290" height="55">
                            <XCUIElementTypeImage type="XCUIElementTypeImage" name="icon_notice" enabled="true" visible="false" x="62" y="246" width="17" height="19"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="通知权限" name="通知权限" label="通知权限" enabled="true" visible="true" x="87" y="246" width="62" height="24"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="用于为您提供恒易贷或合作方的产品或活动信息" name="用于为您提供恒易贷或合作方的产品或活动信息" label="用于为您提供恒易贷或合作方的产品或活动信息" enabled="true" visible="true" x="87" y="271" width="265" height="19"/>
                        </XCUIElementTypeCell>
                        <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="62" y="300" width="290" height="73">
                            <XCUIElementTypeImage type="XCUIElementTypeImage" name="icon_location" enabled="true" visible="false" x="62" y="300" width="17" height="19"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="定位服务权限" name="定位服务权限" label="定位服务权限" enabled="true" visible="true" x="87" y="300" width="92" height="24"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="用于获取您的地理位置信息，以为您提供匹配的风险信资评估服务" name="用于获取您的地理位置信息，以为您提供匹配的风险信资评估服务" label="用于获取您的地理位置信息，以为您提供匹配的风险信资评估服务" enabled="true" visible="true" x="87" y="325" width="265" height="33"/>
                        </XCUIElementTypeCell>
                        <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="62" y="372" width="290" height="73">
                            <XCUIElementTypeImage type="XCUIElementTypeImage" name="icon_mail" enabled="true" visible="false" x="62" y="372" width="17" height="19"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="通讯录权限" name="通讯录权限" label="通讯录权限" enabled="true" visible="true" x="87" y="372" width="77" height="24"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="用于调用设备通讯录以方便您选择联系人电话号码，以辅助填写信息" name="用于调用设备通讯录以方便您选择联系人电话号码，以辅助填写信息" label="用于调用设备通讯录以方便您选择联系人电话号码，以辅助填写信息" enabled="true" visible="true" x="87" y="397" width="265" height="33"/>
                        </XCUIElementTypeCell>
                        <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="62" y="444" width="290" height="73">
                            <XCUIElementTypeImage type="XCUIElementTypeImage" name="icon_camera" enabled="true" visible="false" x="62" y="444" width="17" height="19"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="相机权限" name="相机权限" label="相机权限" enabled="true" visible="true" x="87" y="444" width="62" height="24"/>
                            <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="用于获取您的身份证信息以及脸部图像信息，以核实您身份的真实性" name="用于获取您的身份证信息以及脸部图像信息，以核实您身份的真实性" label="用于获取您的身份证信息以及脸部图像信息，以核实您身份的真实性" enabled="true" visible="true" x="87" y="469" width="265" height="33"/>
                        </XCUIElementTypeCell>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="62" y="516" width="290" height="1"/>
                    </XCUIElementTypeTable>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="我知道了" label="我知道了" enabled="true" visible="true" x="92" y="520" width="230" height="38"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    iKnowChainList = [
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
            "attrs": {"enabled":"true", "visible":"true", "name":"我知道了"}
        },
    ]
    iKnowSoup = utils.bsChainFind(soup, iKnowChainList)
    if iKnowSoup:
        clickCenterPosition(curSession, iKnowSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def wdaDebugJdFinance():

    # debugJdFinanceRightUpperJumpOver(curSession)

    # debugJdFinanceRightUpperClose(curSession)

    # debugJdFinanceNetworkNotStableRetry(curSession)

    # debugJdFinanceFullScreenImage(curSession)

    # debugJdFinanceNetworkNotStableRefresh(curSession)

    # debugJdFinanceHiIAmMaxAlertClose(curSession)

    # debugJdFinancePopupUpperRightCommonClose(curSession)

    # debugJdFinanceSystemAbnormalRetryRefresh(curSession)

    # debugJdFinanceServerBusyLaterRetry(curSession)

    # debugJdFinanceGiveupRegister(curSession)

    # debugJdFinancePopupIKnow(curSession)
    # debugCommonPopupIKnow(curSession)

    pass

if __name__ == "__main__":
    wdaDebugJdFinance()