package com.spring.project3.service;

import javax.servlet.http.HttpServletRequest;

import org.springframework.ui.Model;
import org.springframework.web.multipart.MultipartHttpServletRequest;

public interface Ma_Service {
	//재고추가서비스
	public void inventoryadd(MultipartHttpServletRequest req, Model model);
	
//	//재고수정 서비스
//	public void inventorymodify(HttpServletRequest req, Model model);
//	
	//재고목록
	public void inventoryList(HttpServletRequest req, Model model);
	
	//재품상세
	public void inventoryDetail(HttpServletRequest req, Model model);
//	
//	//제품 삭제
//	public void inventoryDelete(HttpServletRequest req, Model model);
	
	//구매승인,취소 리스트
	public void mabuylist(HttpServletRequest req, Model model);
	
	//고객 리스트
	public void macustomerlist(HttpServletRequest req, Model model);
	
	//환불목록
	public void marefundlist(HttpServletRequest req, Model model);
	
	//구매승인 
	public void purchaseapproval(HttpServletRequest req, Model model);
	
	//환불 승인
	public void marefund(HttpServletRequest req, Model model);
	
	//회원 강제 탈퇴
	public void deleteMember(HttpServletRequest req, Model model);
	
	//결산
	public void settlement(HttpServletRequest req, Model model);
}
