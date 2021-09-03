/**
 * Copyright (c) 2015-present, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

#import "FBCustomCommands.h"

#import <XCTest/XCUIDevice.h>

#import "FBApplication.h"
#import "FBConfiguration.h"
#import "FBExceptionHandler.h"
#import "FBPasteboard.h"
#import "FBResponsePayload.h"
#import "FBRoute.h"
#import "FBRouteRequest.h"
#import "FBRunLoopSpinner.h"
#import "FBScreen.h"
#import "FBSession.h"
#import "FBXCodeCompatibility.h"
#import "FBSpringboardApplication.h"
#import "XCUIApplication+FBHelpers.h"
#import "XCUIDevice+FBHelpers.h"
#import "XCUIElement.h"
#import "XCUIElement+FBIsVisible.h"
#import "XCUIElementQuery.h"
#import "FBUnattachedAppLauncher.h"

@implementation FBCustomCommands

+ (NSArray *)routes
{
  return
  @[
    [[FBRoute POST:@"/timeouts"] respondWithTarget:self action:@selector(handleTimeouts:)],
    [[FBRoute POST:@"/wda/homescreen"].withoutSession respondWithTarget:self action:@selector(handleHomescreenCommand:)],
    [[FBRoute POST:@"/wda/deactivateApp"] respondWithTarget:self action:@selector(handleDeactivateAppCommand:)],
    [[FBRoute POST:@"/wda/keyboard/dismiss"] respondWithTarget:self action:@selector(handleDismissKeyboardCommand:)],
    [[FBRoute POST:@"/wda/lock"].withoutSession respondWithTarget:self action:@selector(handleLock:)],
    [[FBRoute POST:@"/wda/lock"] respondWithTarget:self action:@selector(handleLock:)],
    [[FBRoute POST:@"/wda/unlock"].withoutSession respondWithTarget:self action:@selector(handleUnlock:)],
    [[FBRoute POST:@"/wda/unlock"] respondWithTarget:self action:@selector(handleUnlock:)],
    [[FBRoute GET:@"/wda/locked"].withoutSession respondWithTarget:self action:@selector(handleIsLocked:)],
    [[FBRoute GET:@"/wda/locked"] respondWithTarget:self action:@selector(handleIsLocked:)],
    [[FBRoute GET:@"/wda/screen"] respondWithTarget:self action:@selector(handleGetScreen:)],
    [[FBRoute GET:@"/wda/activeAppInfo"] respondWithTarget:self action:@selector(handleActiveAppInfo:)],
    [[FBRoute GET:@"/wda/activeAppInfo"].withoutSession respondWithTarget:self action:@selector(handleActiveAppInfo:)],
#if !TARGET_OS_TV // tvOS does not provide relevant APIs
    [[FBRoute POST:@"/wda/setPasteboard"] respondWithTarget:self action:@selector(handleSetPasteboard:)],
    [[FBRoute POST:@"/wda/getPasteboard"] respondWithTarget:self action:@selector(handleGetPasteboard:)],
    [[FBRoute GET:@"/wda/batteryInfo"] respondWithTarget:self action:@selector(handleGetBatteryInfo:)],
#endif
    [[FBRoute POST:@"/wda/pressButton"] respondWithTarget:self action:@selector(handlePressButtonCommand:)],
    [[FBRoute POST:@"/wda/siri/activate"] respondWithTarget:self action:@selector(handleActivateSiri:)],
    [[FBRoute POST:@"/wda/apps/launchUnattached"].withoutSession respondWithTarget:self action:@selector(handleLaunchUnattachedApp:)],
    [[FBRoute GET:@"/wda/device/info"] respondWithTarget:self action:@selector(handleGetDeviceInfo:)],
    [[FBRoute GET:@"/wda/device/info"].withoutSession respondWithTarget:self action:@selector(handleGetDeviceInfo:)],
    [[FBRoute OPTIONS:@"/*"].withoutSession respondWithTarget:self action:@selector(handlePingCommand:)],
  ];
}


#pragma mark - Commands

+ (id<FBResponsePayload>)handleHomescreenCommand:(FBRouteRequest *)request
{
  NSError *error;
  if (![[XCUIDevice sharedDevice] fb_goToHomescreenWithError:&error]) {
    return FBResponseWithStatus([FBCommandStatus unknownErrorWithMessage:error.description
                                                               traceback:nil]);
  }
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handleDeactivateAppCommand:(FBRouteRequest *)request
{
  NSNumber *requestedDuration = request.arguments[@"duration"];
  NSTimeInterval duration = (requestedDuration ? requestedDuration.doubleValue : 3.);
  NSError *error;
  if (![request.session.activeApplication fb_deactivateWithDuration:duration error:&error]) {
    return FBResponseWithUnknownError(error);
  }
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handleTimeouts:(FBRouteRequest *)request
{
  // This method is intentionally not supported.
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handleDismissKeyboardCommand:(FBRouteRequest *)request
{
#if TARGET_OS_TV
  if ([self isKeyboardPresentForApplication:request.session.activeApplication]) {
    [[XCUIRemote sharedRemote] pressButton: XCUIRemoteButtonMenu];
  }
#else
  [request.session.activeApplication dismissKeyboard];
#endif
  NSError *error;
  NSString *errorDescription = @"The keyboard cannot be dismissed. Try to dismiss it in the way supported by your application under test.";
  if ([UIDevice.currentDevice userInterfaceIdiom] == UIUserInterfaceIdiomPhone) {
    errorDescription = @"The keyboard on iPhone cannot be dismissed because of a known XCTest issue. Try to dismiss it in the way supported by your application under test.";
  }
  BOOL isKeyboardNotPresent =
  [[[[FBRunLoopSpinner new]
     timeout:5]
    timeoutErrorMessage:errorDescription]
   spinUntilTrue:^BOOL{
     return ![self isKeyboardPresentForApplication:request.session.activeApplication];
   }
   error:&error];
  if (!isKeyboardNotPresent) {
    return FBResponseWithStatus([FBCommandStatus elementNotVisibleErrorWithMessage:error.description traceback:[NSString stringWithFormat:@"%@", NSThread.callStackSymbols]]);
  }
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handlePingCommand:(FBRouteRequest *)request
{
  return FBResponseWithOK();
}

#pragma mark - Helpers

+ (BOOL)isKeyboardPresentForApplication:(XCUIApplication *)application {
  XCUIElement *foundKeyboard = [application.fb_query descendantsMatchingType:XCUIElementTypeKeyboard].fb_firstMatch;
  return foundKeyboard && foundKeyboard.fb_isVisible;
}

+ (id<FBResponsePayload>)handleGetScreen:(FBRouteRequest *)request
{
  FBSession *session = request.session;
  CGSize statusBarSize = [FBScreen statusBarSizeForApplication:session.activeApplication];
  
//  CGSize statusBarSize = CGSizeZero;
//  statusBarSize = [[UIApplication sharedApplication] statusBarFrame].size;

//  if (@available(iOS 13.0, *)) {
//    UIStatusBarManager *manager = [UIApplication sharedApplication].keyWindow.windowScene.statusBarManager;
//    UIWindow *firstWindow = sharedApplication.windows.firstObject;
//    UIWindow *firstWindow = sharedApplication.windows.firstObject;
//    NSArray *windows = [[UIApplication sharedApplication]windows];
//    UIWindow *foundWindow = nil;
//    for (UIWindow *window in windows) {
//        if (window.isKeyWindow) {
//            foundWindow = window;
//            break;
//        }
//    }
    
//    UIWindow* firstWindow = nil;
//    if (@available(iOS 13.0, *))
//    {
//        for (UIWindowScene* windowScene in [UIApplication sharedApplication].connectedScenes)
//        {
//            if (windowScene.activationState == UISceneActivationStateForegroundActive)
//            {
//                firstWindow = windowScene.windows.firstObject;
//                break;
//            }
//        }
//    }else{
//        firstWindow = [UIApplication sharedApplication].keyWindow;
//    }
    
//    UIApplication *sharedApplication = [UIApplication sharedApplication];
//    NSArray *windows = sharedApplication.windows;
//    UIWindow *firstWindow = windows[0];
//    UIWindow *firstWindow = [[[UIApplication sharedApplication] delegate] window];
//    UIStatusBarManager *manager = firstWindow.windowScene.statusBarManager;
//    statusBarSize = manager.statusBarFrame.size;
//  } else {
//    statusBarSize = [[UIApplication sharedApplication] statusBarFrame].size;
//  }
  
  double nativeScale = [FBScreen nativeScale];
  CGRect bounds = [FBScreen bounds];
  CGRect nativeBounds = [FBScreen nativeBounds];
  return FBResponseWithObject(
  @{
    @"statusBarSize": @{
        @"width": @(statusBarSize.width),
        @"height": @(statusBarSize.height),
    },
    @"scale": @([FBScreen scale]),
    @"nativeScale": @(nativeScale),
    @"bounds": @{
        @"x": @(bounds.origin.x),
        @"y": @(bounds.origin.y),
        @"width": @(bounds.size.width),
        @"height": @(bounds.size.height),
    },
    @"nativeBounds": @{
        @"x": @(nativeBounds.origin.x),
        @"y": @(nativeBounds.origin.y),
        @"width": @(nativeBounds.size.width),
        @"height": @(nativeBounds.size.height),
    },
  });
}

+ (id<FBResponsePayload>)handleLock:(FBRouteRequest *)request
{
  NSError *error;
  if (![[XCUIDevice sharedDevice] fb_lockScreen:&error]) {
    return FBResponseWithUnknownError(error);
  }
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handleIsLocked:(FBRouteRequest *)request
{
  BOOL isLocked = [XCUIDevice sharedDevice].fb_isScreenLocked;
  return FBResponseWithObject(isLocked ? @YES : @NO);
}

+ (id<FBResponsePayload>)handleUnlock:(FBRouteRequest *)request
{
  NSError *error;
  if (![[XCUIDevice sharedDevice] fb_unlockScreen:&error]) {
    return FBResponseWithUnknownError(error);
  }
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handleActiveAppInfo:(FBRouteRequest *)request
{
  XCUIApplication *app = request.session.activeApplication ?: FBApplication.fb_activeApplication;
  
  NSString *appName = app.identifier;
  if(appName == nil){
    appName = @"";
  }
  NSString *appLabel = app.label;
  if(appLabel == nil){
    appLabel = @"";
  }
  NSString *appTitle = app.title;
  if(appTitle == nil){
    appTitle = @"";
  }
  unsigned long long generation = app.generation;
  BOOL running = app.running;
  XCUIApplicationState state = app.state;
  NSString *appPath = app.path;
  if(appPath == nil){
    appPath = @"";
  }

  return FBResponseWithObject(@{
    @"pid": @(app.processID),
    @"bundleId": app.bundleID,
    @"name": appName,
    @"processArguments": [self processArguments:app],
    @"label": appLabel,
    @"title": appTitle,
    @"generation": @(generation),
    @"running": @(running),
    @"state": @(state),
    @"path": appPath,
  });
}

/**
 * Returns current active app and its arguments of active session
 *
 * @return The dictionary of current active bundleId and its process/environment argumens
 *
 * @example
 *
 *     [self currentActiveApplication]
 *     //=> {
 *     //       "processArguments" : {
 *     //       "env" : {
 *     //           "HAPPY" : "testing"
 *     //       },
 *     //       "args" : [
 *     //           "happy",
 *     //           "tseting"
 *     //       ]
 *     //   }
 *
 *     [self currentActiveApplication]
 *     //=> {}
 */
+ (NSDictionary *)processArguments:(XCUIApplication *)app
{
  // Can be nil if no active activation is defined by XCTest
  if (app == nil) {
    return @{};
  }

  return
  @{
    @"args": app.launchArguments,
    @"env": app.launchEnvironment
  };
}

#if !TARGET_OS_TV
+ (id<FBResponsePayload>)handleSetPasteboard:(FBRouteRequest *)request
{
  NSString *contentType = request.arguments[@"contentType"] ?: @"plaintext";
  NSData *content = [[NSData alloc] initWithBase64EncodedString:(NSString *)request.arguments[@"content"]
                                                        options:NSDataBase64DecodingIgnoreUnknownCharacters];
  if (nil == content) {
    return FBResponseWithStatus([FBCommandStatus invalidArgumentErrorWithMessage:@"Cannot decode the pasteboard content from base64" traceback:nil]);
  }
  NSError *error;
  if (![FBPasteboard setData:content forType:contentType error:&error]) {
    return FBResponseWithUnknownError(error);
  }
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handleGetPasteboard:(FBRouteRequest *)request
{
  NSString *contentType = request.arguments[@"contentType"] ?: @"plaintext";
  NSError *error;
  id result = [FBPasteboard dataForType:contentType error:&error];
  if (nil == result) {
    return FBResponseWithUnknownError(error);
  }
  return FBResponseWithObject([result base64EncodedStringWithOptions:NSDataBase64Encoding64CharacterLineLength]);
}

+ (id<FBResponsePayload>)handleGetBatteryInfo:(FBRouteRequest *)request
{
  if (![[UIDevice currentDevice] isBatteryMonitoringEnabled]) {
    [[UIDevice currentDevice] setBatteryMonitoringEnabled:YES];
  }
  return FBResponseWithObject(@{
    @"level": @([UIDevice currentDevice].batteryLevel),
    @"state": @([UIDevice currentDevice].batteryState)
  });
}
#endif

+ (id<FBResponsePayload>)handlePressButtonCommand:(FBRouteRequest *)request
{
  NSError *error;
  if (![XCUIDevice.sharedDevice fb_pressButton:(id)request.arguments[@"name"] error:&error]) {
    return FBResponseWithUnknownError(error);
  }
  return FBResponseWithOK();
}

+ (id<FBResponsePayload>)handleActivateSiri:(FBRouteRequest *)request
{
  NSError *error;
  if (![XCUIDevice.sharedDevice fb_activateSiriVoiceRecognitionWithText:(id)request.arguments[@"text"] error:&error]) {
    return FBResponseWithUnknownError(error);
  }
  return FBResponseWithOK();
}

+ (id <FBResponsePayload>)handleLaunchUnattachedApp:(FBRouteRequest *)request
{
  NSString *bundle = (NSString *)request.arguments[@"bundleId"];
  if ([FBUnattachedAppLauncher launchAppWithBundleId:bundle]) {
    return FBResponseWithOK();
  }
  return FBResponseWithStatus([FBCommandStatus unknownErrorWithMessage:@"LSApplicationWorkspace failed to launch app" traceback:nil]);
}

+ (id<FBResponsePayload>)handleGetDeviceInfo:(FBRouteRequest *)request
{
  // Returns locale like ja_EN and zh-Hant_US. The format depends on OS
  // Developers should use this locale by default
  // https://developer.apple.com/documentation/foundation/nslocale/1414388-autoupdatingcurrentlocale
  NSString *currentLocale = [[NSLocale autoupdatingCurrentLocale] localeIdentifier];

  return FBResponseWithObject(@{
    @"currentLocale": currentLocale,
    @"timeZone": self.timeZone,
    @"name": UIDevice.currentDevice.name,
    @"model": UIDevice.currentDevice.model,
    @"uuid": [UIDevice.currentDevice.identifierForVendor UUIDString] ?: @"unknown",
    // https://developer.apple.com/documentation/uikit/uiuserinterfaceidiom?language=objc
    @"userInterfaceIdiom": @(UIDevice.currentDevice.userInterfaceIdiom),
    @"userInterfaceStyle": self.userInterfaceStyle,
#if TARGET_OS_SIMULATOR
    @"isSimulator": @(YES),
#else
    @"isSimulator": @(NO),
#endif
  });
}

/**
 * @return Current user interface style as a string
 */
+ (NSString *)userInterfaceStyle
{
  static id userInterfaceStyle = nil;
  static dispatch_once_t styleOnceToken;
  dispatch_once(&styleOnceToken, ^{
    if ([UITraitCollection respondsToSelector:NSSelectorFromString(@"currentTraitCollection")]) {
      id currentTraitCollection = [UITraitCollection performSelector:NSSelectorFromString(@"currentTraitCollection")];
      if (nil != currentTraitCollection) {
        userInterfaceStyle = [currentTraitCollection valueForKey:@"userInterfaceStyle"];
      }
    }
  });

  if (nil == userInterfaceStyle) {
    return @"unsupported";
  }

  switch ([userInterfaceStyle integerValue]) {
    case 1: // UIUserInterfaceStyleLight
      return @"light";
    case 2: // UIUserInterfaceStyleDark
      return @"dark";
    default:
      return @"unknown";
  }
}

/**
 * @return The string of TimeZone. Returns TZ timezone id by default. Returns TimeZone name by Apple if TZ timezone id is not available.
 */
+ (NSString *)timeZone
{
  NSTimeZone *localTimeZone = [NSTimeZone localTimeZone];
  // Apple timezone name like "US/New_York"
  NSString *timeZoneAbb = [localTimeZone abbreviation];
  if (timeZoneAbb == nil) {
    return [localTimeZone name];
  }

  // Convert timezone name to ids like "America/New_York" as TZ database Time Zones format
  // https://developer.apple.com/documentation/foundation/nstimezone
  NSString *timeZoneId = [[NSTimeZone timeZoneWithAbbreviation:timeZoneAbb] name];
  if (timeZoneId != nil) {
    return timeZoneId;
  }

  return [localTimeZone name];
}

@end
