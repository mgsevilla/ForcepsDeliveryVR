import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# ForcepsDeliveryVR
#

class ForcepsDeliveryVR(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ForcepsDeliveryVR"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Virtual Reality"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  
    self.parent.contributors = ["Monica Garcia-Sevilla (Universidad de Las Palmas de Gran Canaria)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#ForcepsDeliveryVR">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was developed by Monica Garcia-Sevilla and Abian Hernandez at Universidad de Las Palmas de Gran Canaria.
"""

    # Additional initialization step after application startup is complete
    slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#

def registerSampleData():
  """
  Add data sets to Sample Data module.
  """
  # It is always recommended to provide sample data for users to make it easy to try the module,
  # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  import SampleData
  iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # it is recommended to store data sets that are larger than a few MB in a Github release.

  # ForcepsDeliveryVR1
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='ForcepsDeliveryVR',
    sampleName='ForcepsDeliveryVR1',
    # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
    # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
    thumbnailFileName=os.path.join(iconsPath, 'ForcepsDeliveryVR1.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
    fileNames='ForcepsDeliveryVR1.nrrd',
    # Checksum to ensure file integrity. Can be computed by this command:
    #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    checksums = 'SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
    # This node name will be used when the data set is loaded
    nodeNames='ForcepsDeliveryVR1'
  )

  # ForcepsDeliveryVR2
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='ForcepsDeliveryVR',
    sampleName='ForcepsDeliveryVR2',
    thumbnailFileName=os.path.join(iconsPath, 'ForcepsDeliveryVR2.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
    fileNames='ForcepsDeliveryVR2.nrrd',
    checksums = 'SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
    # This node name will be used when the data set is loaded
    nodeNames='ForcepsDeliveryVR2'
  )

#
# ForcepsDeliveryVRWidget
#

class ForcepsDeliveryVRWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self.callbackObserverTag = -1
    self.observerTag = None

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Widget variables
    self.logic = ForcepsDeliveryVRLogic()
    self.vrLogic = slicer.modules.virtualreality.logic()

    # System error margin
    self.errorMargin_dist1 = 0
    self.errorMargin_dist = 0 # mm
    self.errorMargin_angle = 0 # degrees

    # CREATE PATHS
    self.ForcepsDeliveryVR_modelsPath = slicer.modules.forcepsdeliveryvr.path.replace("ForcepsDeliveryVR.py","") + 'Resources/Models/'
    self.ForcepsDeliveryVR_phaseTextsPath = slicer.modules.forcepsdeliveryvr.path.replace("ForcepsDeliveryVR.py","") + 'Resources/Models/Texts/'

    
    self.ForcepsDeliveryVR_iconsPath = slicer.modules.forcepsdeliveryvr.path.replace("ForcepsDeliveryVR.py","") + 'Resources/Data/Icons/'
    # ICONS
    iconPlayPath = os.path.join(self.ForcepsDeliveryVR_iconsPath,'play.png')
    iconPausePath = os.path.join(self.ForcepsDeliveryVR_iconsPath,'pause.png')
    iconRetryPath = os.path.join(self.ForcepsDeliveryVR_iconsPath,'retry.png')
    iconNextPath = os.path.join(self.ForcepsDeliveryVR_iconsPath,'next.png')
    iconHelpPath = os.path.join(self.ForcepsDeliveryVR_iconsPath,'info.png')


    #
    # Setup view
    #

    # show 3D View
    self.layoutManager= slicer.app.layoutManager()
    self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    # quit box and axis
    view = slicer.util.getNode('View1')
    view.SetBoxVisible(0)
    view.SetAxisLabelsVisible(0)

    # UI definition

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    # uiWidget = slicer.util.loadUI(self.resourcePath('UI/ForcepsDeliveryVR.ui'))
    # self.layout.addWidget(uiWidget)
    # self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    # uiWidget.setMRMLScene(slicer.mrmlScene)

    #
    # INITIALIZATION
    #
    self.initCollapsibleButton = ctk.ctkCollapsibleButton()
    self.initCollapsibleButton.text = "INITIALIZATION"
    self.layout.addWidget(self.initCollapsibleButton)

    # Layout within the dummy collapsible button
    initFormLayout = qt.QFormLayout(self.initCollapsibleButton)

    # Activate VR
    self.activateVRButton = qt.QPushButton()
    self.activateVRButton.enabled = True
    self.activateVRButton.setText('Activate VR')
    initFormLayout.addRow(self.activateVRButton)

    # Load models and other data
    self.loadDataButton = qt.QPushButton("Load Data")
    self.loadDataButton.enabled = True
    initFormLayout.addRow(self.loadDataButton)  

    self.configCollapsibleButton = ctk.ctkCollapsibleButton()
    self.configCollapsibleButton.collapsed = True
    self.configCollapsibleButton.text = "CONFIGURATION"
    self.layout.addWidget(self.configCollapsibleButton)

    #
    # CONFIGURATION
    #
    # Layout within the dummy collapsible button
    configFormLayout = qt.QFormLayout(self.configCollapsibleButton)

    # Reset view
    self.resetVRViewButton = qt.QPushButton()
    self.resetVRViewButton.enabled = True
    self.resetVRViewButton.setText('Reset VR View')
    configFormLayout.addRow(self.resetVRViewButton)

    # Controllers visibility
    self.controllersVisibilitySelection = qt.QHBoxLayout()
    configFormLayout.addRow(self.controllersVisibilitySelection)
    self.controllersVisibilityCheckBox = qt.QCheckBox('Hide controllers')
    self.controllersVisibilityCheckBox.checkable = True
    self.controllersVisibilityCheckBox.checked = True
    self.controllersVisibilitySelection.addWidget(self.controllersVisibilityCheckBox)

    #
    # EVALUATION
    #
    self.Step1CollapsibleButton = ctk.ctkCollapsibleButton()
    self.Step1CollapsibleButton.text = "STEP 1: Preparation"
    self.Step1CollapsibleButton.collapsed = True
    self.layout.addWidget(self.Step1CollapsibleButton)

    Step1FormLayout = qt.QFormLayout(self.Step1CollapsibleButton)

    # --- FORCEPS ARRANGEMENT ---
    self.ArrangementGroupBox = ctk.ctkCollapsibleGroupBox()
    self.ArrangementGroupBox.setTitle("Forceps Arrangement")
    self.ArrangementGroupBox.collapsed = True
    Step1FormLayout.addRow(self.ArrangementGroupBox)
    ArrangementGroupBox_Layout = qt.QFormLayout(self.ArrangementGroupBox)
    # self.Step1GroupBox.setStyleSheet("background-color: rgb(176,231,169);")

    self.arrangementText = qt.QLabel('Place forceps together')
    self.arrangementText.setStyleSheet("font-size: 14px; font-weight: bold;")
    ArrangementGroupBox_Layout.addRow(self.arrangementText)

    self.arrangementHorizontalLayout = qt.QHBoxLayout()
    ArrangementGroupBox_Layout.addRow(self.arrangementHorizontalLayout)

    # Start/Stop Real Time
    self.start_arrangement = qt.QPushButton("Start")
    self.start_arrangement.enabled = True
    self.start_arrangement_icon_play = qt.QIcon(iconPlayPath)
    self.start_arrangement_icon_pause = qt.QIcon(iconPausePath)
    self.start_arrangement.setIcon(self.start_arrangement_icon_play)
    self.arrangementHorizontalLayout.addWidget(self.start_arrangement)

    # Next step
    self.next_arrangement = qt.QPushButton("Next")
    self.next_arrangement.enabled = False
    self.next_arrangement_icon = qt.QIcon(iconNextPath)
    self.next_arrangement.setIcon(self.next_arrangement_icon)
    self.arrangementHorizontalLayout.addWidget(self.next_arrangement)

    #  Help
    self.help_arrangement = qt.QPushButton("Help")
    self.help_arrangement.enabled = True
    self.help_arrangement_icon = qt.QIcon(iconHelpPath)
    self.help_arrangement.setIcon(self.help_arrangement_icon)
    self.arrangementHorizontalLayout.addWidget(self.help_arrangement)


    # --- FORCEPS PRESENTATION ---
    self.PresentationGroupBox = ctk.ctkCollapsibleGroupBox()
    self.PresentationGroupBox.setTitle("Forceps Presentation")
    self.PresentationGroupBox.collapsed = True
    Step1FormLayout.addRow(self.PresentationGroupBox)
    PresentationGroupBox_Layout = qt.QFormLayout(self.PresentationGroupBox)
    # self.Step1GroupBox.setStyleSheet("background-color: rgb(176,231,169);")

    self.presentationText = qt.QLabel('Present forceps')
    self.presentationText.setStyleSheet("font-size: 14px; font-weight: bold;")
    PresentationGroupBox_Layout.addRow(self.presentationText)

    self.presentationHorizontalLayout = qt.QHBoxLayout()
    PresentationGroupBox_Layout.addRow(self.presentationHorizontalLayout)

    # Start/Stop Real Time
    self.start_presentation = qt.QPushButton("Start")
    self.start_presentation.enabled = True
    self.start_presentation_icon_play = qt.QIcon(iconPlayPath)
    self.start_presentation_icon_pause = qt.QIcon(iconPausePath)
    self.start_presentation.setIcon(self.start_presentation_icon_play)
    self.presentationHorizontalLayout.addWidget(self.start_presentation)

    # Next step
    self.next_presentation = qt.QPushButton("Next")
    self.next_presentation.enabled = False
    self.next_presentation_icon = qt.QIcon(iconNextPath)
    self.next_presentation.setIcon(self.next_presentation_icon)
    self.presentationHorizontalLayout.addWidget(self.next_presentation)

    #  Help
    self.help_presentation = qt.QPushButton("Help")
    self.help_presentation.enabled = True
    self.help_presentation_icon = qt.QIcon(iconHelpPath)
    self.help_presentation.setIcon(self.help_presentation_icon)
    self.presentationHorizontalLayout.addWidget(self.help_presentation)

    # STEP 2
    self.Step2CollapsibleButton = ctk.ctkCollapsibleButton()
    self.Step2CollapsibleButton.text = "STEP 2: Placement Left Forceps"
    self.Step2CollapsibleButton.collapsed = True
    self.layout.addWidget(self.Step2CollapsibleButton)

    Step2FormLayout = qt.QFormLayout(self.Step2CollapsibleButton)

    # --- INITIAL PLACEMENT LEFT ---
    self.InitialPlacementLeftGroupBox = ctk.ctkCollapsibleGroupBox()
    self.InitialPlacementLeftGroupBox.setTitle("Initial Placement Left")
    self.InitialPlacementLeftGroupBox.collapsed = True
    Step2FormLayout.addRow(self.InitialPlacementLeftGroupBox)
    InitialPlacementLeftGroupBox_Layout = qt.QFormLayout(self.InitialPlacementLeftGroupBox)
    # self.Step1GroupBox.setStyleSheet("background-color: rgb(176,231,169);")

    self.initialPlacementLeftText = qt.QLabel('Place left forceps vertically')
    self.initialPlacementLeftText.setStyleSheet("font-size: 14px; font-weight: bold;")
    InitialPlacementLeftGroupBox_Layout.addRow(self.initialPlacementLeftText)

    self.initialPlacementLeftHorizontalLayout = qt.QHBoxLayout()
    InitialPlacementLeftGroupBox_Layout.addRow(self.initialPlacementLeftHorizontalLayout)
    
    # Start/Stop Real Time
    self.start_initialPlacementLeft = qt.QPushButton("Start")
    self.start_initialPlacementLeft.enabled = True
    self.start_initialPlacementLeft_icon_play = qt.QIcon(iconPlayPath)
    self.start_initialPlacementLeft_icon_pause = qt.QIcon(iconPausePath)
    self.start_initialPlacementLeft.setIcon(self.start_initialPlacementLeft_icon_play)
    self.initialPlacementLeftHorizontalLayout.addWidget(self.start_initialPlacementLeft)

    # Next step
    self.next_initialPlacementLeft = qt.QPushButton("Next")
    self.next_initialPlacementLeft.enabled = False
    self.next_initialPlacementLeft_icon = qt.QIcon(iconNextPath)
    self.next_initialPlacementLeft.setIcon(self.next_initialPlacementLeft_icon)
    self.initialPlacementLeftHorizontalLayout.addWidget(self.next_initialPlacementLeft)

    #  Help
    self.help_initialPlacementLeft = qt.QPushButton("Help")
    self.help_initialPlacementLeft.enabled = True
    self.help_initialPlacementLeft_icon = qt.QIcon(iconHelpPath)
    self.help_initialPlacementLeft.setIcon(self.help_initialPlacementLeft_icon)
    self.initialPlacementLeftHorizontalLayout.addWidget(self.help_initialPlacementLeft)


    # --- FINAL PLACEMENT LEFT ---
    self.FinalPlacementLeftGroupBox = ctk.ctkCollapsibleGroupBox()
    self.FinalPlacementLeftGroupBox.setTitle("Final Placement Left")
    self.FinalPlacementLeftGroupBox.collapsed = True
    Step2FormLayout.addRow(self.FinalPlacementLeftGroupBox)
    FinalPlacementLeftGroupBox_Layout = qt.QFormLayout(self.FinalPlacementLeftGroupBox)
    # self.Step1GroupBox.setStyleSheet("background-color: rgb(176,231,169);")

    self.finalPlacementLeftText = qt.QLabel('Introduce the left forceps')
    self.finalPlacementLeftText.setStyleSheet("font-size: 14px; font-weight: bold;")
    FinalPlacementLeftGroupBox_Layout.addRow(self.finalPlacementLeftText)

    self.finalPlacementLeftHorizontalLayout = qt.QHBoxLayout()
    FinalPlacementLeftGroupBox_Layout.addRow(self.finalPlacementLeftHorizontalLayout)

    # Start/Stop Real Time
    self.start_finalPlacementLeft = qt.QPushButton("Start")
    self.start_finalPlacementLeft.enabled = True
    self.start_finalPlacementLeft_icon_play = qt.QIcon(iconPlayPath)
    self.start_finalPlacementLeft_icon_pause = qt.QIcon(iconPausePath)
    self.start_finalPlacementLeft.setIcon(self.start_finalPlacementLeft_icon_play)
    self.finalPlacementLeftHorizontalLayout.addWidget(self.start_finalPlacementLeft)

    # Next step
    self.next_finalPlacementLeft = qt.QPushButton("Next")
    self.next_finalPlacementLeft.enabled = False
    self.next_finalPlacementLeft_icon = qt.QIcon(iconNextPath)
    self.next_finalPlacementLeft.setIcon(self.next_finalPlacementLeft_icon)
    self.finalPlacementLeftHorizontalLayout.addWidget(self.next_finalPlacementLeft)

    #  Help
    self.help_finalPlacementLeft = qt.QPushButton("Help")
    self.help_finalPlacementLeft.enabled = True
    self.help_finalPlacementLeft_icon = qt.QIcon(iconHelpPath)
    self.help_finalPlacementLeft.setIcon(self.help_finalPlacementLeft_icon)
    self.finalPlacementLeftHorizontalLayout.addWidget(self.help_finalPlacementLeft)

    # STEP 3
    self.Step3CollapsibleButton = ctk.ctkCollapsibleButton()
    self.Step3CollapsibleButton.text = "STEP 3: Placement Right Forceps"
    self.Step3CollapsibleButton.collapsed = True
    self.layout.addWidget(self.Step3CollapsibleButton)

    Step3FormLayout = qt.QFormLayout(self.Step3CollapsibleButton)


    # --- INITIAL PLACEMENT LEFT ---
    self.InitialPlacementRightGroupBox = ctk.ctkCollapsibleGroupBox()
    self.InitialPlacementRightGroupBox.setTitle("Initial Placement Right")
    self.InitialPlacementRightGroupBox.collapsed = True
    Step3FormLayout.addRow(self.InitialPlacementRightGroupBox)
    InitialPlacementRightGroupBox_Layout = qt.QFormLayout(self.InitialPlacementRightGroupBox)
    # self.Step1GroupBox.setStyleSheet("background-color: rgb(176,231,169);")

    self.initialPlacementRightText = qt.QLabel('Place right forceps vertically')
    self.initialPlacementRightText.setStyleSheet("font-size: 14px; font-weight: bold;")
    InitialPlacementRightGroupBox_Layout.addRow(self.initialPlacementRightText)

    self.initialPlacementRightHorizontalLayout = qt.QHBoxLayout()
    InitialPlacementRightGroupBox_Layout.addRow(self.initialPlacementRightHorizontalLayout)
    
    # Start/Stop Real Time
    self.start_initialPlacementRight = qt.QPushButton("Start")
    self.start_initialPlacementRight.enabled = True
    self.start_initialPlacementRight_icon_play = qt.QIcon(iconPlayPath)
    self.start_initialPlacementRight_icon_pause = qt.QIcon(iconPausePath)
    self.start_initialPlacementRight.setIcon(self.start_initialPlacementRight_icon_play)
    self.initialPlacementRightHorizontalLayout.addWidget(self.start_initialPlacementRight)

    # Next step
    self.next_initialPlacementRight = qt.QPushButton("Next")
    self.next_initialPlacementRight.enabled = False
    self.next_initialPlacementRight_icon = qt.QIcon(iconNextPath)
    self.next_initialPlacementRight.setIcon(self.next_initialPlacementRight_icon)
    self.initialPlacementRightHorizontalLayout.addWidget(self.next_initialPlacementRight)

    #  Help
    self.help_initialPlacementRight = qt.QPushButton("Help")
    self.help_initialPlacementRight.enabled = True
    self.help_initialPlacementRight_icon = qt.QIcon(iconHelpPath)
    self.help_initialPlacementRight.setIcon(self.help_initialPlacementRight_icon)
    self.initialPlacementRightHorizontalLayout.addWidget(self.help_initialPlacementRight)


    # --- FINAL PLACEMENT LEFT ---
    self.FinalPlacementRightGroupBox = ctk.ctkCollapsibleGroupBox()
    self.FinalPlacementRightGroupBox.setTitle("Final Placement Right")
    self.FinalPlacementRightGroupBox.collapsed = True
    Step3FormLayout.addRow(self.FinalPlacementRightGroupBox)
    FinalPlacementRightGroupBox_Layout = qt.QFormLayout(self.FinalPlacementRightGroupBox)
    # self.Step1GroupBox.setStyleSheet("background-color: rgb(176,231,169);")

    self.finalPlacementRightText = qt.QLabel('Introduce the right forceps')
    self.finalPlacementRightText.setStyleSheet("font-size: 14px; font-weight: bold;")
    FinalPlacementRightGroupBox_Layout.addRow(self.finalPlacementRightText)

    self.finalPlacementRightHorizontalLayout = qt.QHBoxLayout()
    FinalPlacementRightGroupBox_Layout.addRow(self.finalPlacementRightHorizontalLayout)

    # Start/Stop Real Time
    self.start_finalPlacementRight = qt.QPushButton("Start")
    self.start_finalPlacementRight.enabled = True
    self.start_finalPlacementRight_icon_play = qt.QIcon(iconPlayPath)
    self.start_finalPlacementRight_icon_pause = qt.QIcon(iconPausePath)
    self.start_finalPlacementRight.setIcon(self.start_finalPlacementRight_icon_play)
    self.finalPlacementRightHorizontalLayout.addWidget(self.start_finalPlacementRight)

    # Next step
    self.next_finalPlacementRight = qt.QPushButton("Next")
    self.next_finalPlacementRight.enabled = False
    self.next_finalPlacementRight_icon = qt.QIcon(iconNextPath)
    self.next_finalPlacementRight.setIcon(self.next_finalPlacementRight_icon)
    self.finalPlacementRightHorizontalLayout.addWidget(self.next_finalPlacementRight)

    #  Help
    self.help_finalPlacementRight = qt.QPushButton("Help")
    self.help_finalPlacementRight.enabled = True
    self.help_finalPlacementRight_icon = qt.QIcon(iconHelpPath)
    self.help_finalPlacementRight.setIcon(self.help_finalPlacementRight_icon)
    self.finalPlacementRightHorizontalLayout.addWidget(self.help_finalPlacementRight)



    # add here remaining ui objects
    # ...

    # Add vertical spacer
    self.layout.addStretch(1)


    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = ForcepsDeliveryVRLogic()

    # Connections

    # # These connections ensure that we update parameter node when scene is closed
    # self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)




    # INITIALIZATION
    self.activateVRButton.connect('clicked(bool)', self.onSwitchVirtualRealityActivation)
    self.loadDataButton.connect('clicked(bool)', self.onLoadDataButtonClicked)

    # CONFIGURATION
    self.controllersVisibilityCheckBox.connect('clicked(bool)', self.onControllerVisibilityCheckBoxClicked)
    self.resetVRViewButton.connect('clicked(bool)', self.onResetVRViewButtonClicked)
 

    # STEP 1: Forceps arrangement and presentation
    self.start_arrangement.connect('clicked(bool)', self.onStartArrangementClicked)
    self.start_presentation.connect('clicked(bool)', self.onStartPresentationClicked)
    self.start_initialPlacementLeft.connect('clicked(bool)', self.onStartInitialPlacementLeftClicked)
    self.start_finalPlacementLeft.connect('clicked(bool)', self.onStartFinalPlacementLeftClicked)
    self.start_initialPlacementRight.connect('clicked(bool)', self.onStartInitialPositionRClicked)
    self.start_finalPlacementRight.connect('clicked(bool)', self.onStartFinalPositionRClicked)







  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  # def enter(self):
  #   """
  #   Called each time the user opens this module.
  #   """
  #   print('enter')

  # def exit(self):
  #   """
  #   Called each time the user opens a different module.
  #   """
  #   # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
  #   #self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
  #   print('exit')

  # def onSceneStartClose(self, caller, event):
  #   """
  #   Called just before the scene is closed.
  #   """
  #   print('scene start close')


  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    # if self.parent.isEntered:
    #   self.initializeParameterNode()
    self.loadDataButton.enabled = True
    print('scene end close')


  def onSwitchVirtualRealityActivation(self):
    if (self.logic.vrEnabled):
      self.logic.deactivateVirtualReality()
      self.activateVRButton.setText("Activate VR")
    else:
      self.logic.activateVirtualReality()
      self.activateVRButton.setText("Deactivate VR")
      slicer.modules.virtualreality.viewWidget().updateViewFromReferenceViewCamera()


  def onLoadDataButtonClicked(self):
    logging.debug('Load models')

    try:
      self.forcepsLeftModel = slicer.util.getNode('ForcepsLeftModel')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_modelsPath + 'ForcepsLeftModel.stl')
      self.forcepsLeftModel = slicer.util.getNode(pattern="ForcepsLeftModel")
      self.forcepsLeftModelDisplay=self.forcepsLeftModel.GetModelDisplayNode()
      self.forcepsLeftModelDisplay.SetColor([0.8,0.8,0.8])

    try:
      self.forcepsRightModel = slicer.util.getNode('ForcepsRightModel')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_modelsPath + 'ForcepsRightModel.stl')
      self.forcepsRightModel = slicer.util.getNode(pattern="ForcepsRightModel")
      self.forcepsRightModelDisplay=self.forcepsRightModel.GetModelDisplayNode()
      self.forcepsRightModelDisplay.SetColor([0.8,0.8,0.8])

    try:
      self.babyBodyModel = slicer.util.getNode('BabyBodyModel')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_modelsPath + 'BabyBodyModel.stl')
      self.babyBodyModel = slicer.util.getNode(pattern="BabyBodyModel")
      self.babyBodyModelDisplay=self.babyBodyModel.GetModelDisplayNode()
      self.babyBodyModelDisplay.SetColor([1,0.68,0.62])

    try:
      self.babyHeadModel = slicer.util.getNode('BabyHeadModel')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_modelsPath + 'BabyHeadModel.stl')
      self.babyHeadModel = slicer.util.getNode(pattern="BabyHeadModel")
      self.babyHeadModelDisplay=self.babyHeadModel.GetModelDisplayNode()
      self.babyHeadModelDisplay.SetColor([1,0.68,0.62])

    try:
      self.motherModel = slicer.util.getNode('MotherModel')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_modelsPath + 'MotherModel.stl')
      self.motherModel = slicer.util.getNode(pattern="MotherModel")
      self.motherModelDisplay=self.motherModel.GetModelDisplayNode()
      self.motherModelDisplay.SetColor([1,0.68,0.62])
    #self.motherModel.SetSelectable(0)
      # self.motherModelDisplay.SetOpacity(0.5)

    # Load Texts
    try:
      self.arrangementModel = slicer.util.getNode('arrangement')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_phaseTextsPath + 'arrangement.stl')
      self.arrangementModel = slicer.util.getNode(pattern="arrangement")
      self.arrangementModelDisplay=self.arrangementModel.GetModelDisplayNode()
      self.arrangementModelDisplay.SetVisibility(False)
    
    try:
      self.presentationModel = slicer.util.getNode('presentation')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_phaseTextsPath + 'presentation.stl')
      self.presentationModel = slicer.util.getNode(pattern="presentation")
      self.presentationModelDisplay=self.presentationModel.GetModelDisplayNode()
      self.presentationModelDisplay.SetVisibility(False)

    try:
      self.initialPlacementLeftModel = slicer.util.getNode('initialPlacementLeft')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_phaseTextsPath + 'initialPlacementLeft.stl')
      self.initialPlacementLeftModel = slicer.util.getNode(pattern="initialPlacementLeft")
      self.initialPlacementLeftModelDisplay=self.initialPlacementLeftModel.GetModelDisplayNode()
      self.initialPlacementLeftModelDisplay.SetVisibility(False)

    try:
      self.finalPlacementLeftModel = slicer.util.getNode('finalPlacementLeft')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_phaseTextsPath + 'finalPlacementLeft.stl')
      self.finalPlacementLeftModel = slicer.util.getNode(pattern="finalPlacementLeft")
      self.finalPlacementLeftModelDisplay=self.finalPlacementLeftModel.GetModelDisplayNode()
      self.finalPlacementLeftModelDisplay.SetVisibility(False)

    try:
      self.initialPlacementRightModel = slicer.util.getNode('initialPlacementRight')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_phaseTextsPath + 'initialPlacementRight.stl')
      self.initialPlacementRightModel = slicer.util.getNode(pattern="initialPlacementRight")
      self.initialPlacementRightModelDisplay=self.initialPlacementRightModel.GetModelDisplayNode()
      self.initialPlacementRightModelDisplay.SetVisibility(False)
    
    try:
      self.finalPlacementRightModel = slicer.util.getNode('finalPlacementRight')
    except:
      slicer.util.loadModel(self.ForcepsDeliveryVR_phaseTextsPath + 'finalPlacementRight.stl')
      self.finalPlacementRightModel = slicer.util.getNode(pattern="finalPlacementRight")
      self.finalPlacementRightModelDisplay=self.finalPlacementRightModel.GetModelDisplayNode()
      self.finalPlacementRightModelDisplay.SetVisibility(False)
    

    self.logic.applyForcepsTransform()
    self.logic.resetVRView(125)

    self.loadDataButton.enabled = False
    self.initCollapsibleButton.collapsed = True
    self.configCollapsibleButton.collapsed = False
    self.Step1CollapsibleButton.collapsed = False
    self.ArrangementGroupBox.collapsed = False


  def onControllerVisibilityCheckBoxClicked(self):
    logging.debug('change controller visibility')
    if self.controllersVisibilityCheckBox.checked:
      self.logic.changeControllerVisibility(False)
    else:
      self.logic.changeControllerVisibility(True)

  def onResetVRViewButtonClicked(self):
    logging.debug('reset VR view')
    zoomOut = 100
    self.logic.resetVRView(zoomOut)


  def onStartArrangementClicked(self):
    start_stop = self.start_arrangement.text
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    leftControllerTransform = vrViewNode.GetLeftControllerTransformNode()
    if start_stop == 'Start':
      self.arrangementModelDisplay.SetVisibility(True)
      self.addActionObserver(leftControllerTransform)
      self.start_arrangement.setText('Stop')
      self.start_arrangement.setIcon(self.start_arrangement_icon_pause)
      self.next_arrangement.enabled = False
    else:
      self.arrangementModelDisplay.SetVisibility(False)
      self.removeActionObserver(leftControllerTransform)
      self.start_arrangement.setText('Start')
      self.start_arrangement.setIcon(self.start_arrangement_icon_play)
      self.next_arrangement.enabled = True

  def onStartPresentationClicked(self):
    start_stop = self.start_presentation.text
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    leftControllerTransform = vrViewNode.GetLeftControllerTransformNode()
    if start_stop == 'Start':
      self.presentationModelDisplay.SetVisibility(True)
      self.addActionObserver(leftControllerTransform)
      self.start_presentation.setText('Stop')
      self.start_presentation.setIcon(self.start_presentation_icon_pause)
      self.next_presentation.enabled = False
    else:
      self.presentationModelDisplay.SetVisibility(False)
      self.removeActionObserver(leftControllerTransform)
      self.start_presentation.setText('Start')
      self.start_presentation.setIcon(self.start_presentation_icon_play)
      self.next_presentation.enabled = True

  def onStartInitialPlacementLeftClicked(self):
    start_stop = self.start_initialPlacementLeft.text
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    leftControllerTransform = vrViewNode.GetLeftControllerTransformNode()
    if start_stop == 'Start':
      self.initialPlacementLeftModelDisplay.SetVisibility(True)
      self.addActionObserver(leftControllerTransform)
      self.start_initialPlacementLeft.setText('Stop')
      self.start_initialPlacementLeft.setIcon(self.start_initialPlacementLeft_icon_pause)
      self.next_initialPlacementLeft.enabled = False
    else:
      self.initialPlacementLeftModelDisplay.SetVisibility(False)
      self.removeActionObserver(leftControllerTransform)
      self.start_initialPlacementLeft.setText('Start')
      self.start_initialPlacementLeft.setIcon(self.start_initialPlacementLeft_icon_play)
      self.next_initialPlacementLeft.enabled = True

  def onStartFinalPlacementLeftClicked(self):
    start_stop = self.start_finalPlacementLeft.text
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    leftControllerTransform = vrViewNode.GetLeftControllerTransformNode()
    if start_stop == 'Start':
      self.finalPlacementLeftModelDisplay.SetVisibility(True)
      self.addActionObserver(leftControllerTransform)
      self.start_finalPlacementLeft.setText('Stop')
      self.start_finalPlacementLeft.setIcon(self.start_finalPlacementLeft_icon_pause)
      self.next_finalPlacementLeft.enabled = False
    else:
      self.finalPlacementLeftModelDisplay.SetVisibility(False)
      self.removeActionObserver(leftControllerTransform)
      self.start_finalPlacementLeft.setText('Start')
      self.start_finalPlacementLeft.setIcon(self.start_finalPlacementLeft_icon_play)
      self.next_finalPlacementLeft.enabled = True

  def onStartInitialPositionRClicked(self):
    start_stop = self.start_initialPlacementRight.text
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    rightControllerTransform = vrViewNode.GetRightControllerTransformNode()
    if start_stop == 'Start':
      self.initialPlacementRightModelDisplay.SetVisibility(True)
      self.addActionObserver(rightControllerTransform)
      self.start_initialPlacementRight.setText('Stop')
      self.start_initialPlacementRight.setIcon(self.start_initialPlacementRight_icon_pause)
      self.next_initialPlacementRight.enabled = False
    else:
      self.initialPlacementRightModelDisplay.SetVisibility(False)
      self.removeActionObserver(rightControllerTransform)
      self.start_initialPlacementRight.setText('Start')
      self.start_initialPlacementRight.setIcon(self.start_initialPlacementRight_icon_play)
      self.next_initialPlacementRight.enabled = True

  def onStartFinalPositionRClicked(self):
    start_stop = self.start_finalPlacementRight.text
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    rightControllerTransform = vrViewNode.GetRightControllerTransformNode()
    if start_stop == 'Start':
      self.finalPlacementRightModelDisplay.SetVisibility(True)
      self.addActionObserver(rightControllerTransform)
      self.start_finalPlacementRight.setText('Stop')
      self.start_finalPlacementRight.setIcon(self.start_finalPlacementRight_icon_pause)
      self.next_finalPlacementRight.enabled = False
    else:
      self.finalPlacementRightModelDisplay.SetVisibility(False)
      self.removeActionObserver(rightControllerTransform)
      self.start_finalPlacementRight.setText('Start')
      self.start_finalPlacementRight.setIcon(self.start_finalPlacementRight_icon_play)
      self.next_finalPlacementRight.enabled = True



  def addActionObserver(self, toolToReference):
    if self.callbackObserverTag == -1:
      self.observerClass = slicer.util.VTKObservationMixin()
      self.observerClass.addObserver(toolToReference, toolToReference.TransformModifiedEvent, self.callbackFunction)
      logging.info('addObserver')

    

  def removeActionObserver(self, toolToReference):
    self.observerClass.removeObservers()
    forcepsLeftModelDisplay = slicer.util.getNode('ForcepsLeftModel').GetModelDisplayNode()
    forcepsRightModelDisplay = slicer.util.getNode('ForcepsRightModel').GetModelDisplayNode()
    forcepsLeftModelDisplay.SetColor([0.8,0.8,0.8])
    forcepsRightModelDisplay.SetColor([0.8,0.8,0.8])

    # self.observerTag = toolToReference.RemoveObserver(self.observerTag)
    # self.callbackObserverTag = -1
    # # display message correct
    # viewNodeID = '2'
    # numberOfViews = 2
    # id = self.get3DViewIDfromViewNode(viewNodeID, numberOfViews)
    # if id == -1:
    #   print('Error: ViewNode not found')
    # else:
    #   view=slicer.app.layoutManager().threeDWidget(id).threeDView()
    #   # Set text to "Something"
    #   view.cornerAnnotation().SetText(vtk.vtkCornerAnnotation.UpperRight,"")
    #   # Set color to red
    #   view.cornerAnnotation().GetTextProperty().SetColor(0,1,0)
    #   # Update the view
    #   view.forceRender()
    logging.info('removeObserver')


  def callbackFunction(self, transformNode, event = None):
    message = ''
    forcepsLeftModelDisplay = slicer.util.getNode('ForcepsLeftModel').GetModelDisplayNode()
    forcepsRightModelDisplay = slicer.util.getNode('ForcepsRightModel').GetModelDisplayNode()
    if self.start_arrangement.text == 'Stop':
      margin = 5 + self.errorMargin_dist
      res, message = self.logic.checkArrangement(margin)
      if res:
        # self.displayCornerAnnotation(True, message)
        print('Correct!')
        forcepsLeftModelDisplay.SetColor([0,1,0])
        forcepsRightModelDisplay.SetColor([0,1,0])
      else:
        # self.displayCornerAnnotation(False, message)
        print('Incorrect')
        forcepsLeftModelDisplay.SetColor([1,0,0])
        forcepsRightModelDisplay.SetColor([1,0,0])
          
    elif self.start_presentation.text == 'Stop':
      # error in degrees
      margin = 22.5 + self.errorMargin_angle
      marginVertical = 0 + self.errorMargin_dist
      res, message = self.logic.checkPresentation(margin, marginVertical)
      if res:
        # self.displayCornerAnnotation(True, message)
        print('Correct!')
        forcepsLeftModelDisplay.SetColor([0,1,0])
        forcepsRightModelDisplay.SetColor([0,1,0])
      else:
        # self.displayCornerAnnotation(False, message)
        print('Incorrect')
        forcepsLeftModelDisplay.SetColor([1,0,0])
        forcepsRightModelDisplay.SetColor([1,0,0])

    elif self.start_initialPlacementLeft.text == 'Stop':
      # margin in degrees
      marginAngle = 10 + self.errorMargin_angle
      # margin in mm
      marginDistance = 10 + self.errorMargin_dist
      res, message = self.logic.checkInitialPlacementLeft(marginAngle,marginDistance)
      if res:
        # self.displayCornerAnnotation(True, message)
        print('Correct!')
        forcepsLeftModelDisplay.SetColor([0,1,0])
      else:
        # self.displayCornerAnnotation(False, message)
        print('Incorrect')
        forcepsLeftModelDisplay.SetColor([1,0,0])
      
    elif self.start_finalPlacementLeft.text == 'Stop':
      marginDistance = 30 + self.errorMargin_dist
      marginDistanceCheek = 10 + self.errorMargin_dist
      res, message = self.logic.checkFinalPlacementLeft(marginDistance, marginDistanceCheek)
      if res:
        # self.displayCornerAnnotation(True, message)
        print('Correct!')
        forcepsLeftModelDisplay.SetColor([0,1,0])
      else:
        # self.displayCornerAnnotation(False, message)
        print('Incorrect')
        forcepsLeftModelDisplay.SetColor([1,0,0])

    elif self.start_initialPlacementRight.text == 'Stop':
      # margin in degrees
      marginAngle = 10 + self.errorMargin_angle
      # margin in mm
      marginDistance = 10 + self.errorMargin_dist
      res, message = self.logic.checkInitialPositionR(marginAngle,marginDistance)
      if res:
        # self.displayCornerAnnotation(True, message)
        print('Correct!')
        forcepsRightModelDisplay.SetColor([0,1,0])
      else:
        # self.displayCornerAnnotation(False, message)
        print('Incorrect')
        forcepsRightModelDisplay.SetColor([1,0,0])
    
    elif self.start_finalPlacementRight.text == 'Stop':
      marginDistance = 30 + self.errorMargin_dist
      marginDistanceCheek = 10 + self.errorMargin_dist
      res, message = self.logic.checkFinalPositionR(marginDistance, marginDistanceCheek)
      if res:
        # self.displayCornerAnnotation(True, message)
        print('Correct!')
        forcepsRightModelDisplay.SetColor([0,1,0])
      else:
        # self.displayCornerAnnotation(False, message)
        print('Incorrect')
        forcepsRightModelDisplay.SetColor([1,0,0])



#
# ForcepsDeliveryVRLogic
#

class ForcepsDeliveryVRLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)
    self.vrEnabled = False
    self.threeDView = slicer.app.layoutManager().threeDWidget(0).threeDView()
    self.vrLogic = slicer.modules.virtualreality.logic()


  def activateVirtualReality(self):
    if (self.vrEnabled):
      return

    self.vrLogic.SetVirtualRealityConnected(True)    
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    vrViewNode.SetLighthouseModelsVisible(False)
    vrViewNode.SetControllerModelsVisible(False)

    # Just for being sure
    reference = slicer.app.layoutManager().threeDWidget(0).mrmlViewNode() # 3D View node
    vrViewNode.SetAndObserveReferenceViewNode(reference)
    # self.volumeRendDisplayNode.AddViewNodeID(vrViewNode.GetID())
    # self.setDefaultBackgroundColor(vrViewNode)


    self.vrEnabled = True

    # Devices transforms visible to the scene
    vrViewNode.SetControllerTransformsUpdate(True)
    vrViewNode.SetHMDTransformUpdate(True)

    vrViewNode.Modified()
    
    self.vrLogic.SetVirtualRealityActive(True)
  

  def applyForcepsTransform(self):
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    if not vrViewNode or not vrViewNode.GetControllerTransformsUpdate():
      return
      
    forcepsLeftModel = slicer.util.getNode(pattern="ForcepsLeftModel")
    forcepsLeftModel.SetAndObserveTransformNodeID(vrViewNode.GetLeftControllerTransformNodeID())

    forcepsRightModel = slicer.util.getNode(pattern="ForcepsRightModel")
    tranformNodeID = self.vrLogic.GetVirtualRealityViewNode().GetRightControllerTransformNodeID()
    forcepsRightModel.SetAndObserveTransformNodeID(tranformNodeID)

  def changeControllerVisibility(self, display):
    self.vrLogic.SetVirtualRealityConnected(True)    
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    vrViewNode.SetControllerModelsVisible(display)

  def resetVRView(self, zoomOut):
    vrLogic = slicer.modules.virtualreality.logic()
    vrViewNode = vrLogic.GetVirtualRealityViewNode()
    HMD_transform = vrViewNode.GetHMDTransformNode()
    try:
      modelHMDTransform = slicer.util.getNode('modelHMDTransform')
    except:
      modelHMDTransform = slicer.vtkMRMLLinearTransformNode()
      modelHMDTransform.SetName('modelHMDTransform')
      slicer.mrmlScene.AddNode(modelHMDTransform)
    # get the translation components from the HMD transform
    t_r = HMD_transform.GetMatrixTransformToParent().GetElement(0,3)
    t_a = HMD_transform.GetMatrixTransformToParent().GetElement(1,3)
    t_s = HMD_transform.GetMatrixTransformToParent().GetElement(2,3)
    cam = vrCamera()
    modelTransform = vtk.vtkMatrix4x4()
    modelHMDTransform.GetMatrixTransformToParent(modelTransform)
    modelTransform.Identity()
    modelTransform.SetElement(0, 3, t_r)
    modelTransform.SetElement(1, 3, t_a - zoomOut)
    modelTransform.SetElement(2, 3, t_s - 40)
    cam.SetModelTransformMatrix(modelTransform)
    modelHMDTransform.SetMatrixTransformToParent(modelTransform)
    # make the controllers coincide with the user (HMD) position in the VR scene
    # clone the transform
    nodeToClone = slicer.util.getNode('modelHMDTransform')
    shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
    itemIDToClone = shNode.GetItemByDataNode(nodeToClone)
    clonedItemID = slicer.modules.subjecthierarchy.logic().CloneSubjectHierarchyItem(shNode, itemIDToClone)
    viewControllersTransform = shNode.GetItemDataNode(clonedItemID)
    # invert
    viewControllersTransform.Inverse()
    # make the controllers (forceps) observe that transform
    leftControllerTransform = vrViewNode.GetLeftControllerTransformNode()
    rightControllerTransform = vrViewNode.GetRightControllerTransformNode()
    leftControllerTransform.SetAndObserveTransformNodeID(viewControllersTransform.GetID())
    rightControllerTransform.SetAndObserveTransformNodeID(viewControllersTransform.GetID())


  def checkArrangement(self,margin):
    message = ''
    print('checking')
    return True, message
    # # build transform tree to depend on ForcepsL
    # transformName = 'VirtualReality.LeftController'
    # if self.buildTransformTree(transformName):
    #   # get distances in every axis
    #   fiducials1name = 'CheckFiducialsL'
    #   fiducials2name = 'CheckFiducialsR'
    #   r,a,s = self.getDistanceCoordinates(fiducials1name,fiducials2name)
    #   # check if coordinates in A are within the margins
    #   num_fids = np.size(a)
    #   fidOutOfMargins = False
    #   # check in AP direction
    #   for i in range(num_fids):
    #     if not (-margin)<np.abs(a[i])<=(margin):
    #     #   print 'Arrangement CORRECT in fiducial ' + str(i) + ' (forwards)'
    #     # else:
    #       # print 'Arrangement INCORRECT in fiducial ' + str(i) + ' (forwards)'
    #       fidOutOfMargins = True
    #       message = message + 'HANDLES NOT AT THE SAME LEVEL\n'
    #       break
    #   for i in range(num_fids-1):
    #     if not (-margin)<np.abs(r[i])<=(margin):
    #     #   print 'Arrangement CORRECT in fiducial ' + str(i) + ' (horizontal)'
    #     # else:
    #     #   print 'Arrangement INCORRECT in fiducial ' + str(i) + ' (horizontal)'
    #       fidOutOfMargins = True
    #       message = message + 'FORCEPS NOT CORRECTLY CLOSED\n'
    #       break
    #   if fidOutOfMargins:
        
    #     return False, message
    #   else:
    #     return True, message

  def checkPresentation(self,margin,marginVertical):
    message = ''
    return True, message
    # # build transform tree to depend on Baby
    # transformName = 'BabyHeadModelToBabyHead'
    # if self.buildTransformTree(transformName):
    #   # get distances in every axis
    #   fiducials1name = 'CheckFiducialsL'
    #   fiducials2name = 'CheckFiducialsR'
    #   r,a,s = self.getDistanceCoordinates(fiducials1name,fiducials2name)
    #   # check if coordinates in A are within the margins
    #   num_fids = np.size(a)
    #   fidOutOfMargins = False
    #   # check in IS direction
    #   for i in range(num_fids-1):
    #     if not s[i]<(marginVertical):
    #     #   print 'Arrangement CORRECT in fiducial ' + str(i) + ' (vertical)'
    #     # else:
    #     #   print 'Arrangement INCORRECT in fiducial ' + str(i) + ' (vertical)'
    #       fidOutOfMargins = True
    #       message = message + 'FORCEPS UPSIDE DOWN\n'
    #       break
    #   # check if rotation in A is bigger than the margin
    #   fiducials1name_ideal = 'CheckFiducialsL_finalPosition'
    #   fiducials2name_ideal = 'CheckFiducialsR_finalPosition'
    #   anglesL, translationL = self.checkRegistrationComponents(fiducials1name, fiducials1name_ideal)
    #   anglesR, translationR = self.checkRegistrationComponents(fiducials2name, fiducials2name_ideal)
    #   for i in range(3):
    #     anglesL[i] = math.degrees(anglesL[i])
    #     # print 'Angle L ' + str(i) + ': ' + str(anglesL[i])
    #     anglesR[i] = math.degrees(anglesR[i])
    #     # print 'Angle R ' + str(i) + ': ' + str(anglesR[i])
    #   if np.abs(anglesL[1])>margin:
    #     fidOutOfMargins = True
    #     # print 'Rotation of Forceps Left of: ' + str(anglesL[1]) + ' degrees in AP'
    #     message = message + 'LEFT FORCEPS ROTATED\n'
    #   if np.abs(anglesR[1])>margin:
    #     fidOutOfMargins = True
    #     # print 'Rotation of Forceps Right of: ' + str(anglesR[1]) + ' degrees in AP'
    #     message = message + 'RIGHT FORCEPS ROTATED\n'
    #   # remove created nodes
    #   fidsWorld = slicer.util.getNode('FidsWorld')
    #   slicer.mrmlScene.RemoveNode(fidsWorld)
    #   fidsWorld = slicer.util.getNode('FidsWorld')
    #   slicer.mrmlScene.RemoveNode(fidsWorld)
    #   regL = slicer.util.getNode('RegistrationCheckRotation')
    #   slicer.mrmlScene.RemoveNode(regL)
    #   regR = slicer.util.getNode('RegistrationCheckRotation')
    #   slicer.mrmlScene.RemoveNode(regR)

    #   if fidOutOfMargins:
    #     return False, message
    #   else:
    #     return True, message



  def checkInitialPlacementLeft(self, marginAngle, marginDistance):
    message = ''
    return True, message
    # # build transform tree to depend on Baby
    # transformName = 'BabyHeadModelToBabyHead'
    # if self.buildTransformTree(transformName):
    #   fiducials1name = 'CheckFiducialsL'
    #   # Check the angle between the vertical and our fiducials in Forceps
    #   angle = self.checkVectorsAngle(fiducials1name)
    #   # print 'Angle to ideal direction: ' + str(angle) + '. Margin is ' + str(marginAngle) + ' degrees'
    #   fidOutOfMargins = False
    #   if np.abs(angle)>marginAngle:
    #     fidOutOfMargins = True
    #     message = message + 'INCORRECT ANGLE\n'
    #   # Check the tip of the forceps is in contact with the baby's head
    #   modelName = 'BabyHeadModel'
    #   dist = self.getDistancePointToModel(fiducials1name,modelName)
    #   # print 'Distance to baby: ' + str(dist) + '. Margin is ' + str(marginDistance) + ' mm'
    #   if dist == None:
    #     print('Error: No intersections found')
    #     # fidOutOfMargins = True
    #   elif dist>marginDistance:
    #     fidOutOfMargins = True
    #     message = message + 'TIP TOO FAR FROM FETUS\n'
    #     # print 'Distance out of margin'
    #   # else:
    #   #   print 'Distance within margin'
    #   if fidOutOfMargins:
    #     return False, message
    #   else:
    #     return True, message

  def checkFinalPlacementLeft(self, marginDistance, marginDistanceCheek):
    message = ''
    return True, message
    # # build transform tree to depend on Baby
    # transformName = 'BabyHeadModelToBabyHead'
    # if self.buildTransformTree(transformName):
    #   fiducials1name = 'CheckFiducialsL'
    #   # Check the distance between the tip of the forceps and the eye
    #   dist_eye = self.checkDistanceToEye(fiducials1name, 'left')
    #   # print 'Distance to eye: ' + str(dist_eye) + '. Margin is ' + str(marginDistance) + ' mm'
    #   fidOutOfMargins = False
    #   if not marginDistance<np.abs(dist_eye)<(marginDistance*2):
    #     fidOutOfMargins = True
    #     if marginDistance>np.abs(dist_eye):
    #       message = message + 'TOO CLOSE TO EYE\n'
    #     else:
    #       message = message + 'TOO FAR FROM EYE\n'
    #   # Check the distance between the tip of the forceps and the ear
    #   dist_ear = self.checkDistanceToEar(fiducials1name, 'left')
    #   # print 'Distance to ear: ' + str(dist_ear) + '. Margin is ' + str(marginDistance) + ' mm'
    #   if not marginDistance<np.abs(dist_ear)<(marginDistance*2):
    #     fidOutOfMargins = True
    #     if marginDistance>np.abs(dist_ear):
    #       message = message + 'TOO CLOSE TO EAR\n'
    #     else:
    #       message = message + 'TOO FAR FROM EAR\n'

    #   # Check the distance between the tip of the forceps and the cheek
    #   modelName = 'BabyHeadModel'
    #   dist = self.getDistancePointToModel(fiducials1name,modelName)
    #   # print 'Distance to baby: ' + str(dist) + '. Margin is ' + str(marginDistanceCheek) + ' mm'
    #   if dist == None:
    #     print('Error: No intersections found')
    #     # fidOutOfMargins = True
    #   elif dist>marginDistanceCheek:
    #     fidOutOfMargins = True
    #     message = message + 'TOO FAR FROM CHEEKS\n'
    #     # print 'Distance out of margin'
    #   # else:
    #   #   print 'Distance within margin'
    #   if fidOutOfMargins:
    #     return False, message
    #   else:
    #     return True, message

  def checkInitialPositionR(self,marginAngle, marginDistance):
    message = ''
    return True, message
    # # build transform tree to depend on Baby
    # transformName = 'BabyHeadModelToBabyHead'
    # if self.buildTransformTree(transformName):
    #   fiducials1name = 'CheckFiducialsR'
    #   # Check the angle between the vertical and our fiducials in Forceps
    #   angle = self.checkVectorsAngle(fiducials1name)
    #   # print 'Angle to ideal direction: ' + str(angle) + '. Margin is ' + str(marginAngle) + ' degrees'
    #   fidOutOfMargins = False
    #   if np.abs(angle)>marginAngle:
    #     fidOutOfMargins = True
    #     message = message + 'INCORRECT ANGLE\n'
    #   # Check the tip of the forceps is in contact with the baby's head
    #   modelName = 'BabyHeadModel'
    #   dist = self.getDistancePointToModel(fiducials1name,modelName)
    #   # print 'Distance to baby: ' + str(dist) + '. Margin is ' + str(marginDistance) + ' mm'
    #   if dist == None:
    #     print('Error: No intersections found')
    #     # fidOutOfMargins = True
    #   elif dist>marginDistance:
    #     fidOutOfMargins = True
    #     message = message + 'TIP TOO FAR FROM FETUS\n'
    #   #   print 'Distance out of margin'
    #   # else:
    #   #   print 'Distance within margin'
    #   if fidOutOfMargins:
    #     return False, message
    #   else:
    #     return True, message

  def checkFinalPositionR(self, marginDistance, marginDistanceCheek):
    message = ''
    return True, message
    # # build transform tree to depend on Baby
    # transformName = 'BabyHeadModelToBabyHead'
    # if self.buildTransformTree(transformName):
    #   fiducials1name = 'CheckFiducialsR'
    #   # Check the distance between the tip of the forceps and the eye
    #   dist_eye = self.checkDistanceToEye(fiducials1name, 'right')
    #   # print 'Distance to eye: ' + str(dist_eye) + '. Margin is ' + str(marginDistance) + ' mm'
    #   fidOutOfMargins = False
    #   if not marginDistance<np.abs(dist_eye)<(marginDistance*2):
    #     fidOutOfMargins = True
    #     if marginDistance>np.abs(dist_eye):
    #       message = message + 'TOO CLOSE TO EYE\n'
    #     else:
    #       message = message + 'TOO FAR FROM EYE\n'
    #   # Check the distance between the tip of the forceps and the ear
    #   dist_ear = self.checkDistanceToEar(fiducials1name, 'right')
    #   # print 'Distance to ear: ' + str(dist_ear) + '. Margin is ' + str(marginDistance) + ' mm'
    #   if not marginDistance<np.abs(dist_ear)<(marginDistance*2):
    #     fidOutOfMargins = True
    #     if marginDistance>np.abs(dist_ear):
    #       message = message + 'TOO CLOSE TO EAR\n'
    #     else:
    #       message = message + 'TOO FAR FROM EAR\n'

    #   # Check the distance between the tip of the forceps and the cheek
    #   modelName = 'BabyHeadModel'
    #   dist = self.getDistancePointToModel(fiducials1name,modelName)
    #   # print 'Distance to baby: ' + str(dist) + '. Margin is ' + str(marginDistanceCheek) + ' mm'
    #   if dist == None:
    #     print('Error: No intersections found')
    #     # fidOutOfMargins = True
    #   elif dist>marginDistanceCheek:
    #     fidOutOfMargins = True
    #     message = message + 'TOO FAR FROM CHEEKS\n'
    #   #   print 'Distance out of margin'
    #   # else:
    #   #   print 'Distance within margin'
    #   if fidOutOfMargins:
    #     return False, message
    #   else:
    #     return True, message



  
def isVRInitialized():
  """Determine if VR has been initialized
  """
  vrLogic = slicer.modules.virtualreality.logic()
  if (vrLogic is None
      or vrLogic.GetVirtualRealityViewNode() is None
      or not vrLogic.GetVirtualRealityViewNode().GetVisibility()
      or not vrLogic.GetVirtualRealityViewNode().GetActive()):
      return False
  return True

def vrCamera():
  # Get VR module widget
  if not isVRInitialized():
      return None
  # Get VR camera
  vrViewWidget = slicer.modules.virtualreality.viewWidget()
  if vrViewWidget is None:
    return None
  rendererCollection = vrViewWidget.renderWindow().GetRenderers()
  if rendererCollection.GetNumberOfItems() < 1:
      logging.error('Unable to access VR renderers')
      return None
  return rendererCollection.GetItemAsObject(0).GetActiveCamera()


