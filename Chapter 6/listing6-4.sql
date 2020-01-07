SET @base = '["apple","pear",{"grape":["red","green"]},"strawberry"]';
SELECT JSON_ARRAY_INSERT(@base, '$[0]', "banana") \G
SELECT JSON_ARRAY_INSERT(@base, '$[2].grape[0]', "white") \G
SET @base = '[{"grape":"red"}]';
SELECT JSON_ARRAY_INSERT(@base, '$[0]', '{"grape":"red"}') \G
