if not exists (select * from sys.databases where [name] = 'vuln')
begin
  create database vuln;
end
go

use vuln
go

--create table [user] (
--  id int identity(1,1) primary key not null,
--  [name] nvarchar(100) not null,
--  [pass] nvarchar(150) not null
--);
--go

if not exists (select * from sysobjects where [name] = 'flag' and xtype='U')
begin
  create table [flag] (
    [id] int identity(1,1) not null primary key,
    [key] nvarchar(200) not null,
    [value] nvarchar(2000) not null
  );
end
go

--insert into [user] ([name], [pass]) values
--(N'user1', N'pass1'),
--(N'user2', N'pass2');

--alter table [flag]
--add [user_id] int not null foreign key references [user] ([id]);

--alter table [flag]
--alter column [value] nvarchar(2000) not null;

truncate table flag;
go
