

-- sql
-- {expiration_date}|{start_date}|{full_name}|{company}|{email}|{license_type}|{nodes}
DROP TABLE IF EXISTS `license`;
CREATE TABLE `license` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `company` varchar(100) NOT NULL DEFAULT '' COMMENT '公司',
    `email` varchar(100) NOT NULL DEFAULT '' COMMENT '邮箱',
    `full_name` varchar(100) NOT NULL DEFAULT '' COMMENT '联系人姓名',
    `nodes` int(11) NOT NULL DEFAULT 0 COMMENT '节点数量',
    `license_type` varchar(30) NOT NULL DEFAULT '' COMMENT 'License类型',
    `hostname` varchar(32) NOT NULL DEFAULT '' COMMENT '主机名',
    `start_date` varchar(30) NOT NULL DEFAULT '' COMMENT '生效时间',
    `expiration_date` varchar(30) NOT NULL DEFAULT '' COMMENT '过期时间',
    `ctime` bigint(20) NOT NULL DEFAULT 0 COMMENT '创建时间',
    `cuser` int(11) NOT NULL DEFAULT 0 COMMENT '创建用户',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT charset=utf8 COLLATE=utf8_unicode_ci COMMENT 'License管理表';
