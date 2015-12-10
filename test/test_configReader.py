import unittest
from configManager import configReader
import ConfigParser
import os

class TestConfigReader(unittest.TestCase):
  
  def setUp(self):
    self.SECTION = "demo_section"
    self.KEY = "demo_key"
    self.VALUE = "demo_value"
    self.CONF_FILE = "/tmp/test_conf.cfg"
    if os.path.exists(self.CONF_FILE):
      os.remove(self.CONF_FILE)
    open(self.CONF_FILE, "w").close()
    self.reader = configReader.ConfigReader(self.CONF_FILE)
    self.config = ConfigParser.RawConfigParser()
    self.config.read(self.CONF_FILE)
    self.config.add_section(self.SECTION)
    self.updateConfig()

  def tearDown(self):
    if os.path.exists(self.CONF_FILE):
      os.remove(self.CONF_FILE)

  def test_addSection(self):
    self.config.remove_section(self.SECTION)
    self.reader.addSection(self.SECTION)
    self.config.read(self.CONF_FILE)   
    self.assertTrue(self.config.has_section(self.SECTION))

  def test_setValue(self):
    self.reader.setValue(self.SECTION, self.KEY, self.VALUE)
    self.config.read(self.CONF_FILE)
    self.assertEquals(self.config.get(self.SECTION, self.KEY), self.VALUE)

  def test_getValue(self):
    self.config.set(self.SECTION, self.KEY, self.VALUE)
    self.updateConfig()
    self.assertEquals(self.reader.getValue(self.SECTION, self.KEY), self.VALUE)

  def test_getKeys(self):
    KEY1 = "key1"
    KEY2 = "key2"
    self.config.set(self.SECTION, KEY1, self.VALUE)
    self.config.set(self.SECTION, KEY2, self.VALUE)
    self.updateConfig()
    self.assertEquals(self.reader.getKeys(self.SECTION), self.config.options(self.SECTION))

  def updateConfig(self):
    conf = open(self.CONF_FILE, "w")
    self.config.write(conf)
    conf.close()
    self.config.read(self.CONF_FILE)
    self.reader = configReader.ConfigReader(self.CONF_FILE)   

if __name__ == '__main__':
  unittest.main()

