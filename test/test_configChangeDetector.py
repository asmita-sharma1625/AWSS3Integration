import unittest
import configChangeNotifier
import ConfigParser
import os

class TestConfigChangeDetector(unittest.TestCase):

  def setUp(self):
    self.CONF_FILE_1 = "/tmp/test_conf_1.cfg"
    if os.path.exists(self.CONF_FILE_1):
      os.remove(self.CONF_FILE_1)
    open(self.CONF_FILE_1, "a").close()
    self.config1 = ConfigParser.RawConfigParser()
    self.config1.read(self.CONF_FILE_1)
    self.create_Config(self.CONF_FILE_1, self.config1)
    self.CONF_FILE_2 = "/tmp/test_conf_2.cfg"
    if os.path.exists(self.CONF_FILE_2):
      os.remove(self.CONF_FILE_2)
    open(self.CONF_FILE_2, "a").close()
    self.config2 = ConfigParser.RawConfigParser()
    self.config2.read(self.CONF_FILE_2)
    self.create_Config(self.CONF_FILE_2, self.config2)
    self.configChangeDetector = configChangeNotifier.ConfigChangeDetector(self.CONF_FILE_1, self.CONF_FILE_2)

  def tearDown(self):
    if os.path.exists(self.CONF_FILE_1):
      os.remove(self.CONF_FILE_1)
    if os.path.exists(self.CONF_FILE_2):
      os.remove(self.CONF_FILE_2)

  def test_compareSection_noDiff(self):
    self.assertFalse(self.configChangeDetector.compareSection("demo_section_2"))

  def test_compareSection_diff(self):
    self.addToConfig(self.CONF_FILE_2, self.config2, "demo_section_1", "demo_key_2", "demo_value_2")
    self.configChangeDetector = configChangeNotifier.ConfigChangeDetector(self.CONF_FILE_1, self.CONF_FILE_2)
    self.assertTrue(self.configChangeDetector.compareSection("demo_section_1"))

  def test_compareConfig_noDiff(self):
    self.assertFalse(self.configChangeDetector.compareConfig())

  def test_compareConfig_diff(self):
    self.addToConfig(self.CONF_FILE_2, self.config2, "demo_section_3", "demo_key_1", "demo_value_1")
    self.configChangeDetector = configChangeNotifier.ConfigChangeDetector(self.CONF_FILE_1, self.CONF_FILE_2)
    self.assertTrue(self.configChangeDetector.compareConfig())

  def create_Config(self, confile, config):
    self.addToConfig(confile, config, "demo_section_1", "demo_key_1", "demo_value_1")
    self.addToConfig(confile, config, "demo_section_2", "demo_key_1", "demo_value_1")
    self.addToConfig(confile, config, "demo_section_2", "demo_key_2", "demo_value_2")

  def addToConfig(self, confile, config, section, key = None, value = None):
    conf = open(confile, "a")
    if key is not None:
      if config.has_section(section):
        config.set(section, key, value)
      else:
        config.add_section(section)
        config.set(section, key, value)
    else:
      config.add_section(section)
    config.write(conf)
    conf.close()

if __name__ == '__main__':
  unittest.main()


