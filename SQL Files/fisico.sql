USE rasdb;

CREATE TABLE dbo."user" (
	"Id" INT,
	"Name" VARCHAR(45),
	"Email" VARCHAR(45),
	"Password" VARCHAR(45),
	"Debit" INT,
	PRIMARY KEY ("Id")
);