SET @base = '["apple","pear",{"grape":["red","white"]},"strawberry"]';
SELECT JSON_SET(@base, '$[0]', "orange", '$[2].grape[1]', "green", '$[9]', "123") \G
