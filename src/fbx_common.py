'''
FBX Common Module

This Module:
    this is used to cut down basic fbx uses to a function. like setting up a scene.

-DOURAN
'''
import fbx

def InitializeSdkObjects():
    manager = fbx.FbxManager.Create()
    ios = fbx.FbxIOSettings.Create(manager, fbx.IOSROOT)
    manager.SetIOSettings(ios)
    scene = fbx.FbxScene.Create(manager, "Scene")
    return manager, scene

def LoadScene(manager, scene, filepath):
    importer = fbx.FbxImporter.Create(manager, "")
    status = importer.Initialize(filepath, -1, manager.GetIOSettings())
    if not status:
        return False
    importer.Import(scene)
    importer.Destroy()
    return True
