create table user(id int(8) primary key not null AUTO_INCREMENT,username char(20) not null,password char(20) not null,email char(20) not null,phone char(20) not null,name char(20) not null, studentid char(20) not null,usertype int(8) not null) charset=utf8;

create table course(id int(8) primary key not null AUTO_INCREMENT, teacher char(20) not null, name char(20) not null, description char(20) not null, time char(20) not null, classroom char(20) not null) charset=utf8;

create table courseattend(courseid int(8), userid int(8)) charset=utf8;

create table homework(id int(8) primary key not null AUTO_INCREMENT,courseid int(8) not null, description char(200) not null, deadline char(20) not null) charset=utf8;

create table news(id int(8) primary key not null AUTO_INCREMENT, courseid int(8) not null, description char(200) not null, publisher char(20) not null) charset=utf8;

create table resource(courseid int(8) not null,filename char(50) not null) charset=utf8;

create table homeworksubmit(userid int(8) not null,homeworkid int(8) not null) charset=utf8;
