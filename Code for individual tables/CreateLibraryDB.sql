# SET GLOBAL local_infile = true;
CREATE DATABASE Library;
# mysql --local-infile=0 --load-data-local-dir=/my/local/data
LOAD DATA LOCAL INFILE '/Users/angelaang/Documents/NUS/Y2S2/bt2102/assignment\ 1/LibBooks.txt' INTO TABLE Book;

# Error Code: 1290. The MySQL server is running with the --secure-file-priv option so it cannot execute this statement
# Error Code: 3948. Loading local data is disabled; this must be enabled on both the client and server sides
# Error Code: 2068. LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.
