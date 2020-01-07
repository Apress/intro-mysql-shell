mysqld --defaults-file=primary.cnf > primary_output.txt 2>&1 &
mysqld --defaults-file=secondary1.cnf > secondary1_output.txt 2>&1 &
mysqld --defaults-file=secondary2.cnf > secondary2_output.txt 2>&1 &
mysqld --defaults-file=secondary3.cnf > secondary3_output.txt 2>&1 &
