DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `user` WRITE;
INSERT INTO `user` VALUES (1,'ken'),(2,'hiro'),(3,'yano');

DROP TABLE IF EXISTS `user_copy`;
CREATE TABLE `user_copy` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
LOCK TABLES `user_copy` WRITE;
INSERT INTO `user_copy` VALUES (1,'ken'),(2,'hiro'),(3,'yano');

DROP TABLE IF EXISTS `user_jnl`;
CREATE TABLE `user_jnl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `OPERATION` varchar(1) DEFAULT NULL,
  `old_id` int(11) DEFAULT NULL,
  `new_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
LOCK TABLES `user_jnl` WRITE;
UNLOCK TABLES;

create trigger user_insert_trigger
after insert on user
for each row
begin
insert into user_jnl values(default, 'I', null, NEW.id, NOW());
end;

create trigger user_delete_trigger
after update on user
for each row
begin
insert into user_jnl values(
default, 'U', old.id, new.id, NOW());
end;

create trigger user_update_trigger
after update on user
for each row
begin
insert into user_jnl values(
default, 'U', old.id, new.id, NOW());
end;
