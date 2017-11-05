#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import pymysql
import sys
sys.path.append("..")
import confhelper
import pickledb


class DbHelper(object):
    def __init__(self,dbpath='/mnt/sda1/data/pickledb/test.db'):
        self.db = pickledb.load(dbpath,False)

    def __GetConnect(self):
        if not self.db:
            raise(NameError,u"没有设置数据库信息")
        # self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        if self.dbtype=='mssql':
            pass
        if self.dbtype=='mysql':
            self.conn=pymysql.connect(host=self.host,user=self.user,password=self.pwd,db=self.db,charset='utf8mb4')
        if self.dbtype=='sqlite':

            self.conn=sqlite.connect(self.db)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        #执行并返回数据
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        #执行并提交数据，不返回
        cur = self.__GetConnect()
        cur.execute(sql)
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

