package com.spring.project3.service;

import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.springframework.ui.Model;

public interface Cu_Service {
	
	//--------------------------회원관리-------------------------------------
	
		//중복확인처리
		public void confirmId(HttpServletRequest req,Model model);
			
		//회원가입처리
		public void signInPro(HttpServletRequest req,Model model);
		
		//회원정보 삭제처리
		public void deletePro(HttpServletRequest req,Model model); 
		
		//회원정보 상세보기
		public void modifyView(HttpServletRequest req,Model model);
		
		//회원정보 수정
		public void modifypro(HttpServletRequest req,Model model);
		
		//--------------------------게시판관리-------------------------------------
		
		//글목록
		public void boardList(HttpServletRequest req, Model model);
		
		//글상세 페이지
		public void contentForm(HttpServletRequest req, Model model);
		
		//글수정 상세페이지
		public void boardmodifyView(HttpServletRequest req, Model model);
		
//		//글수정 처리 페이지
//		public void modifyPro(HttpServletRequest req, Model model);
		
		//글쓰기 화면페이지
		public void writeForm(HttpServletRequest req, Model model);
		
		//글쓰기 처리페이지
		public void writePro(HttpServletRequest req, Model model);
		
//		//게시글 삭제 처리
//		public void boardDeletePro(HttpServletRequest req, Model model);
		
		//상품 목록 출력
		public void inventoryList(HttpServletRequest req, Model model);
		
		//--------------------------장바구니-------------------------------------
		
		//장바구니 추가
		public void cartlistAdd(HttpServletRequest req, Model model);
		
		//장바구니 목록
		public void cartlist(HttpServletRequest req, Model model);
		
		//장바구니 삭제
		public void cartlistDelete(HttpServletRequest req, Model model);
		
		//--------------------------구매-------------------------------------
		
//		//장바구니구매처리
//		public void cartbuy(HttpServletRequest req, Model model);
		
		//구매목록
		public void buylist(HttpServletRequest req, Model model);
		
		//구매처리
		public void buy(HttpServletRequest req, Model model);
		
		//--------------------------환불-------------------------------------
		
		//환불
		public void refund(HttpServletRequest req, Model model);
		
		//환불목록
		public void refundlist(HttpServletRequest req, Model model);
		
		public void buystate(HttpServletRequest req, Model model);
		
		//이메일체크
		public void emailChk(HttpServletRequest req, Model model);
		
		//비밀번호 수정처리
		public void pwdmodify(HttpServletRequest req, Model model);
		
		
}
