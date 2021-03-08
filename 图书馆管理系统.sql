/*
Navicat MySQL Data Transfer

Source Server         : test
Source Server Version : 80020
Source Host           : localhost:3306
Source Database       : 图书馆管理系统

Target Server Type    : MYSQL
Target Server Version : 80020
File Encoding         : 65001

Date: 2020-06-14 01:57:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `借阅信息`
-- ----------------------------
DROP TABLE IF EXISTS `借阅信息`;
CREATE TABLE `借阅信息` (
  `学号` varchar(4) NOT NULL,
  `书号` varchar(6) NOT NULL,
  `借书日期` date NOT NULL,
  `还书日期` date NOT NULL,
  `续借状态` varchar(1) NOT NULL,
  PRIMARY KEY (`学号`,`书号`,`借书日期`),
  KEY `书号` (`书号`),
  CONSTRAINT `借阅信息_ibfk_1` FOREIGN KEY (`书号`) REFERENCES `图书` (`书号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 借阅信息
-- ----------------------------

-- ----------------------------
-- Table structure for `图书`
-- ----------------------------
DROP TABLE IF EXISTS `图书`;
CREATE TABLE `图书` (
  `书号` varchar(6) NOT NULL,
  `书名` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `作者` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `出版社` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `可借状态` tinyint unsigned NOT NULL DEFAULT '1',
  `可约状态` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`书号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 图书
-- ----------------------------
INSERT INTO `图书` VALUES ('000006', '建筑信息化设计', '张晨，张秦编著', '中国建筑工业出版社', '1', '0');
INSERT INTO `图书` VALUES ('000007', 'Web前端开发', '刘敏娜，葛代珍编著', '清华大学出版社', '1', '0');
INSERT INTO `图书` VALUES ('000008', 'C++函数式编程', '（塞尔）伊凡·库奇', '机械工业出版社', '1', '0');
INSERT INTO `图书` VALUES ('000011', '小鲤鱼历险记', '小鲤鱼', '小动物出版社', '1', '0');
INSERT INTO `图书` VALUES ('000012', '网络安全意识导论', '朱诗兵主编', '北京电子工业出版社', '1', '0');
INSERT INTO `图书` VALUES ('000013', '三只松鼠历险记', '三只松鼠', '小动物出版社', '1', '0');
INSERT INTO `图书` VALUES ('000015', '高等数学B', '杜广宝', '武汉大学出版社', '1', '0');

-- ----------------------------
-- Table structure for `时间表`
-- ----------------------------
DROP TABLE IF EXISTS `时间表`;
CREATE TABLE `时间表` (
  `时间` varchar(4) NOT NULL,
  `当前时间` date DEFAULT NULL,
  PRIMARY KEY (`时间`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 时间表
-- ----------------------------
INSERT INTO `时间表` VALUES ('time', '2020-06-14');

-- ----------------------------
-- Table structure for `管理员`
-- ----------------------------
DROP TABLE IF EXISTS `管理员`;
CREATE TABLE `管理员` (
  `账号` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `密码` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `姓名` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `性别` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `电话` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`账号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Records of 管理员
-- ----------------------------
INSERT INTO `管理员` VALUES ('100001', '123456', '李洋', '男', '15623687573');
INSERT INTO `管理员` VALUES ('100002', '123456', '李嬿婌', '女', '15612345678');
INSERT INTO `管理员` VALUES ('100003', '123456', '吴梦洁', '女', '15687654321');

-- ----------------------------
-- Table structure for `读者`
-- ----------------------------
DROP TABLE IF EXISTS `读者`;
CREATE TABLE `读者` (
  `学号` varchar(4) NOT NULL,
  `密码` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `姓名` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `性别` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `学院` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `电话` varchar(11) DEFAULT '0',
  `已借图书数` int NOT NULL,
  `可借图书数` int NOT NULL,
  `罚款` float(5,1) DEFAULT '0.0',
  PRIMARY KEY (`学号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 读者
-- ----------------------------
INSERT INTO `读者` VALUES ('0001', '123456', '刘思鉴', '男', '艺术学院', '13888888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0002', '123456', '陈粒', '女', '艺术学院', '13888888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0003', '123456', '隔壁老樊', '男', '艺术学院', '13888888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0004', '123456', '赵四', '男', '计算机学院', '13388888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0005', '123456', '张一', '女', '国家网络安全学院', '13488888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0006', '123456', '张二', '男', '国家网络安全学院', '13588888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0007', '123456', '张三', '男', '国家网络安全学院', '13688888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0008', '123456', '张四', '女', '国家网络安全学院', '13788888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0009', '123456', '李一', '女', '国家网络安全学院', '13988888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0010', '123456', '李二', '男', '国家网络安全学院', '13088888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0011', '123456', '李三', '女', '国家网络安全学院', '15188888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0012', '123456', '李四', '女', '国家网络安全学院', '15288888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0013', '123456', '吴一', '男', '国家网络安全学院', '15388888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0014', '123456', '吴二', '女', '国家网络安全学院', '15488888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0015', '123456', '吴三', '女', '国家网络安全学院', '15588888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0016', '123456', '吴四', '男', '国家网络安全学院', '15688888887', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0017', '123456', '刘一', '男', '国家网络安全学院', '15788888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0018', '123456', '刘二', '男', '国家网络安全学院', '15888888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0019', '123456', '刘三', '女', '国家网络安全学院', '15988888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0020', '123456', '刘四', '男', '国家网络安全学院', '15088888888', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0021', '123456', '李雷', '男', '国家网络安全学院', '15999999999', '0', '3', '0.0');
INSERT INTO `读者` VALUES ('0022', '123456', '李五', '男', '国家网络安全学院', '15988888888', '0', '3', '0.0');

-- ----------------------------
-- Table structure for `预约信息`
-- ----------------------------
DROP TABLE IF EXISTS `预约信息`;
CREATE TABLE `预约信息` (
  `学号` varchar(4) NOT NULL,
  `书号` varchar(6) NOT NULL,
  `取书日期` date DEFAULT NULL,
  PRIMARY KEY (`学号`,`书号`) USING BTREE,
  KEY `fk_3` (`书号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of 预约信息
-- ----------------------------
