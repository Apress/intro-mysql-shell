SET @base = '["apple","pear",{"grape":["red","white"]},"strawberry"]';
SELECT JSON_REPLACE(@base, '$[0]', "orange", '$[2].grape[0]', "green", '$[9]', "waffles") \G
