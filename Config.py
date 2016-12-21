import os

class Config:
  filepath = "files/config.ini"
  tmp = "files/tmp.ini"
  defaultValues = "password=,username="

  def __init__(self):
    if os.path.exists(Config.filepath):
      pass
    else:
      self.__storeValues(Config.defaultValues)
    return


  @staticmethod
  def setPassword(password):
    with open(Config.filepath, 'r') as originalFile, open(Config.tmp, "w") as newFile:
      newFile.writelines(["password={}\n".format(password), originalFile.readlines()[1]])
    os.remove(Config.filepath)
    os.rename(Config.tmp, Config.filepath)
    return


  @staticmethod
  def setUsername(username):
    with open(Config.filepath, 'r') as originalFile, open(Config.tmp, 'w') as newFile:
      newFile.writelines([originalFile.readlines()[0], "username={}\n".format(username)])
    os.remove(Config.filepath)
    os.rename(Config.tmp, Config.filepath)
    return


  @staticmethod
  def checkPassword(password):
    with open(Config.filepath, 'r') as f:
      return password == f.readline().split('=')[1].strip()


  @staticmethod
  def checkUsername(username):
    with open(Config.filepath, 'r') as f:
      return username == f.readlines()[1].split('=')[1]


  @staticmethod
  def hasPassword():
    with open(Config.filepath, 'r') as f:
      password = f.readline()
      if password.split("=")[0] == "":
        return False
      else:
        return True


  def __storeValues(self, values):
    with open(Config.filepath, 'w') as f:
      f.write(values.replace(',', '\n'))
    return
