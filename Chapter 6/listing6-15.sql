SET @base = '{"grapes":["red","white","green"],"berries":["strawberry","raspberry","boysenberry","blackberry"],"numbers":["1","2","3","4","5"]}';
SELECT JSON_SEARCH(@base,'all','red') \G
SELECT JSON_SEARCH(@base,'all','gr____') \G
SELECT JSON_SEARCH(@base,'one','%berry') \G
SELECT JSON_SEARCH(@base,'all','%berry') \G
