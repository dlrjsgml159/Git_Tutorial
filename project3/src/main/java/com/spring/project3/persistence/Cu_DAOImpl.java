package com.spring.project3.persistence;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMessage.RecipientType;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Repository;

import com.spring.project3.vo.Cu_VO;

@Repository
public class Cu_DAOImpl implements Cu_DAO{
	
	@Autowired
	private JavaMailSender mailSender; // xml에 등록한 bean autowired
	
	@Autowired
	SqlSession sqlSession;
	
	//회원가입
	@Override
	public int insertMember(Cu_VO vo) {
		return sqlSession.insert("com.spring.project3.persistence.Cu_DAO.insertMember", vo);
	}

	//중복확인
	@Override
	public int idCheck(String id) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.idCheck", id); 
	}
	//아이디 비밀번호 체크 
	@Override
	public String idpwdCheck(String id) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.idpwdCheck", id); 
	}

	//로그인
	public Map<String, Object> selectUser(String userid){
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.selectUser",userid);
	}

	//회원탈퇴
	@Override
	public int deleteMember(String id) {
		return sqlSession.delete("com.spring.project3.persistence.Cu_DAO.deleteMember",id);
	}
	//회원정보
	@Override
	public Cu_VO getMemberInfo(String id) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.getMemberInfo",id); 
	}
	//회원정보수정
	@Override
	public int updateMember(Cu_VO vo) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.getMemberInfo",vo);
	}

	//개시판 조회수 
	@Override
	public int getArticleCnt() {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.getArticleCnt");
	}

	//게시판 목록 출력
	@Override
	public List<Cu_VO> getArticleList(Map<String,Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Cu_DAO.getArticleList",map);
	}
	
	//게시판 조회수
	@Override
	public void addReadCnt(int num) {
		sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.addReadCnt",num);
	}
	
	//상세페이지 조회 , 수정 상세페이지
	@Override
	public Cu_VO getArticle(int num) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.getArticle",num);
	}
	
	//패스워드체크
	@Override
	public int numPwdCheck(int num, String pwd) {
		return 0;
	}
	
	//글수정
	@Override
	public int updateBoard(int num, Cu_VO vo) {
		
		return 0;
	}
	
	//게시판 글쓰기
	@Override
	public int insertBoard(Cu_VO vo) {
		Map<String,Object> map = new HashMap<>();
		int num = vo.getNum();
		int ref = vo.getRef();
		int ref_step = vo.getRef_step();
		int ref_level = vo.getRef_level();
		ref = 1;
		ref_step = 0;
		ref_level = 0;
		return sqlSession.insert("com.spring.project3.persistence.Cu_DAO.insertBoard",vo);
	}
	//게시판 삭제 처리
	@Override
	public int deletePro(int num) {
//		int deleteCnt = 0;
//			"SELECT * FROM cu_board_tbl WHERE num=?"
//			if(rs.next()) {
//				int ref = rs.getInt("ref");
//				int ref_step = rs.getInt("ref_step");
//				int ref_level = rs.getInt("ref_level");
//				"SELECT * FROM cu_board_tbl WHERE ref=? AND ref_step=?+1 AND ref_level > ?";
//				if(rs.next()) {
//					"DELETE cu_board_tbl WHERE num=? OR (ref=? AND ref_level > ?)";
//				}else {
//					"DELETE cu_board_tbl WHERE num=?";
//				}
//			}
		return 0;
	}
	
	//장바구니 추가 처리
	public int cartlistAddPro2(Cu_VO vo) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.cartlistAddPro2",vo);
	}
	public int cartlistAddPro3(Cu_VO vo) {
		return sqlSession.insert("com.spring.project3.persistence.Cu_DAO.cartlistAddPro3",vo);
	}
	@Override
	public int cartlistAddPro(Cu_VO vo) {
		int insertCnt = 0;
		int cnt = cartlistAddPro2(vo);
		System.out.println("cnt "+cnt);
		if(cnt == 0) {
			insertCnt = cartlistAddPro3(vo);
		}else {
			insertCnt = sqlSession.update("com.spring.project3.persistence.Cu_DAO.cartlistAddPro",vo);
		}
		return insertCnt;
	}
	
	//장바구니 리스트
	@Override
	public List<Cu_VO> cartlistPro(Map<String,Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Cu_DAO.cartlistPro",map);
	}
	//장바구니 갯수
	@Override
	public int cartlistCnt(String memId) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.cartlistCnt",memId);
	}
	//장바구니 삭제 처리
	@Override
	public int cartlistDeletePro(String memId, int arr) {
		return 0;
	}
	//장바구니 구매처리
	@Override
	public int cartbuyPro(String memId, int arr) {
		return 0;
	}
	//구매목록 리스트
	@Override
	public List<Cu_VO> buylistPro(Map<String, Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Cu_DAO.buylistPro",map);
	}
	//구매목록 갯수
	@Override
	public int buylistCnt(String memId) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.buylistCnt",memId);
	}
	//구매처리
	public int buyPro1(Cu_VO vo) {
		int insertCnt = sqlSession.insert("com.spring.project3.persistence.Cu_DAO.buyPro1",vo);
		return insertCnt;
	}
	public int buyPro2(Cu_VO vo) {
		return sqlSession.update("com.spring.project3.persistence.Cu_DAO.buyPro2",vo);
	}
	@Override
	public int buyPro(Cu_VO vo) {
		int insertCnt = buyPro1(vo);
		buyPro2(vo);
		sqlSession.update("com.spring.project3.persistence.Cu_DAO.buyPro",vo);
		return insertCnt; 
	}
	
	public Cu_VO refundPro1(Map<String,Object> map) {
		Cu_VO vo = sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.refundPro1",map); 
		vo.setBUYCU_ID((String)map.get("memId"));
		vo.setBUY_NOTB_ID((int)map.get("notbid"));
		vo.setBUY_NOTB_NUM((int)map.get("notbnum"));
		return vo;
	}
	
	public int refundPro2(Cu_VO vo) {
		return	sqlSession.insert("com.spring.project3.persistence.Cu_DAO.refundPro2",vo);
	}
	public int refundPro3(Cu_VO vo) {
		return sqlSession.insert("com.spring.project3.persistence.Cu_DAO.refundPro3",vo);
	}
	public int refundPro4(Cu_VO vo) {
		return sqlSession.delete("com.spring.project3.persistence.Cu_DAO.refundPro4",vo);
	}
	//환불 처리
	@Override
	public int refundPro(Map<String,Object> map) {
		int insertCnt = 0;
			Cu_VO vo = refundPro1(map);
			if(vo != null) {
				insertCnt = refundPro2(vo);
				refundPro3(vo);
				refundPro4(vo);
			}
		return insertCnt;
	}
	//환불목록
	@Override
	public List<Cu_VO> refundlist(Map<String,Object> map) {
		return sqlSession.selectList("com.spring.project3.persistence.Cu_DAO.refundlist",map);
	}
	//환불 목록 갯수
	@Override
	public int refundlistCnt(String memId) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.refundlistCnt",memId);
	}
	//아이디 이메일 체크
	@Override
	public int Idmailchk(Map<String,Object> map) {
		return sqlSession.selectOne("com.spring.project3.persistence.Cu_DAO.Idmailchk",map);
	}
	
	//이메일 체크
	@Override
    public void sendmail(String email, String key) {
        try{
            MimeMessage message = mailSender.createMimeMessage();
            String txt = "ADLON노트북 입니다. 링크를 눌러 완료하세요." + key;
            
            message.setSubject("회원가입 인증 메일입니다.");
            message.setText(txt, "UTF-8", "html");
            message.setFrom(new InternetAddress("gunhee260@gmail.com"));
            message.addRecipient(RecipientType.TO, new InternetAddress(email));

            mailSender.send(message);

        }catch(Exception e){
            e.printStackTrace();
        }   
    }

	//비밀번호 수정 처리
	@Override
	public int pwdmodifyPro(Map<String,Object> map) {
		return sqlSession.update("com.spring.project3.persistence.Cu_DAO.pwdmodifyPro",map);
	}
}
