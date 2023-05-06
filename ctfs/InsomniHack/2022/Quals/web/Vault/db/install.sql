DROP DATABASE IF EXISTS Vault;
GO

CREATE DATABASE Vault;
GO

USE vault
GO

DROP TABLE IF EXISTS dbo.Vault;
GO

CREATE TABLE dbo.Vault
(
      id int IDENTITY(1,1) PRIMARY KEY,
      username nvarchar(32),
      secret_name nvarchar(32),
      secret_value text
);
GO

DROP TABLE IF EXISTS dbo.Stats;
GO
CREATE TABLE dbo.Stats
(
    username nvarchar(32),
    inserttime datetime default CURRENT_TIMESTAMP
);
GO
 
DROP SECURITY POLICY IF EXISTS dbo.SecurityPolicy;
GO
DROP FUNCTION IF EXISTS dbo.SecurityPredicate;
GO
CREATE FUNCTION dbo.SecurityPredicate
(
  @UserName nvarchar(32)
)
RETURNS TABLE
WITH SCHEMABINDING
AS RETURN
(
  SELECT ok = 1 WHERE USER_NAME() = @UserName
);
GO

CREATE SECURITY POLICY dbo.SecurityPolicy
ADD FILTER PREDICATE dbo.SecurityPredicate(UserName)
ON dbo.Vault WITH (STATE = ON, SCHEMABINDING = ON);
GO

create procedure dbo.CreateUser(
        @login varchar(100),
        @password varchar(100))
as
declare @safe_login varchar(200)
declare @safe_password varchar(200)
set @safe_login = replace(@login,'''', '''''')
set @safe_password = replace(@password,'''', '''''')
declare @sql nvarchar(max)
set @sql = 'create login ' + @safe_login + ' with password="' + @safe_password + '"; create user ' + @safe_login + ' for login ' + @safe_login + '; grant select,insert on dbo.Vault to ' + @safe_login +';grant insert on dbo.Stats to ' + @safe_login + ';'
exec (@sql)
go

