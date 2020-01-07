SET @base = '{"grapes":["red","white","green"],"berries":["strawberry","raspberry","boysenberry","blackberry"],"numbers":["1","2","3","4","5"]}';
SELECT JSON_LENGTH(@base,'$') \G
SELECT JSON_LENGTH(@base,'$.grapes') \G
SELECT JSON_LENGTH(@base,'$.grapes[1]') \G
SELECT JSON_LENGTH(@base,'$.grapes[4]') \G
SELECT JSON_LENGTH(@base,'$.berries') \G
SELECT JSON_LENGTH(@base,'$.numbers') \G
