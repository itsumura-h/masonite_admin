admin table schema
===

## admin_menu

```
CREATE TABLE IF NOT EXISTS "admin_menu" (
    "id" integer not null primary key autoincrement,
    "parent_id" integer not null default '0',
    "order" integer not null default '0',
    "title" varchar not null,
    "icon" varchar not null,
    "uri" varchar null,
    "permission" varchar null,
    "created_at" datetime null,
    "updated_at" datetime null
);
```

## admin_operation_log

```
CREATE TABLE IF NOT EXISTS "admin_operation_log" (
    "id" integer not null primary key autoincrement,
    "user_id" integer not null,
    "path" varchar not null,
    "method" varchar not null,
    "ip" varchar not null,
    "input" text not null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE INDEX "admin_operation_log_user_id_index" on "admin_operation_log" ("user_id");
```

## admin_permissions

```
CREATE TABLE IF NOT EXISTS "admin_permissions" (
    "id" integer not null primary key autoincrement,
    "name" varchar not null,
    "slug" varchar not null,
    "http_method" varchar null,
    "http_path" text null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE UNIQUE INDEX "admin_permissions_name_unique" on "admin_permissions" ("name");
```

## admin_role_menu

```
CREATE TABLE IF NOT EXISTS "admin_role_menu" (
    "role_id" integer not null,
    "menu_id" integer not null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE INDEX "admin_role_menu_role_id_menu_id_index" on "admin_role_menu" ("role_id", "menu_id");
```

## admin_role_permissions

```
CREATE TABLE IF NOT EXISTS "admin_role_permissions" (
    "role_id" integer not null,
    "permission_id" integer not null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE INDEX "admin_role_permissions_role_id_permission_id_index" on "admin_role_permissions" ("role_id", "permission_id");
```

## admin_role_users

```
CREATE TABLE IF NOT EXISTS "admin_role_users" (
    "role_id" integer not null,
    "user_id" integer not null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE INDEX "admin_role_users_role_id_user_id_index" on "admin_role_users" ("role_id", "user_id");
```

## admin_roles

```
CREATE TABLE IF NOT EXISTS "admin_roles" (
    "id" integer not null primary key autoincrement,
    "name" varchar not null,
    "slug" varchar not null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE UNIQUE INDEX "admin_roles_name_unique" on "admin_roles" ("name");
```

## admin_user_permissions

```
CREATE TABLE IF NOT EXISTS "admin_user_permissions" (
    "user_id" integer not null,
    "permission_id" integer not null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE INDEX "admin_user_permissions_user_id_permission_id_index" on "admin_user_permissions" ("user_id", "permission_id");
```

## admin_users

```
CREATE TABLE IF NOT EXISTS "admin_users" (
    "id" integer not null primary key autoincrement,
    "username" varchar not null,
    "password" varchar not null,
    "name" varchar not null,
    "avatar" varchar null,
    "remember_token" varchar null,
    "created_at" datetime null,
    "updated_at" datetime null
);
CREATE UNIQUE INDEX "admin_users_username_unique" on "admin_users" ("username");
```

## password_resets

```
CREATE TABLE IF NOT EXISTS "password_resets" (
    "email" varchar not null,
    "token" varchar not null,
    "created_at" datetime null
);
CREATE INDEX "password_resets_email_index" on "password_resets" ("email");
```