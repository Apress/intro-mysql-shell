SET @base = '{"grapes":["red","white","green"],"berries":["strawberry","raspberry","boysenberry","blackberry"],"numbers":["1","2","3","4","5"]}';
SELECT JSON_EXTRACT(@base,'$') \G
SELECT JSON_EXTRACT(@base,'$.grapes') \G
SELECT JSON_EXTRACT(@base,'$.grapes[*]') \G
SELECT JSON_EXTRACT(@base,'$.grapes[1]') \G
SELECT JSON_EXTRACT(@base,'$.grapes[4]') \G
SELECT JSON_EXTRACT(@base,'$.berries') \G
SELECT JSON_EXTRACT(@base,'$.berries[2]') \G
SELECT JSON_EXTRACT(@base,'$.berries[2]','$.berries[3]') \G
