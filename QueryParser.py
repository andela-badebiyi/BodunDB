from QueryExec import QueryExec
import re

class QueryParser(object):
    def createCommand(self, queryString):
        database = None
        table = None
        tokens = queryString.lower().strip().replace("  ", " ").split(" ")

        if not tokens[0] == "create" and not len[token] == 3:
            raise ValueError("incorrect query command")
        if not tokens[1] == "database" or not tokens[1] == "table":
            raise ValueError("incorrect query command")
        if tokens[1] == "database":
            databaseName = tokens[2]
            QueryExec.createDatabase(databaseName)
        elif tokens[1] == "table":
            tableName = tokens[1]
            rawData = queryString[queryString.index('(') + 1: -1].strip()
            data = self__formatRawData(rawData)
            QueryExec.createTable(tableName, data)
        else:
            raise ValueError("incorrect query command")

        return True


    def insertCommand(self, queryString):
        qs = queryString.strip().lower()
        introQuery = qs[:qs.index('(')]
        tableName = introQuery.strip().split(' ')[2]
        qExec = QueryExec(tableName)
        queryData = qs.split()[qs.index('('):]

        fields = self.__extractInsertFields(queryData)
        values = self.__extractValues(queryData);
        data = dict(zip(fields, values))
        qExec.insert(data)

        return True


    def updateCommand(self, queryString):
        qs = queryString.strip()
        tableName = qs[6:qs.index('set')].strip()
        qExec = QueryExec(tableName)
        conditionStr = qs.split('where')[1].strip()
        updateDataStr = qs.split('where')[0].strip().replace('update {} set'.format(tableName), '').strip()

        newRecord = dict([ [x.split('=')[0], x.split('=')[1]] for x in updateDataStr.split(',') ])
        condition = re.sub(r"[ ]{2,}", " ", conditionStr)

        print("condition: {}".format(condition), "updateData: ", newRecord)
        return True

    def __extractInsertFields(self, qd):
        fieldAndValues = qd.split('values')


    def __formatRawData(self, rd):
        return [x.strip().split(" ")[0] for x in rd.split(",")]
