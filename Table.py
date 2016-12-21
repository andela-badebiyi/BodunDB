import os
from glob import glob
from Database import Db

class Table(object):

  def __init__(self, dbname):
    if not Db.dbexists(dbname):
      raise ValueError('This database does not exists')
    self.dbname = dbname
    if os.path.isdir("files/{}".format(dbname)):
      pass
    else:
      os.makedirs("files/{}".format(dbname))
    return


  def create(self, tbname, fields):
    self.filename = "files/{}/{}.dat".format(self.dbname, tbname)
    if Table.tableExists(self.dbname, tbname):
      raise ValueError('This table already exists')
    else:
      self.__createTable(fields)
    return True


  def showAll(self):
    files = glob("files/{}/*.dat".format(self.dbname))
    return [file.split("/")[2][:-4] for file in files]


  def showFields(self, tbname):
    if Table.tableExists(self.dbname, tbname):
      with open("files/{}/{}.dat".format(self.dbname, tbname)) as f:
        fields = f.readline()
      return fields.split(",")
    return False


  def delete(self, tbname):
    tablefile = "files/{}/{}.dat".format(self.dbname, tbname)
    if Table.tableExists(self.dbname, tbname):
      os.remove(tablefile)
      return True
    return False


  def __createTable(self, fields):
    with open(self.filename, "w") as f:
      f.write(",".join(fields))
    return True

  @staticmethod
  def tableExists(dbname, tbname):
    filename = "files/{}/{}.dat".format(dbname, tbname)
    if os.path.isfile(filename):
      return True
    else:
      return False