SET @base = '["apple","pear",{"grape":"red"},"strawberry"]' \G
SELECT JSON_ARRAY_APPEND(@base, '$[7]', "flesh") \G
