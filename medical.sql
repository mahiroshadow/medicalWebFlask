/*
 Navicat Premium Data Transfer

 Source Server         : local-mysql
 Source Server Type    : MySQL
 Source Server Version : 50536
 Source Host           : localhost:3306
 Source Schema         : medical

 Target Server Type    : MySQL
 Target Server Version : 50536
 File Encoding         : 65001

 Date: 25/03/2024 17:05:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for algorithm
-- ----------------------------
DROP TABLE IF EXISTS `algorithm`;
CREATE TABLE `algorithm`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `algorithm_name` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `algorithm_description` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `upload_time` datetime NOT NULL,
  `save_pth` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `start_code` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `type` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of algorithm
-- ----------------------------
INSERT INTO `algorithm` VALUES (1, '高斯混合', '自定义', '2024-03-17 16:16:47', '/home/baseline/data.csv', NULL, 1);
INSERT INTO `algorithm` VALUES (2, 'XGBOOST', '默认上传', '2024-03-18 15:27:39', '暂无', NULL, 0);

-- ----------------------------
-- Table structure for container
-- ----------------------------
DROP TABLE IF EXISTS `container`;
CREATE TABLE `container`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `container_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `container_name` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `command` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `log` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `user_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `image_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of container
-- ----------------------------
INSERT INTO `container` VALUES (1, '38fda64acb1c', 'romantic_feistel', 'sh ./start.sh', '2024-03-21', 'running', 'stdout', '1', '22c5bcf0d5e7');

-- ----------------------------
-- Table structure for images
-- ----------------------------
DROP TABLE IF EXISTS `images`;
CREATE TABLE `images`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `image_name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `image_size` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `create_time` date NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of images
-- ----------------------------
INSERT INTO `images` VALUES (1, '22c5bcf0d5e7', 'python3.8', '998MB', '2024-03-21');

-- ----------------------------
-- Table structure for model
-- ----------------------------
DROP TABLE IF EXISTS `model`;
CREATE TABLE `model`  (
  `model_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `train_data_id` int(11) NULL DEFAULT NULL,
  `save_pth` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `model_description` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `create_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`model_id`) USING BTREE,
  INDEX `train_data_id`(`train_data_id`) USING BTREE,
  CONSTRAINT `model_ibfk_1` FOREIGN KEY (`train_data_id`) REFERENCES `train` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of model
-- ----------------------------
INSERT INTO `model` VALUES (7, 'model', NULL, NULL, NULL, '111', '2024-03-17 13:15:06');
INSERT INTO `model` VALUES (8, 'model1', NULL, NULL, NULL, '111', '2024-03-17 13:15:48');

-- ----------------------------
-- Table structure for train
-- ----------------------------
DROP TABLE IF EXISTS `train`;
CREATE TABLE `train`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `upload_time` datetime NOT NULL,
  `save_pth` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fill_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `size` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `type` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `file_name`(`file_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of train
-- ----------------------------
INSERT INTO `train` VALUES (12, 'validate_1000.csv', '2024-03-13 14:45:34', 'E://tempFile//validate_1000.csv', NULL, '1741', 'csv');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `avatar_url` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '96096', 'default', '123456', 'https://wsystorage-1316338016.cos.ap-nanjing.myqcloud.com/user/default.png');

SET FOREIGN_KEY_CHECKS = 1;
