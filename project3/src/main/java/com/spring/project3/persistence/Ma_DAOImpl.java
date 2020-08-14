package com.spring.project3.persistence;

import java.util.List;
import java.util.Map;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.spring.project3.vo.Cu_VO;
import com.spring.project3.vo.Ma_VO;

@Repository
public class Ma_DAOImpl implements Ma_DAO{

	@Autowired
	SqlSession sqlSession; 
	
	//결산 목록에 추가 
	public int inadd2(Ma_VO vo) {
		return sqlSession.insert("com.spring.project3.persistence.Ma_DAO.inadd2",vo);
	}
	@Override
	public int inadd(Ma_VO vo) {
		System.out.println(vo);
		int cnt = 0;
		
		Ma_DAO dao = sqlSession.getMapper(Ma_DAO.class);
		cnt = dao.inadd(vo);
		
		inadd2(vo);
		
		return cnt;
	}
	
	@Override
	public int modifypro(int num, Ma_VO vo) {
		return 0;
	}
	
	//상품목록 갯수
	@Override
	public int getArticleCnt() {
		return sqlSession.selectOne("com.spring.project3.persistence.Ma_DAO.getArticleCnt");
	}
	
	//상품목록 출력
	@Override
	public List<Ma_VO> getArticleList(Map<String,Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Ma_DAO.getArticleList",map);
	}

	@Override
	public Ma_VO getArticle(int num) {
		return sqlSession.selectOne("com.spring.project3.persistence.Ma_DAO.getArticle",num);
	}

	@Override
	public int inventoryDeletePro(int num) {
		return 0;
	}
	
	//고객 구매목록 갯수
	@Override
	public int mabuylistCnt() {
		return sqlSession.selectOne("com.spring.project3.persistence.Ma_DAO.mabuylistCnt");
	}
	
	//고객 구매목록
	@Override
	public List<Cu_VO> mabuylistPro(Map<String,Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Ma_DAO.mabuylistPro",map);
	}
	
	//고객 리스트
	@Override
	public List<Cu_VO> macustomerPro(Map<String,Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Ma_DAO.macustomerPro",map);
	}
	
	//고객 수
	@Override
	public int macustomerCnt() {
		return sqlSession.selectOne("com.spring.project3.persistence.Ma_DAO.macustomerCnt");
	}
	
	//환불목록 갯수
	@Override
	public int marefundlistCnt() {
		return sqlSession.selectOne("com.spring.project3.persistence.Ma_DAO.marefundlistCnt");
	}

	//환불목록
	@Override
	public List<Cu_VO> marefundlist(Map<String,Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Ma_DAO.marefundlist",map);
	}
	
	//구매상태 승인 및 변경
	@Override
	public int purchaseapproval(Map<String,Object> map) {
		return sqlSession.update("com.spring.project3.persistence.Ma_DAO.purchaseapproval",map);
	}
	
	//환불상태 변경
	@Override
	public int marefundPro(Map<String,Object> map) {
		return sqlSession.update("com.spring.project3.persistence.Ma_DAO.marefundPro",map);
	}
	
	//회원 강제 탈퇴
	@Override
	public int deleteMember(String id) {
		return sqlSession.delete("com.spring.project3.persistence.Ma_DAO.deleteMember",id);
	}
	
	//결산
	@Override
	public List<Ma_VO> settlementPro() {
		return sqlSession.selectList("com.spring.project3.persistence.Ma_DAO.settlementPro");
	}
	
	//구매상태 별 조회
	@Override
	public List<Cu_VO> buystate(int state) {
		return sqlSession.selectList("com.spring.project3.persistence.Ma_DAO.buystate",state);
	}
}
