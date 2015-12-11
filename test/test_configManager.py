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
    Diff = "I am old Diff"
    DiffFile = "/tmp/dummy_diff.conf" 
    fp = open(DiffFile, "w")
    fp.write(Diff)
    fp.close()
    message = self.manager.notifyConfigChange(objectKey, DiffFile)
    self.assertTrue(objectKey in message)
    self.assertTrue(Diff in message)

  def test_reportConfigChange(self):
    pass


