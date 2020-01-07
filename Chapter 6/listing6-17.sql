SET @base = '{"grapes":["red","white","green"],"berries":["strawberry","raspberry","boysenberry","blackberry"],"numbers":["1","2","3","4","5"]}';
SELECT JSON_KEYS(@base) \G
SELECT JSON_KEYS(@base,'$') \G
SELECT JSON_KEYS('{"z":123,"x":{"albedo":50}}') \G
SELECT JSON_KEYS('{"z":123,"x":{"albedo":50}}', '$.x') \G
