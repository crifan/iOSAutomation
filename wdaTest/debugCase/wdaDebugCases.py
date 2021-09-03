# Functon: debug iOS app/weixin many cases
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


def debugiOSPopupUserPrivacyProtocol(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        恒易贷 用户意思保护协议 我接收：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="用户隐私保护协议" name="用户隐私保护协议" label="用户隐私保护协议" enabled="true" visible="true" x="93" y="86" width="228" height="34"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="感谢您使用恒易贷APP！" name="感谢您使用恒易贷APP！" label="感谢您使用恒易贷APP！" enabled="true" visible="true" x="35" y="143" width="156" height="24"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="恒易贷非常重视您的隐私保护，并将使用多项安全防护措施来保护您的个人信息。请您在使用我们的服务前认真阅读本隐私政策，我们将通过本政策向您说明我们会如何收集、使用及保护您的个人信息。" name="恒易贷非常重视您的隐私保护，并将使用多项安全防护措施来保护您的个人信息。请您在使用我们的服务前认真阅读本隐私政策，我们将通过本政策向您说明我们会如何收集、使用及保护您的个人信息。" label="恒易贷非常重视您的隐私保护，并将使用多项安全防护措施来保护您的个人信息。请您在使用我们的服务前认真阅读本隐私政策，我们将通过本政策向您说明我们会如何收集、使用及保护您的个人信息。" enabled="true" visible="true" x="35" y="178" width="344" height="86"/>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" name="点击我接受即表示您已阅读并同意《用户注册协议》和《用户隐私保护协议》，请详细阅读相关条款，如有疑问可拨打95713。" label="点击我接受即表示您已阅读并同意《用户注册协议》和《用户隐私保护协议》，请详细阅读相关条款，如有疑问可拨打95713。" enabled="true" visible="true" x="35" y="275" width="344" height="59"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="我接受" label="我接受" enabled="true" visible="true" x="67" y="393" width="280" height="44"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="我拒绝" label="我拒绝" enabled="true" visible="true" x="182" y="444" width="50" height="33"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeWindow>
    """
    userPrivacyIAcceptChainList = [
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
            "attrs": {"enabled":"true", "visible":"true", "name": "我接受"}
        },
    ]
    userPrivacyIAcceptSoup = utils.bsChainFind(soup, userPrivacyIAcceptChainList)
    if userPrivacyIAcceptSoup:
        clickCenterPosition(curSession, userPrivacyIAcceptSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup


def debugElementNotFoundApplyLoan(curSession):
    # Not found element {'value': '可申请(元) 200,000', 'name': '可申请(元) 200,000', 'label': '可申请(元) 200,000', 'enabled': 'true', 'x': '85', 'y': '226', 'width': '244', 'height': '102', 'type': 'XCUIElementTypeStaticText'}
    # applyLoanQuery = {'value': '可申请(元) 200,000', 'name': '可申请(元) 200,000', 'label': '可申请(元) 200,000', 'enabled': 'true', 'x': '85', 'y': '226', 'width': '244', 'height': '102', 'type': 'XCUIElementTypeStaticText'}
    # applyLoanQuery = {'value': '可申请(元) 200,000', 'name': '可申请(元) 200,000', 'label': '可申请(元) 200,000', 'enabled': 'true', 'x': '85', 'width': '244', 'height': '102', 'type': 'XCUIElementTypeStaticText'}
    applyLoanQuery = {'enabled': 'true', 'x': '85', 'y': '226', 'width': '244', 'height': '102', 'type': 'XCUIElementTypeStaticText'}
    isFound, respInfo = findElement(curSession, applyLoanQuery)
    print("isFound=%s, respInfo=%s" % (isFound, respInfo))

def debugiOSNaviNameContainBackButton(curSession):
    """恒易贷 验证码登录 左上角 返回 name中有back """
    back_iOS(curSession)


def debugiOSPopupUseWirelessData(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        恒易贷 允许使用无线数据 无线局域网与蜂窝移动网络：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="允许“恒易贷”使用无线数据？" label="允许“恒易贷”使用无线数据？" enabled="true" visible="true" x="72" y="253" width="270" height="230">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="253" width="270" height="230">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="253" width="270" height="230">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="253" width="270" height="230">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="253" width="270" height="230"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="253" width="270" height="230">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="253" width="270" height="230"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="253" width="270" height="230"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="253" width="270" height="230">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="253" width="270" height="97">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="253" width="270" height="97">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="允许“恒易贷”使用无线数据？" name="允许“恒易贷”使用无线数据？" label="允许“恒易贷”使用无线数据？" enabled="true" visible="true" x="88" y="273" width="238" height="21"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="关闭无线数据时，部分功能可能无法使用。" name="关闭无线数据时，部分功能可能无法使用。" label="关闭无线数据时，部分功能可能无法使用。" enabled="true" visible="true" x="88" y="297" width="238" height="32"/>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="349" width="270" height="1">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="349" width="270" height="1"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="349" width="270" height="1"/>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="350" width="270" height="133">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="350" width="270" height="133">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="350" width="270" height="133">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="350" width="270" height="44">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="无线局域网与蜂窝移动网络" label="无线局域网与蜂窝移动网络" enabled="true" visible="true" x="72" y="350" width="270" height="44"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="1">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="394" width="270" height="1"/>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="1"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="仅限无线局域网" label="仅限无线局域网" enabled="true" visible="true" x="72" y="394" width="270" height="45"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="438" width="270" height="1">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="438" width="270" height="1"/>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="438" width="270" height="1"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="438" width="270" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="不允许" label="不允许" enabled="true" visible="true" x="72" y="438" width="270" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>
    """
    wifiCellularChainList = [
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
            "attrs": {"enabled":"true", "visible":"true", "name": "无线局域网与蜂窝移动网络"}
        },
    ]
    wifiCellularSoup = utils.bsChainFind(soup, wifiCellularChainList)
    if wifiCellularSoup:
        clickCenterPosition(curSession, wifiCellularSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

# def debugiOSPopupAlertCommonAlwaysAllow(curSession):
def debugiOSPopupCommonAllow(curSession):
    ScreenX = 414
    ScreenY = 736
    foundAndProcessedPopup = False
    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 弹框 想给您发送信息 允许：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="“京东金融”想给您发送通知" label="“京东金融”想给您发送通知" enabled="true" visible="true" x="72" y="298" width="270" height="141">
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
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="“京东金融”想给您发送通知" name="“京东金融”想给您发送通知" label="“京东金融”想给您发送通知" enabled="true" visible="true" x="88" y="317" width="238" height="21"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="“通知”可能包括提醒、声音和图标标记。这些可在“设置”中配置。" name="“通知”可能包括提醒、声音和图标标记。这些可在“设置”中配置。" label="“通知”可能包括提醒、声音和图标标记。这些可在“设置”中配置。" enabled="true" visible="true" x="88" y="341" width="238" height="33"/>
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
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="允许" label="允许" enabled="true" visible="true" x="207" y="394" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>

        京东金融 弹框 允许在您并未使用该应用时访问您的位置吗？仅在使用应用期间 始终允许：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="允许“京东金融”在您并未使用该应用时访问您的位置吗？" label="允许“京东金融”在您并未使用该应用时访问您的位置吗？" enabled="true" visible="true" x="72" y="224" width="270" height="288">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="224" width="270" height="288">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="224" width="270" height="288">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="224" width="270" height="288">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="224" width="270" height="288"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="224" width="270" height="288">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="224" width="270" height="288"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="224" width="270" height="288"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="224" width="270" height="288">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="224" width="270" height="199">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="224" width="270" height="199">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="允许“京东金融”在您并未使用该应用时访问您的位置吗？" name="允许“京东金融”在您并未使用该应用时访问您的位置吗？" label="允许“京东金融”在您并未使用该应用时访问您的位置吗？" enabled="true" visible="true" x="88" y="244" width="238" height="43"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="为了基于您当前所在位置更精准地为您推荐附近的优惠、提供周边商家搜索服务、提供限定销售区域的金融产品，请您允许京东金融使用位置权限。我们仅定位您当前所处的位置，不会追踪您的行踪轨迹。您可以在设置页面取消位置授权。" name="为了基于您当前所在位置更精准地为您推荐附近的优惠、提供周边商家搜索服务、提供限定销售区域的金融产品，请您允许京东金融使用位置权限。我们仅定位您当前所处的位置，不会追踪您的行踪轨迹。您可以在设置页面取消位置授权。" label="为了基于您当前所在位置更精准地为您推荐附近的优惠、提供周边商家搜索服务、提供限定销售区域的金融产品，请您允许京东金融使用位置权限。我们仅定位您当前所处的位置，不会追踪您的行踪轨迹。您可以在设置页面取消位置授权。" enabled="true" visible="true" x="88" y="290" width="238" height="112"/>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="422" width="270" height="1">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="422" width="270" height="1"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="422" width="270" height="1"/>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="423" width="270" height="89">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="423" width="270" height="89">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="423" width="270" height="89">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="423" width="270" height="44">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="仅在使用应用期间" label="仅在使用应用期间" enabled="true" visible="true" x="72" y="423" width="270" height="44"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="467" width="270" height="1">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="467" width="270" height="1"/>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="467" width="270" height="1"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="467" width="270" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="始终允许" label="始终允许" enabled="true" visible="true" x="72" y="467" width="270" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>

        恒易贷 想给您发送通知 允许：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="“恒易贷”想给您发送通知" label="“恒易贷”想给您发送通知" enabled="true" visible="true" x="72" y="298" width="270" height="141">
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
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="“恒易贷”想给您发送通知" name="“恒易贷”想给您发送通知" label="“恒易贷”想给您发送通知" enabled="true" visible="true" x="88" y="317" width="238" height="21"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="“通知”可能包括提醒、声音和图标标记。这些可在“设置”中配置。" name="“通知”可能包括提醒、声音和图标标记。这些可在“设置”中配置。" label="“通知”可能包括提醒、声音和图标标记。这些可在“设置”中配置。" enabled="true" visible="true" x="88" y="341" width="238" height="33"/>
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
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="允许" label="允许" enabled="true" visible="true" x="207" y="394" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>
    """
    # allowP = re.compile("(始终)?允许") # will also match "不允许"
    allowP = re.compile("^(始终)?允许$") # only match "允许" "始终允许"
    allowChainList = [
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
            # "attrs": {"enabled":"true", "visible":"true", "name":"允许"}
            "attrs": {"enabled":"true", "visible":"true", "name": allowP}
        },
    ]
    allowSoup = utils.bsChainFind(soup, allowChainList)
    if allowSoup:
        # clickCenterPosition(curSession, allowSoup.attrs)
        # foundAndProcessedPopup = True

        # above click position not work for 允许 -> actually click 不允许 !!!
        # change to use wda to find 允许 then click element
        curName = allowSoup.attrs["name"] # 允许 / 始终允许
        # allowButtonQuery = {"type":"XCUIElementTypeButton", "enabled":"true", "name": "允许"}
        allowButtonQuery = {"type":"XCUIElementTypeButton", "enabled":"true", "name": curName}
        foundAndClicked = findAndClickElement(curSession, allowButtonQuery)
        foundAndProcessedPopup = foundAndClicked

    return foundAndProcessedPopup

def debugiOSBackButton(curSession):
    """益路通行 左上角 返回 name中有 back"""
    back_iOS(curSession)

def debugiOSPopupQuit(curSession):
    """
        益路通行 弹框 您是否要退出登录：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="414" height="736"/>
                <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="您是否要退出登录？" label="您是否要退出登录？" enabled="true" visible="true" x="72" y="316" width="270" height="105">
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
                                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="您是否要退出登录？" name="您是否要退出登录？" label="您是否要退出登录？" enabled="true" visible="true" x="88" y="335" width="238" height="21"/>
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
                                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="72" y="376" width="135" height="45"/>
                                            </XCUIElementTypeOther>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="1" height="45">
                                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="207" y="376" width="1" height="45"/>
                                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="1" height="45"/>
                                            </XCUIElementTypeOther>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="135" height="45">
                                                <XCUIElementTypeButton type="XCUIElementTypeButton" name="退出" label="退出" enabled="true" visible="true" x="207" y="376" width="135" height="45"/>
                                            </XCUIElementTypeOther>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeAlert>
    """
    ScreenX = 414
    ScreenY = 736

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False
    alertCancelChainList = [
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
            "attrs": {"enabled":"true", "visible":"true", "name":"取消"}
        },
    ]
    alertCancelSoup = utils.bsChainFind(soup, alertCancelChainList)
    if alertCancelSoup:
        clickCenterPosition(curSession, alertCancelSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup

def debugBack_Syc(curSession):
    """善友筹 左上角 返回"""
    back_iOS(curSession)


def debugiOSPopupCallPhone(curSession):
    """
        iOS 通用弹框 呼叫 打电话：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="‭400 186 6078‬" label="‭400 186 6078‬" enabled="true" visible="true" x="72" y="316" width="270" height="105">
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
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="‭400 186 6078‬" name="‭400 186 6078‬" label="‭400 186 6078‬" enabled="true" visible="true" x="88" y="335" width="238" height="21"/>
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
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="72" y="376" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="1" height="45">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="207" y="376" width="1" height="45"/>
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="1" height="45"/>
                                        </XCUIElementTypeOther>
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="207" y="376" width="135" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="呼叫" label="呼叫" enabled="true" visible="true" x="207" y="376" width="135" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>
    """

    # # for debug click positon of 取消 why not work
    # # centerX = 139
    # centerX = 72 + 10
    # while True:
    #     # centerX -= 10

    #     centerY = 398
    #     curSession.click(centerX, centerY)

    ScreenX = 414
    ScreenY = 736

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False
    callChainList = [
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
            "attrs": {"enabled":"true", "visible":"true", "name":"呼叫"}
        },
    ]
    callSoup = utils.bsChainFind(soup, callChainList)
    if callSoup:
        # parentOtherSoup = callSoup.parent
        # if parentOtherSoup:
        #     parentParentOtherSoup = parentOtherSoup.parent
        #     if parentParentOtherSoup:
        #         cancelSoup = parentParentOtherSoup.find(
        #             "XCUIElementTypeButton",
        #             attrs={"enabled":"true", "visible":"true", "name": "取消"}
        #         )
        #         if cancelSoup:
        #             clickCenterPosition(curSession, cancelSoup.attrs)
        #             foundAndProcessedPopup = True

        # above click position not work for 取消 !!!
        # change to find 取消 then click element

        cancelButtonQuery = {"type":"XCUIElementTypeButton", "enabled":"true", "visible":"true", "name": "取消"}
        foundAndClicked = findAndClickElement(curSession, cancelButtonQuery)
        foundAndProcessedPopup = foundAndClicked

    return foundAndProcessedPopup


def findPopupTopFrameElement(topOtherSoup):
    """
    寻找符合条件的子节点，即当前节点向下找，符合一直是
        type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736"
        且层数 >= 3，然后再找其下一个 非x=0 y=0的节点
            很可能就是 弹框的主体元素
    """
    popupTopFrameElement = None

    MaxFullScreenSizeLevel = 3

    ScreenX = 414
    ScreenY = 736

    FullScreenAttr = {"type": "XCUIElementTypeOther", "enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}

    curFullScreenOtherLevel = 0
    curSoup = topOtherSoup
    while True:
        subOtherSoupList = curSoup.find_all(
            "XCUIElementTypeOther",
            attrs=FullScreenAttr,
            recursive=False,
        )

        if not subOtherSoupList:
            break

        # only have one child
        childOtherSoupNum = len(subOtherSoupList)
        if childOtherSoupNum != 1:
            break

        firstOnlyOtherSoup = subOtherSoupList[0]
        if not firstOnlyOtherSoup:
            break

        if not hasattr(firstOnlyOtherSoup, "attrs"):
            break

        curAttrDict = firstOnlyOtherSoup.attrs

        allAttrSame = True
        for eachToCompareKey in FullScreenAttr.keys():
            eachToCompareValue = FullScreenAttr[eachToCompareKey]
            curValue = curAttrDict.get(eachToCompareKey)
            if curValue != eachToCompareValue:
                allAttrSame = False
                break
        
        if not allAttrSame:
            break

        curSoup = firstOnlyOtherSoup

        curFullScreenOtherLevel += 1

    if curFullScreenOtherLevel >= MaxFullScreenSizeLevel:
        curChildOtherList = curSoup.find_all(
            "XCUIElementTypeOther",
            attrs={"type": "XCUIElementTypeOther", "enabled":"true", "visible":"true"},
            recursive=False,
        )
        if curChildOtherList:
            curChildOtherNum = len(curChildOtherList)
            if curChildOtherNum == 1:
                popupTopFrameElement = curChildOtherList[0]

    return popupTopFrameElement

def debugiOSPopupWindowUpperRightClose(curSession):
    """
    弹框中找 外层Other内部的 非x=0 y=0的元素，则为弹框区域 计算出其右上角的区域，点击 尝试关闭 弹框
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" name="姜老师 姜老师已经帮助超过800多名患者发起了筹款，经验丰富。关于筹款的问题您都可以找她咨询。 gongyiwuyouchou 一键复制老师微信 添加老师微信，专享1对1细致服务，立即开始咨询吧！" label="姜老师 姜老师已经帮助超过800多名患者发起了筹款，经验丰富。关于筹款的问题您都可以找她咨询。 gongyiwuyouchou 一键复制老师微信 添加老师微信，专享1对1细致服务，立即开始咨询吧！" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" name="姜老师 姜老师已经帮助超过800多名患者发起了筹款，经验丰富。关于筹款的问题您都可以找她咨询。 gongyiwuyouchou 一键复制老师微信 添加老师微信，专享1对1细致服务，立即开始咨询吧！" label="姜老师 姜老师已经帮助超过800多名患者发起了筹款，经验丰富。关于筹款的问题您都可以找她咨询。 gongyiwuyouchou 一键复制老师微信 添加老师微信，专享1对1细致服务，立即开始咨询吧！" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" name="姜老师 姜老师已经帮助超过800多名患者发起了筹款，经验丰富。关于筹款的问题您都可以找她咨询。 gongyiwuyouchou 一键复制老师微信 添加老师微信，专享1对1细致服务，立即开始咨询吧！" label="姜老师 姜老师已经帮助超过800多名患者发起了筹款，经验丰富。关于筹款的问题您都可以找她咨询。 gongyiwuyouchou 一键复制老师微信 添加老师微信，专享1对1细致服务，立即开始咨询吧！" enabled="true" visible="true" x="20" y="200" width="374" height="263">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="20" y="200" width="374" height="36"/>
            。。。
    """
    ScreenX = 414
    ScreenY = 736

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False
    allTopOtherSoupList = soup.find_all(
        "XCUIElementTypeOther",
        attrs={"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
    )
    for eachTopOtherSoup in allTopOtherSoupList:
        popupTopOtherSoup = findPopupTopFrameElement(eachTopOtherSoup)
        if popupTopOtherSoup:
            curAttrsDict = popupTopOtherSoup.attrs
            curX = int(curAttrsDict["x"])
            curY = int(curAttrsDict["y"])
            curWidth = int(curAttrsDict["width"])
            curHeight = int(curAttrsDict["height"])
            curX1 = curX + curWidth
            curY1 = curY + curHeight
            PossibleCloseButtonWidth = 40
            PossibleCloseButtonHeight = 40
            possibleCloseButtonX0 = curX1 - PossibleCloseButtonWidth
            # possibleCloseButtonY0 = curY + PossibleCloseButtonHeight
            possibleCloseButtonY0 = curY
            possibleCloseButtonX1 = curX1
            possibleCloseButtonY1 = curY + PossibleCloseButtonHeight
            # possibleCloseButtonCenterX = possibleCloseButtonX0 + int(PossibleCloseButtonWidth / 2)
            # possibleCloseButtonCenterY = possibleCloseButtonY0 + int(PossibleCloseButtonHeight / 2)
            possibleCloseButtonCenterX = int( (possibleCloseButtonX0 + possibleCloseButtonX1) / 2)
            possibleCloseButtonCenterY = int( (possibleCloseButtonY0 + possibleCloseButtonY1) / 2)
            curSession.click(possibleCloseButtonCenterX, possibleCloseButtonCenterY)
        break

def debugiOSPopupPhotoCamera(curSession):
    """
        系统弹框 拍照或录像：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="8" y="530" width="398" height="133">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="8" y="530" width="398" height="133">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="8" y="530" width="398" height="133">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="398" height="133">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="398" height="133">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="398" height="133">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="398" height="133">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="398" height="133">
                                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="398" height="133">
                                                <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true" x="0" y="0" width="398" height="133">
                                                    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="0" width="398" height="45">
                                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="43" width="398" height="2"/>
                                                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="13" y="6" width="1" height="32"/>
                                                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="拍照或录像" name="拍照或录像" label="拍照或录像" enabled="true" visible="true" x="15" y="11" width="87" height="22"/>
                                                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="351" y="6" width="32" height="32"/>
                                                    </XCUIElementTypeCell>
                                                    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="44" width="398" height="45">
                                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="88" width="398" height="1"/>
                                                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="13" y="50" width="1" height="33"/>
                                                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="照片图库" name="照片图库" label="照片图库" enabled="true" visible="true" x="15" y="56" width="70" height="21"/>
                                                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="351" y="50" width="32" height="33"/>
                                                    </XCUIElementTypeCell>
                                                    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true" x="0" y="88" width="398" height="45">
                                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="132" width="398" height="1"/>
                                                        <XCUIElementTypeImage type="XCUIElementTypeImage" enabled="true" visible="false" x="13" y="94" width="1" height="33"/>
                                                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="浏览" name="浏览" label="浏览" enabled="true" visible="true" x="14" y="100" width="36" height="21"/>
                                                        <XCUIElementTypeImage type="XCUIElementTypeImage" name="UIDocumentPicker-more" enabled="true" visible="false" x="351" y="94" width="32" height="33"/>
                                                    </XCUIElementTypeCell>
                                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="132" width="398" height="1"/>
                                                </XCUIElementTypeTable>
                                            </XCUIElementTypeOther>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="8" y="671" width="398" height="57">
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="取消" label="取消" enabled="true" visible="true" x="8" y="671" width="398" height="57"/>
            </XCUIElementTypeOther>
    """
    ScreenX = 414
    ScreenY = 736

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False
    photoCameraChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeTable",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0"}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"enabled":"true", "visible":"true", "value":"拍照或录像"}
        },
    ]
    photoCameraSoup = utils.bsChainFind(soup, photoCameraChainList)
    if photoCameraSoup:
        parentOtherSoup = None
        # find parent
        parentLevelNum = 11
        curParentSoup = photoCameraSoup
        for curLevelIdx in range(parentLevelNum):
            curParentSoup = curParentSoup.parent
            if not curParentSoup:
                break
        if curParentSoup:
            parentOtherSoup = curParentSoup
            nextSiblingList = parentOtherSoup.next_siblings
            if nextSiblingList:
                nextOtherSoup = None
                for eachNextSibling in nextSiblingList:
                    if hasattr(eachNextSibling, "attrs"):
                        curType = eachNextSibling.attrs["type"]
                        if curType == "XCUIElementTypeOther":
                            # next sibling's first XCUIElementTypeOther
                            nextOtherSoup = eachNextSibling
                            break

            if nextOtherSoup:
                cancelSoup = nextOtherSoup.find(
                    "XCUIElementTypeButton",
                    attrs={"visible":"true", "enabled":"true", "name": "取消"}
                )
                if cancelSoup:
                    clickCenterPosition(curSession, cancelSoup.attrs)
                    foundAndProcessedPopup = True

    return foundAndProcessedPopup

def debugKagsPopupNoteIdInfoNotComplete(curSession):
    """
    康爱公社 弹框 提醒 您的身份信息不完整 确定：
        <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="提醒" label="提醒" enabled="true" visible="true" x="72" y="298" width="270" height="141">
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
                                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="提醒" name="提醒" label="提醒" enabled="true" visible="true" x="88" y="317" width="238" height="21"/>
                                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="您的身份信息不完整，请检查身份证信息及手机号是否完善" name="您的身份信息不完整，请检查身份证信息及手机号是否完善" label="您的身份信息不完整，请检查身份证信息及手机号是否完善" enabled="true" visible="true" x="88" y="341" width="238" height="33"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="1">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="394" width="270" height="1"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="1"/>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="394" width="270" height="45">
                                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="72" y="394" width="270" height="45"/>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        </XCUIElementTypeAlert>

        康爱公社 弹框 提示 请登录后再进行操作：
            <XCUIElementTypeAlert type="XCUIElementTypeAlert" name="提示" label="提示" enabled="true" visible="true" x="72" y="306" width="270" height="125">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="306" width="270" height="125">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="306" width="270" height="125">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="306" width="270" height="125">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="306" width="270" height="125"/>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="306" width="270" height="125">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="306" width="270" height="125"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="306" width="270" height="125"/>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="306" width="270" height="125">
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="306" width="270" height="80">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="306" width="270" height="80">
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="提示" name="提示" label="提示" enabled="true" visible="true" x="88" y="325" width="238" height="21"/>
                                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="请登录后再进行操作" name="请登录后再进行操作" label="请登录后再进行操作" enabled="true" visible="true" x="88" y="349" width="238" height="17"/>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="386" width="270" height="1">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="72" y="386" width="270" height="1"/>
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="386" width="270" height="1"/>
                            </XCUIElementTypeOther>
                            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="386" width="270" height="45">
                                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="386" width="270" height="45">
                                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="386" width="270" height="45">
                                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="72" y="386" width="270" height="45">
                                            <XCUIElementTypeButton type="XCUIElementTypeButton" name="确定" label="确定" enabled="true" visible="true" x="72" y="386" width="270" height="45"/>
                                        </XCUIElementTypeOther>
                                    </XCUIElementTypeOther>
                                </XCUIElementTypeOther>
                            </XCUIElementTypeOther>
                        </XCUIElementTypeOther>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeAlert>

    """
    ScreenX = 414
    ScreenY = 736

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False
    alertConfirmChainList = [
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
            "attrs": {"enabled":"true", "visible":"true", "name":"确定"}
        },
    ]
    alertConfirmSoup = utils.bsChainFind(soup, alertConfirmChainList)
    if alertConfirmSoup:
        clickCenterPosition(curSession, alertConfirmSoup.attrs)
        foundAndProcessedPopup = True
    return foundAndProcessedPopup


def debugKagsPopupStillNotLogin(curSession):
    ScreenX = 414
    ScreenY = 736

    curPageXml = getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    foundAndProcessedPopup = False
    """
        康爱公社 弹框 您还未登录：
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="pages/home1/home1[2]" label="pages/home1/home1[2]" enabled="true" visible="false" x="0" y="0" width="414" height="2707">
            。。。
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="135" y="373" width="144" height="30">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="您还未登录" name="您还未登录" label="您还未登录" enabled="true" visible="true" x="146" y="373" width="122" height="30"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="135" y="400" width="144" height="44">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="请先登录后再进行操作" name="请先登录后再进行操作" label="请先登录后再进行操作" enabled="true" visible="true" x="135" y="420" width="144" height="19"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="112" y="473" width="70" height="22">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="暂不登录" name="暂不登录" label="暂不登录" enabled="true" visible="true" x="112" y="473" width="70" height="22"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="232" y="473" width="70" height="22">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="立即登录" name="立即登录" label="立即登录" enabled="true" visible="true" x="232" y="473" width="70" height="22"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
    """
    stillNotLoginChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "x":"0", "width": "%s" % ScreenX}
        },
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"visible":"true", "enabled":"true"}
        },
        {
            "tag": "XCUIElementTypeStaticText",
            "attrs": {"visible":"true", "enabled":"true", "value":"您还未登录"}
        },
    ]
    stillNotLoginSoup = utils.bsChainFind(soup, stillNotLoginChainList)
    if stillNotLoginSoup:
        parentOtherSoup = stillNotLoginSoup.parent
        parentParentOtherSoup = parentOtherSoup.parent
        if parentParentOtherSoup:
            tempNotLoginSoup = parentParentOtherSoup.find(
                "XCUIElementTypeStaticText",
                attrs={"visible":"true", "enabled":"true", "value": "暂不登录"}
            )
            if tempNotLoginSoup:
                clickCenterPosition(curSession, tempNotLoginSoup.attrs)
                foundAndProcessedPopup = True
    return foundAndProcessedPopup

def wdaDebugCases():

    # debugKagsPopupStillNotLogin(curSession)

    # debugKagsPopupNoteIdInfoNotComplete(curSession)
    
    # debugiOSPopupPhotoCamera(curSession)

    # debugiOSPopupWindowUpperRightClose(curSession)

    # debugiOSPopupCallPhone(curSession)

    # debugBack_Syc(curSession)
    
    # debugiOSPopupQuit(curSession)

    # debugiOSBackButton(curSession)

    # debugiOSPopupAlertCommonAlwaysAllow(curSession)
    # debugiOSPopupCommonAllow(curSession)

    # debugiOSPopupUseWirelessData(curSession)

    # debugiOSPopupUserPrivacyProtocol(curSession)

    # debugCommonPopupAccessContactOK(curSession)

    # debugElementNotFoundApplyLoan(curSession)

    # debugiOSNaviNameContainBackButton(curSession)

    pass

if __name__ == "__main__":
    wdaDebugCases()