# pyright: reportMissingImports=false, reportUndefinedVariable=false
import c4d

def err(error):
    file = op.GetObject().GetName()
    print(file + ": " + error)

def essentials():
    root = op.GetObject().GetUp().GetUp()
    if root is None: err("root not found, hierarchy might have been broken"); return

    uiNull = root.GetUp()
    if uiNull is None: err("main null not found, hierarchy might have been broken"); return

    dictNull = doc.SearchObject("py_buildDictionary")
    if uiNull is None: err("dictionary null doesn't exist"); return

    return uiNull, dictNull

def main():
    uiNull = essentials()[0]

    if not uiNull.FindEventNotification(doc, op, c4d.NOTIFY_EVENT_MESSAGE):
        uiNull.AddEventNotification(op, c4d.NOTIFY_EVENT_MESSAGE, 0, c4d.BaseContainer())

def message(msg_type, data):
    uiNull = essentials()[0]
    if (
        msg_type == c4d.MSG_NOTIFY_EVENT and
        data['event_data']['msg_id'] == c4d.MSG_DESCRIPTION_POSTSETPARAMETER and
        data['event_data']['msg_data']['descid'][1].id in [13,8]
    ):
        GINeeded = lightValue(uiNull)
        hideUserData(GINeeded, 41)
        if uiNull[c4d.ID_USERDATA, 40] == True:
            toggleGI(GINeeded)

def lightValue(uiNull):
    collection = doc.SearchObject("un_LCollections")
    children = collection.GetChildren()
    lightValue = uiNull[c4d.ID_USERDATA, 13]

    if lightValue != 999:
        GINeeded = (children[lightValue])[c4d.ID_USERDATA, 1]
    else: return False

    return GINeeded

def toggleGI(GINeeded):
    uiNull = essentials()[0]
    typeBlacklisted = uiNull[c4d.ID_USERDATA, 8] in [1,999]

    render_data = doc.GetActiveRenderData()
    if render_data is None: return
    video_post = render_data.GetFirstVideoPost()

    while video_post is not None:
        if video_post.GetType() == c4d.VPglobalillumination:
            if (typeBlacklisted is False and GINeeded == 1):
                video_post.DelBit(c4d.BIT_VPDISABLED)
            else: video_post.SetBit(c4d.BIT_VPDISABLED)
            break
        video_post = video_post.GetNext()

def hideUserData(trigger, target):
    controller = essentials()[0]
    if target == []: err("targetData is empty"); return
    if type(target) == int: target = [target]

    modifications = []

    for targetId in target:
        udId, bc = accessDictionary_by_UdID(targetId, controller)
        bc[c4d.DESC_HIDE] = trigger == 0
        modifications.append((udId, bc))
    
    for descId, container in modifications:
        controller.SetUserDataContainer(descId, container)

def accessDictionary_by_UdID(userdataid, directory):
    dictNull = essentials()[1]
    userData = directory.GetUserDataContainer()
    userDataDict = eval(dictNull[c4d.ID_USERDATA, 1])

    udId, bc = userData[userDataDict[userdataid]]

    return udId, bc