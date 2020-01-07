SET @base = '{"name": {"last": "Throckmutton", "first": "Billy-bob"}, "address": {"zip": "90125", "city": "Melborne", "state": "California", "street": "4 Main Street"}}';
SELECT @base \G
SELECT JSON_PRETTY(@base) \G
