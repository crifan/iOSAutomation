# Functon: debug iOS app common cases
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

def back_iOS(curSession):
    ScreenX = 414
    ScreenY = 736
    
    isFoundAndClicked = False
    # iOS: NO phisical back button
    # so try support following case to find and click to implement back

    backQueryList = []

    parentNaviBarClassChain = "/XCUIElementTypeNavigationBar[`rect.width = %d`]" % ScreenX

    # case 3.1: app 益路通行 左上角 返回 按钮， name中包含back
    """
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="20" width="414" height="44">
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="ic back gray" label="ic back gray" enabled="true" visible="true" x="8" y="24" width="40" height="40"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="56" y="29" width="298" height="30">
                    <XCUIElementTypeImage type="XCUIElementTypeImage" name="ic_search_gray.png" enabled="true" visible="false" x="68" y="29" width="30" height="30"/>
                    <XCUIElementTypeTextField type="XCUIElementTypeTextField" value="输入关键字查找创想" label="" enabled="true" visible="true" x="106" y="29" width="232" height="30"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="搜索" label="搜索" enabled="true" visible="true" x="358" y="29" width="46" height="30"/>
            </XCUIElementTypeOther>

            注意： 2个back 不过 back top是visible=false
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            。。。
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="20" width="414" height="44">
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="ic back white" label="ic back white" enabled="true" visible="true" x="10" y="20" width="40" height="40"/>
                </XCUIElementTypeOther>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="ic back top" label="ic back top" enabled="false" visible="true" x="396" y="614" width="58" height="54"/>

            特殊： 2个back 且都是enabled=true和visible=true
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                。。。
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="20" width="414" height="44">
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="ic back gray" label="ic back gray" enabled="true" visible="true" x="10" y="20" width="40" height="40"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="为中国乡土按下红点" name="为中国乡土按下红点" label="为中国乡土按下红点" enabled="true" visible="true" x="60" y="32" width="294" height="21"/>
                    </XCUIElementTypeOther>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="ic back top" label="ic back top" enabled="true" visible="true" x="356" y="614" width="58" height="54"/>

            必要 乳液面霜页 左上角返回按钮 name中含back：
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64">
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="64"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="icon back" label="icon back" enabled="true" visible="true" x="10" y="20" width="44" height="44"/>
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="美妆" name="美妆" label="美妆" enabled="true" visible="true" x="110" y="20" width="194" height="44"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="icon share" label="icon share" enabled="true" visible="true" x="360" y="20" width="44" height="44"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="group ic search" label="group ic search" enabled="true" visible="true" x="328" y="30" width="25" height="24"/>
                    </XCUIElementTypeOther>
    """
    NameContainBackText = "back"
    parentOtherClassChain = "/XCUIElementTypeOther[`rect.width = %d`]" % ScreenX
    backReturnQuery = {"type":"XCUIElementTypeButton", "nameContains": NameContainBackText, "enabled": "true"}
    backReturnQuery["parent_class_chains"] = [ parentOtherClassChain ]
    backQueryList.append(backReturnQuery)

    # case 6.1：京东金融 瑞幸咖啡页 图片全屏
    """
        <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="false" x="0" y="64" width="414" height="66">
            <XCUIElementTypeScrollView type="XCUIElementTypeScrollView" enabled="true" visible="false" x="0" y="64" width="414" height="66">
                <XCUIElementTypeButton type="XCUIElementTypeButton" value="1" name="头条" label="头条" enabled="true" visible="false" x="0" y="64" width="207" height="66"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="问答" label="问答" enabled="true" visible="false" x="207" y="64" width="207" height="66"/>
                <XCUIElementTypeImage type="XCUIElementTypeImage" name="/var/containers/Bundle/Application/9D6D5A0D-967F-4411-B1AE-E389C077DB8A/JDJRAppShell.app/JRHomeChannel.bundle/HC_centerSlider_tag@3x.png" enabled="true" visible="false" x="0" y="73" width="18" height="47"/>
                <XCUIElementTypeImage type="XCUIElementTypeImage" name="/var/containers/Bundle/Application/9D6D5A0D-967F-4411-B1AE-E389C077DB8A/JDJRAppShell.app/JRHomeChannel.bundle/HC_centerSlider_Refresh@3x.png" enabled="true" visible="false" x="145" y="81" width="31" height="31"/>
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="90" y="111" width="27" height="5"/>
            </XCUIElementTypeScrollView>
        </XCUIElementTypeScrollView>
    """
    FullScreenImagePartName = "centerSlider"
    parentParentScrollViewClassChain = "/XCUIElementTypeScrollView[`rect.x = 0 AND rect.width = %d`]" % ScreenX
    parentScrollViewClassChain = "/XCUIElementTypeScrollView[`rect.x = 0 AND rect.width = %d`]" % ScreenX
    fullScreenImageQuery = {"type": "XCUIElementTypeImage", "nameContains": FullScreenImagePartName, "enabled":"true", "x":"0"}
    fullScreenImageQuery["parent_class_chains"] = [ parentParentScrollViewClassChain, parentScrollViewClassChain ]
    backQueryList.append(fullScreenImageQuery)

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

    """
        善友筹 二级页面 小满 左上角返回按钮：
        <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="小满丨人生最好的状态是小满" enabled="true" visible="true" x="0" y="20" width="414" height="44">
            <XCUIElementTypeButton type="XCUIElementTypeButton" name="icon fanhui" label="icon fanhui" enabled="true" visible="true" x="20" y="24" width="35" height="36"/>
            <XCUIElementTypeOther type="XCUIElementTypeOther" name="小满丨人生最好的状态是小满" label="小满丨人生最好的状态是小满" enabled="true" visible="true" x="94" y="31" width="226" height="21"/>
        </XCUIElementTypeNavigationBar>
    """
    NaviBarFanhuiText = "fanhui"
    fanhuiButtonQuery = {"type":"XCUIElementTypeButton", "nameContains": NaviBarFanhuiText, "enabled": "true"}
    fanhuiButtonQuery["parent_class_chains"] = [ parentNaviBarClassChain ]
    backQueryList.append(fanhuiButtonQuery)

    """
        恒易贷 验证码登录页面 左上角 返回：
            <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="HYDLoginView" enabled="true" visible="true" x="0" y="20" width="414" height="44">
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="back black" label="back black" enabled="true" visible="true" x="20" y="20" width="40" height="44"/>
            </XCUIElementTypeNavigationBar>
    """
    NaviBarBackText = "back"
    naviContainBackQuery = {"type":"XCUIElementTypeButton", "nameContains": NaviBarBackText, "enabled": "true"}
    naviContainBackQuery["parent_class_chains"] = [ parentNaviBarClassChain ]
    backQueryList.append(naviContainBackQuery)

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

    # case 5: 小程序页面 左上角 返回 按钮
    """
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
    """
    MiniprogramBackButtonText = "返回"
    parentParentOtherClassChain = "/XCUIElementTypeOther[`enabled = 1 AND visible = 1 AND rect.width = %d`]" % ScreenX
    parentOtherClassChain = "/XCUIElementTypeOther[`enabled = 1 AND visible = 1`]"
    miniprogramBackButtonQuery = {"type": "XCUIElementTypeButton", "name": MiniprogramBackButtonText, "label": MiniprogramBackButtonText, "enabled":"true", "visible":"true"}
    miniprogramBackButtonQuery["parent_class_chains"] = [ parentParentOtherClassChain, parentOtherClassChain ]
    backQueryList.append(miniprogramBackButtonQuery)

    # case 6: 小程序页面 右上角 关闭 按钮
    """
        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="87" height="32">
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="320" y="24" width="88" height="32">
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="更多" label="更多" enabled="true" visible="true" x="320" y="24" width="44" height="32"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="关闭" label="关闭" enabled="true" visible="true" x="363" y="24" width="45" height="32"/>
            </XCUIElementTypeOther>
        </XCUIElementTypeOther>
    """
    MiniprogramCloseButtonText = "关闭"
    parentParentOtherClassChain = "/XCUIElementTypeOther[`enabled = 1 AND visible = 1`]"
    parentOtherClassChain = "/XCUIElementTypeOther[`enabled = 1 AND visible = 1`]"
    miniprogramCloseButtonQuery = {"type": "XCUIElementTypeButton", "name": MiniprogramCloseButtonText, "label": MiniprogramCloseButtonText, "enabled":"true", "visible":"true"}
    miniprogramCloseButtonQuery["parent_class_chains"] = [ parentParentOtherClassChain, parentOtherClassChain ]
    backQueryList.append(miniprogramCloseButtonQuery)

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

# def debugJdFinancePopupPermissionAgree(curSession):
def debugPopupCommonUserAgreementAgree(curSession):
    foundAndProcessedPopup = False
    curPageXml = crifanWda.getPageSource(gWdaClient)
    soup = utils.xmlToSoup(curPageXml)
    """
        京东金融 首次进入 协议提示 同意：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
            。。。
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="579" width="414" height="157">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" name="有关个人信息收集、使用更详细的约定请阅读《京东金融隐私政策》全文。我们承诺会不断完善安全技术和制度措施，确保您个人信息的安全。" label="有关个人信息收集、使用更详细的约定请阅读《京东金融隐私政策》全文。我们承诺会不断完善安全技术和制度措施，确保您个人信息的安全。" enabled="true" visible="true" x="16" y="595" width="382" height="59"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="不同意" label="不同意" enabled="true" visible="true" x="16" y="670" width="186" height="50"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="同意" label="同意" enabled="true" visible="true" x="212" y="670" width="186" height="50"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        
        必要 用户服务协议及必要隐私政策 同意：
            <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="38" y="163" width="338" height="410">
                    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="用户服务协议及必要隐私政策" name="用户服务协议及必要隐私政策" label="用户服务协议及必要隐私政策" enabled="true" visible="true" x="38" y="163" width="338" height="53"/>
                    <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="在您注册成为必要用户的过程中，您需要完成我们的注册流程并通过点击同意的形式在线签署以下协议，请您务必仔细阅读、充分理解协议中的条款内容后再点击同意（尤其是以粗体标识的条款，因为这些条款可能会明确您应履行的义务或对您的权利有所限制）：&#10;《用户服务协议》&#10;《必要隐私政策》&#10;【请您注意】如果您不同意上述协议或其中任何条款约定，请您停止注册。您停止注册后将仅可以浏览我们的商品信息但无法享受我们的产品或服务。如您按照注册流程提示填写信息、阅读并点击同意上述协议且完成全部注册流程后，即表示您已充分阅读、理解并接受协议的全部内容；并表明您也同意必要可以依据以上的隐私政策内容来处理您的个人信息。如您对以上协议内容有任何疑问，您可随时与必要客服联系。" enabled="true" visible="true" x="60" y="215" width="294" height="241"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="60" y="455" width="294" height="2"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="60" y="467" width="294" height="56"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="不同意" label="不同意" enabled="true" visible="true" x="38" y="518" width="169" height="55"/>
                    <XCUIElementTypeButton type="XCUIElementTypeButton" name="同意" label="同意" enabled="true" visible="true" x="206" y="518" width="170" height="55"/>
                </XCUIElementTypeOther>
            </XCUIElementTypeOther>
        
        斑马AI课 弹框 个人信息保护政策 同意：
            <XCUIElementTypeWindow type="XCUIElementTypeWindow" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="0" y="0" width="414" height="736">
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="414" height="736"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="false" x="0" y="0" width="414" height="736"/>
                    <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="47" y="148" width="320" height="440">
                        <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="个人信息保护政策" name="个人信息保护政策" label="个人信息保护政策" enabled="true" visible="true" x="47" y="173" width="320" height="23"/>
                        <XCUIElementTypeTextView type="XCUIElementTypeTextView" value="感谢您信任并使用斑马AI课的产品和服务。我们根据最新的法律法规、监管政策要求，更新了《隐私政策》，特向您推送本提示。请您仔细阅读并充分理解相关条款。&#10;斑马AI课会通过《隐私政策》帮助您了解我们手机、使用、存储个人信息的情况，以及您享有的相关权利。&#10;点击【同意】，表示您已阅读并同意相关协议条款，斑马AI课将尽全力保障您的合法权益并继续为您提供优质的产品和服务。&#10;* 您可通过阅读完整版《用户注册协议》《用户隐私协议》《儿童隐私政策》了解详尽条款内容。" enabled="true" visible="true" x="67" y="210" width="280" height="301">
                            <XCUIElementTypeLink type="XCUIElementTypeLink" name="《用户注册协议》" label="《用户注册协议》" enabled="true" visible="true" x="210" y="470" width="115" height="25"/>
                            <XCUIElementTypeLink type="XCUIElementTypeLink" name="《用户隐私协议》" label="《用户隐私协议》" enabled="true" visible="true" x="72" y="493" width="115" height="25"/>
                            <XCUIElementTypeLink type="XCUIElementTypeLink" name="《儿童隐私政策》" label="《儿童隐私政策》" enabled="true" visible="true" x="186" y="493" width="115" height="25"/>
                        </XCUIElementTypeTextView>
                        <XCUIElementTypeOther type="XCUIElementTypeOther" enabled="true" visible="true" x="47" y="525" width="320" height="2"/>
                        <XCUIElementTypeButton type="XCUIElementTypeButton" name="同意" label="同意" enabled="true" visible="true" x="77" y="540" width="260" height="34"/>
                    </XCUIElementTypeOther>
                </XCUIElementTypeOther>
            </XCUIElementTypeWindow>
    """
    commonAgreeChainList = [
        {
            "tag": "XCUIElementTypeOther",
            "attrs": {"enabled":"true", "visible":"true", "x":"0", "y":"0", "width":"%s" % ScreenX, "height":"%s" % ScreenY}
        },
        {
            "tag": "XCUIElementTypeOther",
            # "attrs": {"enabled":"true", "visible":"true", "x":"0", "width":"%s" % ScreenX}
            "attrs": {"enabled":"true", "visible":"true"}
        },
        {
            "tag": "XCUIElementTypeButton",
            "attrs": {"enabled":"true", "visible":"true", "name":"同意"}
        },
    ]
    commonAgreeSoup = utils.bsChainFind(soup, commonAgreeChainList)
    if commonAgreeSoup:
        appCrawlerCommon.clickCenterPosition(curSession, commonAgreeSoup.attrs)
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

    # debugJdFinancePopupPermissionAgree(curSession)
    debugPopupCommonUserAgreementAgree(curSession)

    pass

if __name__ == "__main__":
    wdaDebugCommon()