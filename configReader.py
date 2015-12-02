import ConfigParser

class ConfigReader:  
  
  def __init__(self,configFile):
    config = ConfigParser.RawConfigParser()
    ConfigReader.config.read(configFile)
  
  def getValue(self, section, key):
    try:
      value = ConfigReader.config.get(section, key)
    except ConfigParser.NoSectionError as error:
      raise Exception("key section pair [" + key + ", " + section + "] does not exist")
    return value

