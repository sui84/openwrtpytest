#encoding=utf-8
import pymysql
import sys
sys.path.append("..")
import sqlite3


class SqlHelper(object):
    def __init__(self,host="localhost",user="",pwd="",db="test",dbtype='mssql'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.dbtype = dbtype
        # 51792
        # self.conn = pymssql.connect(host=r"127.0.0.1\SQLEXPRESS", user="sa", password=r"pwd", database="dbname",charset="utf8")
        # File "pymssql.pyx", line 641, in pymssql.connect (pymssql.c:10824) pymssql.OperationalError:
        # (20009, 'DB-Lib error message 20009, severity 9:\nUnable to connect: Adaptive Server is unavailable or does not exist (127.0.0.1\\SQLEXPRESS)\n')

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        # self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        if self.dbtype=='mssql':
            import pyodbc
            self.conn = pyodbc.connect('Driver={SQL Server};Server=self.host;Database=self.db;uid=self.user;pwd=self.pwd')
            #self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db,charset="utf8")
        if self.dbtype=='mysql':
            self.conn=pymysql.connect(host=self.host,user=self.user,password=self.pwd,db=self.db,charset='utf8mb4',local_infile=True)
        if self.dbtype=='sqlite':
            self.conn=sqlite3.connect(self.db)
        if self.dbtype=='dsn':
            import pyodbc
            self.conn = pyodbc.connect('DSN=%s;PWD=%s,charset="utf8"' % (self.host,self.pwd))
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        #执行并返回数据
        print sql
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecQueryWithParas(self,sql,parameters):
        #执行并返回数据
        cur = self.__GetConnect()
        cur.execute(sql,parameters)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        #执行并提交数据，不返回
        print sql
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def ExecNonQueryWithParas(self,sql,parameters):
        #执行并提交数据，不返回
        cur = self.__GetConnect()
        cur.execute(sql,parameters)
        self.conn.commit()
        self.conn.close()

def TestMssqldb(secname):
    conf = confhelper.ConfHelper()
    dbinfo = conf.GetSectionConfig(secname)
    mydb = SqlHelper(host=dbinfo.get("mssqlserver"), user=dbinfo.get("mssqluser"), pwd=dbinfo.get("mssqlpwd"), db=dbinfo.get("testdb"),dbtype='mssql')
    resList = mydb.ExecQuery("SELECT * FROM test")
    print resList

def TestMysqldb(secname):
    conf = confhelper.ConfHelper()
    dbinfo = conf.GetSectionConfig(secname)
    print dbinfo
    mydb = SqlHelper(host=dbinfo.get("mysqlhost"), user=dbinfo.get("mysqluser"), pwd=dbinfo.get("mysqlpwd"), db=dbinfo.get("mysqldb"),dbtype='mysql')
    sqlstr = "insert into urls(name,url) values('%s','%s')" % ("name","url")
    mydb.ExecNonQuery(sqlstr)
    resList = mydb.ExecQuery("SELECT * FROM urls")
    print resList

def TestSqlitedb(secname):
    conf = confhelper.ConfHelper()
    dbinfo = conf.GetSectionConfig(secname)
    mydb = SqlHelper(db=dbinfo.get("sqlitetest"),dbtype='sqlite')
    sqlstr = "insert into company(id,name,age) values(%d,'%s',%d)" % (2,"abddd",8)
    mydb.ExecNonQuery(sqlstr)
    resList = mydb.ExecQuery("select * from company")
    print resList

if __name__ == '__main__':
    TestMssqldb("mssqldb")
    TestMysqldb("mysqldb")
    TestSqlitedb("sqlitedb")

