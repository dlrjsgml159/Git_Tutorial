<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/cartlist.css">
<meta charset="utf-8" />
<script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
<script type="text/javascript">
    	$(function(){
    		$("#allCheck").click(function(){ 
    		if($("#allCheck").prop("checked")){
    			$("input[name=checkbox]").prop("checked",true); 
    			} else { 
    				$("input[name=checkbox]").prop("checked",false);
    			}
    		})
    	}) 
    </script>
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
                <li style="float:left"><a href="${path}main"><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
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
    <div  class="center" align="center">
    <div class="title">
	    		<h2 style="font-size:40px;">환불내역</h2>
	    	</div>
	    	<div class="titleli">	
		    		<ul>
		    			<li>홈 > </li>
		    			<li>내정보 > </li>
		    			<li>환불내역</li>
		    		</ul>
		    </div>	
	    	<div class="litable"> 
	    	<ul>
	    		<li><a href="${path}customer/mypage" class="listyle">정보수정</a></li>
	    		<li><a href="${path}customer/mypage-orderlist" class="listyle">주문내역</a></li>
	    		<li class="hit"><a href="${path}customer/refund" class="listyle">환불내역</a></li>
	    		<li><a href="${path}customer/cartlist" class="listyle">장바구니</a></li>
	    		<li><a href="${path}customer/mypage-leave" class="listyle">회원탈퇴</a></li>
	    		<li><a href="logout" class="listyle">로그아웃</a></li>
	    	</ul>
	    	</div>
    <form action="${path}customer/cartbuy_pro" name="orderlistform" method="post">
	    <div class="cartlist" align="center">
		    <table class="table">
				<tr>
					<th style="width:10%">
						환불상태
					</th>
					<th style="width:10%">
						제품이미지
					</th>
					<th style="width:15%">
						제품명
					</th>
					<th style="width:10%">
						브랜드
					</th>
					<th style="width:10%">
						수량
					</th>
					<th style="width:10%">
						가격
					</th>
				</tr>
				<c:if test="${cnt > 0}">
			<c:forEach var="dto" items="${dtos}"> 
				<tr>
					<td>
						<c:if test="${dto.getREFUND_NOTB_STATE() == 1}">
							환불승인대기중
						</c:if>
						<c:if test="${dto.getREFUND_NOTB_STATE() == 2}">
							환불승인완료
						</c:if>
						<c:if test="${dto.getREFUND_NOTB_STATE() == 3}">
							환불거부 상태
						</c:if>
					</td>
					<td>
						<img src="${path}resources/images/${dto.getREFUND_NOTB_IMG()}" class="imgclass" >
					</td>
					<td>
						${dto.getREFUND_NOTB_NAME()}
					</td>
					<td>
						${dto.getREFUND_NOTB_BRAND()}
					</td>
					<td>
						${dto.getREFUND_NOTB_CNT()}
					</td>
					<td>
						<fmt:formatNumber value="${dto.getREFUND_NOTB_PRICE()}" pattern="#,###"/> 원
					</td>
				</tr>
			</c:forEach>
		</c:if>
		<!-- 게시글이 없으면으면 -->
		<c:if test="${cnt == 0}">
			<tr>
				<td colspan="6" align="center">
					장바구니목록이 없습니다.
				</td>
			</tr>
		</c:if>
		    </table>
		    <table class="paging" style="width:1000px" align="center">
				<tr>
					<th align="center">
						<!-- 게시글이 있으면 -->
						<c:if test="${cnt > 0}">
							<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
							<c:if test="${startPage > pageBlock}">
								<a href="${path}customer/cartlist">[◀◀]</a>
								<a href="${path}customer/cartlist?pageNum=${startPage - pageBlock}">[◀]</a>
							</c:if>
							
							<!-- 블록내의 페이지 번호 -->
							<c:forEach var="i" begin="${startPage}" end="${endPage}">
								<c:if test="${i == currentPage}">
								<span><b>[${i}]</b></span>
								</c:if>
								<c:if test="${i != currentPage}">
									<a href="${path}customer/cartlist?pageNum=${i}">[${i}]</a>
								</c:if>
							</c:forEach>
							<!-- 다음[▶] / 마지막[▶▶] -->
							<c:if test="${pageCount > endPage}">
								<a href="${path}customer/cartlist?pageNum=${startPage + pageBlock}">[▶]</a>
								<a href="${path}customer/cartlist?pageNum=${pageCount}">[▶▶]</a>
							</c:if>
						</c:if>
					</th>
				</tr>
			</table>
		   </div>
	    </form>
	   </div> 
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