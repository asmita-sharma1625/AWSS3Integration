import unittest
from configManager import manager
import os

class TestConfigManager(unittest.TestCase):

  NODE = "dummy_node"
  SERVICE = "dummy_service"
  CONFIG = "test_config_1.conf"
  OBJECT_KEY = os.path.join(os.path.join(NODE, SERVICE), CONFIG) 

  def setUp(self):
    self.manager = manager.ConfigManager("test/Config_Manager_config.conf")
    print "config test/Config_Manager_config.conf  exists :", os.path.exists("test/Config_Manager_config.conf")

  def test_getConfigPath(self):
    self.assertEquals(self.manager.getConfigPath(TestConfigManager.OBJECT_KEY), os.path.join(TestConfigManager.SERVICE, TestConfigManager.CONFIG)) 

  def test_getConfigNode(self):
    self.assertEquals(self.manager.getConfigNode(TestConfigManager.OBJECT_KEY), TestConfigManager.NODE)

  def test_reportAllConfigChange(self):
    #os.system("python configManager/uploadFileToS3.py " + self.manager.BUCKET + " " + TestConfigManager.OBJECT_KEY + " test/test_config_1.conf")
    self.manager.reportAllConfigChange()   
 
  def test_notifyConfigChange(self):
    objectKey = "dummy_key"
    oldDiff = "I am old Diff"
    newDiff = "I am new Diff"
    oldDiffFile = "/tmp/dummy_old_diff.conf"
    newDiffFile = "/tmp/dummy_new_diff.conf" 
    fp1 = open(oldDiffFile, "w")
    fp2 = open(newDiffFile, "w")
    fp1.write(oldDiff)
    fp2.write(newDiff)
    fp1.close()
    fp2.close()
    message = self.manager.notifyConfigChange(objectKey, oldDiffFile, newDiffFile)
    self.assertTrue(objectKey in message)
    self.assertTrue(oldDiff in message)
    self.assertTrue(newDiff in message)
    

  def test_reportConfigChange(self):
    pass


