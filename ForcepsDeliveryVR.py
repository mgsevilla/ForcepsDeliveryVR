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
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["Monica Garcia-Sevilla (Universidad de Las Palmas de Gran Canaria)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#ForcepsDeliveryVR">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
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
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Widget variables
    self.logic = ForcepsDeliveryVRLogic()

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    # uiWidget = slicer.util.loadUI(self.resourcePath('UI/ForcepsDeliveryVR.ui'))
    # self.layout.addWidget(uiWidget)
    # self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    # uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = ForcepsDeliveryVRLogic()

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    # self.ui.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    # self.ui.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    # self.ui.imageThresholdSliderWidget.connect("valueChanged(double)", self.updateParameterNodeFromGUI)
    # self.ui.invertOutputCheckBox.connect("toggled(bool)", self.updateParameterNodeFromGUI)
    # self.ui.invertedOutputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)

    
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


    # connections
    # LOADING
    self.activateVRButton.connect('clicked(bool)', self.onSwitchVirtualRealityActivation)
    self.loadDataButton.connect('clicked(bool)', self.onLoadDataButtonClicked)


    # Add vertical spacer
    self.layout.addStretch(1)


  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    print('enter')

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    #self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    print('exit')

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    print('scene start close')


  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    # if self.parent.isEntered:
    #   self.initializeParameterNode()
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
    print('load')




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
    # self.volRenLogic = slicer.modules.volumerendering.logic()
    self.vrLogic = slicer.modules.virtualreality.logic()

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


  def activateVirtualReality(self):
    if (self.vrEnabled):
      return
    self.vrLogic.SetVirtualRealityConnected(True)
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    vrViewNode.SetLighthouseModelsVisible(False)
    # self.volumeRendDisplayNode.AddViewNodeID(vrViewNode.GetID())
    # self.setDefaultBackgroundColor(vrViewNode)
    self.vrLogic.SetVirtualRealityActive(True)
    self.vrEnabled = True

  def deactivateVirtualReality(self):
    if (not self.vrEnabled):
      return
    self.vrLogic.SetVirtualRealityConnected(False)
    self.vrLogic.SetVirtualRealityActive(False)
    self.vrEnabled = False


  


