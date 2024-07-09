create database if not exists funmovies;
use funmovies;
create table if not exists users(
    userid int primary key,
    name varchar(255) not null,
    email varchar(255) not null,
    phone varchar(10) not null,
    password varchar(255) not null,
    status int not null   
);  
insert into users(userid, name, email, phone, password) values(1, 'varsha', 'varsha@gmail.com', '1234567890', 'v1109' ,0);
insert into users(userid, name, email, phone, password) values(2, 'manoj', 'mbk@yahoo.com', '0987654321', 'm1968',0);
insert into users(userid, name, email, phone, password) values(3, 'sakshi', 'sakshi@gmail.com', '7865102344', 's1234',0);
insert into users(userid, name, email, phone, password) values(4, 'leena', 'leenamanoj@yahoo.com', '5673981023', 'l2120',0);
insert into users(userid, name, email, phone, password) values(5, 'vishnu', 'vm2111@gmail.com', '9876543210', 'v2111',0);

create table if not exists theatre(
    theatreid varchar(50) primary key,
    name varchar(50) not null,
    location varchar(100) not null,
    capacity int not null
);

insert into theatre (theatreid, name, location, capacity) values ('inox1', 'inox', 'gki Delhi', 300);
insert into theatre (theatreid, name, location, capacity) values ('pvr1', 'pvr', 'kalkaji Delhi', 500);
insert into theatre (theatreid, name, location, capacity) values ('inox2', 'inox', 'nehru place Delhi', 200);
insert into theatre (theatreid, name, location, capacity) values ('pvr2', 'pvr', 'vasant kunj Delhi', 400);
insert into theatre (theatreid, name, location, capacity) values ('pvr3', 'pvr', 'gki Delhi', 600);

create table if not exists showtime(
    showid varchar(5) primary key,
    date date not null,
    time time not null
);

insert into showtime (showid, date, time) values ('st1', '2019-12-01', '10:00:00');
insert into showtime (showid, date, time) values ('st2', '2019-12-01', '13:00:00');
insert into showtime (showid, date, time) values ('st3', '2019-12-01', '16:00:00');
insert into showtime (showid, date, time) values ('st4', '2019-12-01', '19:00:00');
insert into showtime (showid, date, time) values ('st5', '2019-12-01', '22:00:00');

create table if not exists movies(
    movieid varchar(10) primary key,
    name varchar(100) not null,
    genre varchar(150) not null,
    releasedate date not null,
    duration int not null,
    showtime varchar(5),
    foreign key(showtime) references showtime(showid)
);

create table if not exists plays(
    theatreid varchar(50),
    movieid varchar(10),
    foreign key(theatreid) references theatre(theatreid),
    foreign key(movieid) references movies(movieid)
);

insert into movies  values('m1', 'avengers', 'action', '2019-04-26', 180, 'st1');
insert into movies  values('m2', 'joker', 'thriller', '2025-10-04', 122, 'st2');
insert into movies  values('m3', 'frozen', 'animation', '2022-11-22', 103, 'st3');
insert into movies  values('m4', 'spiderman', 'action', '2023-07-02', 129, 'st4');
insert into movies  values('m5', 'lion king', 'animation', '2024-07-19', 118, 'st5');

insert into plays (theatreid, movieid) values('inox1', 'm1');
insert into plays (theatreid, movieid) values('pvr1', 'm1');
insert into plays (theatreid, movieid) values('inox2', 'm3');
insert into plays (theatreid, movieid) values('pvr2', 'm4');
insert into plays (theatreid, movieid) values('pvr3', 'm4');

create table if not exists seats(
    seatid varchar(5) primary key,
    type varchar(20) not null,
    price int not null,
    status boolean,
    theatreid varchar(50),
    foreign key(theatreid) references theatre(theatreid)
);

insert into seats (seatid, type, price, status, theatreid) values ('s1', 'gold', 500, false, 'inox1');
insert into seats (seatid, type, price, status, theatreid) values ('s2', 'silver', 300, false, 'inox1');
insert into seats (seatid, type, price, status, theatreid) values ('s3', 'gold', 500, false, 'pvr1');
insert into seats (seatid, type, price, status, theatreid) values ('s4', 'silver', 300, false, 'pvr1');
insert into seats (seatid, type, price, status, theatreid) values ('s5', 'gold', 500, false, 'inox2');

create table if not exists ticket(
    ticketid varchar(20) primary key,
    userid int not null,
    theatreid varchar(50),
    movieid varchar(10),
    showid varchar(5),
    seatid varchar(5),
    foreign key(theatreid) references theatre(theatreid),
    foreign key(movieid) references movies(movieid),
    foreign key(showid) references showtime(showid),
    foreign key(userid) references users(userid),
    foreign key(seatid) references seats(seatid)   
);

insert into ticket (ticketid, userid, theatreid, movieid, showid, seatid) values ('t1', 1, 'inox1', 'm1', 'st1', 's1');
insert into ticket (ticketid, userid, theatreid, movieid, showid, seatid) values ('t2', 2, 'pvr1', 'm1', 'st2', 's2');
insert into ticket (ticketid, userid, theatreid, movieid, showid, seatid) values ('t3', 3, 'inox2', 'm1', 'st3', 's1');
insert into ticket (ticketid, userid, theatreid, movieid, showid, seatid) values ('t4', 4, 'pvr2', 'm1', 'st4', 's2');
insert into ticket (ticketid, userid, theatreid, movieid, showid, seatid) values ('t5', 5, 'pvr3', 'm1', 'st5', 's1');

create table if not exists payment(
    paymentid varchar(5) primary key,
    method varchar(20) not null,
    timing datetime not null,
    amount int not null
);

insert into payment (paymentid, method, timing, amount) values ('p1', 'upi', '2019-12-01 10:00:00', 500);
insert into payment (paymentid, method, timing, amount) values ('p2', 'debit card', '2019-12-01 13:00:00', 300);
insert into payment (paymentid, method, timing, amount) values ('p3', 'net banking', '2019-12-01 16:00:00', 500);
insert into payment (paymentid, method, timing, amount) values ('p4', 'debit card', '2019-12-01 19:00:00', 300);
insert into payment (paymentid, method, timing, amount) values ('p5', 'credit card', '2019-12-01 22:00:00', 500);

select * from users;
select * from theatre;
select * from movies;
select * from showtime;
select * from seats;
select * from ticket;
select * from payment;

select movies.* from movies join plays on movies.movieid = plays.movieid where plays.theatreid = 'inox1';

insert into payment (paymentid, method, timing, amount) values ('p6', 'upi', now(), 300);
insert into ticket (ticketid, userid, theatreid, movieid, showid, seatid) values ('t6', 2, 'pvr1', 'm1', 'st2', 's2');
update seats set status = true where seatid = 's2';

-- step 1: update the corresponding seat's status to false
update seats set status = false where seatid = (select seatid from ticket where ticketid = 't6');
-- step 2: delete the ticket
delete from ticket where ticketid = 't6';

select * from ticket where userid = 2 and movieid = 'm1';

update seats set price = 500*0.75 where type = 'gold' and theatreid = 'inox1';

select seatid, type, price from seats where theatreid = 'inox1' and status = false;

select ticket.*, movies.name as movie_name, showtime.date, showtime.time from ticket join movies on ticket.movieid = movies.movieid join showtime on ticket.showid = showtime.showid where ticket.userid = 2;

select * from movies where releasedate > curdate();

select movies.* from movies join plays on plays.movieid = movies.movieid where genre = 'thriller' and releasedate <= curdate();

select * from theatre where location like '%Delhi%';

delimiter //
create trigger update_seat_insert after insert on ticket
for each row
begin
    update seats set status = true where seatid = new.seatid;
end;
//

delimiter //
create trigger update_seat_delete after delete on ticket
for each row
begin
    update seats set status = false where seatid = old.seatid;
end;
//

delimiter //
create trigger delete_customer after delete on users
for each row
begin
    delete from ticket where userid = old.userid;
    update seats set status = false where seatid in (select seatid from ticket where userid = old.userid);
end;
//

--T1 non-conflicting
start transaction;
select * from users where userid=6;
update users set phone='1234567890' where userid=6;
commit;

--T2 non-conflicting
start transaction;
update users set password='vm1109' where userid=6;
commit;

--T3 non-conflicting
start transaction;
insert into users values(6, 'renu','renu@yahoo.com','9876543210','r1234',0);
commit;

--T4 non-conflicting
start transaction;
delete from users where userid=6;
commit;

--T5 conflicting
start transaction;
update seats set status = true where seatid = 's1';
commit;

--T6 conflicting
start transaction;
delete from movies where movieid='m1';
delete from plays where movieid='m1';
commit;



