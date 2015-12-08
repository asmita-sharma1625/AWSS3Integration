import ConfigParser
#from exceptions import IncorrectConfigException

class ConfigReader:  
  
  def __init__(self,configFile):
    self.configFile = configFile
    self.config = ConfigParser.RawConfigParser()
    self.config.read(self.configFile)
  
  def getValue(self, section, key):
    if self.checkSection(section):
      if self.checkOption(section, key):
        return self.config.get(section, key)
      raise Exception("Key " + key + " does not exist")
    raise Exception("Section " + section + " does not exist")

  def getKeys(self, section):
    if self.checkSection(section):
      return self.config.options(section)
    raise Exception("Section " + section + " does not exist")
  
  def getSections(self):
    return self.config.sections()
      
  def checkSection(self, section):
    return self.config.has_section(section)

  def checkOption(self, section, key):
    return self.config.has_option(section, key)

  def setValue(self, section, key, value):
    if not self.checkSection(section):
      self.addSection(section)
    self.config.set(section, key, value)
    self.updateConfig()

  def addSection(self, section):
    if self.checkSection(section):
      return
    self.config.add_section(section)
    self.updateConfig()

  def getItems(self, section):
    if self.checkSection(section):
      return self.config.items(section)
    raise Exception("Section " + section + " does not exist")


  def updateConfig(self):
    confile = open(self.configFile, "a") 
    self.config.write(confile)
    confile.close()
    self.config.read(self.configFile)
