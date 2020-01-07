SET @base = '["apple","pear",{"grape":["red","white"]},"strawberry"]';
SET @base = JSON_REMOVE(@base, '$[0]');
SET @base = JSON_REMOVE(@base, '$[0]');
SELECT JSON_REMOVE(@base, '$[0].grape[1]') \G
SET @base = '["apple","pear",{"grape":["red","white"]},"strawberry"]';
SELECT JSON_REMOVE(JSON_REMOVE(JSON_REMOVE(@base, '$[0]'), '$[0]'), '$[0].grape[1]') \G
