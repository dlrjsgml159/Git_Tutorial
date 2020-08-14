package com.spring.project3.service;

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;

import com.spring.project3.vo.UserVO;


//로그인이 성공한 경우 실행
public class UserLoginSuccessHandler implements AuthenticationSuccessHandler{

	@Override
	public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response,
			Authentication authentication) throws IOException, ServletException {
		
		UserVO vo = (UserVO)authentication.getPrincipal();
		System.out.println("UserVO == > " + vo);
		
//		String msg = authentication.getName() + "님 환영합니다."; 
//		request.setAttribute("msg", msg);
		request.getSession().setAttribute("memId", vo.getUserid());
		
		if(vo.getUserid().equals("manager")) {
			RequestDispatcher dispatcher = request.getRequestDispatcher("manager/inventory_management");
			dispatcher.forward(request, response);
		}else {
			RequestDispatcher dispatcher = request.getRequestDispatcher("main");
			dispatcher.forward(request, response);
		}
	}
}