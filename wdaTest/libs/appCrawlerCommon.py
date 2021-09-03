# Functon: AppCrawler common functions
# Author: Crifan Li
# Update: 20200603

import os
import logging

from . import utils
from . import crifanLogging
from . import crifanWda

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
# Util Function
################################################################################

def swipe(curSession, swipeBounds, curSwipDuration=0.1):
    curSession.swipe(swipeBounds[0], swipeBounds[1], swipeBounds[2], swipeBounds[3], curSwipDuration)

def swipeLeft(curSession):
    swipeLeftBounds = utils.getSwipeBounds("SwipeLeft", ScreenX, ScreenY, headY=64)
    swipe(curSession, swipeLeftBounds)

def swipeUp(curSession):
    swipeUpBounds = utils.getSwipeBounds("SwipeUp", ScreenX, ScreenY, headY=64)
    swipe(curSession, swipeUpBounds)

def swipeDown(curSession):
    swipeDownBounds = utils.getSwipeBounds("swipeDown", ScreenX, ScreenY, headY=64)
    swipe(curSession, swipeDownBounds)


def clickCenterPosition(curSession, elementAttrDict):
    x = int(elementAttrDict["x"])
    y = int(elementAttrDict["y"])
    width = int(elementAttrDict["width"])
    height = int(elementAttrDict["height"])
    centerX = x + int(width / 2)
    centerY = y + int(height / 2)
    curSession.click(centerX, centerY)
    logging.info("Clicked [%s, %s]", centerX, centerY)

################################################################################
# Main
################################################################################

def wdaCommonInit():
    global gServerUrl, gWdaClient, gCurAppId, gCurSession

    gCurDatetimeStr = utils.getCurDatetimeStr() # '20200316_155954'
    logFolder = os.path.join("debug", "logs")
    curLogFile = "wdaTest_%s.log" % gCurDatetimeStr
    logFullPath = os.path.join(logFolder, curLogFile)
    crifanLogging.loggingInit(logFullPath)

    crifanWda.wdaInit()

    gWdaClient = crifanWda.gWdaClient
    gServerUrl = crifanWda.gServerUrl
    gCurAppId = crifanWda.gCurAppId
    gCurSession = crifanWda.gCurSession
