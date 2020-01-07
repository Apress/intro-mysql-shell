SELECT JSON_MERGE_PATCH('["apple","pear"]', '{"grape":["red","green"]}', '["strawberry"]') \G
SELECT JSON_MERGE_PRESERVE('{"grape":["red","green"]}', '{"grape":["white"]}') \G
