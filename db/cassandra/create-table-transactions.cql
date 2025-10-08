CREATE KEYSPACE IF NOT EXISTS demo 
WITH replication = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 1
};
	
CREATE TABLE IF NOT EXISTS demo.transactions (
   client int,
   amount int,
   PRIMARY KEY (client)
);
