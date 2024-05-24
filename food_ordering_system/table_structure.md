# Table: auth_group

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int | NO | PRI |  | auto_increment |
| name | varchar(150) | NO | UNI |  |  |

# Table: auth_group_permissions

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| group_id | int | NO | MUL |  |  |
| permission_id | int | NO | MUL |  |  |

# Table: auth_permission

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int | NO | PRI |  | auto_increment |
| name | varchar(255) | NO |  |  |  |
| content_type_id | int | NO | MUL |  |  |
| codename | varchar(100) | NO |  |  |  |

# Table: dish_app_allergen

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| name | varchar(100) | NO |  |  |  |

# Table: dish_app_dish

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| name | varchar(100) | NO |  |  |  |
| description | longtext | NO |  |  |  |
| price | decimal(10,2) | NO |  |  |  |
| category | varchar(50) | NO |  |  |  |
| image_url | varchar(200) | NO |  |  |  |
| ingredients | longtext | NO |  |  |  |
| nutrition_info | longtext | NO |  |  |  |
| merchant_id | bigint | NO | MUL |  |  |

# Table: dish_app_dish_allergens

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| dish_id | bigint | NO | MUL |  |  |
| allergen_id | bigint | NO | MUL |  |  |

# Table: dish_app_review

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| rating | int | NO |  |  |  |
| comment | longtext | NO |  |  |  |
| created_at | datetime(6) | NO |  |  |  |
| dish_id | bigint | NO | MUL |  |  |
| user_id | bigint | NO | MUL |  |  |

# Table: django_admin_log

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int | NO | PRI |  | auto_increment |
| action_time | datetime(6) | NO |  |  |  |
| object_id | longtext | YES |  |  |  |
| object_repr | varchar(200) | NO |  |  |  |
| action_flag | smallint unsigned | NO |  |  |  |
| change_message | longtext | NO |  |  |  |
| content_type_id | int | YES | MUL |  |  |
| user_id | bigint | NO | MUL |  |  |

# Table: django_content_type

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | int | NO | PRI |  | auto_increment |
| app_label | varchar(100) | NO | MUL |  |  |
| model | varchar(100) | NO |  |  |  |

# Table: django_migrations

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| app | varchar(255) | NO |  |  |  |
| name | varchar(255) | NO |  |  |  |
| applied | datetime(6) | NO |  |  |  |

# Table: django_session

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| session_key | varchar(40) | NO | PRI |  |  |
| session_data | longtext | NO |  |  |  |
| expire_date | datetime(6) | NO | MUL |  |  |

# Table: merchant_app_merchant

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| name | varchar(100) | NO |  |  |  |
| address | varchar(255) | NO |  |  |  |
| phone | varchar(20) | NO |  |  |  |
| created_at | datetime(6) | NO |  |  |  |
| user_id | bigint | NO | UNI |  |  |

# Table: message_app_notification

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| message | longtext | NO |  |  |  |
| created_at | datetime(6) | NO |  |  |  |
| read | tinyint(1) | NO |  |  |  |
| user_id | bigint | NO | MUL |  |  |

# Table: order_app_order

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| status | varchar(10) | NO |  |  |  |
| order_type | varchar(10) | NO |  |  |  |
| total_price | decimal(10,2) | NO |  |  |  |
| created_at | datetime(6) | NO |  |  |  |
| updated_at | datetime(6) | NO |  |  |  |
| merchant_id | bigint | NO | MUL |  |  |
| user_id | bigint | NO | MUL |  |  |

# Table: order_app_orderdetail

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| quantity | int | NO |  |  |  |
| price | decimal(10,2) | NO |  |  |  |
| dish_id | bigint | NO | MUL |  |  |
| order_id | bigint | NO | MUL |  |  |

# Table: user_app_favoritedish

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| created_at | datetime(6) | NO |  |  |  |
| dish_id | bigint | NO | MUL |  |  |
| user_id | bigint | NO | MUL |  |  |

# Table: user_app_favoritemerchant

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| created_at | datetime(6) | NO |  |  |  |
| merchant_id | bigint | NO | MUL |  |  |
| user_id | bigint | NO | MUL |  |  |

# Table: user_app_user

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| password | varchar(128) | NO |  |  |  |
| last_login | datetime(6) | YES |  |  |  |
| is_superuser | tinyint(1) | NO |  |  |  |
| username | varchar(150) | NO | UNI |  |  |
| first_name | varchar(150) | NO |  |  |  |
| last_name | varchar(150) | NO |  |  |  |
| email | varchar(254) | NO |  |  |  |
| is_staff | tinyint(1) | NO |  |  |  |
| is_active | tinyint(1) | NO |  |  |  |
| date_joined | datetime(6) | NO |  |  |  |
| role | varchar(10) | NO |  |  |  |
| student_id | varchar(20) | YES | UNI |  |  |
| staff_id | varchar(20) | YES | UNI |  |  |
| full_name | varchar(100) | NO |  |  |  |
| gender | varchar(10) | NO |  |  |  |

# Table: user_app_user_groups

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| user_id | bigint | NO | MUL |  |  |
| group_id | int | NO | MUL |  |  |

# Table: user_app_user_user_permissions

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| id | bigint | NO | PRI |  | auto_increment |
| user_id | bigint | NO | MUL |  |  |
| permission_id | int | NO | MUL |  |  |

