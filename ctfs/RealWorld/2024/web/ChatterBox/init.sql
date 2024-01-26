/*
 Navicat Premium Data Transfer

 Source Server         : postgres16&port=15432
 Source Server Type    : PostgreSQL
 Source Server Version : 140010
 Source Host           : localhost:15432
 Source Catalog        : postgres
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 140010
 File Encoding         : 65001

 Date: 30/11/2023 00:49:54
*/

ALTER USER postgres WITH PASSWORD 'postgres';

-- ----------------------------
-- Table structure for message_users
-- ----------------------------
DROP TABLE IF EXISTS "public"."message_users";
CREATE TABLE "public"."message_users" (
  "id" int4,
  "username" text COLLATE "pg_catalog"."default",
  "passwd" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."message_users" OWNER TO "postgres";

-- ----------------------------
-- Records of message_users
-- ----------------------------
BEGIN;
INSERT INTO "public"."message_users" VALUES (1, 'admin', 'xxxxxxx');
COMMIT;

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS "public"."messages";

CREATE TABLE "public"."messages" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE "public"."messages" OWNER TO "postgres";

-- ----------------------------
-- Records of messages
-- ----------------------------
BEGIN;
COMMIT;
