package com.spring.project3.service;

import java.util.List;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.ui.Model;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.multipart.MultipartRequest;

import com.spring.project3.persistence.Cu_DAOImpl;
import com.spring.project3.persistence.Ma_DAOImpl;
import com.spring.project3.vo.Cu_VO;
import com.spring.project3.vo.Ma_VO;


@Service
public class Ma_ServiceImpl implements Ma_Service{
	
	@Autowired
	Ma_DAOImpl dao;
	
	@Autowired
	Cu_DAOImpl dao2;
	
	@Override
	public void inventoryList(HttpServletRequest req, Model model) {
		
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
			List<Ma_VO> dtos = dao.getArticleList(map);
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
	//재고추가
	@Override
	public void inventoryadd(MultipartHttpServletRequest req, Model model) {
		
		MultipartFile file1 = req.getFile("file1");
		MultipartFile file2 = req.getFile("file1");
		
        String saveDir = req.getSession().getServletContext().getRealPath("/resources/images/note_img/");
        String realDir = "C:\\dev65\\workspace\\lgh.notebookstore\\WebContent\\images\\";
        
        try {
        	file1.transferTo(new File(saveDir+file1.getOriginalFilename()));
        	file2.transferTo(new File(saveDir+file2.getOriginalFilename()));
        	//제품이미지
        	FileInputStream fis1 = new FileInputStream(saveDir + file1.getOriginalFilename());
        	FileOutputStream fos1 = new FileOutputStream(realDir + file1.getOriginalFilename());
        	
        	//상세이미지
        	FileInputStream fis2 = new FileInputStream(saveDir + file2.getOriginalFilename());
        	FileOutputStream fos2 = new FileOutputStream(realDir + file2.getOriginalFilename());
        	int data = 0;
        	
        	while((data = fis1.read()) != -1) {
        		fos1.write(data);
        	}
            fis1.close();
            fos1.close();
            
            while((data = fis2.read()) != -1) {
        		fos2.write(data);
        	}
            fis2.close();
            fos2.close();
            
		Ma_VO vo = new Ma_VO();
		
		vo.setNotb_name(req.getParameter("notb_name"));
		vo.setNotb_cnt(Integer.parseInt(req.getParameter("notb_cnt")));
		vo.setNotb_price(Integer.parseInt(req.getParameter("notb_price")));
		vo.setNotb_brand(req.getParameter("notb_brand"));
		vo.setNotb_img(file1.getOriginalFilename());
		vo.setNotb_img_information(file2.getOriginalFilename());
		
		int cnt = dao.inadd(vo);
		
		model.addAttribute("insertCnt", cnt);
		
        }catch(Exception e){
        	e.printStackTrace();
        }
	}
//	//재고수정 처리
//	@Override
//	public void inventorymodify(HttpServletRequest req, Model model) {
////		MultipartRequest mr = null;
////        int maxSize = 10 * 1024 * 1024;
////        String saveDir = req.getSession().getServletContext().getRealPath("/images/note_img/");
////        String realDir = "C:\\dev\\workespace\\lgh.notebookstore\\WebContent\\images\\";
////        String encType = "UTF-8";
////        
////        try {
////        	mr = new MultipartRequest(req, saveDir, maxSize, encType, new DefaultFileRenamePolicy());
////        	FileInputStream fis = new FileInputStream(saveDir + mr.getFilesystemName("file1"));
////        	FileOutputStream fos = new FileOutputStream(realDir + mr.getFilesystemName("file1"));
////        	
////        	FileInputStream fis2 = new FileInputStream(saveDir + mr.getFilesystemName("file2"));
////        	FileOutputStream fos2 = new FileOutputStream(realDir + mr.getFilesystemName("file2"));
////        	int data = 0;
////        	
////        	while((data = fis.read()) != -1) {
////        		fos.write(data);
////        	}
////            fis.close();
////            fos.close();
////            
////            while((data = fis2.read()) != -1) {
////        		fos2.write(data);
////        	}
////            fis2.close();
////            fos2.close();
////            
////        int num = Integer.parseInt(mr.getParameter("notb_id"));
////		//3단계 . 화면으로 부터 입력받은 값을 받아온다.
////		Ma_VO vo = new Ma_VO();
////		//vo 바구니를 생성한다.
////		vo.setNotb_id(Integer.parseInt(mr.getParameter("notb_id")));
////		vo.setNotb_name(mr.getParameter("notb_name"));
////		vo.setNotb_cnt(Integer.parseInt(mr.getParameter("notb_cnt")));
////		vo.setNotb_price(Integer.parseInt(mr.getParameter("notb_price")));
////		vo.setNotb_brand(mr.getParameter("notb_brand"));
////		vo.setNotb_img(mr.getFilesystemName("file1"));
////		vo.setNotb_img_information(mr.getFilesystemName("file2"));
////		
////		//vo 바구니에 입력받은 값을 담는다.
////		//4.단계 다형성 적용, 싱글톤 방식으로 dao 객체 생성
////		
////		
////		int cnt = dao.modifypro(num, vo);
////		
////		//6단계. request나 session으로 처리결과를 저장(jsp에 전달하기 위함)
////		System.out.println("updateCnt = " + cnt);
////		model.addAttribute("UpdateCnt", cnt);
////        }catch(Exception e){
////        	e.printStackTrace();
////       }
//	}
	//제품상세
	@Override
	public void inventoryDetail(HttpServletRequest req, Model model) {
		//3단계. 화면으로부터 입력받은 값(get방식)을 받아온다.
		//contentForm.bo?num=30&pageNum=1&number=30
		int num = Integer.parseInt(req.getParameter("num"));
		int pageNum = Integer.parseInt(req.getParameter("pageNum"));
		int number = Integer.parseInt(req.getParameter("number"));
		
		//5-2단계 . 상세페이지 조회
		Ma_VO vo = dao.getArticle(num);
		
		//6단계. request나 session에 처리결과를 저장(jsp에 전달하기 위함)
		model.addAttribute("dto", vo); //참조변수
		model.addAttribute("pageNum", pageNum);
		model.addAttribute("number", number);
		
	}
//	
//	//제품 삭제
//	@Override
//	public void inventoryDelete(HttpServletRequest req, Model model) {
//		//3단계. 화면으로부터 입력받은 값(get방식)을 받아온다.
//		int num = Integer.parseInt(req.getParameter("num"));
//		int pageNum = Integer.parseInt(req.getParameter("pageNum"));
//		
//		//4단계. 다형성 적용, 싱글톤 방식으로 dao 객체 생성
//		
//		
//		//게시글 삭제 처리
//		int deleteCnt = dao.inventoryDeletePro(num);
//		model.addAttribute("deleteCnt", deleteCnt);
//		System.out.println("delc" + deleteCnt);
//		model.addAttribute("pageNum", pageNum);
//	}
//	
	//구매목록
	@Override
	public void mabuylist(HttpServletRequest req, Model model) {
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
		
		cnt = dao.mabuylistCnt();  //30
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
		Map<String,Object> map = new HashMap<String,Object>();
		map.put("start", start);
		map.put("memId", memId);
		map.put("end", end);
		if(cnt > 0) {
			//5-2단계. 게시글 목록 조회
			List<Cu_VO> dtos = dao.mabuylistPro(map);
			model.addAttribute("dtos2", dtos);
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
	//고객 리스트
	@Override
	public void macustomerlist(HttpServletRequest req, Model model) {
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
		
		cnt = dao.macustomerCnt();  //30
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

		Map<String,Object> map = new HashMap<String,Object>();
		map.put("start", start);
		map.put("end", end);
		
		if(cnt > 0) {
			//5-2단계. 게시글 목록 조회
			List<Cu_VO> dtos = dao.macustomerPro(map);
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
	//환불 목록
	@Override
	public void marefundlist(HttpServletRequest req, Model model) {
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
		
		cnt = dao.marefundlistCnt();  //30
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
		
		Map<String,Object> map = new HashMap<String,Object>();
		map.put("start", start);
		map.put("end", end);
		if(cnt > 0) {
			//환불 목록 조회
			List<Cu_VO> dtos = dao.marefundlist(map);
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
	//구매 상태 변경
	@Override
	public void purchaseapproval(HttpServletRequest req, Model model) {
		
		int state = Integer.parseInt(req.getParameter("state"));
		int notbid = Integer.parseInt(req.getParameter("notbid"));
		String id = req.getParameter("id");
		int notbnum = Integer.parseInt(req.getParameter("notbnum"));
		Map<String,Object> map = new HashMap<String,Object>();
		map.put("state",state);
		map.put("notbid",notbid);
		map.put("notbnum",notbnum);
		map.put("id",id);
 		System.out.println("state" + state);
		dao.purchaseapproval(map);
	}
	//환불 상태 변경
	@Override
	public void marefund(HttpServletRequest req, Model model) {
		
		int state = Integer.parseInt(req.getParameter("state"));
		int notbid = Integer.parseInt(req.getParameter("notbid"));
		int notbnum = Integer.parseInt(req.getParameter("notbnum"));
		String id = req.getParameter("id");
		if(state == 1) {
			state = 2;
		}
		Map<String,Object> map = new HashMap<String,Object>();
		map.put("state",state);
		map.put("notbid",notbid);
		map.put("notbnum",notbnum);
		map.put("id",id);
 		System.out.println("state" + state);
		dao.marefundPro(map);
	}
	
	//회원 삭제 
	@Override
	public void deleteMember(HttpServletRequest req, Model model) {
		String chkArray = req.getParameter("chkArray");
		System.out.println("chkArray"+chkArray);
		String[] chkArrayIn = chkArray.split(","); 
		
		int deleteCnt = 0;
		for(int i = 0; i < chkArrayIn.length; i++){ 
			String memId = chkArrayIn[i]; 
			System.out.println("memId"+memId);
			deleteCnt = dao.deleteMember(memId);
		 } 
		model.addAttribute("deleteCnt", deleteCnt);
		System.out.println("deleteCnt = " + deleteCnt);
	}
	//결산
	@Override
	public void settlement(HttpServletRequest req, Model model) {
		List<Ma_VO> dtos  = dao.settlementPro();
		model.addAttribute("dtos", dtos);
	}
}