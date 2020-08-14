package com.spring.project3.vo;

import java.sql.Timestamp;
import java.util.Collection;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Component;

@Component
public class Cu_VO {
	//===========================회원관리======================================

	private String id;
	private String pwd;
	private String name;
	private String hp;
	private String email;
	private String address;
	private String enabled;
	private String authority;
	private Timestamp reg_date;
	
	//===========================게시판관리======================================
	
	private int num;
	private String writer;
	private String boardpwd;
	private String subject;
	private String content;
	private int readCnt;
	private int ref;
	private int ref_step;
	private int ref_level;
	private Timestamp board_reg_date;
	
	
	//==============================장바구니====================================
	
	private int CART_NOTB_ID;
	private String CU_ID;
	private String CART_NOTB_NAME;
	private int CART_NOTB_CNT;
	private int CART_NOTB_PRICE;
	private String CART_NOTB_BRAND;
	private String CART_NOTB_IMG;
	
	//==============================구매목록===================================
	
	
	private int BUY_NOTB_NUM;
	private String BUYCU_ID;
	private int BUY_NOTB_ID;
	private String BUY_NOTB_NAME;
	private int BUY_NOTB_CNT;
	private int BUY_NOTB_PRICE;
	private String BUY_NOTB_BRAND;
	private String BUY_NOTB_IMG;
	private int BUY_NOTB_STATE;
	
	//==============================환불목록====================================
	
	private int REFUND_NOTB_NUM;
	private String REFUNDCU_NOTB_ID;
	private int REFUND_NOTB_ID;
	private String REFUND_NOTB_NAME;
	private int REFUND_NOTB_CNT;
	private int REFUND_NOTB_PRICE;
	private String REFUND_NOTB_BRAND;
	private String REFUND_NOTB_IMG;
	private int REFUND_NOTB_STATE;
	private Timestamp REFUND_NOTB_DATE;
	
	//==============================구매목록===================================
	
	
	public int getBUY_NOTB_STATE() {
		return BUY_NOTB_STATE;
	}
	public void setBUY_NOTB_STATE(int bUY_NOTB_STATE) {
		BUY_NOTB_STATE = bUY_NOTB_STATE;
	}
	public int getBUY_NOTB_ID() {
		return BUY_NOTB_ID;
	}
	public int getBUY_NOTB_NUM() {
		return BUY_NOTB_NUM;
	}
	public void setBUY_NOTB_NUM(int bUY_NOTB_NUM) {
		BUY_NOTB_NUM = bUY_NOTB_NUM;
	}
	public void setBUY_NOTB_ID(int bUY_NOTB_ID) {
		BUY_NOTB_ID = bUY_NOTB_ID;
	}
	public String getBUYCU_ID() {
		return BUYCU_ID;
	}
	public void setBUYCU_ID(String bUYCU_ID) {
		BUYCU_ID = bUYCU_ID;
	}
	public String getBUY_NOTB_NAME() {
		return BUY_NOTB_NAME;
	}
	public void setBUY_NOTB_NAME(String bUY_NOTB_NAME) {
		BUY_NOTB_NAME = bUY_NOTB_NAME;
	}
	public int getBUY_NOTB_CNT() {
		return BUY_NOTB_CNT;
	}
	public void setBUY_NOTB_CNT(int bUY_NOTB_CNT) {
		BUY_NOTB_CNT = bUY_NOTB_CNT;
	}
	public int getBUY_NOTB_PRICE() {
		return BUY_NOTB_PRICE;
	}
	public void setBUY_NOTB_PRICE(int bUY_NOTB_PRICE) {
		BUY_NOTB_PRICE = bUY_NOTB_PRICE;
	}
	public String getBUY_NOTB_BRAND() {
		return BUY_NOTB_BRAND;
	}
	public void setBUY_NOTB_BRAND(String bUY_NOTB_BRAND) {
		BUY_NOTB_BRAND = bUY_NOTB_BRAND;
	}
	public String getBUY_NOTB_IMG() {
		return BUY_NOTB_IMG;
	}
	public void setBUY_NOTB_IMG(String bUY_NOTB_IMG) {
		BUY_NOTB_IMG = bUY_NOTB_IMG;
	}
	
	
	//==============================장바구니====================================
	
	
	public int getCART_NOTB_ID() {
		return CART_NOTB_ID;
	}
	public void setCART_NOTB_ID(int cART_NOTB_ID) {
		CART_NOTB_ID = cART_NOTB_ID;
	}
	public String getCU_ID() {
		return CU_ID;
	}
	public void setCU_ID(String cU_ID) {
		CU_ID = cU_ID;
	}
	public String getCART_NOTB_NAME() {
		return CART_NOTB_NAME;
	}
	public void setCART_NOTB_NAME(String cART_NOTB_NAME) {
		CART_NOTB_NAME = cART_NOTB_NAME;
	}
	public int getCART_NOTB_CNT() {
		return CART_NOTB_CNT;
	}
	public void setCART_NOTB_CNT(int cART_NOTB_CNT) {
		CART_NOTB_CNT = cART_NOTB_CNT;
	}
	public int getCART_NOTB_PRICE() {
		return CART_NOTB_PRICE;
	}
	public void setCART_NOTB_PRICE(int cART_NOTB_PRICE) {
		CART_NOTB_PRICE = cART_NOTB_PRICE;
	}
	public String getCART_NOTB_BRAND() {
		return CART_NOTB_BRAND;
	}
	public void setCART_NOTB_BRAND(String cART_NOTB_BRAND) {
		CART_NOTB_BRAND = cART_NOTB_BRAND;
	}
	public String getCART_NOTB_IMG() {
		return CART_NOTB_IMG;
	}
	public void setCART_NOTB_IMG(String cART_NOTB_IMG) {
		CART_NOTB_IMG = cART_NOTB_IMG;
	}
	
	//=========================게시판===========================================
	
	public String getEnabled() {
		return enabled;
	}
	public void setEnabled(String enabled) {
		this.enabled = enabled;
	}
	public String getAuthority() {
		return authority;
	}
	public void setAuthority(String authority) {
		this.authority = authority;
	}
	public int getRef_level() {
		return ref_level;
	}
	public void setRef_level(int ref_level) {
		this.ref_level = ref_level;
	}
	public int getNum() {
		return num;
	}
	public void setNum(int num) {
		this.num = num;
	}
	public String getWriter() {
		return writer;
	}
	public void setWriter(String writer) {
		this.writer = writer;
	}
	public String getBoardpwd() {
		return boardpwd;
	}
	public void setBoardpwd(String boardpwd) {
		this.boardpwd = boardpwd;
	}
	public String getSubject() {
		return subject;
	}
	public void setSubject(String subject) {
		this.subject = subject;
	}
	public String getContent() {
		return content;
	}
	public void setContent(String content) {
		this.content = content;
	}
	public int getReadCnt() {
		return readCnt;
	}
	public void setReadCnt(int readCnt) {
		this.readCnt = readCnt;
	}
	public int getRef() {
		return ref;
	}
	public void setRef(int ref) {
		this.ref = ref;
	}
	public int getRef_step() {
		return ref_step;
	}
	public void setRef_step(int ref_step) {
		this.ref_step = ref_step;
	}
	public Timestamp getBoard_reg_date() {
		return board_reg_date;
	}
	public void setBoard_reg_date(Timestamp board_reg_date) {
		this.board_reg_date = board_reg_date;
	}
	
	
	//============================회원관리=====================================
	
	
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public String getPwd() {
		return pwd;
	}
	public void setPwd(String pwd) {
		this.pwd = pwd;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getHp() {
		return hp;
	}
	public void setHp(String hp) {
		this.hp = hp;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public String getAddress() {
		return address;
	}
	public void setAddress(String adress) {
		this.address = adress;
	}
	public Timestamp getReg_date() {
		return reg_date;
	}
	public void setReg_date(Timestamp reg_date) {
		this.reg_date = reg_date;
	}
	
	//============================환불테이블=====================================
	public Timestamp getREFUND_NOTB_DATE() {
		return REFUND_NOTB_DATE;
	}
	public void setREFUND_NOTB_DATE(Timestamp rEFUND_NOTB_DATE) {
		REFUND_NOTB_DATE = rEFUND_NOTB_DATE;
	}
	public String getREFUNDCU_NOTB_ID() {
		return REFUNDCU_NOTB_ID;
	}
	public void setREFUNDCU_NOTB_ID(String rEFUNDCU_NOTB_ID) {
		REFUNDCU_NOTB_ID = rEFUNDCU_NOTB_ID;
	}
	public int getREFUND_NOTB_ID() {
		return REFUND_NOTB_ID;
	}
	public void setREFUND_NOTB_ID(int rEFUND_NOTB_ID) {
		REFUND_NOTB_ID = rEFUND_NOTB_ID;
	}
	public String getREFUND_NOTB_NAME() {
		return REFUND_NOTB_NAME;
	}
	public void setREFUND_NOTB_NAME(String rEFUND_NOTB_NAME) {
		REFUND_NOTB_NAME = rEFUND_NOTB_NAME;
	}
	public int getREFUND_NOTB_CNT() {
		return REFUND_NOTB_CNT;
	}
	public void setREFUND_NOTB_CNT(int rEFUND_NOTB_CNT) {
		REFUND_NOTB_CNT = rEFUND_NOTB_CNT;
	}
	public int getREFUND_NOTB_PRICE() {
		return REFUND_NOTB_PRICE;
	}
	public void setREFUND_NOTB_PRICE(int rEFUND_NOTB_PRICE) {
		REFUND_NOTB_PRICE = rEFUND_NOTB_PRICE;
	}
	public String getREFUND_NOTB_BRAND() {
		return REFUND_NOTB_BRAND;
	}
	public void setREFUND_NOTB_BRAND(String rEFUND_NOTB_BRAND) {
		REFUND_NOTB_BRAND = rEFUND_NOTB_BRAND;
	}
	public String getREFUND_NOTB_IMG() {
		return REFUND_NOTB_IMG;
	}
	public void setREFUND_NOTB_IMG(String rEFUND_NOTB_IMG) {
		REFUND_NOTB_IMG = rEFUND_NOTB_IMG;
	}
	public int getREFUND_NOTB_STATE() {
		return REFUND_NOTB_STATE;
	}
	public void setREFUND_NOTB_STATE(int rEFUND_NOTB_STATE) {
		REFUND_NOTB_STATE = rEFUND_NOTB_STATE;
	}
	public int getREFUND_NOTB_NUM() {
		return REFUND_NOTB_NUM;
	}
	public void setREFUND_NOTB_NUM(int rEFUND_NOTB_NUM) {
		REFUND_NOTB_NUM = rEFUND_NOTB_NUM;
	}
}
