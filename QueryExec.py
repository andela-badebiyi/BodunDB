import os
from Database import Db
from Table import Table

class QueryExec:
  def __init__(self, tbname):
    if Db.currentDb == "":
      raise ValueError("No database has been selected")
    if not Table.tableExists(Db.currentDb, tbname):
      raise ValueError("this table does not exist")
    self.tbname = tbname
    self.tbfile = "files/{}/{}.dat".format(Db.currentDb, tbname)
    self.tmp = "files/{}/tmp-{}.dat".format(Db.currentDb, tbname)
    self.tbcolumns = self.__getTableColumns()
    return

  def setTable(self, tbname):
    self.tbname = tbname


  def getTable(self):
    return self.tbname


  @staticmethod
  def createTable(self, tableName, fields):
    if Db.currentDb == "":
      raise ValueError("No database has been selected")
    myTable = Table(Db.currentDb)
    myTable.create(fields)
    return True

  @staticmethod
  def createDatabase(dbname):
    db = Db()
    db.create(dbname)
    return True


  def insert(self, data):
    if not os.path.isfile(self.tbfile):
      raise ValueError("Table file does not exist")
    self.__insertRecord(data)
    return


  def findBy(self, conditions):
    # self.__checkFields(conditions)
    results = []
    with open(self.tbfile, 'r') as f:
      for line in f:
        record = dict(zip(self.tbcolumns, line.replace('\n', '').split(',')))
        # if self.__passConditions(conditions, record):
        if self.__conditionIsTrue(conditions, record):
          results.append(record)
      return results
    return False


  def alterRecord(self, newRecord, conditions):
    self.__checkFields(newRecord)
    # self.__checkFields(conditions)

    if self.findBy(conditions):
      def updateRecord(o, newRec, record, tbcolumns):
        for key in newRecord:
          record[key] = newRec[key]
        o.write((",").join([record[x] for x in tbcolumns]) + '\n')
      self.__loopFindPerform(conditions, updateRecord, newRecord)
      os.remove(self.tbfile)
      os.rename(self.tmp, self.tbfile)
      return True;
    return False


  def deleteBy(self, conditions):
    # self.__checkFields(conditions)
    if self.findBy(conditions):
      self.__loopFindPerform(conditions, None, None)
      os.remove(self.tbfile)
      os.rename(self.tmp, self.tbfile)
      return True
    return False


  def __insertRecord(self, data):
    dataFields = list(data.keys())
    output = []
    validationResult = self.__validateFields(dataFields)
    if not validationResult == True:
      return (False, validationResult)

    for field in self.tbcolumns:
      if field in dataFields:
        output.append(str(data[field]))
      else:
        output.append('')

    with open(self.tbfile, 'a') as f:
      f.write('\n' + ','.join(output))
    return True


  def __checkFields(self, conditions):
    validationResponse = self.__validateFields([field for field in conditions])
    if not validationResponse == True:
      raise ValueError("Table does not contain column '{}'".format(validationResponse['field']))


  def __validateFields(self, fields):
    for field in fields:
      if field not in self.tbcolumns:
        return {'field': field}
    return True


  def __getTableColumns(self):
    with open(self.tbfile, 'r') as f:
      return f.readline().replace("\n", "").split(",")


  def __passConditions(self, conditions, record):
    for key in conditions:
      if not conditions[key] == record[key]:
        return False
    return True


  def __conditionIsTrue(self, conditions, record):
    #{ field: fname, value: bodun, negate: True, conjunction: and }
    result = 0
    prevConj = None
    # I have no idea what I did here but it works, please believe me :'(
    for condition in conditions:
      value, field, negate, conjunction = condition['value'], condition['field'], condition['negate'], condition['conjunction']
      if negate == False:
        conditionExpression = (not value == record[field])
      else:
        conditionExpression = (value == record[field])

      if conditionExpression:
        if conjunction == 'and':
          return False
        else:
          if prevConj == 'or' or conjunction == 'or':
            result = False or (result if not result == 0 else False)
          else:
            return False
      else:
        result = True
      prevConj = conjunction
    return result


  def __loopFindPerform(self, conditions, action, newRecord):
    with open(self.tbfile, 'r') as f, open(self.tmp, 'w') as o:
      for line in f:
        record = dict(zip(self.tbcolumns, line.replace('\n', '').split(',')))
        if self.__conditionIsTrue(conditions, record):
          if action:
            action(o, newRecord, record, self.tbcolumns)
        else:
          o.write(line)
