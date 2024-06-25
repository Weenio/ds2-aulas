 create database db_agenda;
 use db_agenda;
 create table tbl_contatos(
 id int unsigned auto_increment primary key,
 nome varchar(50),
 email varchar(50),
 telefone varchar(20),
 tipo_telefone enum ("residencial","celular", "não informado")
 
 
 );
select * from tbl_contatos;
 #drop database db_agenda;