import ConfigParser
from exceptions import IncorrectConfigException

class ConfigReader:  
  
  def __init__(self,configFile):
    self.config = ConfigParser.RawConfigParser()
    self.config.read(configFile)
  
  def getValue(self, section, key):
    if self.checkSection(section):
      if self.checkOption(section, key):
        value = self.config.get(section, key)
      else:
        raise IncorrectConfigException("Key " + key + " does not exist")
    else: 
      raise IncorrectConfigException("Section " + section + " does not exist")
    return value

  def getKeys(self, section):
    if self.checkSection(section):
      return self.config.options(section)
    else: 
      raise IncorrectConfigException("Section " + section + " does not exist")
      
  def checkSection(self, section):
    return self.config.has_section(section)

  def checkOption(self, section, key):
    return self.config.has_option(section, key)

  def setValue(self, section, key, value):
    self.config.set(section, key, value)
