<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>       
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/board.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
</head>
<body>
    <header>
       <c:if test="${sessionScope.memId == null}">
        <script type="text/javascript">
    		alert("잘못된 접근입니다. 다시로그인하여주십시오!");     
    		window.location="main"
    	 </script>
    </c:if>    
    <!-- 로그인 성공 -->
    <c:if test="${sessionScope.memId != null}">
        <div class="gnb">
            <ul>
            	<li style="font-size:15px; color:white;">ID : ${sessionScope.memId}</li>
                <li><a href="${path}logout" >로그아웃</a></li>
                <li><a href="${path}customer/mypage">내정보</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="main"><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas">회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board" >자유게시판</a></td>
                <td><a href="${path}customer/consulting" >문의사항</a></td>
            </tr>
        </table>    
        </div>
    </c:if> 
    </header>
    <contents>
    <div class="boarddiv" align="center">
    	<table style="width:1200px;">
	    	<tr>
				<th colspan="6" align="left" style="height:25px">
					자유게시판 | total  ${cnt}
				</th>
			</tr>
    	</table>
    	<table class="board" align="center">
		<tr>
			<th style="width:10%">글번호</th>
			<th style="width:25%">글제목</th>
			<th style="width:10%">작성자</th>
			<th style="width:10%">작성일</th>
			<th style="width:10%">조회수</th>
		</tr>
		
		<!-- 게시글이 있으면 -->
		<c:if test="${cnt > 0}">
			<c:forEach var="dto" items="${dtos}">
				<tr>
					<td>
						${number}
						<c:set var="number" value="${number-1}"/>
					</td>
					<td>
						<!-- 답글인 경우  : 들여쓰기> 1 -->
						<c:if test="${dto.ref_level > 1}">
							<c:set var="wid" value="${(dto.ref_level - 1) * 10} " />
							&nbsp;&nbsp;&nbsp;&nbsp;
						</c:if>
						
						<!-- 답글인 경우 : 들여쓰기> 0 -->
						<c:if test="${dto.ref_level > 0}">
							<img src="${path}resources/images/right-arrow_icon-icons.com_70881.png" border="0" width="20" height="15">
						</c:if>
						
						<!-- hot 이미지 -->
						<a href="${path}customer/contentForm?num=${dto.num}&pageNum=${pageNum}&number=${number+1}">${dto.subject}</a>
					</td>
					<td>
						${dto.writer}
					</td>
					<td>
						<fmt:formatDate type="both" pattern="yyyy-MM-dd HH:mm" value="${dto.reg_date}"/>
					</td>
					<td>
						${dto.readCnt}
					</td>
				</tr>
			</c:forEach>
		</c:if>
		
		<!-- 게시글이 없으면으면 -->
		<c:if test="${cnt == 0}">
			<tr>
				<td colspan="6" align="center">
					게시글이 없습니다. 글을 작성해주세요.!!
				</td>
			</tr>
		</c:if>
	</table>
<!-- 페이지 컨트롤 -->	
<table class="paging" style="width:1000px" align="center">
	<tr>
		<th align="center">
			<!-- 게시글이 있으면 -->
			<c:if test="${cnt > 0}">
				<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
				<c:if test="${startPage > pageBlock}">
					<a href="${path}customer/board">[◀◀]</a>
					<a href="${path}customer/board?pageNum=${startPage - pageBlock}">[◀]</a>
				</c:if>
				
				<!-- 블록내의 페이지 번호 -->
				<c:forEach var="i" begin="${startPage}" end="${endPage}">
					<c:if test="${i == currentPage}">
					<span><b>[${i}]</b></span>
					</c:if>
					<c:if test="${i != currentPage}">
						<a href="${path}customer/board?pageNum=${i}">[${i}]</a>
					</c:if>
				</c:forEach>
				<!-- 다음[▶] / 마지막[▶▶] -->
				<c:if test="${pageCount > endPage}">
					<a href="${path}customer/board?pageNum=${startPage + pageBlock}">[▶]</a>
					<a href="${path}customer/board?pageNum=${pageCount}">[▶▶]</a>
				</c:if>
			</c:if>
			<input id="button"type="button" value="글쓰기" onclick="window.location='${path}customer/boardWriteForm?pageNum=${pageNum}'">
		</th>
	</tr>
</table>
</div>
    </contents>
    <footer>
        <div class="office_adress">
        <pre>
사업자등록번호 : 000-00-00000 
대표이사 : 이건희 
주소 : 서울특별시 O구 OO로 OOO번길
이메일 : gunhee260@gmail.com
		</pre>
		<ul>
			<li></li>
		</ul>
		<pre>
제품이나 사이트 이용에 궁금증을 바로 해결하시려면, 1234-5678 으로 전화하세요.
상담 가능 시간 평일 10:00 - 18:00
        </pre>
        </div>
    </footer>
</body>
</html>