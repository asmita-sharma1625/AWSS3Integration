from s3Dao import S3Dao
from configReader import ConfigReader

class ConfigChangeDetector:
  
  '''
    detects changes in old and new config. Also creates diff files for new and old configs. 
  '''
  
  def __init__(self, oldConfig, newConfig):
    self.newConfig = newConfig
    self.oldConfig = oldConfig
    self.oldConfigReader = ConfigReader(self.oldConfig)
    self.newConfigReader = ConfigReader(self.newConfig)
    self.diff_flag = False
    self.diff_config_old = "/tmp/config_diff_old.conf"
    self.diff_old_config_reader = ConfigReader(self.diff_config_old)
    self.diff_config_new = "/tmp/config_diff_new.conf"
    self.diff_new_config_reader = ConfigReader(self.diff_config_new)
    
  def compareConfig(self):
    oldSections = self.oldConfigReader.getSections()
    newSections = self.newConfigReader.getSections()
    for section in newSections:
      if section not in oldSections:
        self.diff_new_config_reader.addSection(section)
        self.diff_flag = True  
      self.compareSection(oldConfig, newConfig, section)
    return self.diff_flag

  def compareSection(self, section):
    oldKeys = self.oldConfigReader.getKeys(section)
    newKeys = self.newConfigReader.getKeys(section)
    for key in newKeys:
      if key not in oldKeys:
        self.diff_new_config_reader.setValue(section, key, self.diff_new_config_reader.getValue(section, key)
        self.diff_flag = True
      oldValue = self.oldConfigReader.getValue(section, key)
      newValue = self.newConfigReader.getValue(section, key)
      if oldValue != newValue:
        self.diff_old_config_reader.setValue(section, key, self.diff_old_config_reader.getValue(section, key)
        self.diff_new_config_reader.setValue(section, key, self.diff_new_config_reader.getValue(section, key)
        self.diff_flag = True
    return self.diff_flag

  def getDiffInOldConfig(self):
    return self.diff_config_old

  def getDiffInNewConfig(self):
    return self.diff_config_new



class ConfigChangeApplier:
  
  '''
    applies config change to remote host by copying new config to the specified path on the given node.  
  '''

  def __init__(self, config, node, path):
    self.config = config
    self.node = node
    self.path = path 
    Helper.copyConfigToRemote(config, node, path) 
