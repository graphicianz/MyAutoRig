import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader 
import time as t
import os
import shutil
import json
import maya.mel as mm

class myautorig():
	def __init__(self):
		UI_FILE = r"G:\MEGA_Script\MyAutoRig\design.ui"

		self.convertToRelative(UI_FILE)

		ui_file = QFile(UI_FILE)
		ui_file.open(QFile.ReadOnly)
		loader = QUiLoader()
		self.ui = loader.load(ui_file)
		ui_file.close()


		self.rootPath = self.initRoot()
		self.ui.setroot_btt.clicked.connect(self.setRootClicked)

		self.ui.createNew_btt.clicked.connect(self.createNewClicked)	

		self.ui.existsRig_btt.clicked.connect(self.readExistsRigClicked)


		#process#
		self.ui.newScene_btt.clicked.connect(self.newSceneClicked)
		self.ui.importModel_btt.clicked.connect(self.importModelClicked)
		self.ui.createGroup_btt.clicked.connect(self.createGroupClicked)
		self.ui.importSkeleton_btt.clicked.connect(self.rebuildSkeletonClicked)
		self.ui.buildBiped_btt.clicked.connect(self.buildBipedClicked)
		self.ui.buildBody_btt.clicked.connect(self.buildBodyClicked)
		self.ui.buildLeg_btt.clicked.connect(self.buildLegClicked)
		self.ui.buildArm_btt.clicked.connect(self.buildArmClicked)
		self.ui.buildFinger_btt.clicked.connect(self.buildFingerClicked)
		#########

		self.ui.saveChange_btt.clicked.connect(self.saveChangeClicked)
		self.ui.buildRig_btt.clicked.connect(self.buildRigClicked)

		self.iconColorDict = {'BLANK': "G:\MEGA_Script\MyAutoRig\icon\circle_gray.png",
		                      'GREEN': "G:\MEGA_Script\MyAutoRig\icon\circle_green.png",
		                      "RED": "G:\MEGA_Script\MyAutoRig\icon\circle_red.png"}

		self.GREEN = "background-color: rgb(102, 116, 5);"
		self.RED = "background-color: rgb(100, 29, 45);"
		self.initDataDict = {"modelPath": "", "groupName": "Geo_GRP",
		                     "01_newScene_checkbox_status": True,
		                     "02_importModel_checkbox_status": True,
		                     "03_createGroup_checkbox_status": True}

		self.initSkeletonSpinDict = {"spine1_jnt":{'tx':0.0,'ty':70.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':0.0,'jointOrientZ':0.0},
		                             "spine2_jnt":{'tx':0.0,'ty':30.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':0.0,'jointOrientZ':0.0},
		                             "spine3_jnt":{'tx':0.0,'ty':30.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':0.0,'jointOrientZ':0.0},
		                             "spine4_jnt":{'tx':0.0,'ty':30.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':0.0,'jointOrientZ':0.0},
		                             "spine5_jnt":{'tx':0.0,'ty':30.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':0.0,'jointOrientZ':0.0}}

		self.initSkeletonLegDict = {"upperLeg_L_jnt":{'tx':18.445,'ty':70.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':-5.0,'jointOrientZ':-90.0},
								    "lowerLeg_L_jnt":{'tx':30.0,'ty':0.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':10.0,'jointOrientZ':0.0},
								    "foot_L_jnt":{'tx':30.0,'ty':0.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':-60.0,'jointOrientZ':0.0},
								    "toeBase_L_jnt":{'tx':17.731,'ty':0.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':-35.0,'jointOrientZ':0.0},
								    "toeEnd_L_jnt":{'tx':20.0,'ty':0.0,'tz':0.0,'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':0.0,'jointOrientY':10.0,'jointOrientZ':0.0}}	                             
		self.initSkeletonDict = {"spine":self.initSkeletonSpinDict,
		                         "leg":self.initSkeletonLegDict}



		self.ui.newScene2_btt.clicked.connect(self.newSceneClicked)
		self.ui.importModel2_btt.clicked.connect(self.importModelClicked)
		self.ui.rebuildSkeleton_btt.clicked.connect(self.rebuildSkeletonClicked)
		self.ui.exportSetting_btt.clicked.connect(self.exportSettingClicked)
		self.ui.exportSkeleton_btt.clicked.connect(self.exportSkeletonClicked)

		self.statusIconList = [self.ui.newSceneIcon,
		                       self.ui.importModelIcon,
		                       self.ui.createGroupIcon,
		                       self.ui.importSkeletonIcon,
		                       self.ui.buildBipedIcon,
		                       self.ui.buildBodyIcon,
		                       self.ui.buildLegIcon,
		                       self.ui.buildArmIcon,
		                       self.ui.buildFingerIcon]

		self.ui.setWindowFlags(Qt.WindowStaysOnTopHint)		                  

	def convertToRelative(self, ui_file):
		keywordList = [["<pixmap>icon/", "<pixmap>G:/MEGA_Script/MyAutoRig/icon/"],
		               ["<normalon>icon/", "<normalon>G:/MEGA_Script/MyAutoRig/icon/"]]
		for keyword in keywordList:		              
			with open(ui_file) as r:
				#<pixmap>icon/
				text = r.read().replace(keyword[0], keyword[1])
			with open(ui_file, "w") as w:
				w.write(text)

	def setStatusIcon(self, status, component):
		#status ['BLANK', 'GREEN', 'RED']
		component.setPixmap(self.iconColorDict[status])
		cmds.refresh()

	def clearStatusIcon(self):
		# iconList = [self.ui.newSceneIcon,
		#             self.ui.importModelIcon,
		#             self.ui.createGroupIcon]

		for icon in self.statusIconList:
			self.setStatusIcon('BLANK', icon)

	def setBlink(self, component, style, emptystyle="", timer=200):
		component.setStyleSheet(style)
		QTimer.singleShot(timer, lambda: component.setStyleSheet(emptystyle))

	def setStyle(self, component, style):
		component.setStyleSheet(style)

	def createFolder(self, path):
		os.mkdir(path)

	def sendConsole(self,text, append=False):
		if append:
			tmp = self.ui.logConsole_tb.toPlainText()
			self.ui.logConsole_tb.setText(tmp+text)
		else:
			self.ui.logConsole_tb.setText(text)

	### root ###
	def initRoot(self):
		#read init file#
		f = open(r"G:\MEGA_Script\MyAutoRig\init.ini",'r')
		text = f.readline()
		self.ui.root_tb.setText(text)
		f.close()
		return text

	def setRootClicked(self):
		gettext = self.ui.root_tb.text()
		f = open(r"G:\MEGA_Script\MyAutoRig\init.ini",'w')
		f.write(gettext)
		f.close()

		self.setBlink(self.ui.root_tb, self.GREEN)
		self.setStyle(self.ui.logConsole_tb, "")

		self.ui.logConsole_tb.setText("set root path to {0}".format(gettext))

		self.rootPath = gettext
	############

	### create new ###
	def createNewClicked(self):
		rigname = self.ui.createNew_tb.text()

		parent = self.ui.root_tb.text()
		try:
			os.mkdir(parent+'\\'+rigname)

			self.ui.existsRig_tb.setText(rigname)
			self.ui.logConsole_tb.setText("create rig : {0}\nto path : {1}".format(rigname,parent+'\\'+rigname))
			self.setStyle(self.ui.logConsole_tb, "")
			self.setBlink(self.ui.createNew_tb, self.GREEN)

			self.initNewRig(parent+'\\'+rigname)
		except Exception,e:
			self.setBlink(self.ui.createNew_tb, self.RED)
			self.setStyle(self.ui.logConsole_tb, self.RED)
			#self.ui.createNew_tb.setStyleSheet("background-color: rgb(100, 29, 45);")
			#self.ui.logConsole_tb.setStyleSheet("background-color: rgb(100, 29, 45);")
			#QTimer.singleShot(200, lambda: self.ui.createNew_tb.setStyleSheet(""))		
			self.ui.logConsole_tb.setText("can not create rig name : {0}\n{1}".format(rigname, e))
			self.ui.existsRig_tb.setText("")

	def initNewRig(self, rigPath):
		self.createFolder(rigPath+'\\model')
		self.createFolder(rigPath+'\\skinweight')
		self.createFolder(rigPath+'\\published')

		f = open(rigPath+'\\rigdata.json', 'w')
		f.close()

		f2 = open(rigPath+'\\skeletondata.json', 'w')
		f2.close()

		if os.path.exists(self.ui.model_tb.text()):
			source = self.ui.model_tb.text()
			modelFile = source.split('\\')[-1]
			dest = rigPath+'\\model\\{0}'.format(modelFile)
			shutil.copyfile(source, dest)

			#dataDict = {"modelPath": dest, "groupName": "Geo_GRP"}
			self.initDataDict['modelPath'] = dest
			with open(rigPath+'\\rigdata.json', 'w') as json_file:
  				json.dump(self.initDataDict, json_file)

			with open(rigPath+'\\skeletondata.json', 'w') as json_file:
  				json.dump(self.initSkeletonDict, json_file)  				

		self.ui.modelPath_tb.setText(dest)
		self.ui.groupName_tb.setText("Geo_GRP")

		self.ui.newScene_cb.setChecked(self.initDataDict['01_newScene_checkbox_status'])
		self.ui.importModel_cb.setChecked(self.initDataDict['02_importModel_checkbox_status'])
		self.ui.createGroup_cb.setChecked(self.initDataDict['03_createGroup_checkbox_status'])		

		#copy skeleton#
		skeletonSource = r"G:\MEGA_Script\MyAutoRig\skeleton.ma"
		skeletonDest = rigPath+'\\skeleton.ma'
		shutil.copyfile(skeletonSource, skeletonDest)

		self.sendConsole('\ncreate {0}model'.format(rigPath), append=True)
		self.sendConsole('\ncreate {0}skinweight'.format(rigPath), append=True)
		self.sendConsole('\ncreate {0}published'.format(rigPath), append=True)
		self.sendConsole('\ncreate {0}rigdata.json'.format(rigPath), append=True)

		if os.path.exists(self.ui.model_tb.text()):
			self.sendConsole('\ncopy from {0} to {1}'.format(source, dest), append=True)

		self.fullRigPath = rigPath
		self.fullSkeletonPath = skeletonDest

		self.clearStatusIcon()

	############


	### read exists rig ###
	def readExistsRigClicked(self):
		try:
			existsRig = self.rootPath+'\\'+self.ui.existsRig_tb.text()
			self.fullRigPath = existsRig
			self.fullSkeletonPath = existsRig+'\\skeleton.ma'

			#read json#
			# with open(existsRig+'\\rigdata.json', 'r') as f:
			# 	data = json.load(f)		
			f = open(existsRig+'\\rigdata.json', 'r')
			self.data = json.load(f)
			modelPath = self.data['modelPath']
			groupName = self.data['groupName']
			self.ui.modelPath_tb.setText(modelPath)
			self.ui.groupName_tb.setText(groupName)
			self.fullRigPath = existsRig
			self.ui.model_tb.setText(modelPath)

			#read checkbox status#
			self.ui.newScene_cb.setChecked(bool(self.data['01_newScene_checkbox_status']))
			self.ui.importModel_cb.setChecked(bool(self.data['02_importModel_checkbox_status']))
			self.ui.createGroup_cb.setChecked(bool(self.data['03_createGroup_checkbox_status']))

			self.sendConsole('read {0}'.format(existsRig), append=False)

		except Exception,e:
			print('read error')
			print(e)
			self.sendConsole(str(e), append=False)

		self.clearStatusIcon()


	############

	### process ###
	def newSceneClicked(self):
		try:
			scene = cmds.file(new=True, force=True)
			self.setStatusIcon('GREEN', self.ui.newSceneIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.newSceneIcon)
			self.sendConsole(str(e), append=False)

	def importModelClicked(self):
		try:
			cmds.file(self.ui.modelPath_tb.text(), i=True)
			self.setStatusIcon('GREEN', self.ui.importModelIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.importModelIcon)
			self.sendConsole(str(e), append=False)		

	def buildBipedClicked(self):
		#side
		#type
		#otherType
		self.SIDE = {'LEFT':1, 'RIGHT':2}
		self.TYPE = {'NONE':0, 'ROOT':1, 'HIP':2, 'KNEE':3, 'FOOT':4, 'TOE':5, 'SPINE':6, 'NECK':7, 'HEAD':8,
		             'COLLAR':9, 'SHOULDER':10, 'ELBOW':11, 'HAND':12, 'FINGER':13, 'THUMB':14, 'PROPA':15, 'PROPB':16, 'PROPC':17,
		             'OTHER':18, 'INDEXFINGER':19, 'MIDDLEFINGER':20, 'RINGFINGER':21, 'PINKYFINGER':22, 'EXTRAFINGER':23,
		             'BIGTOE':24, 'INDEXTOE':25, 'MIDDLETOE':26, 'RINGTOE':27, 'PINKYTOE':28, 'FOOTTHUMB':29}
		print('build biped')

		try:
			cmds.group( em=True, name='BindJnt_Grp')
			cmds.select(clear=True)

			#build spine joint#
			RootBND_jnt = cmds.joint(name='RootBND_jnt')
			HipBND_jnt = cmds.joint(name='HipBND_jnt')
			self.snapTo('Root', RootBND_jnt, False)

			Spine0BND_jnt = cmds.joint(name='Spine0BND_jnt')
			self.snapTo('Root', Spine0BND_jnt, False)
			Spine1BND_jnt = cmds.joint(name='Spine1BND_jnt')
			self.snapTo('Spine1', Spine1BND_jnt, False)
			Spine2BND_jnt = cmds.joint(name='Spine2BND_jnt')
			self.snapTo('Spine2', Spine2BND_jnt, False)	
			Spine3BND_jnt = cmds.joint(name='Spine3BND_jnt')
			self.snapTo('Chest', Spine3BND_jnt, False)	

			ChestBND_jnt = cmds.joint(name='ChestBND_jnt')
			self.snapTo('Chest', ChestBND_jnt, False)				

			#build leg joint#
			cmds.select(HipBND_jnt)
			UpperLegBND_LFT_jnt = cmds.joint(name='UpperLegBND_LFT_jnt')	
			self.snapTo('upperLeg', UpperLegBND_LFT_jnt, False)	
			LowerLegBND_LFT_jnt = cmds.joint(name='LowerLegBND_LFT_jnt')	
			self.snapTo('lowerLeg', LowerLegBND_LFT_jnt, False)		
			FootBND_LFT_jnt = cmds.joint(name='FootBND_LFT_jnt')	
			self.snapTo('Foot', FootBND_LFT_jnt, False)
			ToeBND_LFT_jnt = cmds.joint(name='ToeBND_LFT_jnt')	
			self.snapTo('Toe', ToeBND_LFT_jnt, False)	
			ToeEndBND_LFT_jnt = cmds.joint(name='ToeEndBND_LFT_jnt')	
			self.snapTo('ToeEnd', ToeEndBND_LFT_jnt, False)		

			#build neck joint#
			cmds.select(ChestBND_jnt)
			NeckBND_jnt = cmds.joint(name='NeckBND_jnt')
			self.snapTo('Neck', NeckBND_jnt, False)
			HeadBND_jnt = cmds.joint(name='HeadBND_jnt')
			self.snapTo('Head', HeadBND_jnt, False)
			HeadEndBND_jnt = cmds.joint(name='HeadEndBND_jnt')
			self.snapTo('HeadEnd', HeadEndBND_jnt, False)			

			#build arm joint#
			cmds.select(ChestBND_jnt)
			ShoulderBND_LFT_jnt = cmds.joint(name='ShoulderBND_LFT_jnt')	
			self.snapTo('Scapula', ShoulderBND_LFT_jnt, False)
			UpperArmBND_LFT_jnt = cmds.joint(name='UpperArmBND_LFT_jnt')	
			self.snapTo('Shoulder', UpperArmBND_LFT_jnt, False)	
			LowerArmBND_LFT_jnt = cmds.joint(name='LowerArmBND_LFT_jnt')	
			self.snapTo('Elbow', LowerArmBND_LFT_jnt, False)
			HandBND_LFT_jnt = cmds.joint(name='HandBND_LFT_jnt')	
			self.snapTo('Wrist', HandBND_LFT_jnt, False)

			#build finger joint#
			ThumbFinger1BND_LFT_jnt = cmds.joint(name='ThumbFinger1BND_LFT_jnt')	
			self.snapTo('ThumbFinger1', ThumbFinger1BND_LFT_jnt, False)	
			ThumbFinger2BND_LFT_jnt = cmds.joint(name='ThumbFinger2BND_LFT_jnt')	
			self.snapTo('ThumbFinger2', ThumbFinger2BND_LFT_jnt, False)	
			ThumbFinger3BND_LFT_jnt = cmds.joint(name='ThumbFinger3BND_LFT_jnt')	
			self.snapTo('ThumbFinger3', ThumbFinger3BND_LFT_jnt, False)		
			ThumbFinger4BND_LFT_jnt = cmds.joint(name='ThumbFinger4BND_LFT_jnt')	
			self.snapTo('ThumbFinger4', ThumbFinger4BND_LFT_jnt, False)		

			cmds.select('HandBND_LFT_jnt')
			IndexFinger1BND_LFT_jnt = cmds.joint(name='IndexFinger1BND_LFT_jnt')	
			self.snapTo('IndexFinger1', IndexFinger1BND_LFT_jnt, False)	
			IndexFinger2BND_LFT_jnt = cmds.joint(name='IndexFinger2BND_LFT_jnt')	
			self.snapTo('IndexFinger2', IndexFinger2BND_LFT_jnt, False)	
			IndexFinger3BND_LFT_jnt = cmds.joint(name='IndexFinger3BND_LFT_jnt')	
			self.snapTo('IndexFinger3', IndexFinger3BND_LFT_jnt, False)		
			IndexFinger4BND_LFT_jnt = cmds.joint(name='IndexFinger4BND_LFT_jnt')	
			self.snapTo('IndexFinger4', IndexFinger4BND_LFT_jnt, False)		

			cmds.select('HandBND_LFT_jnt')
			MidFinger1BND_LFT_jnt = cmds.joint(name='MidFinger1BND_LFT_jnt')	
			self.snapTo('MidFinger1', MidFinger1BND_LFT_jnt, False)	
			MidFinger2BND_LFT_jnt = cmds.joint(name='MidFinger2BND_LFT_jnt')	
			self.snapTo('MidFinger2', MidFinger2BND_LFT_jnt, False)	
			MidFinger3BND_LFT_jnt = cmds.joint(name='MidFinger3BND_LFT_jnt')	
			self.snapTo('MidFinger3', MidFinger3BND_LFT_jnt, False)		
			MidFinger4BND_LFT_jnt = cmds.joint(name='MidFinger4BND_LFT_jnt')	
			self.snapTo('MidFinger4', MidFinger4BND_LFT_jnt, False)		
			
			cmds.select('HandBND_LFT_jnt')
			CupBND_LFT_jnt = cmds.joint(name='CupBND_LFT_jnt')	
			self.snapTo('Cup', CupBND_LFT_jnt, False)	

			cmds.select(CupBND_LFT_jnt)
			RingFinger1BND_LFT_jnt = cmds.joint(name='RingFinger1BND_LFT_jnt')	
			self.snapTo('RingFinger1', RingFinger1BND_LFT_jnt, False)	
			RingFinger2BND_LFT_jnt = cmds.joint(name='RingFinger2BND_LFT_jnt')	
			self.snapTo('RingFinger2', RingFinger2BND_LFT_jnt, False)	
			RingFinger3BND_LFT_jnt = cmds.joint(name='RingFinger3BND_LFT_jnt')	
			self.snapTo('RingFinger3', RingFinger3BND_LFT_jnt, False)		
			RingFinger4BND_LFT_jnt = cmds.joint(name='RingFinger4BND_LFT_jnt')	
			self.snapTo('RingFinger4', RingFinger4BND_LFT_jnt, False)	

			cmds.select(CupBND_LFT_jnt)
			PinkyFinger1BND_LFT_jnt = cmds.joint(name='PinkyFinger1BND_LFT_jnt')	
			self.snapTo('PinkyFinger1', PinkyFinger1BND_LFT_jnt, False)	
			PinkyFinger2BND_LFT_jnt = cmds.joint(name='PinkyFinger2BND_LFT_jnt')	
			self.snapTo('PinkyFinger2', PinkyFinger2BND_LFT_jnt, False)	
			PinkyFinger3BND_LFT_jnt = cmds.joint(name='PinkyFinger3BND_LFT_jnt')	
			self.snapTo('PinkyFinger3', PinkyFinger3BND_LFT_jnt, False)		
			PinkyFinger4BND_LFT_jnt = cmds.joint(name='PinkyFinger4BND_LFT_jnt')	
			self.snapTo('PinkyFinger4', PinkyFinger4BND_LFT_jnt, False)	

			#build ik fk arm#
			cmds.select('ShoulderBND_LFT_jnt')
			UpperArmIK_LFT_jnt = cmds.joint(name='UpperArmIK_LFT_jnt')	
			self.snapTo('Shoulder', UpperArmIK_LFT_jnt, False)	
			LowerArmIK_LFT_jnt = cmds.joint(name='LowerArmIK_LFT_jnt')	
			self.snapTo('Elbow', LowerArmIK_LFT_jnt, False)			
			HandIK_LFT_jnt = cmds.joint(name='HandIK_LFT_jnt')	
			self.snapTo('Wrist', HandIK_LFT_jnt, False)
			HandEndIK_LFT_jnt = cmds.joint(name='HandEndIK_LFT_jnt')	
			self.snapTo('MidFinger1BND_LFT_jnt', HandEndIK_LFT_jnt, False)			

			cmds.select('ShoulderBND_LFT_jnt')
			UpperArmFK_LFT_jnt = cmds.joint(name='UpperArmFK_LFT_jnt')	
			self.snapTo('Shoulder', UpperArmFK_LFT_jnt, False)	
			LowerArmFK_LFT_jnt = cmds.joint(name='LowerArmFK_LFT_jnt')	
			self.snapTo('Elbow', LowerArmFK_LFT_jnt, False)			
			HandFK_LFT_jnt = cmds.joint(name='HandFK_LFT_jnt')	
			self.snapTo('Wrist', HandFK_LFT_jnt, False)		
			HandEndFK_LFT_jnt = cmds.joint(name='HandEndFK_LFT_jnt')	
			self.snapTo('MidFinger1BND_LFT_jnt', HandEndFK_LFT_jnt, False)					

			#mirror leg#
			cmds.select(UpperLegBND_LFT_jnt)	
			cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=('_LFT_', '_RGT_'))		

			#mirror arm#
			cmds.select(ShoulderBND_LFT_jnt)	
			cmds.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=('_LFT_', '_RGT_'))					

									


			cmds.parent(RootBND_jnt, 'BindJnt_Grp')
			cmds.parent('BindJnt_Grp', 'Joint_Grp')

			self.setStatusIcon('GREEN', self.ui.buildBipedIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.buildBipedIcon)
			self.sendConsole(str(e), append=False)				

	def buildBodyClicked(self):
		try:
			#circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 40 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;#
			#Body FK Controller#
			#spineFK_A_ctrl = cmds.circle(n='spineFK_A_ctrl', c=(0,0,0), nr=(0,1,0), sw=360, r=40, d=30, ut=0, tol=0.01, s=8, ch=1)
			spineFK_A_ctrl = self.createController('circle', 'spineFK_A_ctrl')
			cmds.delete(spineFK_A_ctrl , constructionHistory = True)
			spineFK_AOffset_Grp = self.createZeroGrp(spineFK_A_ctrl[0])
			spineFK_AOut = self.createOutGrp(spineFK_A_ctrl[0])

			#spineFK_B_ctrl = cmds.circle(n='spineFK_B_ctrl', c=(0,0,0), nr=(0,1,0), sw=360, r=40, d=30, ut=0, tol=0.01, s=8, ch=1)
			spineFK_B_ctrl = self.createController('circle', 'spineFK_B_ctrl')
			cmds.delete(spineFK_B_ctrl , constructionHistory = True)
			spineFK_BOffset_Grp = self.createZeroGrp(spineFK_B_ctrl[0])
			spineFK_BOut = self.createOutGrp(spineFK_B_ctrl[0])

			#spineFK_C_ctrl = cmds.circle(n='spineFK_C_ctrl', c=(0,0,0), nr=(0,1,0), sw=360, r=40, d=30, ut=0, tol=0.01, s=8, ch=1)
			spineFK_C_ctrl = self.createController('circle', 'spineFK_C_ctrl')
			cmds.delete(spineFK_C_ctrl , constructionHistory = True)
			spineFK_COffset_Grp = self.createZeroGrp(spineFK_C_ctrl[0])
			spineFK_COut = self.createOutGrp(spineFK_C_ctrl[0])		

			self.snapTo('Root', spineFK_AOffset_Grp, False, freeze=False)
			self.snapTo('Spine1', spineFK_BOffset_Grp, False, freeze=False)	
			self.snapTo('Chest', spineFK_COffset_Grp, False, freeze=False)

			self.setColor(spineFK_A_ctrl[0], color=(1,1,0))
			self.setColor(spineFK_B_ctrl[0], color=(1,1,0))
			self.setColor(spineFK_C_ctrl[0], color=(1,1,0))

			self.addControllerOrderSuperChild(ctrl=spineFK_A_ctrl[0], offset=spineFK_AOffset_Grp, out=spineFK_AOut)
			self.addControllerOrderSuperChild(ctrl=spineFK_B_ctrl[0], offset=spineFK_BOffset_Grp, out=spineFK_BOut)
			self.addControllerOrderSuperChild(ctrl=spineFK_C_ctrl[0], offset=spineFK_COffset_Grp, out=spineFK_COut)

			cmds.parentConstraint(spineFK_AOut, spineFK_BOffset_Grp, mo=True)
			cmds.parentConstraint(spineFK_BOut, spineFK_COffset_Grp, mo=True)

			cmds.parent(spineFK_AOffset_Grp, 'Ctrl_Grp')
			cmds.parent(spineFK_BOffset_Grp, 'Ctrl_Grp')
			cmds.parent(spineFK_COffset_Grp, 'Ctrl_Grp')


			#Hip#
			Hip_ctrl = self.createController('cube', 'hip_ctrl')
			cmds.select(Hip_ctrl)
			cmds.scale( 80,20,80 )
			self.setColor(Hip_ctrl, color=(1,1,1))
			cmds.makeIdentity( Hip_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(Hip_ctrl , constructionHistory = True)
			Hip_Offset_Grp = self.createZeroGrp(Hip_ctrl)
			Hip_Out = self.createOutGrp(Hip_ctrl)

			self.addControllerOrderSuperChild(ctrl=Hip_ctrl, offset=Hip_Offset_Grp, out=Hip_Out)

			cmds.parent(Hip_Offset_Grp, 'Ctrl_Grp')	

			#COG#
			cog_ctrl = self.createController('cog', 'cog_ctrl')
			cmds.select(cog_ctrl)
			cmds.scale( 80,80,80 )
			self.setColor(cog_ctrl, color=(1,1,0))
			cmds.makeIdentity( cog_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(cog_ctrl , constructionHistory = True)
			cog_Offset_Grp = self.createZeroGrp(cog_ctrl)
			cog_Out = self.createOutGrp(cog_ctrl)

			self.addControllerOrderSuperChild(ctrl=cog_ctrl, offset=cog_Offset_Grp, out=cog_Out)

			cmds.parent(cog_Offset_Grp, 'Ctrl_Grp')				

			cmds.parentConstraint('HipBND_jnt', cog_Offset_Grp, mo=False)
			cmds.delete(cog_Offset_Grp, cn=True)

			#cmds.parentConstraint(cog_Out, Hip_Offset_Grp, mo=True)


			#Root and SuperRoot#
			root_ctrl = self.createController('square', 'Root_ctrl')
			cmds.select(root_ctrl)
			cmds.scale( 70,70,70 )
			self.setColor(root_ctrl, color=(1,1,0))
			cmds.makeIdentity( root_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(root_ctrl , constructionHistory = True)
			root_Offset_Grp = self.createZeroGrp(root_ctrl)
			root_Out = self.createOutGrp(root_ctrl)		

			SuperRoot_ctrl = self.createController('square', 'SuperRoot_ctrl')
			cmds.select(SuperRoot_ctrl)
			cmds.scale( 85,85,85 )
			self.setColor(SuperRoot_ctrl, color=(1,1,0))
			cmds.makeIdentity( SuperRoot_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(SuperRoot_ctrl , constructionHistory = True)
			SuperRoot_Offset_Grp = self.createZeroGrp(SuperRoot_ctrl)
			SuperRoot_Out = self.createOutGrp(SuperRoot_ctrl)	

			cmds.parent(root_Offset_Grp, SuperRoot_Out, a=True)					

			self.snapTo('Root', Hip_Offset_Grp, False, freeze=False)
			cmds.parent(SuperRoot_Offset_Grp, 'Ctrl_Grp')

			cmds.parentConstraint(root_Out, cog_Offset_Grp, mo=True)
			cmds.parentConstraint('cogOut', 'RootBND_jnt', mo=True)

			#cmds.pointConstraint('cogOut', 'spineFK_AOffset_Grp', mo=True)
			cmds.parentConstraint('spineFK_AOut', 'Spine0BND_jnt', mo=True)
			cmds.parentConstraint('spineFK_BOut', 'Spine1BND_jnt', mo=True)
			cmds.parentConstraint('spineFK_COut', 'ChestBND_jnt', mo=True)

			self.createSpaceAttr('spineFK_A_ctrl', 'cog:global', 'spineFK_AOffset_Grp', ['cogOut', 'RootOut'], parentType='orient')
			cmds.pointConstraint('cogOut', 'spineFK_AOffset_Grp', mo=True)

			self.createSpaceAttr('hip_ctrl', 'cog:global', 'hipOffset_Grp', ['cogOut', 'RootOut'])


			#Neck#
			neck_ctrl = self.createController('cube', 'neck_ctrl')
			cmds.select(neck_ctrl)
			cmds.scale( 70,5,70 )
			self.setColor(neck_ctrl, color=(1,1,0))
			cmds.makeIdentity( neck_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(neck_ctrl , constructionHistory = True)
			neck_Offset_Grp = self.createZeroGrp(neck_ctrl)
			neck_Out = self.createOutGrp(neck_ctrl)	
			cmds.parentConstraint('NeckBND_jnt', neck_Offset_Grp, mo=False)
			cmds.delete(neck_Offset_Grp, cn=True)
			self.addControllerOrderSuperChild(ctrl=neck_ctrl, offset=neck_Offset_Grp, out=neck_Out)			

			cmds.parentConstraint('neckOut', 'NeckBND_jnt', mo=True)

			#self.createSpaceAttr('neck_ctrl', 'local:global', 'neckOffset_Grp', ['spineFK_COut', 'RootOut'], parentType='orient')			

			# cmds.parentConstraint('spineFK_COut', 'neckOffset_Grp', mo=True)
			# mm.eval('CBdeleteConnection "neckOffset_Grp.rx";')
			# mm.eval('CBdeleteConnection "spineFK_COut.rx";')
			# mm.eval('CBdeleteConnection "neckOffset_Grp.ry";')
			# mm.eval('CBdeleteConnection "spineFK_COut.ry";')
			# mm.eval('CBdeleteConnection "neckOffset_Grp.rz";')
			# mm.eval('CBdeleteConnection "spineFK_COut.rz";')

			# self.createSpaceAttr('neck_ctrl', 'local:global', 'neckOffset_Grp', ['spineFK_COut', 'RootOut'], parentType='orient')			
			cmds.parentConstraint('spineFK_COut', 'neckOffset_Grp', mo=True)
			cmds.parent(neck_Offset_Grp, 'Ctrl_Grp')

			#Head#
			head_ctrl = self.createController('head', 'head_ctrl')
			cmds.select(head_ctrl)
			cmds.scale( 20,20,20 )
			self.setColor(head_ctrl, color=(1,1,0))
			cmds.makeIdentity( head_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(head_ctrl , constructionHistory = True)
			head_Offset_Grp = self.createZeroGrp(head_ctrl)
			head_Out = self.createOutGrp(head_ctrl)	
			cmds.parentConstraint('HeadBND_jnt', head_Offset_Grp, mo=False)
			cmds.delete(head_Offset_Grp, cn=True)
			self.addControllerOrderSuperChild(ctrl=head_ctrl, offset=head_Offset_Grp, out=head_Out)		


			cmds.parent(head_Offset_Grp, 'Ctrl_Grp')
			cmds.parentConstraint(neck_Out, head_Offset_Grp, mo=True)
			cmds.parentConstraint(head_Out, 'HeadBND_jnt', mo=True)

			self.setStatusIcon('GREEN', self.ui.buildBodyIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.buildBodyIcon)
			self.sendConsole(str(e), append=False)			

	def buildLegClicked(self):

		try:
			print('build leg')

			#leg foot#
			legIK_LFT_ctrl = self.createController('square', 'legIK_LFT_ctrl')
			cmds.select(legIK_LFT_ctrl)
			cmds.scale( 40,1,25 )
			self.setColor(legIK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( legIK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(legIK_LFT_ctrl , constructionHistory = True)
			legIK_LFTOffset_Grp = self.createZeroGrp(legIK_LFT_ctrl)
			legIK_LFTOut = self.createOutGrp(legIK_LFT_ctrl)

			self.snapTo('ToeBND_LFT_jnt', legIK_LFTOffset_Grp, False, freeze=False)
			sup, child = self.addControllerOrderSuperChild(ctrl='legIK_LFT_ctrl', offset='legIK_LFTOffset_Grp', out='legIK_LFTOut')
			cmds.parent(legIK_LFTOffset_Grp, 'Ctrl_Grp')

			#foot pivot#
			gFront = cmds.group(empty=True, name='legIKFrontPivot_LFT_Grp', world=True)	
			# self.snapTo('ToeEnd', gFront, False, freeze=False)
			gBack = cmds.group(empty=True, name='legIKBackPivot_LFT_Grp', world=True)		
			# self.snapTo('ToeEnd3', gFront, False, freeze=False)
			gLeft = cmds.group(empty=True, name='legIKLeftPivot_LFT_Grp', world=True)		
			# self.snapTo('ToeEnd2', gFront, False, freeze=False)
			gRight = cmds.group(empty=True, name='legIKRightPivot_LFT_Grp', world=True)		
			# self.snapTo('ToeEnd1', gFront, False, freeze=False)

			cmds.parent(gRight, gLeft)
			cmds.parent(gLeft, gBack)
			cmds.parent(gBack, gFront)
			cmds.parent(gFront, child)
			cmds.parent(legIK_LFTOut, gRight, r=True)

			self.snapTo('ToeEnd', gFront, False, freeze=False)
			self.snapTo('ToeEnd3', gBack, False, freeze=False)
			self.snapTo('ToeEnd2', gLeft, False, freeze=False)
			self.snapTo('ToeEnd1', gRight, False, freeze=False)

			self.addControllerAttri(legIK_LFT_ctrl, 'upperScale')
			self.addControllerAttri(legIK_LFT_ctrl, 'lowerScale')
			self.addControllerAttri(legIK_LFT_ctrl, 'HeelRoll')
			self.addControllerAttri(legIK_LFT_ctrl, 'HeelSide')
			self.addControllerAttri(legIK_LFT_ctrl, 'ToeRoll')
			self.addControllerAttri(legIK_LFT_ctrl, 'ToeSide')		
			self.addControllerAttri(legIK_LFT_ctrl, 'FootRocker')		


			#config ik fk#
			legGlobal_LFT_ctrl = self.createController('config', 'legGlobal_LFT_ctrl')
			cmds.select(legGlobal_LFT_ctrl)
			cmds.scale( 10,10,10 )
			self.setColor(legGlobal_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( legGlobal_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(legGlobal_LFT_ctrl , constructionHistory = True)
			legGlobal_OffsetLFT_ctrl = self.createZeroGrp(legGlobal_LFT_ctrl)
			legGlobal_Out = self.createOutGrp(legGlobal_LFT_ctrl)						

			self.snapTo('ToeBND_LFT_jnt', legGlobal_OffsetLFT_ctrl, False, freeze=False)
			cmds.select(legGlobal_LFT_ctrl)
			cmds.setAttr('{0}.tz'.format(legGlobal_LFT_ctrl), -40)
			cmds.rotate(0,0,90)
			self.hideAllAttr(legGlobal_LFT_ctrl)
			self.addControllerAttri(legGlobal_LFT_ctrl, 'ikfk')

			cmds.parent(legGlobal_OffsetLFT_ctrl, 'Ctrl_Grp')

			cmds.parentConstraint('ToeBND_LFT_jnt', legGlobal_OffsetLFT_ctrl, mo=True)


			#knee pole#
			legPole_LFT_ctrl = self.createController('locator', 'legPole_LFT_ctrl')
			cmds.select(legPole_LFT_ctrl)
			cmds.scale( 10,10,10 )
			self.setColor(legPole_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( legPole_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(legPole_LFT_ctrl , constructionHistory = True)
			legPole_OffsetLFT_grp = self.createZeroGrp(legPole_LFT_ctrl)
			legPole_LFTOut = self.createOutGrp(legPole_LFT_ctrl)				

			#aimConstraint -offset 0 0 0 -weight 1 -aimVector 0 0 1 -upVector 0 1 0 -worldUpType "vector" -worldUpVector 0 1 0 -skip x -skip z;
			gTmp1 = cmds.group(empty=True, world=True)
			gTmp2 = cmds.group(empty=True, world=True)
			cmds.parent(gTmp2, gTmp1)
			cmds.parentConstraint('FootBND_LFT_jnt', gTmp1)
			cmds.setAttr(gTmp2+'.tx', -30)
			cmds.setAttr(gTmp2+'.ty', -30)

			cmds.pointConstraint(gTmp2, legPole_OffsetLFT_grp, mo=False)
			cmds.aimConstraint('FootBND_LFT_jnt', legPole_OffsetLFT_grp, aimVector=(0,0,1), upVector=(0,1,0), skip=['x','z'])

			self.hideRSVAttr(legPole_LFT_ctrl)
			cmds.parent(legPole_OffsetLFT_grp, 'Ctrl_Grp')

			cmds.delete(gTmp1)
			cmds.delete(legPole_OffsetLFT_grp, cn=True)

			legPoleLine = cmds.annotate(legPole_LFT_ctrl, tx='  ', p=(0,0,0) )


			#ik leg joint#
			cmds.select('UpperLegBND_LFT_jnt')
			UpperLegIK_LFT_jnt = cmds.duplicate(name='UpperLegIK_LFT_jnt')[0]
			cmds.select(UpperLegIK_LFT_jnt)
			mm.eval('searchReplaceNames "BND" "IK" "hierarchy";')
			cmds.parent(legPoleLine, 'FootIK_LFT_jnt', r=True)

			#create ik handle#
			LegIKHandle_LFT_ikh = cmds.ikHandle( n='LegIKHandle_LFT_ikh', sj='UpperLegIK_LFT_jnt', ee='ToeIK_LFT_jnt' )
			FootIKHandle_LFT_ikh = cmds.ikHandle( n='FootIKHandle_LFT_ikh', sj='ToeIK_LFT_jnt', ee='ToeEndIK_LFT_jnt' )
			cmds.parent(FootIKHandle_LFT_ikh[0], LegIKHandle_LFT_ikh[0])
			cmds.parent(LegIKHandle_LFT_ikh[0], legIK_LFTOut)

			#polevector constraint#
			cmds.poleVectorConstraint( legPole_LFT_ctrl, LegIKHandle_LFT_ikh[0] )


			#fk leg joint#
			cmds.select('UpperLegBND_LFT_jnt')
			UpperLegFK_LFT_jnt = cmds.duplicate(name='UpperLegFK_LFT_jnt')[0]
			cmds.select(UpperLegFK_LFT_jnt)
			mm.eval('searchReplaceNames "BND" "FK" "hierarchy";')			

			#fk upper leg controller#
			legUpperFK_LFT_ctrl = self.createController('cubeUpperLegFK', 'legUpperFK_LFT_ctrl')
			cmds.select(legUpperFK_LFT_ctrl)
			cmds.scale( 30,30,30 )
			self.setColor(legUpperFK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( legUpperFK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(legUpperFK_LFT_ctrl , constructionHistory = True)
			legUpperFK_LFTOffset_grp = self.createZeroGrp(legUpperFK_LFT_ctrl)
			legUpperFK_LFTOut = self.createOutGrp(legUpperFK_LFT_ctrl)	
			self.addControllerOrderSuperChild(ctrl=legUpperFK_LFT_ctrl, offset=legUpperFK_LFTOffset_grp, out=legUpperFK_LFTOut)			
			cmds.parentConstraint('UpperLegFK_LFT_jnt', legUpperFK_LFTOffset_grp, mo=False)
			cmds.delete(legUpperFK_LFTOffset_grp, cn=True)

			#fk lower leg controller#
			legLowerFK_LFT_ctrl = self.createController('cubeLowerLegFK', 'legLowerFK_LFT_ctrl')
			cmds.select(legLowerFK_LFT_ctrl)
			cmds.scale( 25,25,25 )
			self.setColor(legLowerFK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( legLowerFK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(legLowerFK_LFT_ctrl , constructionHistory = True)
			legLowerFK_LFTOffset_grp = self.createZeroGrp(legLowerFK_LFT_ctrl)
			legLowerFK_LFTOut = self.createOutGrp(legLowerFK_LFT_ctrl)	
			self.addControllerOrderSuperChild(ctrl=legLowerFK_LFT_ctrl, offset=legLowerFK_LFTOffset_grp, out=legLowerFK_LFTOut)			
			cmds.parentConstraint('LowerLegFK_LFT_jnt', legLowerFK_LFTOffset_grp, mo=False)	
			cmds.delete(legLowerFK_LFTOffset_grp, cn=True)

			#fk foot controller#
			FootFK_LFT_ctrl = self.createController('cubeFootFK', 'FootFK_LFT_ctrl')
			cmds.select(FootFK_LFT_ctrl)
			cmds.scale( 25,25,25 )
			self.setColor(FootFK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( FootFK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(FootFK_LFT_ctrl , constructionHistory = True)
			FootFK_LFTOffset_grp = self.createZeroGrp(FootFK_LFT_ctrl)
			FootFK_LFTOut = self.createOutGrp(FootFK_LFT_ctrl)	
			self.addControllerOrderSuperChild(ctrl=FootFK_LFT_ctrl, offset=FootFK_LFTOffset_grp, out=FootFK_LFTOut)			
			cmds.parentConstraint('FootFK_LFT_jnt', FootFK_LFTOffset_grp, mo=False)	
			cmds.delete(FootFK_LFTOffset_grp, cn=True)

			#fk toe controller#
			ToeFK_LFT_ctrl = self.createController('cubeToeFK', 'ToeFK_LFT_ctrl')
			cmds.select(ToeFK_LFT_ctrl)
			cmds.scale( 25,25,25 )
			self.setColor(ToeFK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( ToeFK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(ToeFK_LFT_ctrl , constructionHistory = True)
			ToeFK_LFTOffset_grp = self.createZeroGrp(ToeFK_LFT_ctrl)
			ToeFK_LFTOut = self.createOutGrp(ToeFK_LFT_ctrl)	
			self.addControllerOrderSuperChild(ctrl=ToeFK_LFT_ctrl, offset=ToeFK_LFTOffset_grp, out=ToeFK_LFTOut)			
			cmds.parentConstraint('ToeFK_LFT_jnt', ToeFK_LFTOffset_grp, mo=False)	
			cmds.delete(ToeFK_LFTOffset_grp, cn=True)								

			#move all fk to ctrl_grp#
			cmds.parent(legUpperFK_LFTOffset_grp, 'Ctrl_Grp')
			cmds.parent(legLowerFK_LFTOffset_grp, 'Ctrl_Grp')
			cmds.parent(FootFK_LFTOffset_grp, 'Ctrl_Grp')
			cmds.parent(ToeFK_LFTOffset_grp, 'Ctrl_Grp')

			#contraint hip to fk controller#
			cmds.parentConstraint('hipOut', legUpperFK_LFTOffset_grp, mo=True)
			cmds.parentConstraint(legUpperFK_LFTOut, legLowerFK_LFTOffset_grp, mo=True)
			cmds.parentConstraint(legLowerFK_LFTOut, FootFK_LFTOffset_grp, mo=True)
			cmds.parentConstraint(FootFK_LFTOut, ToeFK_LFTOffset_grp, mo=True)

			#constraint fk controller to fk joint#
			cmds.parentConstraint(legUpperFK_LFTOut, 'UpperLegFK_LFT_jnt', mo=True)
			cmds.parentConstraint(legLowerFK_LFTOut, 'LowerLegFK_LFT_jnt', mo=True)
			cmds.parentConstraint(FootFK_LFTOut, 'FootFK_LFT_jnt', mo=True)
			cmds.parentConstraint(ToeFK_LFTOut, 'ToeFK_LFT_jnt', mo=True)

			#bind all attribute value [upperScale, lowerScale]
			cmds.connectAttr(legIK_LFT_ctrl+'.upperScale', 'UpperLegIK_LFT_jnt.sx')
			cmds.connectAttr(legIK_LFT_ctrl+'.lowerScale', 'LowerLegIK_LFT_jnt.sx')

			cmds.connectAttr(legIK_LFT_ctrl+'.HeelRoll', 'legIKBackPivot_LFT_Grp.rz')
			cmds.connectAttr(legIK_LFT_ctrl+'.HeelSide', 'legIKBackPivot_LFT_Grp.ry')
			#cmds.connectAttr(legIK_LFT_ctrl+'.ToeRoll', 'legIKFrontPivot_LFT_Grp.rz')
			cmds.expression(s='legIKFrontPivot_LFT_Grp.rz = -1*legIK_LFT_ctrl.ToeRoll')
			cmds.connectAttr(legIK_LFT_ctrl+'.ToeSide', 'legIKFrontPivot_LFT_Grp.ry')

			cmds.parentConstraint('ToeBND_LFT_jnt', legGlobal_OffsetLFT_ctrl, mo=True)
			cmds.parentConstraint('hipOut', 'HipBND_jnt', mo=True)


			#do ikfk switch#		
			self.createIKFKSwitch(['UpperLegIK_LFT_jnt', 'LowerLegIK_LFT_jnt', 'FootIK_LFT_jnt', 'ToeIK_LFT_jnt'],
				                  ['UpperLegFK_LFT_jnt', 'LowerLegFK_LFT_jnt', 'FootFK_LFT_jnt', 'ToeFK_LFT_jnt'],
				                  ['UpperLegBND_LFT_jnt', 'LowerLegBND_LFT_jnt', 'FootBND_LFT_jnt', 'ToeBND_LFT_jnt'],
				                  'legGlobal_LFT_ctrl.IKFK',
				                  ['legIK_LFTOffset_Grp', 'legPole_LFTOffset_Grp', 'annotation1'],
				                  ['legUpperFK_LFTOffset_Grp', 'legLowerFK_LFTOffset_Grp', 'FootFK_LFTOffset_Grp', 'ToeFK_LFTOffset_Grp'])


			#set space to leg#
			self.createSpaceAttr('legIK_LFT_ctrl', 'hip:cog:global', 'legIK_LFTOffset_Grp', ['hipOut', 'cogOut', 'RootOut'],parentType='parent')
			#set space to polevector#
			self.createSpaceAttr('legPole_LFT_ctrl', 'local:hip:cog:global', 'legPole_LFTOffset_Grp', ['legIK_LFTOut', 'hipOut', 'cogOut', 'RootOut'])
			#set space to hip#
			#self.createSpaceAttr('hip_ctrl', 'cog:global', 'hipOffset_Grp', ['cogOut', 'RootOut'])
			#set space leg fk#
			#self.createSpaceAttr('legUpperFK_LFT_ctrl', 'hip:cog:global', 'legUpperFK_LFTOffset_Grp', ['hipOut', 'cogOut', 'RootOut'],parentType='orient')
			#cmds.pointConstraint('hipOut', legUpperFK_LFTOffset_grp, mo=True)

			self.setStatusIcon('GREEN', self.ui.buildLegIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.buildLegIcon)
			self.sendConsole(str(e), append=False)	

	def buildArmClicked(self):
		try:
			print('build arm')

			#Shoulder#
			shoulder_LFT_ctrl = self.createController('shoulder', 'shoulder_LFT_ctrl')
			cmds.select(shoulder_LFT_ctrl)
			cmds.scale( 20,20,20 )
			self.setColor(shoulder_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( shoulder_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(shoulder_LFT_ctrl , constructionHistory = True)
			shoulder_Offset_Grp = self.createZeroGrp(shoulder_LFT_ctrl)
			shoulder_Out = self.createOutGrp(shoulder_LFT_ctrl)	
			cmds.parentConstraint('ShoulderBND_LFT_jnt', shoulder_Offset_Grp, mo=False)
			cmds.delete(shoulder_Offset_Grp, cn=True)
			self.addControllerOrderSuperChild(ctrl=shoulder_LFT_ctrl, offset=shoulder_Offset_Grp, out=shoulder_Out)	
			cmds.parent(shoulder_Offset_Grp, 'Ctrl_Grp')

			cmds.parentConstraint('spineFK_COut', shoulder_Offset_Grp, mo=True)
			cmds.parentConstraint(shoulder_Out, 'ShoulderBND_LFT_jnt', mo=True)

			#HandIK#
			handIK_LFT_ctrl = self.createController('hand', 'handIK_LFT_ctrl')
			cmds.select(handIK_LFT_ctrl)
			cmds.scale( 20,20,20 )
			self.setColor(handIK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( handIK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(handIK_LFT_ctrl , constructionHistory = True)
			handIK_Offset_Grp = self.createZeroGrp(handIK_LFT_ctrl)
			handIK_Out = self.createOutGrp(handIK_LFT_ctrl)	
			cmds.parentConstraint('Wrist', handIK_Offset_Grp, mo=False)
			cmds.delete(handIK_Offset_Grp, cn=True)
			self.addControllerOrderSuperChild(ctrl=handIK_LFT_ctrl, offset=handIK_Offset_Grp, out=handIK_Out)	
			self.createSpaceAttr('handIK_LFT_ctrl', 'chest:cog:global', handIK_Offset_Grp, ['spineFK_COut', 'cogOut', 'RootOut'], parentType='parent')
			cmds.parent(handIK_Offset_Grp, 'Ctrl_Grp')

			#config ik fk#
			armGlobal_LFT_ctrl = self.createController('config', 'armGlobal_LFT_ctrl')
			cmds.select(armGlobal_LFT_ctrl)
			cmds.scale( 10,10,10 )
			self.setColor(armGlobal_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( armGlobal_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(armGlobal_LFT_ctrl , constructionHistory = True)
			armGlobal_OffsetLFT_ctrl = self.createZeroGrp(armGlobal_LFT_ctrl)
			armGlobal_Out = self.createOutGrp(armGlobal_LFT_ctrl)						

			self.snapTo('HandBND_LFT_jnt', armGlobal_OffsetLFT_ctrl, False, freeze=False)
			cmds.select(armGlobal_LFT_ctrl)
			cmds.setAttr('{0}.tz'.format(armGlobal_LFT_ctrl), -40)
			cmds.rotate(0,0,90)
			self.hideAllAttr(armGlobal_LFT_ctrl)
			self.addControllerAttri(armGlobal_LFT_ctrl, 'ikfk')

			cmds.parent(armGlobal_OffsetLFT_ctrl, 'Ctrl_Grp')
			cmds.parentConstraint('HandBND_LFT_jnt', armGlobal_OffsetLFT_ctrl, mo=True)


			#upperArm FK#
			armUpperFK_LFT_ctrl = self.createController('cubeUpperLegFK', 'armUpperFK_LFT_ctrl')
			cmds.select(armUpperFK_LFT_ctrl)
			cmds.scale( 30,30,30 )
			self.setColor(armUpperFK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( armUpperFK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(armUpperFK_LFT_ctrl , constructionHistory = True)
			armUpperFK_Offset_Grp = self.createZeroGrp(armUpperFK_LFT_ctrl)
			armUpperFK_Out = self.createOutGrp(armUpperFK_LFT_ctrl)	
			cmds.parentConstraint('UpperArmBND_LFT_jnt', armUpperFK_Offset_Grp, mo=False)
			cmds.delete(armUpperFK_Offset_Grp, cn=True)
			self.addControllerOrderSuperChild(ctrl=armUpperFK_LFT_ctrl, offset=armUpperFK_Offset_Grp, out=armUpperFK_Out)	
			#self.createSpaceAttr('handIK_LFT_ctrl', 'chest:cog:global', handIK_Offset_Grp, ['spineFK_COut', 'cogOut', 'RootOut'], parentType='parent')
			cmds.parent(armUpperFK_Offset_Grp, 'Ctrl_Grp')		

			cmds.parentConstraint(shoulder_Out, armUpperFK_Offset_Grp, mo=True)	

			#lowerArm FK#
			armLowerFK_LFT_ctrl = self.createController('cubeUpperLegFK', 'armLowerFK_LFT_ctrl')
			cmds.select(armLowerFK_LFT_ctrl)
			cmds.scale( 35,30,30 )
			self.setColor(armLowerFK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( armLowerFK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(armLowerFK_LFT_ctrl , constructionHistory = True)
			armLowerFK_Offset_Grp = self.createZeroGrp(armLowerFK_LFT_ctrl)
			armLowerFK_Out = self.createOutGrp(armLowerFK_LFT_ctrl)	
			cmds.parentConstraint('LowerArmBND_LFT_jnt', armLowerFK_Offset_Grp, mo=False)
			cmds.delete(armLowerFK_Offset_Grp, cn=True)
			self.addControllerOrderSuperChild(ctrl=armLowerFK_LFT_ctrl, offset=armLowerFK_Offset_Grp, out=armLowerFK_Out)	
			#self.createSpaceAttr('handIK_LFT_ctrl', 'chest:cog:global', handIK_Offset_Grp, ['spineFK_COut', 'cogOut', 'RootOut'], parentType='parent')
			cmds.parent(armLowerFK_Offset_Grp, 'Ctrl_Grp')	

			cmds.parentConstraint(armUpperFK_Out, armLowerFK_Offset_Grp, mo=True)

			#Hand FK#
			HandFK_LFT_ctrl = self.createController('cubeUpperLegFK', 'HandFK_LFT_ctrl')
			cmds.select(HandFK_LFT_ctrl)
			cmds.scale( 35,30,30 )
			self.setColor(HandFK_LFT_ctrl, color=(0,0,1))
			cmds.makeIdentity( HandFK_LFT_ctrl, apply=True, scale=True , rotate=True)
			cmds.delete(HandFK_LFT_ctrl , constructionHistory = True)
			HandFK_Offset_Grp = self.createZeroGrp(HandFK_LFT_ctrl)
			HandFK_Out = self.createOutGrp(HandFK_LFT_ctrl)	
			cmds.parentConstraint('HandBND_LFT_jnt', HandFK_Offset_Grp, mo=False)
			cmds.delete(HandFK_Offset_Grp, cn=True)
			self.addControllerOrderSuperChild(ctrl=HandFK_LFT_ctrl, offset=HandFK_Offset_Grp, out=HandFK_Out)	
			#self.createSpaceAttr('handIK_LFT_ctrl', 'chest:cog:global', handIK_Offset_Grp, ['spineFK_COut', 'cogOut', 'RootOut'], parentType='parent')
			cmds.parent(HandFK_Offset_Grp, 'Ctrl_Grp')	

			cmds.parentConstraint(armLowerFK_Out, HandFK_Offset_Grp, mo=True)


			#arm ik#
			ArmIKHandle_LFT_ikh = cmds.ikHandle( n='ArmIKHandle_LFT_ikh', sj='UpperArmIK_LFT_jnt', ee='HandIK_LFT_jnt' )
			HandIKHandle_LFT_ikh = cmds.ikHandle( n='HandIKHandle_LFT_ikh', sj='HandIK_LFT_jnt', ee='HandEndIK_LFT_jnt' )
			cmds.parent(HandIKHandle_LFT_ikh[0], ArmIKHandle_LFT_ikh[0] )
			cmds.parent(ArmIKHandle_LFT_ikh[0], handIK_Out)
			# cmds.parentConstraint(handIK_Out, 'HandIK_LFT_jnt', mo=True)

			#arm fk#
			cmds.parentConstraint(armUpperFK_Out, 'UpperArmFK_LFT_jnt', mo=True)
			cmds.parentConstraint(armLowerFK_Out, 'LowerArmFK_LFT_jnt', mo=True)
			cmds.parentConstraint(HandFK_Out, 'HandFK_LFT_jnt', mo=True)

			#do ikfk switch#		
			self.createIKFKSwitch(['UpperArmIK_LFT_jnt', 'LowerArmIK_LFT_jnt', 'HandIK_LFT_jnt'],
				                  ['UpperArmFK_LFT_jnt', 'LowerArmFK_LFT_jnt', 'HandFK_LFT_jnt'],
				                  ['UpperArmBND_LFT_jnt', 'LowerArmBND_LFT_jnt', 'HandBND_LFT_jnt'],
				                  'armGlobal_LFT_ctrl.IKFK',
				                  ['handIK_LFTOffset_Grp'],
				                  ['armUpperFK_LFTOffset_Grp', 'armLowerFK_LFTOffset_Grp', 'HandFK_LFTOffset_Grp'])


			self.setStatusIcon('GREEN', self.ui.buildArmIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.buildArmIcon)
			self.sendConsole(str(e), append=False)	

	def buildFingerClicked(self):
		try:
			print('build finger')

			#finger pose#
			cmds.addAttr('armGlobal_LFT_ctrl', ln='Curl', at='float', keyable=True, min=-5, max=10)
			cmds.addAttr('armGlobal_LFT_ctrl', ln='BaseCurl', at='float', keyable=True, min=0, max=10)
			cmds.addAttr('armGlobal_LFT_ctrl', ln='Spread', at='float', keyable=True, min=0, max=10)

			# cmds.addAttr('armGlobal_LFT_ctrl', ln='CurlThumb', at='float', keyable=True, min=-5, max=10)
			# cmds.addAttr('armGlobal_LFT_ctrl', ln='CurlIndex', at='float', keyable=True, min=-5, max=10)
			# cmds.addAttr('armGlobal_LFT_ctrl', ln='CurlMid', at='float', keyable=True, min=-5, max=10)
			# cmds.addAttr('armGlobal_LFT_ctrl', ln='CurlRing', at='float', keyable=True, min=-5, max=10)
			# cmds.addAttr('armGlobal_LFT_ctrl', ln='CurlPinky', at='float', keyable=True, min=-5, max=10)

			fingerList = ['thumb', 'Index', 'Mid', 'Ring', 'Pinky']
			fingerCurlList = [-2, -8, -8, -8, -8]
			fingerSpreadList = [2, 2, 0, -1, -2]
			fingerAttrList = ['CurlThumb', 'CurlIndex', 'CurlMid', 'CurlRing', 'CurlPinky']
			jointList = ['ThumbFinger{0}BND_LFT_jnt', 'IndexFinger{0}BND_LFT_jnt', 'MidFinger{0}BND_LFT_jnt', 'RingFinger{0}BND_LFT_jnt', 'PinkyFinger{0}BND_LFT_jnt']
			g = cmds.group(em=True, name='fingerPose_LFT_Grp')
			cmds.parentConstraint('HandBND_LFT_jnt', g, mo=False)
			for j,finger in enumerate(fingerList):
				for i in range(1,4):
					Offset_Grp = cmds.group(em=True, name='{0}{1}Offset_Grp'.format(finger,i))
					AnimCurl_Grp = cmds.group(em=True, name='{0}{1}AnimCurl_Grp'.format(finger,i))
					cmds.expression(s='{0}.ry = {1}*armGlobal_LFT_ctrl.Curl;'.format(AnimCurl_Grp, fingerCurlList[j]))
					AnimBaseCurl_Grp = cmds.group(em=True, name='{0}{1}AnimBaseCurl_Grp'.format(finger,i))
					if i==1 and not j==0: cmds.expression(s='{0}.ry = {1}*armGlobal_LFT_ctrl.BaseCurl;'.format(AnimBaseCurl_Grp, fingerCurlList[j]))
					Spread_Grp = cmds.group(em=True, name='{0}{1}Spread_Grp'.format(finger,i))
					if i==1: cmds.expression(s='{0}.rz = {1}*armGlobal_LFT_ctrl.Spread;'.format(Spread_Grp, fingerSpreadList[j]))
					AnimCurl2_Grp = cmds.group(em=True, name='{0}{1}AnimCurl2_Grp'.format(finger,i))
					#cmds.expression(s='{0}.ry = {1}*armGlobal_LFT_ctrl.{2};'.format(AnimCurl2_Grp, fingerCurlList[j], fingerAttrList[i]))
					out_Grp = cmds.group(em=True, name='{0}{1}Out_Grp'.format(finger,i))

					cmds.parent(out_Grp, AnimCurl2_Grp)
					cmds.parent(AnimCurl2_Grp, Spread_Grp)
					cmds.parent(Spread_Grp, AnimBaseCurl_Grp)
					cmds.parent(AnimBaseCurl_Grp, AnimCurl_Grp)
					cmds.parent(AnimCurl_Grp, Offset_Grp)

					cmds.parentConstraint(jointList[j].format(i), Offset_Grp, mo=False)
					cmds.delete(Offset_Grp, cn=True)

					cmds.parent(Offset_Grp, g, a=True)

					cmds.parentConstraint(out_Grp, jointList[j].format(i), mo=True)


			for finger in fingerList:
				cmds.parentConstraint('{0}1Out_Grp'.format(finger), '{0}2Offset_Grp'.format(finger), mo=True)
				cmds.parentConstraint('{0}2Out_Grp'.format(finger), '{0}3Offset_Grp'.format(finger), mo=True)

			cmds.parent(g, 'Ctrl_Grp')

			self.setStatusIcon('GREEN', self.ui.buildFingerIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.buildFingerIcon)
			self.sendConsole(str(e), append=False)	

	def createSpaceAttr(self, switchCtrl, enumList, child, parentList, parentType='parent'):
		cmds.addAttr(switchCtrl, ln='Space', at='enum', en=enumList, keyable=True)
		#constraint#
		conList = []
		i = 0
		for p in parentList:
			if parentType=='parent':
				con = cmds.parentConstraint(p, child, mo=True)
			elif parentType=='orient':
				con = cmds.orientConstraint(p, child, mo=True)
			conText = '{0}.{1}W{2}'.format(con[0], p, i)
			conList.append(conText)
			i += 1

		expressionText = ''
		for con in conList:
			expressionText += '{0} = 0;\n'.format(con)

		for i,con in enumerate(conList):
			expressionText += 'if ({0}.Space=={1}){{ {2}=1; }}\n'.format(switchCtrl, i,con)

		cmds.expression(s=expressionText)



	def createIKFKSwitch(self, ikJointList, fkJointList ,bindJointList, switchCtrl, ikCtrlList, fkCtrlList):
		for i in range(len(ikJointList)):
			con = cmds.parentConstraint(ikJointList[i], bindJointList[i], mo=True)
			con = cmds.parentConstraint(fkJointList[i], bindJointList[i], mo=True)
			ikCon = '{0}.{1}W0'.format(con[0], ikJointList[i])
			fkCon = '{0}.{1}W1'.format(con[0], fkJointList[i])
			cmds.expression(s='{0} = 1-{1};{2} = {1};'.format(ikCon, switchCtrl, fkCon))

		#ik ctrl#
		for con in ikCtrlList:
			cmds.expression(s='{0}.v = 1-{1}'.format(con, switchCtrl))
		for con in fkCtrlList:
			cmds.expression(s='{0}.v = {1}'.format(con, switchCtrl))			

	def createController(self, shapeName, controllerName):
		#shapeName = ['circle']
		shapeDataDict = {'circle': "circle -n {0} -c 0 0 0 -nr 0 1 0 -sw 360 -r 40 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;",
		                 "cube": 'curve -n {0} -d 1 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5;',
		                 "square": 'curve -n {0} -d 1 -p 1 0 -1 -p -1 0 -1 -p -1 0 1 -p 1 0 1 -p 1 0 -1;',
		                 "squareFoot": 'curve -n {0} -d 1 -p 1 0 -1 -p -1 0 -1 -p -1 0 1 -p 1 0 1 -p 1 0 -1;',
		                 "config": 'curve -n {0} -d 3 -p -0.4 0 -0.4 -p -0.4 0 -0.4 -p -0.4 0 -0.4 -p -0.4 0 -0.79 -p -0.4 0 -0.79 -p -0.4 0 -0.99 -p -0.2 0 -0.99 -p 0.2 0 -0.99 -p 0.2 0 -0.99 -p 0.4 0 -0.99 -p 0.4 0 -0.79 -p 0.4 0 -0.79 -p 0.4 0 -0.4 -p 0.4 0 -0.4 -p 0.4 0 -0.4 -p 0.79 0 -0.4 -p 0.79 0 -0.4 -p 0.99 0 -0.4 -p 0.99 0 -0.2 -p 0.99 0 -0.2 -p 0.99 0 0.2 -p 0.99 0 0.2 -p 0.99 0 0.4 -p 0.79 0 0.4 -p 0.4 0 0.4 -p 0.4 0 0.4 -p 0.4 0 0.4 -p 0.4 0 0.79 -p 0.4 0 0.79 -p 0.4 0 0.99 -p 0.2 0 0.99 -p -0.2 0 0.99 -p -0.2 0 0.99 -p -0.4 0 0.99 -p -0.4 0 0.79 -p -0.4 0 0.4 -p -0.4 0 0.4 -p -0.4 0 0.4 -p -0.79 0 0.4 -p -0.79 0 0.4 -p -0.99 0 0.4 -p -0.99 0 0.2 -p -0.99 0 -0.2 -p -0.99 0 -0.2 -p -0.99 0 -0.4 -p -0.79 0 -0.4 -p -0.4 0 -0.4 -p -0.4 0 -0.4 -p -0.4 0 -0.4;',
		                 "locator": 'curve -n {0} -d 1 -p -1 0 0 -p 1 0 0 -p 0 0 0 -p 0 0 1 -p 0 0 -1 -p 0 0 0 -p 0 1 0 -p 0 -1 0;',
		                 "cubeUpperLegFK": 'curve -n {0} -d 1 -p 0.97 0.5 0.5 -p 0.97 0.5 -0.5 -p -0.03 0.5 -0.5 -p -0.03 -0.5 -0.5 -p 0.97 -0.5 -0.5 -p 0.97 0.5 -0.5 -p -0.03 0.5 -0.5 -p -0.03 0.5 0.5 -p 0.97 0.5 0.5 -p 0.97 -0.5 0.5 -p 0.97 -0.5 -0.5 -p -0.03 -0.5 -0.5 -p -0.03 -0.5 0.5 -p 0.97 -0.5 0.5 -p -0.03 -0.5 0.5 -p -0.03 0.5 0.5;',
		                 "cubeLowerLegFK": 'curve -n {0} -d 1 -p 0.97 0.5 0.5 -p 0.97 0.5 -0.5 -p -0.03 0.5 -0.5 -p -0.03 -0.5 -0.5 -p 0.97 -0.5 -0.5 -p 0.97 0.5 -0.5 -p -0.03 0.5 -0.5 -p -0.03 0.5 0.5 -p 0.97 0.5 0.5 -p 0.97 -0.5 0.5 -p 0.97 -0.5 -0.5 -p -0.03 -0.5 -0.5 -p -0.03 -0.5 0.5 -p 0.97 -0.5 0.5 -p -0.03 -0.5 0.5 -p -0.03 0.5 0.5;',
		                 "cubeFootFK": 'curve -n {0} -d 1 -p 0.97 0.5 0.5 -p 0.97 0.5 -0.5 -p -0.03 0.5 -0.5 -p -0.03 -0.5 -0.5 -p 0.97 -0.5 -0.5 -p 0.97 0.5 -0.5 -p -0.03 0.5 -0.5 -p -0.03 0.5 0.5 -p 0.97 0.5 0.5 -p 0.97 -0.5 0.5 -p 0.97 -0.5 -0.5 -p -0.03 -0.5 -0.5 -p -0.03 -0.5 0.5 -p 0.97 -0.5 0.5 -p -0.03 -0.5 0.5 -p -0.03 0.5 0.5;',
		                 "cubeToeFK": 'curve -n {0} -d 1 -p 0.96 0.72 0.5 -p 0.96 0.72 -0.5 -p -0.04 0.72 -0.5 -p -0.04 -0.28 -0.5 -p 0.96 -0.28 -0.5 -p 0.96 0.72 -0.5 -p -0.04 0.72 -0.5 -p -0.04 0.72 0.5 -p 0.96 0.72 0.5 -p 0.96 -0.28 0.5 -p 0.96 -0.28 -0.5 -p -0.04 -0.28 -0.5 -p -0.04 -0.28 0.5 -p 0.96 -0.28 0.5 -p -0.04 -0.28 0.5 -p -0.04 0.72 0.5;',
		                 "cog": 'curve -n {0} -d 1 -p 0 0 -1 -p 0.38 0 -0.93 -p 0.71 0 -0.71 -p 0.93 0 -0.38 -p 1 0 0 -p 0.93 0 0.38 -p 0.71 0 0.71 -p 0.38 0 0.93 -p 0 0 1 -p 0 0 0 -p 0 0 -1 -p -0.38 0 -0.93 -p -0.71 0 -0.71 -p -0.93 0 -0.38 -p -1 0 0 -p 0 0 0 -p 1 0 0 -p 0.93 0 0.38 -p 0.71 0 0.71 -p 0.38 0 0.93 -p 0 0 1 -p -0.38 0 0.93 -p -0.71 0 0.71 -p -0.93 0 0.38 -p -1 0 0;',
		                 "head": 'curve -n {0} -d 1 -p 0 1.36 1 -p -0.19 1.54 0.96 -p -0.37 1.72 0.9 -p -0.56 1.88 0.8 -p -0.37 1.88 0.8 -p -0.19 1.88 0.8 -p -0.19 2.02 0.68 -p -0.19 2.13 0.53 -p -0.19 2.22 0.37 -p -0.19 2.27 0.19 -p -0.37 2.22 0.19 -p -0.53 2.13 0.19 -p -0.68 2.02 0.19 -p -0.8 1.88 0.19 -p -0.8 1.88 0.37 -p -0.8 1.88 0.56 -p -0.9 1.72 0.37 -p -0.96 1.54 0.19 -p -1 1.36 0 -p -0.96 1.54 -0.19 -p -0.9 1.72 -0.37 -p -0.8 1.88 -0.56 -p -0.8 1.88 -0.37 -p -0.8 1.88 -0.19 -p -0.68 2.02 -0.19 -p -0.53 2.13 -0.19 -p -0.37 2.22 -0.19 -p -0.19 2.27 -0.19 -p -0.19 2.22 -0.37 -p -0.19 2.13 -0.53 -p -0.19 2.02 -0.68 -p -0.19 1.88 -0.8 -p -0.37 1.88 -0.8 -p -0.56 1.88 -0.8 -p -0.37 1.72 -0.9 -p -0.19 1.54 -0.96 -p 0 1.36 -1 -p 0.19 1.54 -0.96 -p 0.37 1.72 -0.9 -p 0.56 1.88 -0.8 -p 0.37 1.88 -0.8 -p 0.19 1.88 -0.8 -p 0.19 2.02 -0.68 -p 0.19 2.13 -0.53 -p 0.19 2.22 -0.37 -p 0.19 2.27 -0.19 -p 0.37 2.22 -0.19 -p 0.53 2.13 -0.19 -p 0.68 2.02 -0.19 -p 0.8 1.88 -0.19 -p 0.8 1.88 -0.37 -p 0.8 1.88 -0.56 -p 0.9 1.72 -0.37 -p 0.96 1.54 -0.19 -p 1 1.36 0 -p 0.96 1.54 0.19 -p 0.9 1.72 0.37 -p 0.8 1.88 0.56 -p 0.8 1.88 0.37 -p 0.8 1.88 0.19 -p 0.68 2.02 0.19 -p 0.53 2.13 0.19 -p 0.37 2.22 0.19 -p 0.19 2.27 0.19 -p 0.19 2.22 0.37 -p 0.19 2.13 0.53 -p 0.19 2.02 0.68 -p 0.19 1.88 0.8 -p 0.37 1.88 0.8 -p 0.56 1.88 0.8 -p 0.37 1.72 0.9 -p 0.19 1.54 0.96 -p 0 1.36 1;',
		                 "shoulder": 'curve -n {0} -d 3 -p 0 1 -1.23 -p 0 1 -1.36 -p 0 0.95 -1.62 -p 0 0.73 -1.96 -p 0 0.39 -2.18 -p 0 0 -2.26 -p 0 -0.39 -2.18 -p 0 -0.73 -1.96 -p 0 -0.95 -1.62 -p 0 -1 -1.36 -p 0 -1 -1.23;',
		                 "hand": 'curve -n {0} -d 1 -p 1.98 1 0 -p -0.02 1 0 -p -0.02 -1 0 -p 1.98 -1 0 -p 1.98 1 0;'}
		controller = mm.eval(shapeDataDict[shapeName].format(controllerName))
		return controller

	def addControllerOrderSuperChild(self, ctrl=None, offset=None, out=None, percent=10):
		cmds.select(ctrl)
		if 'LFT' in ctrl or 'RGT' in ctrl:
			ctrlName = ctrl.replace('_LFT_ctrl','Super_LFT_ctrl').replace('_RGT_ctrl','Super_RGT_ctrl')
			ctrlChildName = ctrl.replace('_LFT_ctrl','Child_LFT_ctrl').replace('_RGT_ctrl','Child_RGT_ctrl')
		else:
			ctrlName = ctrl.replace('_ctrl','Super_ctrl')
			ctrlChildName = ctrl.replace('_ctrl','Child_ctrl')
		dup = cmds.duplicate(n=ctrlName)
		cmds.delete('{0}|{1}'.format(dup[0], dup[-1]))
		self.setColor(dup[0], color=(0.5,0.5,0.5))

		cmds.select(ctrl)
		g = cmds.group(n=ctrl.replace('_ctrl','Con_Grp'), parent=offset)

		cmds.select(dup[0])
		gSup = cmds.group(n=dup[0].replace('_ctrl','Con_Grp'), parent=offset)	

		cmds.select(dup[0])
		s = 1+(percent/100.0)
		cmds.scale(s,s,s)	
		cmds.makeIdentity( dup[0], apply=True, scale=True , rotate=True)
		self.hideSVAttr(dup[0])
		self.addControllerAttri(dup[0], 'rotateOrder')

		cmds.select(ctrl)
		dupChild = cmds.duplicate(n=ctrlChildName)
		cmds.delete('{0}|{1}'.format(dupChild[0], dupChild[-1]))
		self.setColor(dupChild[0], color=(0.5,0.5,0.5))

		cmds.select(dupChild[0])
		s = 1-(percent/100.0)
		cmds.scale(s,s,s)
		cmds.makeIdentity( dupChild[0], apply=True, scale=True , rotate=True)
		cmds.parent(dupChild[0], ctrl)
		cmds.parent(out, dupChild[0])
		self.hideSVAttr(dupChild[0])
		self.addControllerAttri(dupChild[0], 'rotateOrder')		

		self.addControllerAttri(ctrl, 'rotateOrder')
		self.addControllerAttri(ctrl, 'super')
		self.addControllerAttri(ctrl, 'child')

		self.hideSVAttr(ctrl)

		cmds.connectAttr(ctrl+'.rotOrder', ctrl+'.rotateOrder')
		cmds.connectAttr(ctrl+'.SuperVIS', gSup+'.v')
		cmds.connectAttr(ctrl+'.ChildVIS', dupChild[0]+'.v')

		cmds.parentConstraint(dup[0], g, mo=True)

		return dup[0], dupChild[0]

	def hideRSVAttr(self, obj):
		# cmds.setAttr(obj+'.tx', lock=True, keyable=False, cb=False)
		# cmds.setAttr(obj+'.ty', lock=True, keyable=False, cb=False)
		# cmds.setAttr(obj+'.tz', lock=True, keyable=False, cb=False)		
		cmds.setAttr(obj+'.rx', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.ry', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.rz', lock=True, keyable=False, cb=False)		
		cmds.setAttr(obj+'.sx', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.sy', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.sz', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.v', lock=False, keyable=False, cb=False)	

	def hideAllAttr(self, obj):
		cmds.setAttr(obj+'.tx', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.ty', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.tz', lock=True, keyable=False, cb=False)		
		cmds.setAttr(obj+'.rx', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.ry', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.rz', lock=True, keyable=False, cb=False)		
		cmds.setAttr(obj+'.sx', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.sy', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.sz', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.v', lock=False, keyable=False, cb=False)		

	def hideSVAttr(self, obj):
		cmds.setAttr(obj+'.sx', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.sy', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.sz', lock=True, keyable=False, cb=False)
		cmds.setAttr(obj+'.v', lock=False, keyable=False, cb=False)

	def addControllerAttri(self, obj, attr):
		#attr = ['rotateOrder', 'super', 'child', 'ikfk']
		print(obj)
		print(attr)
		if attr=='rotateOrder':
			#addAttr -ln "TestTest"  -at "enum" -en "Green:Blue:"  |Rig_Grp|Ctrl_Grp|hipOffset_Grp|hipSuperCon_Grp|hipSuper_ctrl;
			cmds.addAttr(obj, ln='rotOrder', at='enum', en='xyz:yzx:zxy:xzy:yxz:zyx', keyable=True)
			cmds.setAttr(obj+'.rotOrder', cb=True, keyable=False)

		if attr=='super':
			cmds.addAttr(obj, ln='SuperVIS', at='enum', en='off:on', keyable=True)
			cmds.setAttr(obj+'.SuperVIS', cb=True, keyable=False)

		if attr=='child':
			cmds.addAttr(obj, ln='ChildVIS', at='enum', en='off:on', keyable=True)		
			cmds.setAttr(obj+'.ChildVIS', cb=True, keyable=False)	

		if attr=='ikfk':
			cmds.addAttr(obj, ln='IKFK', at='float', keyable=True, min=0, max=1)

		if attr=='upperScale':
			cmds.addAttr(obj, ln='upperScale', at='float', keyable=True, min=0, dv=1)		

		if attr=='lowerScale':
			cmds.addAttr(obj, ln='lowerScale', at='float', keyable=True, min=0, dv=1)	

		if attr=='HeelRoll':
			cmds.addAttr(obj, ln='HeelRoll', at='float', keyable=True, min=0)	

		if attr=='HeelSide':
			cmds.addAttr(obj, ln='HeelSide', at='float', keyable=True,)									

		if attr=='ToeRoll':
			cmds.addAttr(obj, ln='ToeRoll', at='float', keyable=True, min=0)	

		if attr=='ToeSide':
			cmds.addAttr(obj, ln='ToeSide', at='float', keyable=True,)			

	def setColor(self, obj, color=(0,0,0)):
		rgb = ("R","G","B")
		#setAttr group7.overrideColorRGB 0.2 0.4 0.6;
		cmds.setAttr(obj + ".overrideEnabled",1)
		cmds.setAttr(obj + ".overrideRGBColors",1)
		cmds.setAttr(obj + ".overrideColorR", color[0])
		cmds.setAttr(obj + ".overrideColorG", color[1])
		cmds.setAttr(obj + ".overrideColorB", color[2])
    	# for channel, color in zip(rgb, color):
     #    	cmds.setAttr(obj + ".overrideColor%s" %channel, color)		

	def snapTo(self, source, dest, offset, freeze=True):
		print('source : {0}, dest : {1}'.format(source, dest))
		cmds.parentConstraint(source, dest, mo=offset)
		cmds.select(dest)
		cmds.delete(cn=True)
		
		if freeze:cmds.makeIdentity( dest, apply=True, scale=True , rotate=True)

	def createZeroGrp(self, obj):
		grpName = obj.replace('_ctrl','Offset_Grp')
		g = cmds.group(em=True, name=grpName)
		cmds.parent(obj, g, a=True)
		return g

	def createOutGrp(self, obj):
		grpName = obj.replace('_ctrl','Out')
		g = cmds.group(em=True, name=grpName)
		cmds.parent(g, obj, a=True)
		return g

	def createGroupClicked(self):
		try:
			cmds.group( em=True, name='Rig_Grp' )
			cmds.group( em=True, name='Geo_Grp' )
			cmds.group( em=True, name='Joint_Grp' )
			cmds.group( em=True, name='Ctrl_Grp' )
			cmds.group( em=True, name='Util_Grp' )

			cmds.parent( self.ui.groupName_tb.text(), 'Geo_Grp', a=True)

			cmds.parent( 'Geo_Grp', 'Rig_Grp', a=True)
			cmds.parent( 'Joint_Grp', 'Rig_Grp', a=True)
			cmds.parent( 'Ctrl_Grp', 'Rig_Grp', a=True)
			cmds.parent( 'Util_Grp', 'Rig_Grp', a=True)
			self.setStatusIcon('GREEN', self.ui.createGroupIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.createGroupIcon)
			self.sendConsole(str(e), append=False)			

	############

	### build ###

	def saveChangeClicked(self):
		# dataDict = {"modelPath": dest}
		# with open(rigPath+'\\rigdata.json', 'w') as json_file:
		# 		json.dump(dataDict, json_file)

		dataDict = {"modelPath": self.ui.modelPath_tb.text(),
		            "groupName": self.ui.groupName_tb.text(),
		            "01_newScene_checkbox_status": self.ui.newScene_cb.isChecked(),
		            "02_importModel_checkbox_status": self.ui.importModel_cb.isChecked(),
		            "03_createGroup_checkbox_status": self.ui.createGroup_cb.isChecked()}
		with open(self.fullRigPath+'\\rigdata.json', 'w') as json_file:
				json.dump(dataDict, json_file)

	def buildRigClicked(self):
		self.clearStatusIcon()
		try:
			if self.ui.newScene_cb.isChecked():
				if not self.newSceneClicked(): raise Exception("Stop")

			if self.ui.importModel_cb.isChecked():
				if not self.importModelClicked(): raise Exception("Stop")

			if self.ui.createGroup_cb.isChecked():
				if not self.createGroupClicked(): raise Exception("Stop")

			if self.ui.importSkeleton_cb.isChecked():
				if not self.rebuildSkeletonClicked(): raise Exception("Stop")	

			if self.ui.buildBiped_cb.isChecked():
				if not self.buildBipedClicked(): raise Exception("Stop")	

			if self.ui.buildBody_cb.isChecked():
				if not self.buildBodyClicked(): raise Exception("Stop")	

			if self.ui.buildLeg_cb.isChecked():
				if not self.buildLegClicked(): raise Exception("Stop")	

			if self.ui.buildArm_cb.isChecked():
				if not self.buildArmClicked(): raise Exception("Stop")	

			if self.ui.buildFinger_cb.isChecked():
				if not self.buildFingerClicked(): raise Exception("Stop")																						
		except Exception,e:
			print(e)

	def rebuildSkeletonClicked(self):
		#self.fullSkeletonPath
		print(self.fullSkeletonPath)
		try:
			cmds.file(self.fullSkeletonPath, i=True)
			self.setStatusIcon('GREEN', self.ui.importSkeletonIcon)
			return True
		except Exception,e:
			self.setStatusIcon('RED', self.ui.importSkeletonIcon)
			self.sendConsole(str(e), append=False)				

	def exportSettingClicked(self):
		print('test')

	def exportSkeletonClicked(self):
		print('export skeleton')
		#self.fullSkeletonPath
		print(self.fullSkeletonPath)
		cmds.select('__skeleton')
		cmds.file(self.fullSkeletonPath, force = True, options = "v = 0", type = "mayaAscii", exportSelected = True)

	def rebuildSkeletonClickedBackup1(self):
		existsRig = self.rootPath+'\\'+self.ui.existsRig_tb.text()
		f = open(existsRig+'\\skeletondata.json', 'r')
		self.skeletondata = json.load(f)
		f.close()

		__buildSkeleton_Grp = cmds.group(name='__buildSkeleton_Grp', empty=True)
		spineJnt_Grp = cmds.group(name='spineJnt_Grp', empty=True)
		armJnt_Grp = cmds.group(name='armJnt_Grp', empty=True)
		legJnt_Grp = cmds.group(name='legJnt_Grp', empty=True)
		headJnt_Grp = cmds.group(name='headJnt_Grp', empty=True)
		cmds.parent(spineJnt_Grp, __buildSkeleton_Grp, a=True)
		cmds.parent(armJnt_Grp, __buildSkeleton_Grp, a=True)
		cmds.parent(legJnt_Grp, __buildSkeleton_Grp, a=True)
		cmds.parent(headJnt_Grp, __buildSkeleton_Grp, a=True)

		#create spine#
		spineDict = self.skeletondata['spine']
		keyList = spineDict.keys()
		keyList.sort()
		for key in keyList:
			j = cmds.joint( name=key)
			cmds.setAttr("{0}.tx".format(j), spineDict[key]['tx'])
			cmds.setAttr("{0}.ty".format(j), spineDict[key]['ty'])
			cmds.setAttr("{0}.tz".format(j), spineDict[key]['tz'])
			cmds.setAttr("{0}.jointOrientX".format(j), spineDict[key]['jointOrientX'])
			cmds.setAttr("{0}.jointOrientY".format(j), spineDict[key]['jointOrientY'])
			cmds.setAttr("{0}.jointOrientZ".format(j), spineDict[key]['jointOrientZ'])
		cmds.parent('spine1_jnt', spineJnt_Grp, a=True)

		#create leg (left)#
		cmds.select(clear=True)
		legDict = self.skeletondata['leg']
		legkeyList = legDict.keys()
		legkeyList.sort()
		for key in legkeyList:
			j = cmds.joint( name=key)
			cmds.setAttr("{0}.tx".format(j), legDict[key]['tx'])
			cmds.setAttr("{0}.ty".format(j), legDict[key]['ty'])
			cmds.setAttr("{0}.tz".format(j), legDict[key]['tz'])
			cmds.setAttr("{0}.jointOrientX".format(j), legDict[key]['jointOrientX'])
			cmds.setAttr("{0}.jointOrientY".format(j), legDict[key]['jointOrientY'])
			cmds.setAttr("{0}.jointOrientZ".format(j), legDict[key]['jointOrientZ'])
		cmds.parent('upperLeg_L_jnt', legJnt_Grp, a=True)		

	def exportSettingClickedBackup1(self):
		spineList = ['spine1_jnt', 'spine2_jnt', 'spine3_jnt', 'spine4_jnt', 'spine5_jnt']
		self.skeletonSpinDict = {}
		self.skeletonDict = {}
		for j in spineList:
			cmds.makeIdentity( j, apply=True, scale=True , rotate=True)
			t = cmds.getAttr('{0}.t'.format(j))[0]
			ox = cmds.getAttr('{0}.jointOrientX'.format(j))
			oy = cmds.getAttr('{0}.jointOrientY'.format(j))
			oz = cmds.getAttr('{0}.jointOrientZ'.format(j))
			self.skeletonSpinDict[j] = {'tx':t[0],'ty':t[1],'tz':t[2],'rx':0.0,'ry':0.0,'rz':0.0,'jointOrientX':ox,'jointOrientY':oy,'jointOrientZ':oz}

		self.skeletonDict = {"spine":self.skeletonSpinDict}	
		print(self.skeletonDict)
		with open(self.fullRigPath+'\\skeletondata.json', 'w') as json_file:
			json.dump(self.skeletonDict, json_file)  			

	############