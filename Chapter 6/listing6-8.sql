SET @base = '["apple","pear",{"grape":["red","white"]},"strawberry"]';
SELECT JSON_REMOVE(@base, '$[0]', '$[0]', '$[0].grape[1]') \G
