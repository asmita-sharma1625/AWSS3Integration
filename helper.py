import os, getpass
import shutil

class Helper:

  '''
    We need to generate (on the source machine) and install (on the destination machine) an ssh key beforehand 
    so that the scp automatically gets authenticated with our public ssh key 
    (in other words, so that the script doesn't ask for a password). 
  '''

  @staticmethod
  def copyConfigFromRemote(node, srcpath, destpath):
    user = getpass.getuser()
    node = user+"@"+node
    os.system("scp: " + node + ":" + srcpath + " " + destpath)    
  
  @staticmethod
  def copyConfigToRemote(node, srcpath, destpath):
    user = getpass.getuser()
    node = user+"@"+node
    os.system("scp " + srcpath + " " + node + ":" + destpath)

  @staticmethod
  def mapToPath(objectKey):
    return objectKey.split("/", 2)[1]

  @staticmethod
  def mapToNode(objectKey):
    return objectKey.split("/", 2)[0]

  @staticmethod
  def getFilename(path):
    os.path.basename(path)

  @staticmethod
  def prependToFilename(prefix, path):
    filename = prefix + Helper.getFilename
    return os.path.dirname(path) + filename 

  @staticmethod
  def getNewConfigPathFromResponseMailSubject(subject):
    ''' subject structure - Topic:Path '''
    return subject.split(":")[1]

  @staticmethod
  def getTimestampFromPath(path):
    ''' path structure - /tmp/timestamp/......'''
    return path.split("/")[2]    

  @staticmethod
  def deleteAllConfigsBeforeTime(dirpath, timestamp):
    subdir = next(os.walk(dirpath))[1]
    for x in subdir:
      if x <= timestamp:
        shutil.rmtree(os.path.join(dirpath, x))
