import pymysql

# pymysql.version_info=(1,3,13,"final",0)
pymysql.version_info = (1, 4, 6, "final", 0)  # 设置为 Django 接受的版本
pymysql.install_as_MySQLdb()