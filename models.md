## user

Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | integer | nextval | NO | YES
firstname | character | None | NO
firstname | character varying | None | NO 
email | character varying | None | NO 
phone | int | None | NO
create_at | timestamp without time zone | (timezone('utc'::text, now()) + '1 day'::interval) | YES 

## city

Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | integer | nextval | NO | YES
name | character | None | NO |
english_name | character | NO |NO
available | boolean |TRUE | NO


## category
Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | integer | nextval | NO | YES
name | character | None | NO |
english_name | character | NO | NO
available | boolean |TRUE | NO 


## company
Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | Integer | nextval | NO | YES
name | Character | None | NO |
english_name | Character | None |YES
description | Text |None | YES |
category_id | int | None | YES 
available | Boolean |TRUE | No 


## Product

Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | Integer | nextval | NO | YES
name | Character | None | NO |
english_name | Character | None |YES
description | Text |None | YES |
Coupon | character | None | YES
price | float | None | Yes
visited | int | None | YES | 
like | int | None | YES | 
unlike | int | None | YES | 
category_id | int | None | YES 
company_id | int | None | YES 
create_at | timestamp without time zone | (timezone('utc'::text, now()) + '1 day'::interval) | YES 
expiration | timestamp without time zone | (timezone('utc'::text, now()) + '1 day'::interval) | YES 
available | Boolean |TRUE | No 



## user_product

Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | Integer | nextval | NO | YES
product_id | Integer |  None | NO
user_id | Integer | None | NO
create_at | timestamp | None | NO

## transaction
Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | Integer | nextval | NO | YES
product_id | Integer |  None | NO
user_id | Integer | None | NO
state | Integer | sucess:1 | NO 
price |double | None |NO


## contact
Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | Integer | nextval | NO | YES
fullname | character varying | None | NO 
email | character varying | None | NO 
description | Text | None | YES |


## banner
Column | Type | Default | Nullable | PK
--- | --- | --- | --- |---
id | Integer | nextval | NO | YES
photo | character varying | None | NO 
slider |Boolean |TRUE | No 
expiration | timestamp without time zone | (timezone('utc'::text, now()) + '1 day'::interval) | YES 
available | Boolean |TRUE | No 

