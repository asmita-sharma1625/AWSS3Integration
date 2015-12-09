import os, getpass

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
  def copyConfig(srcpath, destpath):
    os.system("cp " + srcpath + " " + destpath)

  @staticmethod
  def copyConfigToRemote(node, srcpath, destpath):
    user = getpass.getuser()
    node = user+"@"+node
    os.system("scp " + srcpath + " " + node + ":" + destpath)

  @staticmethod
  def mapToPath(objectKey):
    print "***KEY***", objectKey
    return objectKey.split("/", 1)[1]

  @staticmethod
  def mapToNode(objectKey):
    return objectKey.split("/", 1)[0]

  @staticmethod
  def getFilename(path):
    os.path.basename(path)
 
  @staticmethod
  def getFileContents(filename):
    fp = open(filename, "rb")
    content = fp.read()
    fp.close()
    return content 
