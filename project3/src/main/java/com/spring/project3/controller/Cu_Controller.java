package com.spring.project3.controller;


import javax.servlet.http.HttpSession;

import org.apache.catalina.servlet4preview.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import com.spring.project3.service.Cu_ServiceImpl;
import com.spring.project3.service.Ma_ServiceImpl;

@Controller
public class Cu_Controller {
	
	private static final Logger logger = LoggerFactory.getLogger(Cu_Controller.class);
	
	@Autowired
	Cu_ServiceImpl service;
	
	@Autowired
	Ma_ServiceImpl service2;
	
	//로그인 페이지
	@RequestMapping("login")
	public String login() {
		logger.info("url ==> login");
		
		return "guest/login";
	}
	//로그아웃
	@RequestMapping("logout")
	public String logout(HttpServletRequest req,Model model, HttpSession session) {
		logger.info("url ==> logout");
//		System.out.println(req.getParameter("memId"));
//		System.out.println(req.getSession());
		System.out.println(req.getSession());
		System.out.println(req.getParameter("memId"));
		session.invalidate();
		SecurityContextHolder.clearContext();
		model.addAttribute("selectCnt",3);
		
		return "guest/main";
	}
	//메인페이지
	@RequestMapping("main")
	public String main1() {
		logger.info("url ==> main");
		
		return "guest/main";
	}
	//메인페이지
	@RequestMapping("customer/main")
	public String main2() {
		logger.info("url ==> main");
		
		return "guest/main";
	}
	//드라이버설치
	@RequestMapping("driver")
	public String driver() {
		logger.info("url ==> driver");
		
		return "guest/driver";
	}
	
	//윈도우10설치
	@RequestMapping("window10")
	public String window10() {
		logger.info("url ==> window10");
		
		return "guest/window10";
	}
	
	//회사소개
	@RequestMapping("aboutas")
	public String aboutas() {
		logger.info("url ==> aboutas");
		
		return "guest/aboutas";
	}
	
	//회원가입페이지
	@RequestMapping("signUp")
	public String signUp() {
		logger.info("url ==> signUp");
		
		return "guest/signUp";
	}
	
	//회원가입처리
	@RequestMapping("signUppro")
	public String signUppro(HttpServletRequest req,Model model) {
		logger.info("url ==> signUppro");
		service.signInPro(req, model);
		
		return "guest/signUppro";
	}
	//중복체크
	@RequestMapping("confirmId")
	public String confirmId(HttpServletRequest req,Model model) {
		logger.info("url ==> confirmId");
		service.confirmId(req, model);
		
		return "guest/confirmId";
	}
	//회원정보수정
	@RequestMapping("customer/mypagepro")
	public String mypagepro(HttpServletRequest req,Model model) {
		logger.info("url ==> mypagepro");
		service.modifypro(req, model);
		
		return "guest/mypagepro";
	}
	//주문
	@RequestMapping("customer/order")
	public String order1(HttpServletRequest req,Model model) {
		logger.info("url ==> order");
		service.inventoryList(req, model);
		
		return "guest/order";
	}
	//주문
	@RequestMapping("order")
	public String order2(HttpServletRequest req,Model model) {
		logger.info("url ==> order");
		service.inventoryList(req, model);
		
		return "guest/order";
	}
	//게시판
	@RequestMapping("customer/board")
	public String board(HttpServletRequest req,Model model) {
		logger.info("url ==> board");
		service.boardList(req, model);
		
		return "customer/board";
	}
	
	//게시판 글쓰기 폼
	@RequestMapping("customer/boardWriteForm")
	public String boardWriteForm(HttpServletRequest req,Model model) {
		logger.info("url ==> boardWriteForm");
		service.writeForm(req, model);
		
		return "customer/boardWriteForm";
	}
	//게시판 글쓰기 처리
	@RequestMapping("customer/boardWritePro")
	public String boardWritePro(HttpServletRequest req,Model model) {
		logger.info("url ==> boardWritePro");
		service.writePro(req, model);
		
		return "customer/boardWritePro";
	}
	//문의
	@RequestMapping("customer/consulting")
	public String consulting(HttpServletRequest req,Model model) {
		logger.info("url ==> consulting");
		
		return "customer/consulting";
	}
	//마이페이지
	@RequestMapping("customer/mypage")
	public String mypage(HttpServletRequest req,Model model) {
		logger.info("url ==> mypage");
		service.modifyView(req, model);
		
		return "customer/mypage";
	}
	//회원탈퇴페이지
	@RequestMapping("customer/mypage-leave")
	public String mypageleave(HttpServletRequest req,Model model) {
		logger.info("url ==> mypage-leave");
		
		return "customer/mypage-leave";
	}
	//회원탈퇴처리
	@RequestMapping("customer/mypage-leave-pro")
	public String mypageleavepro(HttpServletRequest req,Model model) {
		logger.info("url ==> mypage-leave-pro");
		service.deletePro(req, model);
		
		return "customer/mypage-leave-pro";
	}
	
	//주문목록
	@RequestMapping("customer/mypage-orderlist")
	public String mypageorderlist(HttpServletRequest req,Model model) {
		logger.info("url ==> mypage-orderlist");
		service.buylist(req, model);
		
		return "customer/mypage-orderlist";
	}
	//환불목록
	@RequestMapping("customer/refund")
	public String refund(HttpServletRequest req,Model model) {
		logger.info("url ==> refund");
		service.refundlist(req, model);
		
		return "customer/refund";
	}
	//상품설명 페이지
	@RequestMapping("productinformation")
	public String productinformation(HttpServletRequest req,Model model) {
		logger.info("url ==> productinformation");
		service2.inventoryDetail(req,model);
		
		return "guest/productinformation";
	}	
	//장바구니목록
	@RequestMapping("customer/cartlist")
	public String cartlist(HttpServletRequest req,Model model) {
		logger.info("url ==> cartlist");
		service.cartlist(req, model);
		
		return "customer/cartlist";
	}	
	//장바구니 추가
	@RequestMapping("customer/cartlist_pro")
	public String cartlist_pro(HttpServletRequest req,Model model) {
		logger.info("url ==> cartlist_pro");
		service.cartlistAdd(req, model);
		
		return "customer/cartlist_pro";
	}	
	
	//즉시구매처리
	@RequestMapping("customer/buy_pro")
	public String buy_pro(HttpServletRequest req,Model model) {
		logger.info("url ==> buy_pro");
		service.buy(req, model);
		
		return "customer/buy_pro";
	}	
	//환불
	@RequestMapping("customer/refund_Pro")
	public String refund_pro(HttpServletRequest req,Model model) {
		logger.info("url ==> refund_Pro");
		service.refund(req, model);
		
		return "customer/refund_Pro";
	}	
	
	//이메일 인증창 
	@RequestMapping("chkemail")
	public String chkemail(HttpServletRequest req,Model model) {
		logger.info("url ==> refund_Pro");
		
		return "guest/chkemail";
	}	
	
	// 아이디찾기 이메일 코드 보내기
    @RequestMapping(value="pwdchkemail", method=RequestMethod.GET)
    public String pwdchkemail(HttpServletRequest req, Model model) {
    	service.emailChk(req, model);
        
        return "guest/email";
    }
    
    //비밀번호 변경폼
  	@RequestMapping("pwdChk")
  	public String pwdChk(HttpServletRequest req,Model model) {
  		logger.info("url ==> pwdChk");
  		service.pwdemail(req,model);
  		
  		return "guest/pwdChk";
  	}
  	//비밀번호 변경처리
  	@RequestMapping("pwdchange")
  	public String pwdchange(HttpServletRequest req,Model model) {
  		logger.info("url ==> pwdchange");
  		service.pwdmodify(req, model);
  		
  		return "guest/login";
  	}
    
	//=========================메니저===========================
	
	//재고 리스트
	@RequestMapping("manager/inventory_management")
	public String inventory_management(HttpServletRequest req,Model model) {
		logger.info("url ==> manager/inventory_management");
		service2.inventoryList(req, model);
		
		return "manager/inventory_management";
	}
	
	//재고추가페이지
	@RequestMapping("manager/inventory_add")
	public String inventory_add(HttpServletRequest req,Model model) {
		logger.info("url ==> inventory_add");
		
		return "manager/inventory_add";
	}
	
	//재고추가처리
	@RequestMapping(value="manager/inventory_add_pro", method=RequestMethod.POST)
	public String inventory_add_pro(MultipartHttpServletRequest req,Model model) {
		logger.info("url ==> inventory_add_pro");
		service2.inventoryadd(req, model);
		
		return "manager/inventory_add_pro";
	}
	
	//재고 리스트
	@RequestMapping("manager/orderconfirmation")
	public String orderconfirmation(HttpServletRequest req,Model model) {
		logger.info("url ==> orderconfirmation");
		service2.mabuylist(req, model);
		
		return "manager/orderconfirmation";
	}
	//구매승인
	@RequestMapping("manager/orderconfirmation_pro")
	public String orderconfirmation_pro(HttpServletRequest req,Model model) {
		logger.info("url ==> orderconfirmation_pro");
		service2.purchaseapproval(req, model);
		
		return "manager/orderconfirmation_pro";
	}
	//환불 목록
	@RequestMapping("manager/refund_request")
	public String refund_request(HttpServletRequest req,Model model) {
		logger.info("url ==> refund_request");
		service2.marefundlist(req, model);
		
		return "manager/refund_request";
	}
	//환불승인
	@RequestMapping("manager/marefund_pro")
	public String marefund_pro(HttpServletRequest req,Model model) {
		logger.info("url ==> marefund_pro");
		service2.marefund(req, model);
		
		return "manager/marefund_pro";
	}
	
	//회원 목록출력
	@RequestMapping("manager/member_management")
	public String member_management(HttpServletRequest req,Model model) {
		logger.info("url ==> member_management");
		service2.macustomerlist(req, model);
		
		return "manager/member_management";
	}
	
	//결산
	@RequestMapping("manager/settlement")
	public String settlement(HttpServletRequest req,Model model) {
		logger.info("url ==> settlement");
		service2.settlement(req, model);
		
		return "manager/settlement";
	}
	
	//회원 목록출력
	@RequestMapping("manager/deleteMember")
	public String deleteMember(HttpServletRequest req,Model model) {
		logger.info("url ==> deleteMember");
		service2.deleteMember(req, model);
		
		return "manager/deleteMember";
	}
	
	//구매상태별 조회
	@RequestMapping("manager/buystate")
	public String buystate(HttpServletRequest req,Model model) {
		logger.info("url ==> buystate");
		service.buystate(req, model);
		
		return "manager/buystate";
	}
	
}
