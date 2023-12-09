CREATE TABLE u_data (userid String,  movieid String,  rating String, unixtime String) ENGINE=Hive('thrift://hive:9083', 'default', 'u_data') PARTITION BY '';
