

CREATE TABLE IF NOT EXISTS "django_migrations" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

INSERT INTO django_migrations VALUES(1,'contenttypes','0001_initial','2025-06-30 10:59:11.183899');
INSERT INTO django_migrations VALUES(2,'contenttypes','0002_remove_content_type_name','2025-06-30 10:59:11.217490');
INSERT INTO django_migrations VALUES(3,'auth','0001_initial','2025-06-30 10:59:11.386119');
INSERT INTO django_migrations VALUES(4,'auth','0002_alter_permission_name_max_length','2025-06-30 10:59:11.448252');
INSERT INTO django_migrations VALUES(5,'auth','0003_alter_user_email_max_length','2025-06-30 10:59:11.822399');
INSERT INTO django_migrations VALUES(6,'auth','0004_alter_user_username_opts','2025-06-30 10:59:11.832703');
INSERT INTO django_migrations VALUES(7,'auth','0005_alter_user_last_login_null','2025-06-30 10:59:11.846111');
INSERT INTO django_migrations VALUES(8,'auth','0006_require_contenttypes_0002','2025-06-30 10:59:11.850630');
INSERT INTO django_migrations VALUES(9,'auth','0007_alter_validators_add_error_messages','2025-06-30 10:59:11.862145');
INSERT INTO django_migrations VALUES(10,'auth','0008_alter_user_username_max_length','2025-06-30 10:59:11.870462');
INSERT INTO django_migrations VALUES(11,'auth','0009_alter_user_last_name_max_length','2025-06-30 10:59:11.879821');
INSERT INTO django_migrations VALUES(12,'auth','0010_alter_group_name_max_length','2025-06-30 10:59:11.890216');
INSERT INTO django_migrations VALUES(13,'auth','0011_update_proxy_permissions','2025-06-30 10:59:11.905910');
INSERT INTO django_migrations VALUES(14,'auth','0012_alter_user_first_name_max_length','2025-06-30 10:59:11.914272');
INSERT INTO django_migrations VALUES(15,'login','0001_initial','2025-06-30 10:59:11.939828');
INSERT INTO django_migrations VALUES(16,'admin','0001_initial','2025-06-30 10:59:11.953969');
INSERT INTO django_migrations VALUES(17,'admin','0002_logentry_remove_auto_add','2025-06-30 10:59:11.967709');
INSERT INTO django_migrations VALUES(18,'admin','0003_logentry_add_action_flag_choices','2025-06-30 10:59:11.978891');
INSERT INTO django_migrations VALUES(19,'login','0002_pedido_mercado_pago_id_pedido_status_pagamento','2025-06-30 10:59:11.987498');
INSERT INTO django_migrations VALUES(20,'sessions','0001_initial','2025-06-30 10:59:11.996432');

CREATE TABLE IF NOT EXISTS "django_content_type" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO django_content_type VALUES(1,'admin','logentry');
INSERT INTO django_content_type VALUES(2,'auth','permission');
INSERT INTO django_content_type VALUES(3,'auth','group');
INSERT INTO django_content_type VALUES(4,'contenttypes','contenttype');
INSERT INTO django_content_type VALUES(5,'sessions','session');
INSERT INTO django_content_type VALUES(6,'login','pedido');
INSERT INTO django_content_type VALUES(7,'login','create_user');
INSERT INTO django_content_type VALUES(8,'login','endereco');
INSERT INTO django_content_type VALUES(9,'login','carrinho');

CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "group_id" int NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" int NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "auth_permission" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "content_type_id" int NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

INSERT INTO auth_permission VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO auth_permission VALUES(2,1,'change_logentry','Can change log entry');
INSERT INTO auth_permission VALUES(3,1,'delete_logentry','Can delete log entry');
INSERT INTO auth_permission VALUES(4,1,'view_logentry','Can view log entry');
INSERT INTO auth_permission VALUES(5,2,'add_permission','Can add permission');
INSERT INTO auth_permission VALUES(6,2,'change_permission','Can change permission');
INSERT INTO auth_permission VALUES(7,2,'delete_permission','Can delete permission');
INSERT INTO auth_permission VALUES(8,2,'view_permission','Can view permission');
INSERT INTO auth_permission VALUES(9,3,'add_group','Can add group');
INSERT INTO auth_permission VALUES(10,3,'change_group','Can change group');
INSERT INTO auth_permission VALUES(11,3,'delete_group','Can delete group');
INSERT INTO auth_permission VALUES(12,3,'view_group','Can view group');
INSERT INTO auth_permission VALUES(13,4,'add_contenttype','Can add content type');
INSERT INTO auth_permission VALUES(14,4,'change_contenttype','Can change content type');
INSERT INTO auth_permission VALUES(15,4,'delete_contenttype','Can delete content type');
INSERT INTO auth_permission VALUES(16,4,'view_contenttype','Can view content type');
INSERT INTO auth_permission VALUES(17,5,'add_session','Can add session');
INSERT INTO auth_permission VALUES(18,5,'change_session','Can change session');
INSERT INTO auth_permission VALUES(19,5,'delete_session','Can delete session');
INSERT INTO auth_permission VALUES(20,5,'view_session','Can view session');
INSERT INTO auth_permission VALUES(21,6,'add_pedido','Can add pedido');
INSERT INTO auth_permission VALUES(22,6,'change_pedido','Can change pedido');
INSERT INTO auth_permission VALUES(23,6,'delete_pedido','Can delete pedido');
INSERT INTO auth_permission VALUES(24,6,'view_pedido','Can view pedido');
INSERT INTO auth_permission VALUES(25,7,'add_create_user','Can add create_ user');
INSERT INTO auth_permission VALUES(26,7,'change_create_user','Can change create_ user');
INSERT INTO auth_permission VALUES(27,7,'delete_create_user','Can delete create_ user');
INSERT INTO auth_permission VALUES(28,7,'view_create_user','Can view create_ user');
INSERT INTO auth_permission VALUES(29,8,'add_endereco','Can add endereco');
INSERT INTO auth_permission VALUES(30,8,'change_endereco','Can change endereco');
INSERT INTO auth_permission VALUES(31,8,'delete_endereco','Can delete endereco');
INSERT INTO auth_permission VALUES(32,8,'view_endereco','Can view endereco');
INSERT INTO auth_permission VALUES(33,9,'add_carrinho','Can add carrinho');
INSERT INTO auth_permission VALUES(34,9,'change_carrinho','Can change carrinho');
INSERT INTO auth_permission VALUES(35,9,'delete_carrinho','Can delete carrinho');
INSERT INTO auth_permission VALUES(36,9,'view_carrinho','Can view carrinho');

CREATE TABLE IF NOT EXISTS "auth_group" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "name" varchar(150) NOT NULL UNIQUE);

CREATE TABLE IF NOT EXISTS "login_create_user" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "nome" varchar(100) NOT NULL, "cpf" varchar(14) NULL UNIQUE, "email" varchar(254) NOT NULL UNIQUE, "telefone" varchar(20) NULL, "role" varchar(20) NOT NULL, "ativo" bool NOT NULL, "criado_em" datetime NOT NULL, "mfa_secret" varchar(16) NULL, "mfa_enabled" bool NOT NULL, "is_active" bool NOT NULL, "is_staff" bool NOT NULL);
INSERT INTO login_create_user VALUES(1,'!gJAoHhSvqJUkTq5cksjqXaj4iwsYOgyyLccQRI0o','2025-06-30 11:15:25.511444',0,'Gustavo Ribeiro da Silva Said','gAAAAABoYnG4GOvONar61C1ihkCy_R1rDtQGEn5NJhhXbgJEeGi9VOlBkN_h6pD2W8SXX8Ev3Mylt2hPyi8mUDRiVmQmWSuGEQ==','teste13@gmail.com','34996336172','cliente',1,'2025-06-30 11:15:04.040442','G7VHOFZ5WIKSZRJOFY2YVZCP6RNIGY23',1,1,0);

CREATE TABLE IF NOT EXISTS "login_create_user_groups" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "create_user_id" bigint NOT NULL REFERENCES "login_create_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" int NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "login_create_user_user_permissions" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "create_user_id" bigint NOT NULL REFERENCES "login_create_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" int NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "login_endereco" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "endereco" varchar(50) NOT NULL, "bairro" varchar(50) NOT NULL, "numero" varchar(5) NOT NULL, "complemento" varchar(25) NOT NULL, "cep" varchar(9) NOT NULL, "userEndereco_id" bigint NOT NULL REFERENCES "login_create_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "login_carrinho" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "quantidade" int NOT NULL, "usuario_id" bigint NOT NULL REFERENCES "login_create_user" ("id") DEFERRABLE INITIALLY DEFERRED, "produto_id" bigint NOT NULL REFERENCES "login_pedido" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" int NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "login_create_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);

CREATE TABLE IF NOT EXISTS "login_pedido" ("id" int NOT NULL PRIMARY KEY AUTO_INCREMENT, "categoria" varchar(50) NULL, "foto" varchar(100) NOT NULL, "descricao" text NOT NULL, "valor" decimal NOT NULL, "data_criacao" datetime NOT NULL, "mercado_pago_id" varchar(100) NULL, "status_pagamento" varchar(20) NOT NULL);

CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

INSERT INTO django_session VALUES('lg1a9cnd6520qbrp7y05obnqovq55qkx','.eJxVjM0OwiAQhN-FsyFsQagevfsMzVJ2BX9KU8rJ-O62SY3pcb75Zt5iptfY1UJTl4I4w0HUUnFK-Rc7rHP8CwLEjnnsHzSsRbjjcMuyz8M8JS9XRW5tkdcc6HnZ3N1BxBKXNSsPRzaBiRom9sooAG_BB-sMN1YbQ3gCcE5b7VQgwNbQg
thx02onPl8EaULr:1uWCTt:zUDwvPwuogPiDcJHaLpgufxWRIekSZ7UkMAVp2T8knw','2025-07-14 11:15:25.514964');

DELETE FROM sqlite_sequence;

INSERT INTO sqlite_sequence VALUES('django_migrations',20);
INSERT INTO sqlite_sequence VALUES('django_content_type',9);
INSERT INTO sqlite_sequence VALUES('auth_permission',36);
INSERT INTO sqlite_sequence VALUES('auth_group',0);
INSERT INTO sqlite_sequence VALUES('django_admin_log',0);
INSERT INTO sqlite_sequence VALUES('login_pedido',0);
INSERT INTO sqlite_sequence VALUES('login_create_user',1);

CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

CREATE UNIQUE INDEX "login_create_user_groups_create_user_id_group_id_6a1c3d86_uniq" ON "login_create_user_groups" ("create_user_id", "group_id");

CREATE INDEX "login_create_user_groups_create_user_id_657b5357" ON "login_create_user_groups" ("create_user_id");

CREATE INDEX "login_create_user_groups_group_id_7fa0552a" ON "login_create_user_groups" ("group_id");

CREATE UNIQUE INDEX "login_create_user_user_permissions_create_user_id_permission_id_35e6ef65_uniq" ON "login_create_user_user_permissions" ("create_user_id", "permission_id");

CREATE INDEX "login_create_user_user_permissions_create_user_id_da8fc360" ON "login_create_user_user_permissions" ("create_user_id");

CREATE INDEX "login_create_user_user_permissions_permission_id_27f846e5" ON "login_create_user_user_permissions" ("permission_id");

CREATE INDEX "login_endereco_userEndereco_id_ff941dee" ON "login_endereco" ("userEndereco_id");

CREATE INDEX "login_carrinho_usuario_id_2c8b8dc0" ON "login_carrinho" ("usuario_id");

CREATE INDEX "login_carrinho_produto_id_3258ea1b" ON "login_carrinho" ("produto_id");

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

