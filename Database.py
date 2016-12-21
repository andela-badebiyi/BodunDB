from os import path, stat

class Db(object):
  filename = "files/database.dat"
  currentDb = ""

  def __init__(self):
    if path.isfile(Db.filename):
      pass
    else:
      f = open(Db.filename, "w")
      f.close()
    return


  def create(self, dbname):
    if Db.dbexists(dbname):
      return false
    else:
      self.__dbstore(dbname)
    return


  def fetchall(self):
    with open(Db.filename) as f:
      dbs = f.readline().split(",")
    return dbs


  def delete(self, dbname):
    if Db.dbexists(dbname):
      with open(Db.filename, "r+") as f:
        dbs = f.readline().split(",")
      dbs.remove(dbname)
      self.__dbstore(dbs, "w")
    else:
      return false


  @staticmethod
  def dbexists(dbname):
    with open(Db.filename) as f:
      dbs = f.readline().split(",")
    return dbname in dbs


  def __dbstore(self, dbname, mode="a"):
    with open(Db.filename, mode) as f:
      if type(dbname) is str:
        self.__writeToFile(f, dbname)
      elif type(dbname) is list:
        self.__writeToFile(f, ','.join(dbname))
    return True


  def __writeToFile(self, f, text):
    if stat(Db.filename).st_size == 0:
      f.write(text)
    else:
      f.write("," + text)
    return

