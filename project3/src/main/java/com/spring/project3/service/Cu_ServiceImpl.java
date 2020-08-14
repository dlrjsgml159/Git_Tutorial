package com.spring.project3.service;

import java.sql.Timestamp;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.ui.Model;

import com.spring.project3.persistence.Cu_DAO;
import com.spring.project3.persistence.Ma_DAOImpl;
import com.spring.project3.vo.Cu_VO;
import com.spring.project3.vo.Ma_VO;


@Service
public class Cu_ServiceImpl implements Cu_Service{

	@Autowired
	Cu_DAO dao;
	@Autowired
	Ma_DAOImpl dao2;
	@Autowired
	Cu_VO vo;
	@Autowired // 의존성 주입
	BCryptPasswordEncoder passwordEncoder; //비밀번호 암호화 객체 
	
	@Override
	public void signInPro(HttpServletRequest req, Model model) {
		
		String passwd = req.getParameter("pwd");
		//비밀번호 암호화 전
		System.out.println("암호화전의 비밀번호  : " + passwd);
		
		//비밀번호 암호화
		String enctyptPassword = passwordEncoder.encode(passwd);
		
		//비밀번호 암호화  후
		System.out.println("암호화후의 비밀번호  : " + enctyptPassword);
		
		//vo 바구니를 생성한다.
		vo.setId(req.getParameter("id"));
		vo.setPwd(enctyptPassword);
		vo.setName(req.getParameter("name"));
		
		//adress
		String address = "";
		String address1 = req.getParameter("address1");
		String address2 = req.getParameter("address2");
		String address3 = req.getParameter("address3");
		
		address = address1 + address2 + address3;
		vo.setAddress(address);
		
		//hp
		String hp = "";
		String hp1 = req.getParameter("hp1");
		String hp2 = req.getParameter("hp2");
		String hp3 = req.getParameter("hp3");
		
		hp = hp1 + "-" + hp2 + "-" + hp3;
		System.out.println("hp ="+hp);
		vo.setHp(hp);
		
		//email
		String email ="";
		String email1 = req.getParameter("email1");
		String email2 = req.getParameter("email2");
		
		if(!email1.equals("") && !email2.equals("")) {
		email = email1+"@"+email2;
		}
		vo.setEmail(email);
		//reg_date
		vo.setReg_date(new Timestamp(System.currentTimeMillis()));
		
		String id = req.getParameter("id");
		if(id.equals("manager")) {
			vo.setAuthority("ROLE_ADMIN");
		}else {
			vo.setAuthority("ROLE_USER");
		}
		//vo 바구니에 입력받은 값을 담는다.
		//4.단계 다형성 적용, 싱글톤 방식으로 dao 객체 생성
		
		//5단계.  회원가입 처리
		int cnt = dao.insertMember(vo);
		//6단계. request나 session으로 처리결과를 저장(jsp에 전달하기 위함)
		System.out.println("insertCnt = " + cnt);
		model.addAttribute("insertCnt", cnt);
	}
	
	//아이디 중복확인
	@Override
	public void confirmId(HttpServletRequest req, Model model) {
		// 3단계. 화면으로부터 입력받은 값을 받아온다.
		String strId = req.getParameter("id");
		
		//5단계. 중복된 id 가 있는지확인
		int cnt = dao.idCheck(strId);
		
		//model.addAttribute("key",값);
		model.addAttribute("selectCnt",cnt);
		model.addAttribute("id", strId);
	}

		//회원정보 삭제처리
		@Override
		public void deletePro(HttpServletRequest req, Model model) {
			int cnt = 0;
			String pwd1 = req.getParameter("pwd");
			int deleteCnt = 0;
			String id = (String)req.getSession().getAttribute("memId");
			String pwd2 = dao.idpwdCheck(id);
			//5-2단계. 일치하면 회원탈퇴
			if(passwordEncoder.matches(pwd1,pwd2)) {
				deleteCnt = dao.deleteMember(id);
				cnt = 2;
			}else {
				cnt = 1;
			}
			model.addAttribute("selectCnt",cnt);
			model.addAttribute("deleteCnt", deleteCnt);
		}
		//회원정보 상세보기
		@Override
		public void modifyView(HttpServletRequest req, Model model) {
			//3단계 화면으로 부터 입력받은 값을 가져온다.
			String id = (String)req.getSession().getAttribute("memId");
			
			//5-1단계. id, 패스워드가 일치하는지 확인
			System.out.println("id"+ id);
			//5-2단계. 일치하면 로그인한 id로 정보 조회
			Cu_VO vo = dao.getMemberInfo(id);
			//6단계. request나 session으로 처리결과를 저장(jsp에 전달하기위함)
			model.addAttribute("vo", vo);
		}
		//회원정보 수정
		@Override
		public void modifypro(HttpServletRequest req, Model model) {
			//3단계 화면으로 부터 입력받은 값을 받아와서 vo 바구니에 담는다.
			String id = (String)req.getSession().getAttribute("memId");
			Cu_VO vo = new Cu_VO();
			//비밀번호
			vo.setPwd(req.getParameter("pwd"));
				
			System.out.println(vo.getPwd());
			//주소
			if(req.getParameter("address1") == "" && req.getParameter("address2") == "" && req.getParameter("address3") == ""){
				vo.setAddress(req.getParameter("hiddenaddress"));
			}else {
				String address = "";
				String address1 = req.getParameter("address1");
				String address2 = req.getParameter("address2");
				String address3 = req.getParameter("address3");
				
				address = address1 + address2 + address3;
				vo.setAddress(address);
			}
			String hp = "";
			String hp1 = req.getParameter("hp1");
			String hp2 = req.getParameter("hp2");
			String hp3 = req.getParameter("hp3");
			
			hp = hp1 + "-" + hp2 + "-" + hp3;
			vo.setHp(hp);
			
			//email
			String email ="";
			String email1 = req.getParameter("email1");
			String email2 = req.getParameter("email2");
			
			if(!email1.equals("") && !email2.equals("")){
				email = email1+"@"+email2;
			}
			vo.setEmail(email);
			vo.setId(id);
			//5단계. 회원정보 수정 처리
			int cnt = dao.updateMember(vo);
			//6단계. request나 session으로 처리결과를 저장(jsp에 전달하기위함)
			model.addAttribute("updateCnt", cnt);
		}
		
		//================================ 게시판 관리 =======================================
		
		@Override
		public void boardList(HttpServletRequest req, Model model) {
			//3단계 .화면으로 부터 입력받은 값을 받아온다.
			
			//페이징
			int pageSize = 10; //한페이지당 출력할 글 갯수
			int pageBlock = 3; //한 블럭당 페이지 갯수
			
			int cnt = 0; //글갯수
			int start = 0; //현재 페이지 시작 글번호
			int end = 0; //현재 페이지 마지막 글번호
			int number = 0; //출력용 글번호
			String pageNum = ""; //페이지 번호
			int currentPage = 0; //현재페이지
			
			int pageCount = 0;  //페이지 갯수
			int startPage = 0; //시작 페이지
			int endPage = 0;  //마지막 페이지
			
			//5-1단계. 글갯수 구하기
			cnt = dao.getArticleCnt();  //30
			System.out.println("cnt => " + cnt);
			
			pageNum = req.getParameter("pageNum");
			if(pageNum == null) {
				pageNum = "1"; //첫페이지를 1페이지로 지정
			}
			System.out.println(pageNum);
			//글 30건 기준
			currentPage = Integer.parseInt(pageNum);
			System.out.println("currentPage : " + currentPage);
			
			//페이지 갯수 6 = (30 / 5) + (0)
			pageCount = (cnt / pageSize) + (cnt % pageSize > 0 ? 1 : 0); //페이지 갯수  + 나머지 있으면 1
			
			//현재페이지 시작 글번호(페이지별) 
			//1= (1 - 1) * 5 + 1
			start = (currentPage - 1) * pageSize + 1;
			
			//현제 페이지 마지막 글번호(페이지별)
			//5= 1 + 5 - 1;
			end = start + pageSize - 1;
			
			System.out.println("start : " + start);
			System.out.println("end : " + end);
			
			//출력용 글번호
			//30 = 30 - (1 - 1) * 5;
			number = cnt - (currentPage -1)* pageSize;
			
			System.out.println("start : " + start);
			System.out.println("end : " + pageSize);

			
			Map<String,Object> map = new HashMap<>();
			map.put("start", start);
			map.put("end", end);
			if(cnt > 0) {
				//5-2단계. 게시글 목록 조회
				List<Cu_VO> dtos = dao.getArticleList(map);
				model.addAttribute("dtos", dtos);
			}
			//1 = (1 / 3) * 3 + 1;
			startPage = (currentPage / pageBlock) * pageBlock + 1;
			if(currentPage % pageBlock == 0) startPage -= pageBlock;
			
			System.out.println("startPage : " + startPage);
			//마지막페이지
			endPage = startPage + pageBlock - 1;
			if(endPage > pageCount)endPage = pageCount;
			
			System.out.println("endPage : " + endPage);
			System.out.println("====================");
			
			model.addAttribute("cnt", cnt);        //글갯수
			model.addAttribute("number", number);  //출력용 글번호
			model.addAttribute("pageNum", pageNum); //페이지 번호
			
			if(cnt > 0) {
				model.addAttribute("startPage", startPage); //시작 페이지
				model.addAttribute("endPage", endPage);	//마지막 페이지
				model.addAttribute("pageBlock", pageBlock); //한블럭당 페이지 갯수
				model.addAttribute("pageCount", pageCount);	//페이지 갯수
				model.addAttribute("currentPage", currentPage);//현재페이지
			}
		}
		//글상세 페이지
		@Override
		public void contentForm(HttpServletRequest req, Model model) {
			int num = Integer.parseInt(req.getParameter("num"));
			int pageNum = Integer.parseInt(req.getParameter("pageNum"));
			int number = Integer.parseInt(req.getParameter("number"));
			
			//5-1단계. 조회수 증가
			dao.addReadCnt(num);
			//5-2단계 . 상세페이지 조회
			Cu_VO vo = dao.getArticle(num);
			System.out.println("vo = " + vo.getPwd());  //잘나오는지 확인
			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)
			model.addAttribute("dto", vo); //참조변수
			model.addAttribute("pageNum", pageNum);
			model.addAttribute("number", number);
		}
		//글수정 상세페이지
		@Override
		public void boardmodifyView(HttpServletRequest req, Model model) {
			//3단계. 화면으로부터 입력받은 값(get방식)을 받아온다.
			String pwd = req.getParameter("pwd");
			int num = Integer.parseInt(req.getParameter("num"));
			int pageNum = Integer.parseInt(req.getParameter("pageNum"));
			//5-1단계. 비밀번호 인증
			int selectCnt = dao.numPwdCheck(num, pwd);
			System.out.println("selectCnt = " + selectCnt);
			
			if(selectCnt == 1) {
				Cu_VO vo = dao.getArticle(num);
				model.addAttribute("dto", vo); // 참조변수
			}
			model.addAttribute("pageNum", pageNum);
			model.addAttribute("num", num);
			model.addAttribute("selectCnt", selectCnt);
		}
//		//글수정 처리 페이지
//		@Override
//		public void modifyPro(HttpServletRequest req, Model model) {
//			//3단계. 화면으로부터 입력받은 값(get방식)을 받아온다.
//			int num = Integer.parseInt(req.getParameter("num"));
//			int pageNum = Integer.parseInt(req.getParameter("pageNum"));
//			
//			//바구니 생성후 바구니에 담는다
//			Cu_VO vo = new Cu_VO();
//			vo.setSubject(req.getParameter("subject"));
//			vo.setContent(req.getParameter("content"));
//			
//			int updateCnt = dao.updateBoard(num, vo);
//			
//			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)
//			model.addAttribute("updateCnt", updateCnt);
//			model.addAttribute("num", num);
//			model.addAttribute("pageNum", pageNum);
//		}
		//글쓰기 화면페이지
		@Override
		public void writeForm(HttpServletRequest req, Model model) {
			//3단계. 화면으로부터 입력받은 값
			//신규 제목글(답변글이 아닌경우 )	
			int num = 0;
			int pageNum = 0;	
			int ref = 0;
			int ref_step = 0;
			int ref_level = 0;
			
			// 답변글 작성시	
			if(req.getParameter("num") != null) {
				num = Integer.parseInt(req.getParameter("num"));
				ref = Integer.parseInt(req.getParameter("ref"));
				ref_step = Integer.parseInt(req.getParameter("ref_step"));
				ref_level = Integer.parseInt(req.getParameter("ref_level"));
			}
			pageNum = Integer.parseInt(req.getParameter("pageNum"));
			
			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)	
			model.addAttribute("num", num);
			model.addAttribute("pageNum", pageNum);
			model.addAttribute("ref", ref);
			model.addAttribute("ref_step", ref_step);
			model.addAttribute("ref_level", ref_level);
		}
		
		//글쓰기 처리페이지
		@Override
		public void writePro(HttpServletRequest req, Model model) {
			
			//3-1단계.writeForm 화면으로부터 입력받은 값(hidden 값)
			int pageNum = Integer.parseInt(req.getParameter("pageNum"));
			vo.setNum(Integer.parseInt(req.getParameter("num")));
			vo.setRef(Integer.parseInt(req.getParameter("ref")));
			vo.setRef_step(Integer.parseInt(req.getParameter("ref_step")));
			vo.setRef_level(Integer.parseInt(req.getParameter("ref_level")));
			
			//3-2단계.writeForm 화면으로부터 입력받은 값(input 값)
			vo.setWriter((req.getParameter("writer")));
			vo.setBoardpwd(req.getParameter("pwd"));
			vo.setSubject(req.getParameter("subject"));
			vo.setContent(req.getParameter("content"));
			
			//3-3단계.
			//db에서 reg_date에 null로 insert시킬 경우, dedault에 sysdate로 설정되어 있으면 sysdate로 insert됨
			vo.setBoard_reg_date(new Timestamp(System.currentTimeMillis()));
			
			//5단계 글쓰기 처리
			int insertCnt = dao.insertBoard(vo);
			System.out.println("insertCnt = " +insertCnt );
			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)	
			model.addAttribute("insertCnt", insertCnt);
			model.addAttribute("pageNum", pageNum);
		}
//		//게시글삭제
//		@Override
//		public void boardDeletePro(HttpServletRequest req, Model model) {
//			//3단계. 화면으로부터 입력받은 값(get방식)을 받아온다.
//			int num = Integer.parseInt(req.getParameter("num"));
//			int pageNum = Integer.parseInt(req.getParameter("pageNum"));
//			String pwd = req.getParameter("pwd");
//			
//			
//			//비밀번호 체크
//			int selectCnt = dao.numPwdCheck(num, pwd);
//			System.out.println(selectCnt);
//			//게시글 삭제 처리
//			if(selectCnt != 0) {
//				int deleteCnt = dao.deletePro(num);
//				model.addAttribute("deleteCnt", deleteCnt);
//				System.out.println(deleteCnt);
//			}
//			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)	
//			model.addAttribute("selectCnt", selectCnt);
//			model.addAttribute("pageNum", pageNum);
//		}
//
//		//-------------------------상품 출력-------------------------------------
//		
		//상품목록출력
		@Override
		public void inventoryList(HttpServletRequest req, Model model) {
			
			//3단계 .화면으로 부터 입력받은 값을 받아온다.
			
			//페이징
			int pageSize = 12; //한페이지당 출력할 글 갯수
			int pageBlock = 5; //한 블럭당 페이지 갯수
			
			int cnt = 0; //글갯수
			int start = 0; //현재 페이지 시작 글번호
			int end = 0; //현재 페이지 마지막 글번호
			int number = 0; //출력용 글번호
			String pageNum = ""; //페이지 번호
			int currentPage = 0; //현재페이지
			
			int pageCount = 0;  //페이지 갯수
			int startPage = 0; //시작 페이지
			int endPage = 0;  //마지막 페이지
			
			
			
			//5-1단계. 글갯수 구하기
			cnt = dao2.getArticleCnt();  //30
			System.out.println("cnt => " + cnt);
			
			pageNum = req.getParameter("pageNum");
			if(pageNum == null) {
				pageNum = "1"; //첫페이지를 1페이지로 지정
			}
			System.out.println(pageNum);
			//글 30건 기준
			currentPage = Integer.parseInt(pageNum);
			System.out.println("currentPage : " + currentPage);
			
			//페이지 갯수 6 = (30 / 5) + (0)
			pageCount = (cnt / pageSize) + (cnt % pageSize > 0 ? 1 : 0); //페이지 갯수  + 나머지 있으면 1
			
			//현재페이지 시작 글번호(페이지별) 
			//1= (1 - 1) * 5 + 1
			start = (currentPage - 1) * pageSize + 1;
			
			//현제 페이지 마지막 글번호(페이지별)
			//5= 1 + 5 - 1;
			end = start + pageSize - 1;
			
			System.out.println("start : " + start);
			System.out.println("end : " + end);
			
			//출력용 글번호
			//30 = 30 - (1 - 1) * 5;
			number = cnt - (currentPage -1)* pageSize;
			
			System.out.println("start : " + start);
			System.out.println("end : " + pageSize);

			Map<String,Object> map = new HashMap<>();
			map.put("start", start);
			map.put("end", end);
			if(cnt > 0) {
				List<Ma_VO> dtos = dao2.getArticleList(map);
				model.addAttribute("dtos", dtos);
			}
			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)
			//시작페이지
			//1 = (1 / 3) * 3 + 1;
			startPage = (currentPage / pageBlock) * pageBlock + 1;
			if(currentPage % pageBlock == 0) startPage -= pageBlock;
			
			System.out.println("startPage : " + startPage);
			//마지막페이지
			endPage = startPage + pageBlock - 1;
			if(endPage > pageCount)endPage = pageCount;
			
			System.out.println("endPage : " + endPage);
			System.out.println("====================");
			
			model.addAttribute("cnt", cnt);        //글갯수
			model.addAttribute("number", number);  //출력용 글번호
			model.addAttribute("pageNum", pageNum); //페이지 번호
			
			if(cnt > 0) {
				model.addAttribute("startPage", startPage); //시작 페이지
				model.addAttribute("endPage", endPage);	//마지막 페이지
				model.addAttribute("pageBlock", pageBlock); //한블럭당 페이지 갯수
				model.addAttribute("pageCount", pageCount);	//페이지 갯수
				model.addAttribute("currentPage", currentPage);//현재페이지
			}
		}
		
		//=======================장바구니 =======================================
		
		//장바구니 추가
		@Override
		public void cartlistAdd(HttpServletRequest req, Model model) {
			
			Cu_VO vo = new Cu_VO();
			
			vo.setCART_NOTB_ID(Integer.parseInt(req.getParameter("CART_NOTB_ID")));
			vo.setCU_ID(req.getParameter("CU_ID"));
			vo.setCART_NOTB_NAME(req.getParameter("CART_NOTB_NAME"));
			vo.setCART_NOTB_CNT(Integer.parseInt(req.getParameter("CART_NOTB_CNT")));
			vo.setCART_NOTB_PRICE(Integer.parseInt(req.getParameter("CART_NOTB_PRICE")));
			vo.setCART_NOTB_BRAND(req.getParameter("CART_NOTB_BRAND"));
			vo.setCART_NOTB_IMG(req.getParameter("CART_NOTB_IMG"));
			
			int insertCnt = dao.cartlistAddPro(vo);
			
			//값전달
			model.addAttribute("insertCnt", insertCnt);
			System.out.println("insertCnt = " + insertCnt);
		}
		
		//장바구니 목록
		@Override
		public void cartlist(HttpServletRequest req, Model model) {
			//3단계 .화면으로 부터 입력받은 값을 받아온다.
			String memId = (String)req.getSession().getAttribute("memId");
			System.out.println("memId" + memId);
			//페이징
			int pageSize = 10; //한페이지당 출력할 글 갯수
			int pageBlock = 3; //한 블럭당 페이지 갯수
			
			int cnt = 0; //글갯수
			int start = 0; //현재 페이지 시작 글번호
			int end = 0; //현재 페이지 마지막 글번호
			int number = 0; //출력용 글번호
			String pageNum = ""; //페이지 번호
			int currentPage = 0; //현재페이지
			
			int pageCount = 0;  //페이지 갯수
			int startPage = 0; //시작 페이지
			int endPage = 0;  //마지막 페이지
			
			
			
			//5-1단계. 글갯수 구하기
			cnt = dao.cartlistCnt(memId);  //30
			System.out.println("cnt => " + cnt);
			
			pageNum = req.getParameter("pageNum");
			if(pageNum == null) {
				pageNum = "1"; //첫페이지를 1페이지로 지정
			}
			System.out.println(pageNum);
			//글 30건 기준
			currentPage = Integer.parseInt(pageNum);
			System.out.println("currentPage : " + currentPage);
			
			//페이지 갯수 6 = (30 / 5) + (0)
			pageCount = (cnt / pageSize) + (cnt % pageSize > 0 ? 1 : 0); //페이지 갯수  + 나머지 있으면 1
			
			//현재페이지 시작 글번호(페이지별) 
			//1= (1 - 1) * 5 + 1
			start = (currentPage - 1) * pageSize + 1;
			
			//현제 페이지 마지막 글번호(페이지별)
			//5= 1 + 5 - 1;
			end = start + pageSize - 1;
			
			System.out.println("start : " + start);
			System.out.println("end : " + end);
			
			//출력용 글번호
			//30 = 30 - (1 - 1) * 5;
			number = cnt - (currentPage -1)* pageSize;
			
			System.out.println("start : " + start);
			System.out.println("end : " + pageSize);

			Map<String,Object> map = new HashMap<>();
			map.put("start",start);
			map.put("end",end);
			map.put("memId",memId);
			
			if(cnt > 0) {
				//5-2단계. 게시글 목록 조회
				List<Cu_VO> dtos = dao.cartlistPro(map);
				model.addAttribute("dtos", dtos);
			}
			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)
			//시작페이지
			//1 = (1 / 3) * 3 + 1;
			startPage = (currentPage / pageBlock) * pageBlock + 1;
			if(currentPage % pageBlock == 0) startPage -= pageBlock;
			
			System.out.println("startPage : " + startPage);
			//마지막페이지
			endPage = startPage + pageBlock - 1;
			if(endPage > pageCount)endPage = pageCount;
			
			System.out.println("endPage : " + endPage);
			System.out.println("====================");
			
			model.addAttribute("cnt", cnt);        //글갯수
			model.addAttribute("number", number);  //출력용 글번호
			model.addAttribute("pageNum", pageNum); //페이지 번호
			
			if(cnt > 0) {
				model.addAttribute("startPage", startPage); //시작 페이지
				model.addAttribute("endPage", endPage);	//마지막 페이지
				model.addAttribute("pageBlock", pageBlock); //한블럭당 페이지 갯수
				model.addAttribute("pageCount", pageCount);	//페이지 갯수
				model.addAttribute("currentPage", currentPage);//현재페이지
			}
		}
		//장바구니 삭제
		@Override
		public void cartlistDelete(HttpServletRequest req, Model model) {
			String chkArray = req.getParameter("chkArray");
			System.out.println("chkArray" + chkArray);
			String memId = (String)req.getSession().getAttribute("memId");
			String[] chkArrayIn = chkArray.split(","); 
			
			 int deleteCnt = 0; 
			 for(int i = 0; i < chkArrayIn.length;i++){ 
				 int notbid = Integer.parseInt(chkArrayIn[i]); 
				 deleteCnt = dao.cartlistDeletePro(memId,notbid); 
			 } 
			 System.out.println("deleteCnt" + deleteCnt); 
			 model.addAttribute("deleteCnt", deleteCnt);
		}
		//즉시구매처리
		@Override
		public void buy(HttpServletRequest req, Model model) {
			Cu_VO vo = new Cu_VO();
			vo.setBUYCU_ID(req.getParameter("CU_ID"));
			vo.setBUY_NOTB_ID(Integer.parseInt(req.getParameter("CART_NOTB_ID")));
			vo.setBUY_NOTB_NAME(req.getParameter("CART_NOTB_NAME"));
			vo.setBUY_NOTB_CNT(Integer.parseInt(req.getParameter("CART_NOTB_CNT")));
			vo.setBUY_NOTB_PRICE(Integer.parseInt(req.getParameter("CART_NOTB_PRICE")));
			vo.setBUY_NOTB_BRAND(req.getParameter("CART_NOTB_BRAND"));
			vo.setBUY_NOTB_IMG(req.getParameter("CART_NOTB_IMG"));
			
			int insertCnt = 0;
			insertCnt = dao.buyPro(vo);
			//값전달
			model.addAttribute("insertCnt", insertCnt);
			System.out.println("insertCnt = " + insertCnt);
		}
//		//장바구니 구매처리
//		@Override
//		public void cartbuy(HttpServletRequest req, Model model) {
//			String chkArray = req.getParameter("chkArray");
//			System.out.println("chkArray" + chkArray);
//			String memId = (String)req.getSession().getAttribute("memId");
//			String[] chkArrayIn = chkArray.split(","); 
//			
//			int insertCnt = 0;
//			 for(int i = 0; i < chkArrayIn.length;i++){ 
//				 int notbid = Integer.parseInt(chkArrayIn[i]); 
//				 insertCnt = dao.cartbuyPro(memId,notbid);
//			 } 
//			//값전달
//			model.addAttribute("insertCnt", insertCnt);
//			System.out.println("insertCnt = " + insertCnt);
//		}
		//구매목록
		@Override
		public void buylist(HttpServletRequest req, Model model) {
			//3단계 .화면으로 부터 입력받은 값을 받아온다.
			String memId = (String)req.getSession().getAttribute("memId");
			System.out.println("memId" + memId);
			//페이징
			int pageSize = 10; //한페이지당 출력할 글 갯수
			int pageBlock = 3; //한 블럭당 페이지 갯수
			
			int cnt = 0; //글갯수
			int start = 0; //현재 페이지 시작 글번호
			int end = 0; //현재 페이지 마지막 글번호
			int number = 0; //출력용 글번호
			String pageNum = ""; //페이지 번호
			int currentPage = 0; //현재페이지
			
			int pageCount = 0;  //페이지 갯수
			int startPage = 0; //시작 페이지
			int endPage = 0;  //마지막 페이지
			
			//5-1단계. 글갯수 구하기
			cnt = dao.buylistCnt(memId);  //30
			System.out.println("cnt => " + cnt);
			
			pageNum = req.getParameter("pageNum");
			if(pageNum == null) {
				pageNum = "1"; //첫페이지를 1페이지로 지정
			}
			System.out.println(pageNum);
			//글 30건 기준
			currentPage = Integer.parseInt(pageNum);
			System.out.println("currentPage : " + currentPage);
			
			//페이지 갯수 6 = (30 / 5) + (0)
			pageCount = (cnt / pageSize) + (cnt % pageSize > 0 ? 1 : 0); //페이지 갯수  + 나머지 있으면 1
			
			//현재페이지 시작 글번호(페이지별) 
			//1= (1 - 1) * 5 + 1
			start = (currentPage - 1) * pageSize + 1;
			
			//현제 페이지 마지막 글번호(페이지별)
			//5= 1 + 5 - 1;
			end = start + pageSize - 1;
			
			System.out.println("start : " + start);
			System.out.println("end : " + end);
			
			//출력용 글번호
			//30 = 30 - (1 - 1) * 5;
			number = cnt - (currentPage -1)* pageSize;
			
			System.out.println("start : " + start);
			System.out.println("end : " + pageSize);

			Map<String,Object> map = new HashMap<>();
			map.put("start",start);
			map.put("end",end);
			map.put("memId",memId);
			
			if(cnt > 0) {
				//5-2단계. 게시글 목록 조회
				List<Cu_VO> dtos = dao.buylistPro(map);
				model.addAttribute("dtos2", dtos);
			}
			//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)
			//시작페이지
			//1 = (1 / 3) * 3 + 1;
			startPage = (currentPage / pageBlock) * pageBlock + 1;
			if(currentPage % pageBlock == 0) startPage -= pageBlock;
			
			System.out.println("startPage : " + startPage);
			//마지막페이지
			endPage = startPage + pageBlock - 1;
			if(endPage > pageCount)endPage = pageCount;
			
			System.out.println("endPage : " + endPage);
			System.out.println("====================");
			
			model.addAttribute("cnt1", cnt);        //글갯수
			model.addAttribute("number1", number);  //출력용 글번호
			model.addAttribute("pageNum1", pageNum); //페이지 번호
			
			if(cnt > 0) {
				model.addAttribute("startPage1", startPage); //시작 페이지
				model.addAttribute("endPage1", endPage);	//마지막 페이지
				model.addAttribute("pageBlock1", pageBlock); //한블럭당 페이지 갯수
				model.addAttribute("pageCount1", pageCount);	//페이지 갯수
				model.addAttribute("currentPage1", currentPage);//현재페이지
			}
		}
		//환불 신청
		@Override
		public void refund(HttpServletRequest req, Model model) {
			String chkArray = req.getParameter("chkArray");
			String notbnumArray = req.getParameter("notbnumArray");
			System.out.println("chkArray" + chkArray);
			System.out.println("notbnumArray" + notbnumArray);
			String memId = (String)req.getSession().getAttribute("memId");
			String[] notbnumArrayIn = notbnumArray.split(",");
			String[] chkArrayIn = chkArray.split(","); 
			 int insertCnt = 0; 
			 System.out.println("chkArrayIN" + chkArrayIn.length);
			 for(int i = 0; i < chkArrayIn.length; i++){ 
				 int notbnum = Integer.parseInt(notbnumArrayIn[i]);
				 int notbid = Integer.parseInt(chkArrayIn[i]); 
				 Map<String,Object> map = new HashMap<>();
					map.put("memId",memId);
					map.put("notbid",notbid);
					map.put("notbnum",notbnum);
					
				 insertCnt = dao.refundPro(map); 
				 System.out.println("insertCntrefund" + insertCnt);
			 } 
			 System.out.println("insertCnt" + insertCnt); 
			 model.addAttribute("insertCnt", insertCnt);
		}
		
		//환불 목록
		@Override
		public void refundlist(HttpServletRequest req, Model model) {
			//3단계 .화면으로 부터 입력받은 값을 받아온다.
			String memId = (String)req.getSession().getAttribute("memId");
			System.out.println("memId" + memId);
			//페이징
			int pageSize = 10; //한페이지당 출력할 글 갯수
			int pageBlock = 3; //한 블럭당 페이지 갯수
			
			int cnt = 0; //글갯수
			int start = 0; //현재 페이지 시작 글번호
			int end = 0; //현재 페이지 마지막 글번호
			int number = 0; //출력용 글번호
			String pageNum = ""; //페이지 번호
			int currentPage = 0; //현재페이지
			
			int pageCount = 0;  //페이지 갯수
			int startPage = 0; //시작 페이지
			int endPage = 0;  //마지막 페이지
			
			//5-1단계. 글갯수 구하기
			cnt = dao.refundlistCnt(memId);  //30
			System.out.println("cnt => " + cnt);
			
			pageNum = req.getParameter("pageNum");
			if(pageNum == null) {
				pageNum = "1"; //첫페이지를 1페이지로 지정
			}
			System.out.println(pageNum);
			//글 30건 기준
			currentPage = Integer.parseInt(pageNum);
			System.out.println("currentPage : " + currentPage);
			
			pageCount = (cnt / pageSize) + (cnt % pageSize > 0 ? 1 : 0); //페이지 갯수  + 나머지 있으면 1
			
			start = (currentPage - 1) * pageSize + 1;
			
			end = start + pageSize - 1;
			
			System.out.println("start : " + start);
			System.out.println("end : " + end);
			
			//출력용 글번호
			//30 = 30 - (1 - 1) * 5;
			number = cnt - (currentPage -1)* pageSize;
			
			System.out.println("start : " + start);
			System.out.println("end : " + pageSize);

			Map<String,Object> map = new HashMap<>();
			map.put("start",start);
			map.put("end",end);
			map.put("memId",memId);
			
			if(cnt > 0) {
				//환불 목록 조회
				List<Cu_VO> dtos = dao.refundlist(map);
				model.addAttribute("dtos", dtos);
			}
			//1 = (1 / 3) * 3 + 1;
			startPage = (currentPage / pageBlock) * pageBlock + 1;
			if(currentPage % pageBlock == 0) startPage -= pageBlock;
			
			System.out.println("startPage : " + startPage);
			//마지막페이지
			endPage = startPage + pageBlock - 1;
			if(endPage > pageCount)endPage = pageCount;
			
			System.out.println("endPage : " + endPage);
			System.out.println("====================");
			
			model.addAttribute("cnt", cnt);        //글갯수
			model.addAttribute("number", number);  //출력용 글번호
			model.addAttribute("pageNum", pageNum); //페이지 번호
			
			if(cnt > 0) {
				model.addAttribute("startPage", startPage); //시작 페이지
				model.addAttribute("endPage", endPage);	//마지막 페이지
				model.addAttribute("pageBlock", pageBlock); //한블럭당 페이지 갯수
				model.addAttribute("pageCount", pageCount);	//페이지 갯수
				model.addAttribute("currentPage", currentPage);//현재페이지
			}
		}
		//상태코드별 출력
		@Override
		public void buystate(HttpServletRequest req, Model model) {
			int state = Integer.parseInt(req.getParameter("state"));
			List<Cu_VO> dtos = dao2.buystate(state);
			model.addAttribute("dtos", dtos);
		}
		//이메일체크
		@Override
	    public void emailChk(HttpServletRequest req, Model model) {
	        String id = req.getParameter("id");
	        //email
			String email ="";
			String email1 = req.getParameter("email1");
			String email2 = req.getParameter("email2");
			
			if(!email1.equals("") && !email2.equals("")) {
			email = email1+"@"+email2;
			}
	        System.out.println("email : " + email);
	        
	        StringBuffer temp = new StringBuffer();
	        Random rnd = new Random();
	        Map<String,Object> map = new HashMap<>();
	        map.put("email", email);
	        map.put("id",id);
	        
	        for(int i = 0; i < 6; i++) {
	            int rIndex = rnd.nextInt(2);
	            switch(rIndex) {
	            case 0:
	                // A-Z
	                temp.append((char) ((int) (rnd.nextInt(26)) + 65));
	                break;
	            case 1:
	                // 0-9
	                temp.append((rnd.nextInt(10)));
	                break;
	            }
	        }
	        
	        String key = temp.toString();// StringBuffer 형식인 Key를 String으로 변환
	        System.out.println("key : " + key);
	        int cnt = dao.Idmailchk(map);
	        if(cnt == 0) {
	        	//없는 이메일
	        	model.addAttribute("cnt", cnt);
	        }else{
	        	//이메일 있을때
		        model.addAttribute("cnt", cnt);
		        model.addAttribute("key" , key);
		        model.addAttribute("id" , id);
		        dao.sendmail(email, key);
	        }
	    }
		public void pwdemail(HttpServletRequest req, Model model) {
			String id = req.getParameter("id");
			String codes = req.getParameter("codes");
			String code = req.getParameter("code");
			int cnt = 0;
			if(codes.equals(code)) {
				cnt = 1;
			}
			model.addAttribute("id" , id);
			model.addAttribute("cnt", cnt);
		}
		//회원비밀번호 수정
		@Override
		public void pwdmodify(HttpServletRequest req, Model model) {
			
			int updateCnt = 0;
			
			String id = req.getParameter("id");  //화면에서 받아온 아이디
			String pwd = req.getParameter("pwd"); //화면에서 받아온 패스워드
			String enctyptPassword = passwordEncoder.encode(pwd);
			Map<String,Object> map = new HashMap<>();
		       map.put("pwd", enctyptPassword);
		       map.put("id",id);
			updateCnt = dao.pwdmodifyPro(map);
			model.addAttribute("updateCnt", updateCnt);
		}
}
