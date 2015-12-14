DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Teachers;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS PPT;
DROP TABLE IF EXISTS Notes;
DROP TABLE IF EXISTS Material;
DROP TABLE IF EXISTS Software;
DROP TABLE IF EXISTS Homework;
DROP TABLE IF EXISTS Evaluation;
DROP TABLE IF EXISTS assign;
DROP TABLE IF EXISTS is_of;
DROP TABLE IF EXISTS contain;
DROP TABLE IF EXISTS attach_to;
DROP TABLE IF EXISTS belong_to;
DROP TABLE IF EXISTS enrolls;
DROP TABLE IF EXISTS own_p;
DROP TABLE IF EXISTS own_n;
DROP TABLE IF EXISTS own_m;
DROP TABLE IF EXISTS own_so;

create database JindouCloud character set 'utf8' collate 'utf8_general_ci';

use JindouCloud;

create table Students(
    username varchar(20),
    s_id int primary key,
    password int,
    name varchar(20),
    mail varchar(30),
    tel int);

create table Teachers(
    username varchar(20),
    t_id int PRIMARY KEY,
    password int,
    name varchar(20),
    mail varchar(30),
    tel int);

create table Courses(
    c_id int PRIMARY KEY,
    name varchar(20),
    time varchar(20));

create table PPT(
    p_id int PRIMARY KEY,
    chapter varchar(20));

create table Notes(
    n_id int PRIMARY KEY,
    chapter varchar(20));

create table Material(
    m_id int PRIMARY KEY,
    chapter varchar(20));

create table Software(
    so_id int PRIMARY KEY,
    chapter varchar(20));

create table Homework(
    h_id int PRIMARY KEY,
    chapter varchar(20));

create table Evaluation(
    e_id int PRIMARY KEY,
    chapter varchar(20),
    course varchar(20));

create table assign(
    t_id int,
    h_id int,
    foreign key(t_id) references Teachers(t_id),
    foreign key(h_id) references Homework(h_id));

create table is_of(
    t_id int,
    c_id int,
    foreign key(t_id) references Teachers(t_id),
    foreign key(c_id) references Courses(c_id));

create table contain(
    h_id int,
    c_id int,
    foreign key(h_id) references Homework(h_id),
    foreign key(c_id) references Courses(c_id));

create table attach_to(
    h_id int,
    e_id int,
    foreign key(h_id) references Homework(h_id),
    foreign key(e_id) references Evaluation(e_id));

create table belong_to(
    e_id int,
    s_id int,
    foreign key(e_id) references Evaluation(e_id));

create table belong_to(
    e_id int,
    s_id int,
    foreign key(e_id) references Evaluation(e_id),
    foreign key(s_id) references Students(s_id));

create table enrolls(
    c_id int,
    s_id int,
    foreign key(c_id) references Courses(c_id),
    foreign key(s_id) references Students(s_id));

create table own_p(
    c_id int,
    p_id int,
    foreign key(c_id) references Courses(c_id),
    foreign key(p_id) references PPT(p_id));

create table own_n(
    c_id int,
    n_id int,
    foreign key(c_id) references Courses(c_id),
    foreign key(n_id) references Notes(n_id));

create table own_m(
    c_id int,
    m_id int,
    foreign key(c_id) references Courses(c_id),
    foreign key(m_id) references Material(m_id));

create table own_so(
    c_id int,
    so_id int,
    foreign key(c_id) references Courses(c_id),
    foreign key(so_id) references Software(so_id));

create view sumup(student,student_id,course,teacher,time)
    as select Students.name,Students.s_id,Courses.name,Teachers.name,Courses.time
    from Students,Courses,Teachers,enrolls,is_of
    where enrolls.c_id = Courses.c_id AND is_of.t_id = Teachers.t_id AND enrolls.c_id
= is_of.c_id;

create table Notice(
    no_id int PRIMARY KEY,
    content varchar(100));

create table publish(
    c_id int,
    no_id int,
    foreign key(c_id) references Courses(c_id),
    foreign key(no_id) references Notice(no_id));


