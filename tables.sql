create table StudentInfo(USN char(10) primary key, Name text, Passwd text, Sem int);

create table StudContact(contactid int, USN char(10), PhNo int, primary key(USN, PhNo, contactid), foreign key(USN) references StudentInfo);

create table StudEmail(emailid int, USN char(10), Email text, primary key(USN, Email, emailid), foreign key(USN) references StudentInfo);

create table Project(ProjID  int primary key, Title text, DateOfReg date, Status text, Synopsis text, Complete boolean);

create table ProjFiles(ProjID int, FileID int, FPath text, ADate date, primary key(ProjID, FileID), foreign key(ProjID) references Project);

create table Domains(DomID int primary key, DomainName text);

create table ProjDom(projdomid int, ProjID int, DomID int, primary key(ProjID, DomID, projdomid), foreign key(ProjID) references Project, foreign key(DomID) references Domains);

create table StudProjGrade(evalid int, USN char(10), ProjID int, Grade char(1), primary key(USN, ProjID, evalid), foreign key(USN) references StudentInfo, foreign key(ProjID) references Project);

create table ProfInfo(ProfID int primary key, Name text, Passwd text);

create table ProfIdea(ProfID int, NewProjID int primary key, Idea text, Synopsis text, foreign key(ProfID) references ProfInfo);

create table ProfContact(contactid int, ProfID int, PhNo int, primary key(ProfID, PhNo, contactid), foreign key(ProfID) references ProfInfo);

create table ProfEmail(emailid int, ProfID int, Email text, primary key(ProfID, Email, emailid), foreign key(ProfID) references ProfInfo);

create table ProjProf(projprofid int, ProjID int, ProfID int, primary key(ProjID, ProfID, projprofid), foreign key(ProjID) references Project, foreign key(ProfID) references ProfInfo);

create table ProjProfCom(ProjID int, ProfID int, CommentID int, Comment text, primary key(ProjID, ProfID, CommentID), foreign key(ProjID) references Project, foreign key(ProfID) references ProfInfo);

create table Chat(ChatID int,USN char(10),ProjID int ,ChatContent text,time_stamp timestamp with time zone,primary key(ChatID,USN,ProjID) ,foreign key(USN) references StudentInfo,foreign key(ProjID) references Project);
