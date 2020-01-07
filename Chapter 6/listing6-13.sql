SET @base = '{"grapes":["red","white","green"],"berries":["strawberry","raspberry","boysenberry","blackberry"],"numbers":["1","2","3","4","5"]}';
SELECT JSON_CONTAINS_PATH(@base,'one','$') \G
SELECT JSON_CONTAINS_PATH(@base,'all','$') \G
SELECT JSON_CONTAINS_PATH(@base,'all','$.grapes','$.berries') \G
SELECT JSON_CONTAINS_PATH(@base,'all','$.grapes','$.berries','$.numbers') \G
SELECT JSON_CONTAINS_PATH(@base,'all','$.grapes','$.berries','$.num') \G
SELECT JSON_CONTAINS_PATH(@base,'one','$.grapes','$.berries','$.num') \G
SELECT JSON_CONTAINS_PATH(@base,'one','$.grapes') \G
SELECT JSON_CONTAINS_PATH(@base,'all','$.grape') \G
SELECT JSON_CONTAINS_PATH(@base,'one','$.berries') \G
SELECT JSON_CONTAINS_PATH(@base,'all','$.berries') \G
