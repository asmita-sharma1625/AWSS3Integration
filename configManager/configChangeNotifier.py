import configReader 
import logging
import helper
import os
import difflib
import filecmp

logger = logging.getLogger("s3Integration")

class ConfigChangeDetector:
  
  '''
    detects changes in old and new config. Also creates diff files for new and old configs. 
  '''
  
  def __init__(self, oldConfig, newConfig):
    print "oldconfig ------", oldConfig
    print "newconfig ------", newConfig
    self.oldConfig = oldConfig
    self.newConfig = newConfig
    self.diff = "/tmp/config_diff.conf"
    '''
    self.diff_old = "/tmp/config_diff_old.conf"
    self.diff_new = "/tmp/config_diff_new.conf"
    self.initializeReaders(self.oldConfig, self.newConfig, self.diff_old, self.diff_new)
    '''
  '''
  def initializeReaders(self, oldConfig, newConfig, diff_old, diff_new, overwriteFlag = True):
    if overwriteFlag is True:
      if os.path.exists(self.diff_new):
        os.remove(self.diff_new)
      if os.path.exists(self.diff_old):
        os.remove(self.diff_old)
    self.newConfig = newConfig
    self.oldConfig = oldConfig
    self.oldConfigReader = configReader.ConfigReader(self.oldConfig)
    self.newConfigReader = configReader.ConfigReader(self.newConfig)
    self.diff_flag = False
    self.diff_config_old = diff_old
    self.diff_config_new = diff_new
    self.diff_old_config_reader = configReader.ConfigReader(self.diff_config_old)
    self.diff_new_config_reader = configReader.ConfigReader(self.diff_config_new)
   '''
  def compareConfig(self):
    flag = filecmp.cmp(self.newConfig, self.oldConfig)
    if flag is True:
      return True
    fp = open(self.diff, "w")
    for line in difflib.unified_diff(open(self.oldConfig).readlines(), open(self.newConfig).readlines(), self.oldConfig, self.newConfig):
      fp.write(line)
    fp.close()
    return False
    '''
    flag1 = self.compareConfigRelativeToNew()
    self.initializeReaders(self.newConfig, self.oldConfig, self.diff_new, self.diff_old, False)
    flag2 = self.compareConfigRelativeToNew()
    return flag1 or flag2  
    '''
  '''
  def compareConfigRelativeToNew(self):
    oldSections = self.oldConfigReader.getSections()
    newSections = self.newConfigReader.getSections()
    for section in newSections:
      if section not in oldSections:
        self.diff_new_config_reader.addSection(section)
        self.diff_flag = True 
        for key in self.newConfigReader.getKeys(section):
          self.diff_new_config_reader.setValue(section, key, self.newConfigReader.getValue(section, key)) 
      else:
        self.compareSection(section)
    return self.diff_flag 

  def compareSection(self, section):
    oldKeys = self.oldConfigReader.getKeys(section)
    newKeys = self.newConfigReader.getKeys(section)
    for key in newKeys:
      if key not in oldKeys:
        self.diff_new_config_reader.setValue(section, key, self.newConfigReader.getValue(section, key))
        self.diff_flag = True
      else:
        oldValue = self.oldConfigReader.getValue(section, key)
        newValue = self.newConfigReader.getValue(section, key)
        if oldValue != newValue:
          self.diff_old_config_reader.setValue(section, key, self.oldConfigReader.getValue(section, key))
          self.diff_new_config_reader.setValue(section, key, self.newConfigReader.getValue(section, key))
          self.diff_flag = True
    return self.diff_flag

  def getDiffInOldConfig(self):
    return self.diff_old

  def getDiffInNewConfig(self):
    return self.diff_new
  '''
  def getDiff(self):
    return self.diff


class ConfigChangeApplier:
  
  '''
    applies config change to remote host by copying new config to the specified path on the given node.  
  '''

  def __init__(self, config, node, path):
    self.config = config
    self.node = node
    self.path = path 
    try:
      helper.Helper.copyConfigToRemote(config, node, path) 
    except Exception:
      logger.error("Unable to copy file " + config + " to node " + node + " at location " + path)
      raise Exception("Unable to copy file " + config + " to node " + node + " at location " + path)
