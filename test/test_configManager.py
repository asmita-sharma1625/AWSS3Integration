import unittest
from configManager import manager
import os

class TestConfigManager(unittest.TestCase):

  NODE = "dummy_node"
  SERVICE = "dummy_service"
  CONFIG = "dummy_config.conf"
  OBJECT_KEY = os.path.join(os.path.join(NODE, SERVICE), CONFIG) 

  def setUp(self):
    self.manager = manager.ConfigManager()

  def test_getConfigPath(self):
    self.assertEquals(self.manager.getConfigPath(TestConfigManager.OBJECT_KEY), os.path.join(TestConfigManager.SERVICE, TestConfigManager.CONFIG)) 

  def test_getConfigNode(self):
    self.assertEquals(self.manager.getConfigNode(TestConfigManager.OBJECT_KEY), TestConfigManager.NODE)

  def test_reportAllConfigChange_noDiff(self):
    pass

  def test_reportAllConfigChange_diff(self):
    pass

  def test_notifyConfigChange(self):
    pass

  def test_reportConfigChange(self):
    pass


