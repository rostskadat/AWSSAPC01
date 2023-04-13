This folder contain a sample CSV file the format of the CSV file is as follow:

*NOTE* The column `locations` (longblob) has been intentionally removed...

```cs
1,AWTMyh6xmd5YcHdIAdN5,1095,BLOCKER,0,"'PASSWORD' detected in this expression, review this potentially hardcoded credential.",10,,RESOLVED,FALSE-POSITIVE,59ddb6f0eabdd7ac9f0929c1d1389f21,,,nobody-n090536@allfundsbank.com,,,30,1532444156458,1539094836760,1408546085000,1532508129000,,"cert,cwe,owasp-a2,sans-top25-porous",AWTMyh2zmd5YcHdIAdNo,AWTMyhqBhBuYi4NY5FWG,0A08080A100A181F203B,3
```

## Columns
```
+---------------------+----------------+------+-----+---------+----------------+
| Field               | Type           | Null | Key | Default | Extra          |
+---------------------+----------------+------+-----+---------+----------------+
| id                  | bigint(20)     | NO   | PRI | NULL    | auto_increment |
| kee                 | varchar(50)    | NO   | UNI | NULL    |                |
| rule_id             | int(11)        | YES  | MUL | NULL    |                |
| severity            | varchar(10)    | YES  |     | NULL    |                |
| manual_severity     | tinyint(1)     | NO   |     | NULL    |                |
| message             | varchar(4000)  | YES  |     | NULL    |                |
| line                | int(11)        | YES  |     | NULL    |                |
| gap                 | decimal(30,20) | YES  |     | NULL    |                |
| status              | varchar(20)    | YES  |     | NULL    |                |
| resolution          | varchar(20)    | YES  | MUL | NULL    |                |
| checksum            | varchar(1000)  | YES  |     | NULL    |                |
| reporter            | varchar(255)   | YES  |     | NULL    |                |
| assignee            | varchar(255)   | YES  | MUL | NULL    |                |
| author_login        | varchar(255)   | YES  |     | NULL    |                |
| action_plan_key     | varchar(50)    | YES  |     | NULL    |                |
| issue_attributes    | varchar(4000)  | YES  |     | NULL    |                |
| effort              | int(11)        | YES  |     | NULL    |                |
| created_at          | bigint(20)     | YES  |     | NULL    |                |
| updated_at          | bigint(20)     | YES  | MUL | NULL    |                |
| issue_creation_date | bigint(20)     | YES  | MUL | NULL    |                |
| issue_update_date   | bigint(20)     | YES  |     | NULL    |                |
| issue_close_date    | bigint(20)     | YES  |     | NULL    |                |
| tags                | varchar(4000)  | YES  |     | NULL    |                |
| component_uuid      | varchar(50)    | YES  | MUL | NULL    |                |
| project_uuid        | varchar(50)    | YES  | MUL | NULL    |                |
| issue_type          | tinyint(2)     | YES  |     | NULL    |                |
+---------------------+----------------+------+-----+---------+----------------+
```