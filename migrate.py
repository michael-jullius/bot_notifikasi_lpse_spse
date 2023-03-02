import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
)

cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS `bot`;")
cursor.execute("CREATE DATABASE bot;")

db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='bot',
)

cursor = db.cursor()
cursor.execute("CREATE TABLE `bot`.`data` (`id`  BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, `loop_id` text NOT NULL, `nama` text NOT NULL, `harga` text NOT NULL, `url` text NOT NULL, `tanggal` text NOT NULL, `create_at` datetime NOT NULL) ENGINE=InnoDB")
cursor.execute(
    "CREATE TABLE `bot`.`url` ( `id` BIGINT NOT NULL AUTO_INCREMENT , `url` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
cursor.execute("CREATE TABLE `bot`.`user_pu` ( `id` BIGINT NOT NULL AUTO_INCREMENT , `nama` TEXT NOT NULL , `id_user` INT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
cursor.execute("CREATE TABLE `bot`.`user` ( `id` INT NOT NULL AUTO_INCREMENT , `nama` TEXT NOT NULL , `id_user` INT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
cursor.execute("CREATE TABLE `bot`.`error_log` (`id` BIGINT NOT NULL AUTO_INCREMENT , `name_error` TEXT NOT NULL , `create_at` DATETIME NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
cursor.execute("CREATE TABLE `bot`.`user_log` (`id` BIGINT NOT NULL AUTO_INCREMENT , `id_user` TEXT NOT NULL , `nama` TEXT NOT NULL , `massage` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
cursor.execute("CREATE TABLE `bot`.`user_log_pu` (`id` BIGINT NOT NULL AUTO_INCREMENT , `id_user` TEXT NOT NULL , `nama` TEXT NOT NULL , `massage` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
cursor.execute("CREATE TABLE `bot`.`status` (`id` BIGINT NOT NULL AUTO_INCREMENT , `status` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
cursor.close()
