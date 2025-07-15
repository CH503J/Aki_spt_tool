/*
 Navicat Premium Dump SQL

 Source Server         : 123
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 15/07/2025 17:47:37
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for language_info
-- ----------------------------
DROP TABLE IF EXISTS "language_info";
CREATE TABLE "language_info" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "item_id" text,
  "name" TEXT,
  "short_name" TEXT,
  "description" TEXT,
  "fail_message" TEXT,
  "success_message" TEXT,
  "accept_player_message" TEXT,
  "decline_player_message" TEXT,
  "complete_player_message" TEXT,
  "other_value" TEXT,
  "type" TEXT
);

-- ----------------------------
-- Auto increment value for language_info
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 114736 WHERE name = 'language_info';

PRAGMA foreign_keys = true;




-- =====================================SQL=====================================
-- name: get_language_info
INSERT INTO language_info (
                item_id,
                name,
                short_name,
                description,
                fail_message,
                success_message,
                accept_player_message,
                decline_player_message,
                complete_player_message,
                other_value,
                type
            ) VALUES (
                :item_id,
                :name,
                :short_name,
                :description,
                :fail_message,
                :success_message,
                :accept_player_message,
                :decline_player_message,
                :complete_player_message,
                :other_value,
                :type
            )

-- name: delete_language_info
DELETE FROM language_info

-- name: search_data
SELECT *
FROM language_info
WHERE
    item_id LIKE '%' || ? || '%' OR
    name LIKE '%' || ? || '%' OR
    short_name LIKE '%' || ? || '%' OR
    description LIKE '%' || ? || '%' OR
    fail_message LIKE '%' || ? || '%' OR
    success_message LIKE '%' || ? || '%' OR
    accept_player_message LIKE '%' || ? || '%' OR
    decline_player_message LIKE '%' || ? || '%' OR
    complete_player_message LIKE '%' || ? || '%' OR
    other_value LIKE '%' || ? || '%';

-- name: search_data_by_field
SELECT *
FROM language_info
WHERE {key} LIKE ?



-- name: search_data_by_type
SELECT *
FROM language_info
WHERE (
    item_id LIKE :kw OR
    name LIKE :kw OR
    short_name LIKE :kw OR
    description LIKE :kw OR
    fail_message LIKE :kw OR
    success_message LIKE :kw OR
    accept_player_message LIKE :kw OR
    decline_player_message LIKE :kw OR
    complete_player_message LIKE :kw OR
    other_value LIKE :kw
) AND type = :type;

-- name: search_data_all
SELECT *
FROM language_info
WHERE
    item_id LIKE :kw OR
    name LIKE :kw OR
    short_name LIKE :kw OR
    description LIKE :kw OR
    fail_message LIKE :kw OR
    success_message LIKE :kw OR
    accept_player_message LIKE :kw OR
    decline_player_message LIKE :kw OR
    complete_player_message LIKE :kw OR
    other_value LIKE :kw;