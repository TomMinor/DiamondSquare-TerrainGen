import maya.cmds as cmds
import functools

#Globals

# Makes it easier to update button names in one place if necessary
UI_Widgets = {
    # Generic
    'WidthInput'       : 'width_lineEdit',
    'HeightInput'      : 'height_lineEdit',
    'FeatureSizeInput' : 'featureSize_lineEdit',
    'FeatureSizeSlider': 'featureSize_slider',
    'SquareCheckbox'   : 'squareSize_chkBox',
    'FacesRadioBtn'    : 'moveFaces_radio',
    'VerticesRadioBtn' : 'moveVertices_radio',
    'DeleteTerrainCheckbox' : 'deleteTerrain_chkBox',
    'GenerateProgress' : 'generate_progessBar',
    
    # Layer 
    'LayersList'       : 'layer_listview',
    'DeleteLayerBtn'   : 'deleteLayer_btn',
    'AddLayerBtn'      : 'addLayer_btn',
    
    # Layer config
    'LayerNameInput' : 'layerName_lineEdit',
    'ResInput'       : 'res_lineEdit',
    'ResSlider'      : 'res_slider',
    'WeightInput'    : 'weight_lineEdit',
    'WeightSlider'   : 'weight_slider',
    'ScaleInput'     : 'scale_lineEdit',
    'ScaleSlider'    : 'scale_slider',
    'MinHeightInput' : 'minHeight_lineEdit',
    'MaxHeightInput' : 'maxHeight_lineEdit',
    'InterpType'     : 'interpType_combo'
}

class LayerConfig:
    def __init__(self, name):
        self.name = name
        self.res = 3 # Store power of 2, default is 2**3 == 8
        self.weight = 0.5
        self.scale = 1.0
        self.minHeight = 0
        self.maxHeight = 1
        self.interpType = 'Linear' # 'Cosine' is also valid

layers = [] # Store LayerConfig instances

# Gui Functions
# ------------------------------ Layer Callbacks ------------------------------ 
def addLayer():
    global layers
    newLayerName = 'layer' + str(len(layers))
    cmds.textScrollList(UI_Widgets['LayersList'], edit=True, append=newLayerName)
    layers.append(LayerConfig(newLayerName))

def deleteLayer():
    selectedItem = cmds.textScrollList( UI_Widgets['LayersList'], query=True, si = True)
    if(selectedItem):
        cmds.textScrollList( UI_Widgets['LayersList'], edit=True, removeItem = selectedItem[0] )

def layerSelectionChanged(*args):
    selectedItemID = cmds.textScrollList( UI_Widgets['LayersList'], query=True, selectIndexedItem = True)[0]
    
    currentLayer = layers[selectedItemID - 1]
    
    cmds.textField(UI_Widgets['LayerNameInput'], edit=True, text=currentLayer.name)
    
    cmds.textField(UI_Widgets['MinHeightInput'], edit=True, text=currentLayer.minHeight)
    cmds.textField(UI_Widgets['MaxHeightInput'], edit=True, text=currentLayer.maxHeight)
    
    for i in range(cmds.optionMenu(UI_Widgets['InterpType'], q=True, numberOfItems=True)):
        cmds.optionMenu(UI_Widgets['InterpType'], e=True, numberOfItems=True)
    
    print 

    
def generateTerrain():
    print "Generating terrain..."
    
    cmds.intSlider(UI_Widgets['FeatureSizeSlider'], query=True, v=True)
    
if 'window' in globals():
    if (cmds.window(window, exists=True)):
        cmds.deleteUI(window)
        cmds.treeView(UI_Widgets['LayersList'], e=True, removeAll=True)

window = cmds.loadUI(uiFile="/home/i7245143/maya/2014-x64/resources/terrain_gui.ui")

cmds.textScrollList(UI_Widgets['LayersList'], e=True, selectCommand = layerSelectionChanged)

cmds.showWindow(window)
