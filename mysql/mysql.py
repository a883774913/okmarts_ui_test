import pymysql


class Mysql:

    def con_db(self, user, pwd, host, db, port=3306):
        # 连接数据库
        con = pymysql.connect(user=user, passwd=pwd,
                              host=host, db=db,
                              port=port)
        # 创建游标
        cur = con.cursor(pymysql.cursors.DictCursor)
        return con, cur

    def dql(self, cur, sql):
        cur.execute(sql)
        res = cur.fetchall()  # 获取所有查询结果，查询结果为空返回()，不为空返回[{'xx':yy}]
        return res

    def dml(self, con, cur, sql):
        cur.execute(sql)
        con.commit()  # 所有SQL执行完成后，提交事务

    def close(self, con, cur):
        cur.close()
        con.close()



    # 删除数据库数据
    def drop_table(self,user,pwd,host,db,port,sql):
        con, cur = self.con_db(user=user, pwd=pwd, host=host, db=db, port=port)
        self.dml(con, cur, sql)
        self.close(con, cur)



