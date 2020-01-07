SET @base = '["apple","pear",{"grape":["red","green"]},"strawberry"]';
SELECT JSON_INSERT(@base, '$[9]', "banana", '$[2].grape[3]', "white", '$[0]', "orange") \G
