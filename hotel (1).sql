-- drop database hotel;

create database hotel default character set gbk;
use hotel;

create table room(
    rid int PRIMARY KEY AUTO_INCREMENT ,
    state enum('yes','no') not null default 'no'
);
create table worker(
	wid int PRIMARY KEY AUTO_INCREMENT ,
    name varchar(20),
    password varchar(20),
    identify enum('管理','雇员')
);
create table user(
    creditcard varchar(20) PRIMARY KEY unique,
    name varchar(20),
    password varchar(20),
    money decimal(10,2) default 0
);
create table base(
    bid int PRIMARY KEY AUTO_INCREMENT ,
	time date,
    money decimal(10,2) default 500.00,
    changgui int default 0,
    yufujin int default 0,
    tiqian60 int default 0,
    zong int default 0
);
create table plan(
    pid int PRIMARY KEY AUTO_INCREMENT,
    roomid int,
	usercredit varchar(20),
    plantype varchar(20),
    plantime timestamp  default now(),
    arrivetime date,
    leavetime date,
    paytime datetime  default null,
CONSTRAINT 信用卡约束 foreign key (usercredit) references user(creditcard),
CONSTRAINT 房间约束 foreign key (roomid) references room(rid)
);
create table ticket(
tid int PRIMARY KEY AUTO_INCREMENT,
tcard varchar(20),
tmoney decimal(10,2),
tjudge enum('yes','no') not null default 'no',
CONSTRAINT 罚单信用卡约束 foreign key (tcard) references user(creditcard)
);
create table mailbox(
mid int PRIMARY KEY AUTO_INCREMENT,
mcard varchar(20),
mail varchar(30),
mtime date default null,
content varchar(100) default null,
CONSTRAINT 邮箱信用卡约束 foreign key (mcard) references user(creditcard)
);
insert into worker(name,password,identify) 
values ('李娜','000000','管理'),
('刘冰','000000','雇员'),
('谢婷','000000','雇员'),
('张林','000000','雇员'),
('王林','000000','雇员');
insert into user(name,password,creditcard)
values('小红','000000','1'),
('小白','000000','2');



DELIMITER $$
DROP PROCEDURE IF EXISTS createroom $$
CREATE PROCEDURE createroom () 
BEGIN
declare i int default 1;
START TRANSACTION;
WHILE
		i <= 45 DO
	INSERT INTO room () VALUES();
	SET i = i + 1;		
    END WHILE;
	COMMIT;
end $$
CALL createroom();

DELIMITER $$
DROP PROCEDURE IF EXISTS createDates $$
CREATE PROCEDURE createDates()
    BEGIN
DECLARE num INT; 
SET num=1; 
WHILE num < 365 DO 
INSERT INTO base(time) VALUES(DATE_ADD(now(),INTERVAL num DAY)); 
SET num=num+1;
END WHILE;
    END$$
call createDates();


delimiter $$
drop trigger if exists  预付金预订房间 $$
create trigger 预付金预订房间
 after insert  
 on plan for each row
 begin  
     if (new.plantype='预付金预订') 
     then     
    update  user set money=(select sum(base.money*0.75) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
    update  room set room.state='yes' where new.roomid=room.rid;
     end if; 
end$$

delimiter $$
drop trigger if exists  提前60天预订房间 $$
create trigger 提前60天预订房间
 after insert  
 on plan for each row
 begin  
     if (new.plantype='提前60天预订') 
     then     
    update  user set money=(select sum(base.money*0.85) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
    update  room set room.state='yes' where new.roomid=room.rid;
     end if; 
end$$

delimiter $$
drop trigger if exists  常规预订房间 $$
create trigger 常规预订房间
 after insert 
 on plan for each row
 begin  
     if (new.plantype='常规预订') 
     then     
    update  user set money=(select sum(base.money) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
    update  room set room.state='yes' where new.roomid=room.rid;
     end if; 
end$$

delimiter $$
drop trigger if exists  修改预订 $$
create trigger 修改预订
 after update 
 on plan for each row
 begin 
     if (new.plantype='提前60天预订' or new.plantype='预付金预订') 
     then 
     update  user set money=(select sum(base.money*1.1) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
     update  room set room.state='yes' where new.roomid=room.rid;
     update  room set room.state='no' where old.roomid=room.rid;
     end if; 
end$$
delimiter $$

drop trigger if exists  取消常规预订 $$
create trigger 取消常规预订
 after delete
 on plan for each row
 begin 
     if (old.plantype='常规预订') 
     then 
     update  user set money=(select base from base where time=old.arrivetime) where user.creditcard=old.usercredit;
     update  room set room.state='no' where old.roomid=room.rid;
     end if; 
end$$

delimiter $$
drop trigger if exists  取消预订 $$
create trigger 取消预订
 after delete
 on plan for each row
 begin 
     if (old.plantype='提前60天预订' or old.plantype='预付金预订') 
     then 
     update  room set room.state='no' where old.roomid=room.rid;
     end if; 
end$$

delimiter $$
drop trigger if exists  修改常规预订 $$
create trigger 修改常规预订
 after update 
 on plan for each row
 begin 
     if (old.plantype='常规预订') 
     then 
     update  room set room.state='yes' where new.roomid=room.rid;
     update  room set room.state='no' where old.roomid=room.rid;
     end if; 
end$$
-- drop database hotel;

create database hotel default character set gbk;
use hotel;

create table room(
    rid int PRIMARY KEY AUTO_INCREMENT ,
    state enum('yes','no') not null default 'no'
);
create table worker(
	wid int PRIMARY KEY AUTO_INCREMENT ,
    name varchar(20),
    password varchar(20),
    identify enum('管理','雇员')
);
create table user(
    creditcard varchar(20) PRIMARY KEY unique,
    name varchar(20),
    password varchar(20),
    money decimal(10,2) default 0
);
create table base(
    bid int PRIMARY KEY AUTO_INCREMENT ,
	time date,
    money decimal(10,2) default 500.00
);
create table plan(
    pid int PRIMARY KEY AUTO_INCREMENT,
    roomid int,
	usercredit varchar(20),
    plantype varchar(20),
    plantime timestamp  default now(),
    arrivetime date,
    leavetime date,
CONSTRAINT 信用卡约束 foreign key (usercredit) references user(creditcard),
CONSTRAINT 房间约束 foreign key (roomid) references room(rid)
);
-- insert into worker(name,password,identify)
-- values ('李娜','000000','管理'),
-- ('刘冰','000000','雇员'),
-- ('谢婷','000000','雇员'),
-- ('张林','000000','雇员'),
-- ('王林','000000','雇员');
-- insert into user(name,password,creditcard)
-- values('小红','000000','1'),
-- ('小白','000000','2');
-- 可以不用在这里创建用户


DELIMITER $$
DROP PROCEDURE IF EXISTS createroom $$
CREATE PROCEDURE createroom () 
BEGIN
declare i int default 1;
START TRANSACTION;
WHILE
		i <= 45 DO
	INSERT INTO room () VALUES();
	SET i = i + 1;		
    END WHILE;
	COMMIT;
end $$
CALL createroom();

DELIMITER $$
DROP PROCEDURE IF EXISTS createDates $$
CREATE PROCEDURE createDates()
    BEGIN
DECLARE num INT; 
SET num=1; 
WHILE num < 365 DO 
INSERT INTO base(time) VALUES(DATE_ADD(now(),INTERVAL num DAY)); 
SET num=num+1;
END WHILE;
    END$$
call createDates();


delimiter $$
drop trigger if exists  预订金预订房间 $$
create trigger 预订金预订房间
 after insert  
 on plan for each row
 begin  
     if (new.plantype='预付金预订') 
     then     
    update  user set money=(select sum(base.money*0.75) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
    update  room set room.state='yes' where new.roomid=room.rid;
    update base set base.yufujin=base.yufujin+1 where base.time<=new.leavetime and base.time>=new.arrivetime;
    update base set base.zong=base.zong+1 where base.time<=new.leavetime and base.time>=new.arrivetime;
     end if; 
end$$

delimiter $$
drop trigger if exists  提前60天预订房间 $$
create trigger 提前60天预订房间
 after insert  
 on plan for each row
 begin  
     if (new.plantype='提前60天预订') 
     then     
    update  user set money=(select sum(base.money*0.85) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
    update  room set room.state='yes' where new.roomid=room.rid;
    update base set base.tiqian60=base.tiqian60+1 where base.time<=new.leavetime and base.time>=new.arrivetime;
    update base set base.zong=base.zong+1 where base.time<=new.leavetime and base.time>=new.arrivetime;
     end if; 
end$$

delimiter $$
drop trigger if exists  常规预订房间 $$
create trigger 常规预订房间
 after insert 
 on plan for each row
 begin  
     if (new.plantype='常规预订') 
     then     
    update  user set money=(select sum(base.money) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
    update  room set room.state='yes' where new.roomid=room.rid;
    update base set base.changgui=base.changgui+1 where base.time<=new.leavetime and base.time>=new.arrivetime;
    update base set base.zong=base.zong+1 where base.time<=new.leavetime and base.time>=new.arrivetime;
     end if; 
end$$

delimiter $$
drop trigger if exists  修改预订 $$
create trigger 修改预订
 after update 
 on plan for each row
 begin 
     if (new.plantype='提前60天预订' or new.plantype='预付金预订') 
     then 
     update  user set money=(select sum(base.money*1.1) from base where time<=new.leavetime and time>=new.arrivetime) where user.creditcard=new.usercredit;
     update  room set room.state='no' where old.roomid=room.rid;
     update  room set room.state='yes' where new.roomid=room.rid;
     end if; 
end$$

delimiter $$
drop trigger if exists  取消常规预订 $$
create trigger 取消常规预订
 after delete
 on plan for each row
 begin 
     if (old.plantype='常规预订') 
     then 
     update  user set money=(select money from base where time=old.arrivetime) where user.creditcard=old.usercredit;
     update  room set room.state='no' where old.roomid=room.rid;
     update base set base.changgui=base.changgui-1 where base.time<=old.leavetime and base.time>=old.arrivetime;
    update base set base.zong=base.zong-1 where base.time<=old.leavetime and base.time>=old.arrivetime;
     end if; 
end$$

delimiter $$
drop trigger if exists  取消提前60天预订 $$
create trigger 取消提前60天预订
 after delete
 on plan for each row
 begin 
     if (old.plantype='提前60天预订') 
     then 
     update  room set room.state='no' where old.roomid=room.rid;
     update base set base.tiqian60=base.tiqian60-1 where base.time<=old.leavetime and base.time>=old.arrivetime;
    update base set base.zong=base.zong-1 where base.time<=old.leavetime and base.time>=old.arrivetime;
     end if; 
end$$
delimiter $$
drop trigger if exists  取消预付金预订 $$
create trigger 取消预付金预订
 after delete
 on plan for each row
 begin 
     if (old.plantype='预付金预订') 
     then 
     update  room set room.state='no' where old.roomid=room.rid;
     update base set base.yufujin=base.yufujin-1 where base.time<=old.leavetime and base.time>=old.arrivetime;
    update base set base.zong=base.zong-1 where base.time<=old.leavetime and base.time>=old.arrivetime;
     end if; 
end$$

delimiter $$
drop trigger if exists  修改常规预订 $$
create trigger 修改常规预订
 after update 
 on plan for each row
 begin 
     if (old.plantype='常规预订') 
     then 
     update  room set room.state='no' where room.rid=old.roomid;
     update  room set room.state='yes' where room.rid=new.roomid;
     end if; 
end$$
-- SET SQL_SAFE_UPDATES = 0;
-- insert into plan(roomid,usercredit,plantype,arrivetime,leavetime)
-- values(1,1,'常规预订','2023-01-06','2023-01-26'),
-- (2,2,'提前60天预订','2023-01-05','2023-01-28'),
-- (3,3,'预付金预订','2023-01-07','2023-01-16'),
-- (4,4,'提前60天预订','2023-01-08','2023-01-26'),
-- (5,5,'预付金预订','2023-01-05','2023-01-19'),
-- (6,6,'常规预订','2023-01-08','2023-01-21');
CREATE VIEW dayarrive AS select name username,plantype,roomid,leavetime
                            from user,plan
                            where user.creditcard=plan.usercredit and DATEDIFF(plan.arrivetime,NOW())=0
                            order by user.name;
CREATE VIEW daylive AS select roomid ,name,leavetime
                           from user,plan
                           where user.creditcard=plan.usercredit and plan.arrivetime<=now() and plan.leavetime>now()
                           order by plan.roomid;

-- 预计入住的报表  是一页纸的管理报表，显示未来30天中每个晚上在当前已被预订的房间数。报表的每一行显示日期
-- ，预订金预付、提前60天预付、常规预订和奖励预订的数量，以及被预订的房间总数。

create view livenotes as select bid,time ,yufujin , tiqian60 ,changgui , zong  from base where CURDATE()<=date(time) and date(time) <=DATE_SUB(CURDATE(),INTERVAL -30 DAY);
-- drop view dayarrive;
-- drop view daylive;
-- drop view livenotes;
-- 预计房间收入报表  是一页纸的管理报表，显示未来30天中每个晚上从房间出租上预计得到的收入。报表的每一行显示日期和那个晚上预计的收入。
-- 报表的最后两行是那个时期的总收入和平均收入。
create view moneynotes as select bid,time,(yufujin*money*0.75+changgui*money+tiqian60*money*0.85) income from base where CURDATE()<=date(time) and date(time) <=DATE_SUB(CURDATE(),INTERVAL -30 DAY);
-- drop view moneynotes;
-- 产品必须能够打印“票据”，能够反映该票据打印的日期、卡号、客人姓名、房间号、达到日期、离开日期、入住的天数和总金额。
-- 对于预付金预订和提前60天预订的情况，该票据还能反映提前支付的日期和金额。在客人结帐时把票据交给客人。
create view notes as select now() now_field,plan.usercredit,user.name , plan.roomid , plan.arrivetime , plan.leavetime , datediff(plan.leavetime,plan.arrivetime) datediffer, plan.paytime, user.money
                from user,plan where plan.usercredit=user.creditcard;
-- drop view notes
