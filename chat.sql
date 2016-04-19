create table Chat(ChatID int primary key,usn text, name text, ProjID int ,ChatContent text,time_stamp timestamp with time zone, foreign key(ProjID) references Project);
