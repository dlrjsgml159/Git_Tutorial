package com.spring.project3.persistence;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.springframework.ui.Model;

import com.spring.project3.vo.Cu_VO;



public interface Cu_DAO {
	
	//중복확인 체크
	public int idCheck(String id);
	
	//회원가입 처리 페이지
	public int insertMember(Cu_VO vo);
	
	//아이디 체크
	public String idpwdCheck(String id);
	//회원탈퇴처리
	public int deleteMember(String id);
	
	//회원정보 가져오기
	public Cu_VO getMemberInfo(String id);
	
	//회원정보 수정 처리
	public int updateMember(Cu_VO vo);
	
	//-------------------------게시판------------------------------
	
	//게시글 갯수 구하기
	public int getArticleCnt();
	
	//게시글 목록 조회
	public List<Cu_VO> getArticleList(Map<String,Object> map);
	
	//조회수 증가
	public void addReadCnt(int num);
	
	//상세페이지 조회 , 수정 상세페이지
	public Cu_VO getArticle(int num);
	
	//게시글 수정 - 비밀번호 인증
	public int numPwdCheck(int num, String pwd);
	
	//게시글 수정 처리
	public int updateBoard(int num, Cu_VO vo);
	
	//글쓰기 처리페이지
	public int insertBoard(Cu_VO vo);
	
	//게시글 삭제 처리 
	public int deletePro(int num);
	
	//---------------------------장바구니--------------------------
	
	//장바구니 추가 처리
	public int cartlistAddPro(Cu_VO vo);
	
	//장바구니 목록 조회
	public List<Cu_VO> cartlistPro(Map<String,Object> map);
	
	//장바구니 갯수
	public int cartlistCnt(String memId);
	
	//장바구니 삭제처리
	public int cartlistDeletePro(String memId,int arr);
	
	//장바구니 구매처리
	public int cartbuyPro(String memId,int arr);
	
	//---------------------------구매목록--------------------------
	
	//구매목록
	public List<Cu_VO> buylistPro(Map<String,Object> map);
	
	//구매목록 갯수
	public int buylistCnt(String memId);
	
	//즉시구매처리
	public int buyPro(Cu_VO vo);
	
	//---------------------------환불목록--------------------------
	
	//환불신청
	public int refundPro(Map<String,Object> map);
	
	//환불 목록
	public List<Cu_VO> refundlist(Map<String,Object> map);
	
	//환불목록 갯수
	public int refundlistCnt(String memId);
	
	//이메일 유무 체크
	public int Idmailchk(Map<String,Object> map);
	
	//이메일 발송
	public void sendmail(String email, String key);
	
	//비밀번호 수정 처리
	public int pwdmodifyPro(Map<String,Object> map);
}
