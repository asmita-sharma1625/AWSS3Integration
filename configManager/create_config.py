import configReader
import sys

if len(sys.argv) is not 5:
  raise Exception("Required arguments - [config_file_path, section, key, value]")

config_file = sys.argv[1]
section = sys.argv[2]
key = sys.argv[3]
value = sys.argv[4] 

reader = configReader.ConfigReader(config_file)
reader.setValue(section, key, value)
