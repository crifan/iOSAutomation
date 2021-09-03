import os
import sys
import io
import re
import codecs
import json
import time
from datetime import datetime,timedelta

from PIL import Image, ImageDraw
cfgDefaultImageResample = Image.BICUBIC # Image.LANCZOS

from bs4 import BeautifulSoup


################################################################################
# Config & Const
################################################################################


################################################################################
# Global Variable
################################################################################

gVal = {
    'calTimeKeyDict': {}
}


################################################################################
# Utils
################################################################################


#-------------------------------------------------------------------------------
# File
#-------------------------------------------------------------------------------

def saveTextToFile(fullFilename, text, fileEncoding="utf-8"):
    """save text content into file"""
    with codecs.open(fullFilename, 'w', encoding=fileEncoding) as fp:
        fp.write(text)
        fp.close()

def saveJsonToFile(fullFilename, jsonValue, indent=2, fileEncoding="utf-8"):
    """
        save json dict into file
        for non-ascii string, output encoded string, without \\u xxxx
    """
    with codecs.open(fullFilename, 'w', encoding=fileEncoding) as jsonFp:
        json.dump(jsonValue, jsonFp, indent=indent, ensure_ascii=False)
        # logging.debug("Complete save json %s", fullFilename)

def loadTextFromFile(fullFilename, fileEncoding="utf-8"):
    """load file text content from file"""
    with codecs.open(fullFilename, 'r', encoding=fileEncoding) as fp:
        allText = fp.read()
        # logging.debug("Complete load text from %s", fullFilename)
        return allText

def findNextNumberFilename(curFilename):
    """Find the next available filename from current name

    Args:
        curFilename (str): current filename
    Returns:
        next available (not existed) filename
    Raises:
    Examples:
        (1) 'crifanLib/demo/input/image/20201219_172616_drawRect_40x40.jpg'
            not exist -> 'crifanLib/demo/input/image/20201219_172616_drawRect_40x40.jpg'
        (2) 'crifanLib/demo/input/image/20191219_172616_drawRect_40x40.jpg'
            exsit -> next until not exist 'crifanLib/demo/input/image/20191219_172616_drawRect_40x40_3.jpg'
    """
    newFilename = curFilename

    newPathRootPart, pointSuffix = os.path.splitext(newFilename)
    # 'crifanLib/demo/input/image/20191219_172616_drawRect_40x40_1'
    filenamePrefix = newPathRootPart
    while os.path.exists(newFilename):
        newTailNumberInt = 1
        foundTailNumber = re.search("^(?P<filenamePrefix>.+)_(?P<tailNumber>\d+)$", newPathRootPart)
        if foundTailNumber:
            tailNumberStr = foundTailNumber.group("tailNumber") # '1'
            tailNumberInt = int(tailNumberStr)
            newTailNumberInt = tailNumberInt + 1 # 2
            filenamePrefix = foundTailNumber.group("filenamePrefix") # 'crifanLib/demo/input/image/20191219_172616_drawRect_40x40'
        # existed previously saved, change to new name
        newPathRootPart = "%s_%s" % (filenamePrefix, newTailNumberInt)
        # 'crifanLib/demo/input/image/20191219_172616_drawRect_40x40_2'
        newFilename = newPathRootPart + pointSuffix
        # 'crifanLib/demo/input/image/20191219_172616_drawRect_40x40_2.jpg'

    return newFilename

def isFileObject(fileObj):
    """"check is file like object or not"""
    if sys.version_info[0] == 2:
        return isinstance(fileObj, file)
    else:
        # for python 3:
        # has read() method for:
        # io.IOBase
        # io.BytesIO
        # io.StringIO
        # io.RawIOBase
        return hasattr(fileObj, 'read')

#-------------------------------------------------------------------------------
# Media - Image
#-------------------------------------------------------------------------------

def resizeImage(inputImage,
                newSize,
                resample=cfgDefaultImageResample,
                outputFormat=None,
                outputImageFile=None
                ):
    """
        resize input image
        resize normally means become smaller, reduce size
    :param inputImage: image file object(fp) / filename / binary bytes
    :param newSize: (width, height)
    :param resample: PIL.Image.NEAREST, PIL.Image.BILINEAR, PIL.Image.BICUBIC, or PIL.Image.LANCZOS
        https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.thumbnail
    :param outputFormat: PNG/JPEG/BMP/GIF/TIFF/WebP/..., more refer:
        https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
        if input image is filename with suffix, can omit this -> will infer from filename suffix
    :param outputImageFile: output image file filename
    :return:
        input image file filename: output resized image to outputImageFile
        input image binary bytes: resized image binary bytes
    """
    openableImage = None
    if isinstance(inputImage, str):
        openableImage = inputImage
    elif isFileObject(inputImage):
        openableImage = inputImage
    elif isinstance(inputImage, bytes):
        inputImageLen = len(inputImage)
        openableImage = io.BytesIO(inputImage)

    if openableImage:
        imageFile = Image.open(openableImage)
    elif isinstance(inputImage, Image.Image):
        imageFile = inputImage
    # <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=3543x3543 at 0x1065F7A20>
    imageFile.thumbnail(newSize, resample)
    if outputImageFile:
        # save to file
        imageFile.save(outputImageFile)
        imageFile.close()
    else:
        # save and return binary byte
        imageOutput = io.BytesIO()
        # imageFile.save(imageOutput)
        outputImageFormat = None
        if outputFormat:
            outputImageFormat = outputFormat
        elif imageFile.format:
            outputImageFormat = imageFile.format
        imageFile.save(imageOutput, outputImageFormat)
        imageFile.close()
        compressedImageBytes = imageOutput.getvalue()
        compressedImageLen = len(compressedImageBytes)
        compressRatio = float(compressedImageLen)/float(inputImageLen)
        print("%s -> %s, resize ratio: %d%%" % (inputImageLen, compressedImageLen, int(compressRatio * 100)))
        return compressedImageBytes

def imageDrawRectangle(inputImgOrImgPath,
    rectLocation,
    outlineColor="green",
    outlineWidth=0,
    isShow=False,
    isAutoSave=True,
    saveTail="_drawRect_%wx%h",
    isDrawClickedPosCircle=True,
    clickedPos=None,
):
    """Draw a rectangle for image (and a small circle), and show it,

    Args:
        inputImgOrImgPath (Image/str): a pillow(PIL) Image instance or image file path
        rectLocation (tuple/list/Rect): the rectangle location, (x, y, width, height)
        outlineColor (str): Color name
        outlineWidth (int): rectangle outline width
        isShow (bool): True to call image.show() for debug
        isAutoSave (bool): True to auto save the image file with drawed rectangle
        saveTail(str): save filename tail part. support format %x/%y/%w/%h use only when isAutoSave=True
        clickedPos (tuple): x,y of clicked postion; default None; if None, use the center point
        isDrawClickedPosCircle (bool): draw small circle in clicked point
    Returns:
        modified image
    Raises:
    """
    inputImg = inputImgOrImgPath
    if isinstance(inputImgOrImgPath, str):
        inputImg = Image.open(inputImgOrImgPath)
    draw = ImageDraw.Draw(inputImg)

    isRectObj = False
    hasX = hasattr(rectLocation, "x")
    hasY = hasattr(rectLocation, "y")
    hasWidth = hasattr(rectLocation, "width")
    hasHeight = hasattr(rectLocation, "height")
    isRectObj = hasX and hasY and hasWidth and hasHeight
    if isinstance(rectLocation, tuple):
        x, y, w, h = rectLocation
    if isinstance(rectLocation, list):
        x = rectLocation[0]
        y = rectLocation[1]
        w = rectLocation[2]
        h = rectLocation[3]
    elif isRectObj:
        x = rectLocation.x
        y = rectLocation.y
        w = rectLocation.width
        h = rectLocation.height

    w = int(w)
    h = int(h)

    x0 = x
    y0 = y
    x1 = x0 + w
    y1 = y0 + h
    draw.rectangle(
        [x0, y0, x1, y1],
        # fill="yellow",
        # outline="yellow",
        outline=outlineColor,
        width=outlineWidth,
    )

    if isDrawClickedPosCircle:
        # radius = 3
        # radius = 2
        radius = 4
        # circleOutline = "yellow"
        circleOutline = "red"
        circleLineWidthInt = 1
        # circleLineWidthInt = 3

        if clickedPos:
            clickedX, clickedY = clickedPos
        else:
            clickedX = x + w/2
            clickedY = y + h/2
        startPointInt = (int(clickedX - radius), int(clickedY - radius))
        endPointInt = (int(clickedX + radius), int(clickedY + radius))
        draw.ellipse([startPointInt, endPointInt], outline=circleOutline, width=circleLineWidthInt)

    if isShow:
        inputImg.show()

    if isAutoSave:
        saveTail = saveTail.replace("%x", str(x))
        saveTail = saveTail.replace("%y", str(y))
        saveTail = saveTail.replace("%w", str(w))
        saveTail = saveTail.replace("%h", str(h))

        inputImgPath = None
        if isinstance(inputImgOrImgPath, str):
            inputImgPath = str(inputImgOrImgPath)
        elif inputImg.filename:
            inputImgPath = str(inputImg.filename)

        if inputImgPath:
            imgFolderAndName, pointSuffix = os.path.splitext(inputImgPath)
            imgFolderAndName = imgFolderAndName + saveTail
            newImgPath = imgFolderAndName + pointSuffix
            newImgPath = findNextNumberFilename(newImgPath)
        else:
            curDatetimeStr = getCurDatetimeStr() # '20191219_143400'
            suffix = str(inputImg.format).lower() # 'jpeg'
            newImgFilename = "%s%s.%s" % (curDatetimeStr, saveTail, suffix)
            imgPathRoot = os.getcwd()
            newImgPath = os.path.join(imgPathRoot, newImgFilename)

        inputImg.save(newImgPath)

    return inputImg

#-------------------------------------------------------------------------------
# Time/Datetime
#-------------------------------------------------------------------------------

def calcTimeStart(uniqueKey):
    """init for calculate elapsed time"""
    global gVal

    gVal['calTimeKeyDict'][uniqueKey] = time.time()
    return


def calcTimeEnd(uniqueKey):
    """
        to get elapsed time
        Note: before call this, should use calcTimeStart to init
    :param uniqueKey:
    :return:
    """
    global gVal

    return time.time() - gVal['calTimeKeyDict'][uniqueKey]


def getCurDatetimeStr(outputFormat="%Y%m%d_%H%M%S"):
    """
    get current datetime then format to string

    eg:
        20171111_220722

    :param outputFormat: datetime output format
    :return: current datetime formatted string
    """
    curDatetime = datetime.now() # 2017-11-11 22:07:22.705101
    curDatetimeStr = curDatetime.strftime(format=outputFormat) #'20171111_220722'
    return curDatetimeStr

#-------------------------------------------------------------------------------
# bs4 = BeautifulSoup v4
#-------------------------------------------------------------------------------

def xmlToSoup(xmlStr):
    """convert to xml string to soup
        Note: xml is tag case sensitive -> retain tag upper case -> NOT convert tag to lowercase

    Args:
        xmlStr (str): xml str, normally page source
    Returns:
        soup
    Raises:
    """
    # HtmlParser = 'html.parser'
    # XmlParser = 'xml'
    XmlParser = 'lxml-xml'
    curParser = XmlParser
    soup = BeautifulSoup(xmlStr, curParser)
    return soup

def bsChainFind(curLevelSoup, queryChainList):
    """BeautifulSoup find with query chain

    Args:
        curLevelSoup (soup): BeautifulSoup
        queryChainList (list): str list of all level query dict
    Returns:
        soup
    Raises:
    Examples:
        input: 
            [
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
        output:
            soup node of 
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="可能离开微信，打开第三方应用" name="可能离开微信，打开第三方应用" label="可能离开微信，打开第三方应用" enabled="true" visible="true" x="71" y="331" width="272" height="18"/>
                in :
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
    foundSoup = None
    if queryChainList:
        chainListLen = len(queryChainList)

        if chainListLen == 1:
            # last one
            curLevelFindDict = queryChainList[0]
            curTag = curLevelFindDict["tag"]
            curAttrs = curLevelFindDict["attrs"]
            foundSoup = curLevelSoup.find(curTag, attrs=curAttrs)
        else:
            highestLevelFindDict = queryChainList[0]
            curTag = highestLevelFindDict["tag"]
            curAttrs = highestLevelFindDict["attrs"]
            foundSoupList = curLevelSoup.find_all(curTag, attrs=curAttrs)
            if foundSoupList:
                childrenChainList = queryChainList[1:]
                for eachSoup in foundSoupList:
                    eachSoupResult = bsChainFind(eachSoup, childrenChainList)
                    if eachSoupResult:
                        foundSoup = eachSoupResult
                        break

    return foundSoup

#-------------------------------------------------------------------------------
# AppCralwer Common Functions
#-------------------------------------------------------------------------------

# def get_navigationBar_bounds(curSession, curPageXml):
def get_navigationBar_bounds(curSession):
    """
        计算微信顶部系统导航栏的区域bounds
    """
    # soup = utils.xmlToSoup(curPageXml)
    """
        微信 顶部 导航栏：
            <XCUIElementTypeNavigationBar type="XCUIElementTypeNavigationBar" name="公众号" enabled="true" visible="true" x="0" y="20" width="375" height="44">
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="通讯录" label="通讯录" enabled="true" visible="true" x="10" y="20" width="64" height="44"/>
                <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" value="公众号" name="公众号" label="公众号" enabled="true" visible="true" x="187" y="24" width="1" height="36"/>
                <XCUIElementTypeButton type="XCUIElementTypeButton" name="添加" label="添加" enabled="true" visible="true" x="317" y="20" width="58" height="44"/>
            </XCUIElementTypeNavigationBar>
    """
    bounds = None
    naviBarQuery = {"type":"XCUIElementTypeNavigationBar", "enabled":"true", "x": "0"}
    isFound, naviBarElement = findElement(curSession, naviBarQuery)
    if isFound:
        isVisible = naviBarElement.visible
        if isVisible:
            curRect = naviBarElement.bounds
            x0 = curRect.x
            y0 = curRect.y
            x1 = curRect.x1
            y1 = curRect.y1
            bounds = [x0, y0, x1, y1]
    
    return bounds

def debugCalcHeadY(curSession):
    # curPageXml = getPageSource(gWdaClient)
    # get_navigationBar_bounds(curSession, curPageXml)
    bounds = get_navigationBar_bounds(curSession)

def calcHeadY(curSession):
    bounds = get_navigationBar_bounds(curSession)
    y1 = bounds[-1]
    headY = y1
    return headY

def getSwipeBounds(swipeDirectoin, curScreenX, curScreenY, headY=64):
    middleX = int(curScreenX / 2) # 207
    middleY = int(curScreenY / 2) # 368

    BottomY = curScreenY # 736

    swipeStartX = middleX # 207
    swipeVerticalRange = int(curScreenY // 4) # 184
    vertialTopY = int(headY + swipeVerticalRange) # 248
    vertialBottomY = int(BottomY - swipeVerticalRange) # 552

    SwipeUpBounds = [swipeStartX, vertialTopY, swipeStartX, vertialBottomY] # [207, 248, 207, 552]
    SwipeDownBounds = [swipeStartX, vertialBottomY, swipeStartX, vertialTopY] # [207, 552, 207, 248]
    SwipeLeftBounds = [int(round(curScreenX * 0.9)), middleY, int(round(curScreenX * 0.1)), middleY] # [373, 368, 41, 368]

    SwipeBoundsDict = {
        "SwipeUp": SwipeUpBounds,
        "SwipeDown": SwipeDownBounds,
        "SwipeLeft": SwipeLeftBounds,
    }
    curSwipeBounds = SwipeBoundsDict[swipeDirectoin]

    return curSwipeBounds
