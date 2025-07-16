/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EStockType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 证券类别
 *
 */
public enum EStockType {
	/**
	 * 默认 (0)
	 */
	MINOR_KIND_UNDEFINED(0),

	/**
	 * 指数 (1)
	 */
	MAJOR_KIND_INDEX(1),

	/**
	 * 股票 (2)
	 */
	MAJOR_KIND_STOCK(2),

	/**
	 * 基金 (3)
	 */
	MAJOR_KIND_FUND(3),

	/**
	 * 债券 (4)
	 */
	MAJOR_KIND_BOND(4),

	/**
	 * 权证 (5)
	 */
	MAJOR_KIND_WARRANT(5),

	/**
	 * 质押式回购交易 (6)
	 */
	MAJOR_KIND_REPO(6),

	/**
	 * 期权 (7)
	 */
	MAJOR_KIND_OPTION(7),

	/**
	 * 优先股 (8)
	 */
	MAJOR_KIND_PREFERRED_STOCK(8),

	/**
	 * 资产支持证券 (9)
	 */
	MAJOR_KIND_ABS(9),

	/**
	 * 非交易 (10)
	 */
	MAJOR_KIND_FJY(10),

	/**
	 * 房地产信托投资基金(REITs) (11)
	 */
	MAJOR_KIND_REIT(11),

	/**
	 * 以人民币交易的股票（主板） (12)
	 */
	SH_MINOR_KIND_STOCK_ASH(12),

	/**
	 * 以美元交易的股票 (13)
	 */
	SH_MINOR_KIND_STOCK_BSH(13),

	/**
	 * 以人民币交易的股票（科创板） (14)
	 */
	SH_MINOR_KIND_STOCK_KSH(14),

	/**
	 * 其它股票 (15)
	 */
	SH_MINOR_KIND_STOCK_OEQ(15),

	/**
	 * 封闭式基金 (16)
	 */
	SH_MINOR_KIND_FUND_CEF(16),

	/**
	 * 开放式基金 (17)
	 */
	SH_MINOR_KIND_FUND_OEF(17),

	/**
	 * ETF基金 (18)
	 */
	SH_MINOR_KIND_FUND_EBS(18),

	/**
	 * 跨市场 / 跨境基金 (19)
	 */
	SH_MINOR_KIND_FUND_FBL(19),

	/**
	 * 其它基金 (20)
	 */
	SH_MINOR_KIND_FUND_OFN(20),

	/**
	 * LOF基金 (21)
	 */
	SH_MINOR_KIND_FUND_LOF(21),

	/**
	 * 国债、地方债、政府支持债、政策性金融债 (22)
	 */
	SH_MINOR_KIND_BOND_GBF(22),

	/**
	 * 无息国债 (弃用) (23)
	 */
	SH_MINOR_KIND_BOND_GBZ(23),

	/**
	 * 国债分销（仅用于分销阶段） (24)
	 */
	SH_MINOR_KIND_BOND_DST(24),

	/**
	 * 公司债（地方债）分销 (25)
	 */
	SH_MINOR_KIND_BOND_DVP(25),

	/**
	 * 企业债券 (26)
	 */
	SH_MINOR_KIND_BOND_CBF(26),

	/**
	 * 可转换企业债券 (27)
	 */
	SH_MINOR_KIND_BOND_CCF(27),

	/**
	 * 公司债、企业债、可交换债、政府支持债 (28)
	 */
	SH_MINOR_KIND_BOND_CPF(28),

	/**
	 * 金融机构发行债券 (弃用) (29)
	 */
	SH_MINOR_KIND_BOND_FBF(29),

	/**
	 * 通用质押式回购 (30)
	 */
	SH_MINOR_KIND_BOND_CRP(30),

	/**
	 * 质押式企债回购 (弃用) (31)
	 */
	SH_MINOR_KIND_BOND_BRP(31),

	/**
	 * 买断式债券回购 (弃用) (32)
	 */
	SH_MINOR_KIND_BOND_ORP(32),

	/**
	 * 分离式可转债 (弃用) (33)
	 */
	SH_MINOR_KIND_BOND_CBD(33),

	/**
	 * 其它债券 (34)
	 */
	SH_MINOR_KIND_BOND_OBD(34),

	/**
	 * 国债预发行 (35)
	 */
	SH_MINOR_KIND_BOND_WIT(35),

	/**
	 * 集合资产管理计划 (36)
	 */
	SH_MINOR_KIND_AMP(36),

	/**
	 * 公开发行优先股 (37)
	 */
	SH_MINOR_KIND_OPS(37),

	/**
	 * 非公开发行优先股 (38)
	 */
	SH_MINOR_KIND_PPS(38),

	/**
	 * 报价回购 (39)
	 */
	SH_MINOR_KIND_QRP(39),

	/**
	 * 控制指令（中登身份认证密码服务产品复用CMD证券子类别） (40)
	 */
	SH_MINOR_KIND_CMD(40),

	/**
	 * 上网证券发行申购 (41)
	 */
	SH_FJY_MINOR_KIND_IN(41),

	/**
	 * 老股东增发证券发行申购 (42)
	 */
	SH_FJY_MINOR_KIND_IS(42),

	/**
	 * IPO配号 (43)
	 */
	SH_FJY_MINOR_KIND_PH(43),

	/**
	 * IPO扣款 (44)
	 */
	SH_FJY_MINOR_KIND_KK(44),

	/**
	 * IPO还款 (45)
	 */
	SH_FJY_MINOR_KIND_HK(45),

	/**
	 * 可转债转股 / 可交换公司债换股 (46)
	 */
	SH_FJY_MINOR_KIND_CV(46),

	/**
	 * 可转债回售 (47)
	 */
	SH_FJY_MINOR_KIND_CR(47),

	/**
	 * 股票配股行权行权 (48)
	 */
	SH_FJY_MINOR_KIND_R1(48),

	/**
	 * 股票转配股配股行权 (49)
	 */
	SH_FJY_MINOR_KIND_R2(49),

	/**
	 * 职工股转配股配股行权 (50)
	 */
	SH_FJY_MINOR_KIND_R3(50),

	/**
	 * 股票配转债行权 (51)
	 */
	SH_FJY_MINOR_KIND_R4(51),

	/**
	 * 开放式基金认购 (52)
	 */
	SH_FJY_MINOR_KIND_OS(52),

	/**
	 * 开放式基金申购 (53)
	 */
	SH_FJY_MINOR_KIND_OC(53),

	/**
	 * 开放式基金赎回 (54)
	 */
	SH_FJY_MINOR_KIND_OR(54),

	/**
	 * 开放式基金分红选择 (55)
	 */
	SH_FJY_MINOR_KIND_OD(55),

	/**
	 * 开放式基金份额转出 (56)
	 */
	SH_FJY_MINOR_KIND_OT(56),

	/**
	 * 开放式基金转换 (57)
	 */
	SH_FJY_MINOR_KIND_OV(57),

	/**
	 * ETF申购 (58)
	 */
	SH_FJY_MINOR_KIND_EC(58),

	/**
	 * ETF赎回 (59)
	 */
	SH_FJY_MINOR_KIND_ER(59),

	/**
	 * 申赎资金代码 (60)
	 */
	SH_FJY_MINOR_KIND_EZ(60),

	/**
	 * 回购入库 (61)
	 */
	SH_FJY_MINOR_KIND_BD(61),

	/**
	 * 回购出库 (62)
	 */
	SH_FJY_MINOR_KIND_BW(62),

	/**
	 * 要约预受 (63)
	 */
	SH_FJY_MINOR_KIND_FS(63),

	/**
	 * 要约撤销 (64)
	 */
	SH_FJY_MINOR_KIND_FC(64),

	/**
	 * 余券划转 (65)
	 */
	SH_FJY_MINOR_KIND_ST(65),

	/**
	 * 还券划转 (66)
	 */
	SH_FJY_MINOR_KIND_SR(66),

	/**
	 * 担保品划入 (67)
	 */
	SH_FJY_MINOR_KIND_CI(67),

	/**
	 * 担保品划出 (68)
	 */
	SH_FJY_MINOR_KIND_CO(68),

	/**
	 * 券源划入 (69)
	 */
	SH_FJY_MINOR_KIND_SI(69),

	/**
	 * 券源划出 (70)
	 */
	SH_FJY_MINOR_KIND_SO(70),

	/**
	 * 密码激活(注销) (71)
	 */
	SH_FJY_MINOR_KIND_PA(71),

	/**
	 * 指定登记 (72)
	 */
	SH_FJY_MINOR_KIND_DT(72),

	/**
	 * 指定撤销 (73)
	 */
	SH_FJY_MINOR_KIND_DC(73),

	/**
	 * 其它 (74)
	 */
	SH_FJY_MINOR_KIND_QT(74),
	/**
	 * 科创板ETF基金 (75)
	 */
	SH_MINOR_KIND_FUND_KES(75),

	/**
	 * 科创板LOF基金 (76)
	 */
	SH_MINOR_KIND_FUND_KOF(76),

	/**
	 * 定向可转债 (77)
	 */
	SH_MINOR_KIND_BOND_TCB(77),

	/**
	 * 科创板可转债 (78)
	 */
	SH_MINOR_KIND_BOND_KCCF(78),

	/**
	 * REITs (79)
	 */
	SH_MINOR_KIND_REITS_RET(79),

	/**
	 * 主板 A 股
	 */
	SZ_MINOR_KIND_STOCK_ZHU_BAN_A(80),

	/**
	 * 中小板股票
	 */
	SZ_MINOR_KIND_STOCK_ZHONG_XIAO_BAN(81),

	/**
	 * 创业板股票
	 */
	SZ_MINOR_KIND_STOCK_CHUANG_YE_BAN(82),

	/**
	 * 主板 B 股
	 */
	SZ_MINOR_KIND_STOCK_ZHU_BAN_B(83),

	/**
	 * 国债（含地方债）
	 */
	SZ_MINOR_KIND_BOND_TREASURY_BOND(84),

	/**
	 * 企业债
	 */
	SZ_MINOR_KIND_BOND_ENTERPRISE_BOND(85),

	/**
	 * 公司债
	 */
	SZ_MINOR_KIND_BOND_CORPORATE_BOND(86),

	/**
	 * 可转债
	 */
	SZ_MINOR_KIND_BOND_CONVERTIBLE_BOND(87),

	/**
	 * 私募债
	 */
	SZ_MINOR_KIND_BOND_PRIVATELY_RAISED_COMPANY_BONDS(88),

	/**
	 * 可交换私募债
	 */
	SZ_MINOR_KIND_BOND_EXCHANGEABLE_PB(89),

	/**
	 * 证券公司次级债
	 */
	SZ_MINOR_KIND_BOND_SECURITY_COMPANY_SUB_DEBT(90),

	/**
	 * 质押式回购
	 */
	SZ_MINOR_KIND_REPO_PLEDGE_STYLE_REPO(91),

	/**
	 * 资产支持证券
	 */
	SZ_MINOR_KIND_ASSET_BACKED_SECURITIES(92),

	/**
	 * 本市场股票 ETF
	 */
	SZ_MINOR_KIND_FUND_STOCK_ETF(93),

	/**
	 * 跨市场股票 ETF
	 */
	SZ_MINOR_KIND_FUND_INTER_MARKET_STOCK_ETF(94),

	/**
	 * 跨境 ETF
	 */
	SZ_MINOR_KIND_FUND_CROSS_BORDER_ETF(95),

	/**
	 * 本市场实物债券 ETF
	 */
	SZ_MINOR_KIND_FUND_BEARER_BOND_ETF(96),

	/**
	 * 现金债券 ETF
	 */
	SZ_MINOR_KIND_FUND_CASH_BOND_ETF(97),

	/**
	 * 黄金 ETF
	 */
	SZ_MINOR_KIND_FUND_GOLD_ETF(98),

	/**
	 * 货币 ETF
	 */
	SZ_MINOR_KIND_FUND_CURRENCY_ETF(99),

	/**
	 * 杠杆 ETF
	 */
	SZ_MINOR_KIND_FUND_LEVER_ETF(100),

	/**
	 * 商品期货 ETF
	 */
	SZ_MINOR_KIND_FUND_COMMODITY_FUTURES_ETF(101),

	/**
	 * 标准 LOF
	 */
	SZ_MINOR_KIND_FUND_STANDARD_LOF(102),

	/**
	 * 分级子基金
	 */
	SZ_MINOR_KIND_FUND_GRADED_SUB_FUNDS(103),

	/**
	 * 封闭式基金
	 */
	SZ_MINOR_KIND_FUND_CLOSED_END_FUNDS(104),

	/**
	 * 仅申赎基金
	 */
	SZ_MINOR_KIND_FUND_REDEMPTION_FUND(105),

	/**
	 * 权证
	 */
	SZ_MINOR_KIND_WARRANT(106),

	/**
	 * 个股期权
	 */
	SZ_MINOR_KIND_OPTION_STOCK_OPTION(107),

	/**
	 * ETF 期权
	 */
	SZ_MINOR_KIND_OPTION_ETF_OPTION(108),

	/**
	 * 优先股
	 */
	SZ_MINOR_KIND_PREFERRED_STOCK(109),

	/**
	 * 证券公司短期债
	 */
	SZ_MINOR_KIND_BOND_SECURITY_COMPANY_SHORT_TERM_BOND(110),

	/**
	 * 可交换公司债
	 */
	SZ_MINOR_KIND_BOND_EXCHANGEABLE_CORPORATE_BOND(111),

	/**
	 * 主板、中小板存托凭证
	 */
	SZ_MINOR_KIND_STOCK_CDR(112),

	/**
	 * 创业板存托凭证
	 */
	SZ_MINOR_KIND_STOCK_CHUANG_YE_CDR(113),

	/**
	 * 基础设施基金
	 */
	SZ_MINOR_KIND_FUND_INFRASTRUCTURE_FUND(114),

	/**
	 * 定向可转债
	 */
	SZ_MINOR_KIND_BOND_ORIENT_CONVERTIBLE_BOND(115),
		 
	/**
	 * 网上认购
	 */
	SZ_FJY_MINOR_KIND_ISSUE(116),

	/**
	 * 债券分销
	 */
	SZ_FJY_MINOR_KIND_BOND_DISTRIBUTION(117),

	/**
	 * 配股
	 */
	SZ_FJY_MINOR_KIND_RIGHTS_ISSUE(118),

	/**
	 * 衍生品交易
	 */
	SZ_FJY_MINOR_KIND_DERIVATIVEAUCTION(119),

	/**
	 * 协议交易
	 */
	SZ_FJY_MINOR_KIND_NEGOTIATION(120),

	/**
	 * 增发
	 */
	SZ_FJY_MINOR_KIND_ISSUE_ADDITIONNAL(121),

	/**
	 * 配债
	 */
	SZ_FJY_MINOR_KIND_BOND_RIGHTS_ISSUE(122),

	/**
	 * 两网公司及退市公司A股
	 */
	NEEQ_MINOR_KIND_STOCK_DELIST_COMPANY_A(123),

	/**
	 * 两网公司及退市公司B股
	 */
	NEEQ_MINOR_KIND_STOCK_DELIST_COMPANY_B(124),

	/**
	 * 挂牌公司股票
	 */
	NEEQ_MINOR_KIND_STOCK_LISTED_COMPANY(125),

	/**
	 * 优先股
	 */
	NEEQ_MINOR_KIND_PREFERRED_STOCK(126),

	/**
	 * 要约收购
	 */
	NEEQ_MINOR_KIND_TENDER_OFFER(127),

	/**
	 * 要约回购
	 */
	NEEQ_MINOR_KIND_OFFER_TO_REPURCHASE(128),

	/**
	 * 股权激励期权
	 */
	NEEQ_MINOR_KIND_EQUITY_INCENTIVE_OPTION(129),

	/**
	 * 指数
	 */
	NEEQ_MINOR_KIND_INDEX(130),

	/**
	 * 发行业务
	 */
	NEEQ_MINOR_KIND_ISSUE_TRANSACTION(131),

	/**
	 * 可转债
	 */
	NEEQ_MINOR_KIND_CONVERTIBLE_BOND(132),

	/**
	 * 定向可转债
	 */
	NEEQ_MINOR_KIND_ORIENT_CONVERTIBLE_BOND(133),

	/**
	 * 退市可转债
	 */
	NEEQ_MINOR_KIND_DELIST_CONVERTIBLE_BOND(134),

	/**
	 * 国债
	 */
	SHFI_MINOR_KIND_TREASURY_BOND(135),

	/**
	 * 公司债
	 */
	SHFI_MINOR_KIND_CORPORATE_BOND(136),

	/**
	 * 私募债券
	 */
	SHFI_MINOR_KIND_PRIVATE_PLACEMENT_BOND(137),

	/**
	 * 信贷资产支持证券
	 */
	SHFI_MINOR_KIND_ABS(138),

	/**
	 * 特定债券
	 */
	SHFI_MINOR_KIND_SPECIAL_BOND(139),

	/**
	 * 公募REITs
	 */
	SHFI_MINOR_KIND_REITS(140),

	/**
	 * 公募可转债
	 */
	SHFI_MINOR_KIND_CONVERTIBLE_BOND(141),
 
    
    _C_PRTP_COUNT(142);

    public final int value;
    
    EStockType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
