-- Create the 'fl4g' table
CREATE TABLE fl4g (
    flag VARCHAR(255)
);

-- Insert the flag value into the 'flag' column
INSERT INTO fl4g (flag) VALUES ('ISITDTU{test_test_test}');

REVOKE ALL PRIVILEGES ON *.* FROM 'isitdtu'@'%';
GRANT SELECT ON fl4g.* TO 'isitdtu'@'%';
