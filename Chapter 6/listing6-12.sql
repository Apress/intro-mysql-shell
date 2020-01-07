SET @base = '{"grapes":["red","white","green"],"berries":["strawberry","raspberry","boysenberry","blackberry"]}';
SELECT JSON_CONTAINS(@base,'["red","white","green"]') \G
SELECT JSON_CONTAINS(@base,'{"grapes":["red","white","green"]}') \G
SELECT JSON_CONTAINS(@base,'["red","white","green"]','$.grapes') \G
SELECT JSON_CONTAINS(@base,'"blackberry"','$.berries') \G
SELECT JSON_CONTAINS(@base,'blackberry','$.berries') \G
SELECT JSON_CONTAINS(@base,'"red"','$.grapes') \G
