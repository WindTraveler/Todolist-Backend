/*
 Navicat Premium Data Transfer

 Source Server         : localhost_5432
 Source Server Type    : PostgreSQL
 Source Server Version : 90605
 Source Host           : localhost:5432
 Source Catalog        : notedb
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 90605
 File Encoding         : 65001

 Date: 18/12/2017 18:42:37
*/


-- ----------------------------
-- Sequence structure for notes_note_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."notes_note_id_seq";
CREATE SEQUENCE "public"."notes_note_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_user_id_seq";
CREATE SEQUENCE "public"."users_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for notes
-- ----------------------------
DROP TABLE IF EXISTS "public"."notes";
CREATE TABLE "public"."notes" (
  "note_id" int4 NOT NULL DEFAULT nextval('notes_note_id_seq'::regclass),
  "content" varchar(255) COLLATE "pg_catalog"."default" NOT NULL DEFAULT NULL,
  "completed" bool NOT NULL DEFAULT NULL,
  "deleted" bool NOT NULL DEFAULT NULL,
  "user_id" int4 NOT NULL DEFAULT NULL
)
;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "user_id" int4 NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
  "user_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL DEFAULT NULL,
  "pwd_hash" varchar(255) COLLATE "pg_catalog"."default" NOT NULL DEFAULT NULL
)
;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."notes_note_id_seq"
OWNED BY "public"."notes"."note_id";
SELECT setval('"public"."notes_note_id_seq"', 9, true);
ALTER SEQUENCE "public"."users_user_id_seq"
OWNED BY "public"."users"."user_id";
SELECT setval('"public"."users_user_id_seq"', 3, true);

-- ----------------------------
-- Primary Key structure for table notes
-- ----------------------------
ALTER TABLE "public"."notes" ADD CONSTRAINT "notes_pkey" PRIMARY KEY ("note_id");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("user_id");
