package com.spring.project3.vo;

public class Ma_VO {
	
	//재고 추가
	private int notb_id; 
	private String notb_name;
	private int notb_cnt;
	private int notb_price;
	private String notb_brand;
	private String notb_img;
	private String notb_img_information;
	//=============================결산=============================
	
	private String settlement_NOTB_NAME;
	private String settlement_NOTB_BRAND;
	private int settlement_NOTB_PRICE;
	private int settlement_NOTB_CNT;
	
	//=============================결산=============================
	
	public String getSettlement_NOTB_NAME() {
		return settlement_NOTB_NAME;
	}
	public void setSettlement_NOTB_NAME(String settlement_NOTB_NAME) {
		this.settlement_NOTB_NAME = settlement_NOTB_NAME;
	}
	public String getSettlement_NOTB_BRAND() {
		return settlement_NOTB_BRAND;
	}
	public void setSettlement_NOTB_BRAND(String settlement_NOTB_BRAND) {
		this.settlement_NOTB_BRAND = settlement_NOTB_BRAND;
	}
	public int getSettlement_NOTB_PRICE() {
		return settlement_NOTB_PRICE;
	}
	public void setSettlement_NOTB_PRICE(int settlement_NOTB_PRICE) {
		this.settlement_NOTB_PRICE = settlement_NOTB_PRICE;
	}
	public int getSettlement_NOTB_CNT() {
		return settlement_NOTB_CNT;
	}
	public void setSettlement_NOTB_CNT(int settlement_NOTB_CNT) {
		this.settlement_NOTB_CNT = settlement_NOTB_CNT;
	}
 	
	public String getNotb_img_information() {
		return notb_img_information;
	}
	public void setNotb_img_information(String notb_img_information) {
		this.notb_img_information = notb_img_information;
	}
	public int getNotb_cnt() {
		return notb_cnt;
	}
	public void setNotb_cnt(int notb_cnt) {
		this.notb_cnt = notb_cnt;
	}
	public int getNotb_id() {
		return notb_id;
	}
	public void setNotb_id(int notb_id) {
		this.notb_id = notb_id;
	}
	public String getNotb_name() {
		return notb_name;
	}
	public void setNotb_name(String notb_name) {
		this.notb_name = notb_name;
	}
	public int getNotb_price() {
		return notb_price;
	}
	public void setNotb_price(int notb_price) {
		this.notb_price = notb_price;
	}
	public String getNotb_brand() {
		return notb_brand;
	}
	public void setNotb_brand(String notb_brand) {
		this.notb_brand = notb_brand;
	}
	public String getNotb_img() {
		return notb_img;
	}
	public void setNotb_img(String notb_img) {
		this.notb_img = notb_img;
	}
}
