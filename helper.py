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
  def getFileContents(filename):
    fp = open(filename, "rb")
    content = fp.read()
    fp.close()
    return content 
