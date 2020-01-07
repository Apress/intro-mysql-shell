SELECT JSON_DEPTH('8') \G
SELECT JSON_DEPTH('[]') \G
SELECT JSON_DEPTH('{}') \G
SELECT JSON_DEPTH('[12,3,4,5,6]') \G
SELECT JSON_DEPTH('[[], {}]') \G
SET @base = '{"grapes":["red","white","green"],"berries":["strawberry","raspberry","boysenberry","blackberry"],"numbers":["1","2","3","4","5"]}';
SELECT JSON_DEPTH(@base) \G
SELECT JSON_DEPTH(JSON_EXTRACT(@base, '$.grapes')) \G
