package com.spring.project3.persistence;

import java.util.List;
import java.util.List;
import java.util.Map;

import com.spring.project3.vo.Cu_VO;
import com.spring.project3.vo.Ma_VO;

public interface Ma_DAO {
	//재고추가처리
	public int inadd(Ma_VO vo); 
	
	//재고수정처리
	public int modifypro(int num, Ma_VO vo);
	
	//게시글 갯수 구하기
	public int getArticleCnt();
		
	//게시글 목록 조회
	public List<Ma_VO> getArticleList(Map<String,Object> map);
	
	//상세페이지 조회 , 수정 상세페이지
	public Ma_VO getArticle(int num);
	
	//재고 삭제처리
	public int inventoryDeletePro(int num);
	
	//구매목록 갯수
	public int mabuylistCnt();
	
	//구매목록
	public List<Cu_VO> mabuylistPro(Map<String,Object> map);
	
	//회원목록
	public List<Cu_VO> macustomerPro(Map<String,Object> map);
	
	//회원인원수 조회
	public int macustomerCnt();
	
	//환불목록 갯수
	public int marefundlistCnt();
	
	//환불 목록
	public List<Cu_VO> marefundlist(Map<String,Object> map);
	
	//구매승인
	public int purchaseapproval(Map<String,Object> map);
	
	//환불 상태 변경
	public int marefundPro(Map<String,Object> map);
	
	//회원 강제 탈퇴
	public int deleteMember(String id);
	
	//결산
	public List<Ma_VO> settlementPro();
	
	//구매상태별 출력
	public  List<Cu_VO> buystate(int state);
}
