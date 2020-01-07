SET @base = '["apple","pear",{"grape":"red"},"strawberry"]';
SELECT JSON_ARRAY_APPEND(@base, '$', "banana") \G
SELECT JSON_ARRAY_APPEND(@base, '$[2].grape', "green") \G
SET @base = '{"grape":"red"}';
SELECT JSON_ARRAY_APPEND(@base, '$', '{"grape":"red"}') \G
