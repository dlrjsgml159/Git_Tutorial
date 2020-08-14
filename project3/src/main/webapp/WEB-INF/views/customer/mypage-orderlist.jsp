<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>       
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/mypage-orderlist.css">
<script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
<script type="text/javascript">
	function refund(){
		
		var notbnumArray = new Array();
		var Arrayo = new Array();
		var chkArray = new Array();
		
		if(confirm("정말 환불하시겠습니까?")){
			$("input[name=checkbox]:checked").each(function(){
				Arrayo.push($(this).val());
			})
			for(var i =0; i<Arrayo.length; i++){
				chkArray[i] = Arrayo[i].split(',')[0]
				notbnumArray[i] = Arrayo[i].split(',')[1]
			}
			window.location="refund_Pro?chkArray="+chkArray+"&notbnumArray="+notbnumArray;
				
		}else{
			return;
		}
	}
	
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
    <meta charset="utf-8" />
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
    <content>
    <div class="center" align="center">
	    <div class="title">
	    		<h2 style="font-size:40px;">구매내역</h2>
	    	</div>
	    	<div class="titleli">	
		    		<ul>
		    			<li>홈 > </li>
		    			<li>내정보 > </li>
		    			<li>구매내역</li>
		    		</ul>
		    </div>	
	    	<div class="litable">
	    	<ul>
	    		<li><a href="${path}customer/mypage" class="listyle">정보수정</a></li>
	    		<li class="hit"><a href="${path}customer/mypage-orderlist" class="listyle">주문내역</a></li>
	    		<li><a href="${path}customer/refund" class="listyle">환불내역</a></li>
	    		<li><a href="${path}customer/cartlist" class="listyle">장바구니</a></li>
	    		<li><a href="${path}customer/mypage-leave" class="listyle">회원탈퇴</a></li>
	    		<li><a href="logout" class="listyle">로그아웃</a></li>
	    	</ul>
	    	</div>
	    <form action="${path}customer/refund_pro" name="orderlistform" method="post">
	    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
	    <div class="cartlist" align="center">
	    <table class="table">
	    		<tr>
					<th style="width:3%">
						<input type='checkbox' name="checkAll" id="allCheck" onclick="checkAll();">
					</th>
					<th style="width:10%">
						배송상태
					</th>
					<th style="width:10%">
						제품이미지
					</th>
					<th style="width:20%">
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
	    		<c:forEach var="dto2" items="${dtos2}" >
	    		<tr>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 1}">
	    			<td></td>
	    			<td>승인대기중</td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 2}">
	    			<td></td>
	    			<td>승인완료 배송준비중</td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 3}">
	    			<td></td>
	    			<td>배송중</td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 4}">
	    			<td><input type='checkbox' name="checkbox" value="${dto2.getBUY_NOTB_ID()},${dto2.getBUY_NOTB_NUM()}"></td>
	    			<td>배송완료</td>
	    			</c:if>
	    			<td><img src="${path}resources/images/${dto2.getBUY_NOTB_IMG()}" width="100" height="100"></a></td>
	    			<td>${dto2.getBUY_NOTB_NAME()}</td>
	    			<td>${dto2.getBUY_NOTB_BRAND()}</td>
	    			<td>${dto2.getBUY_NOTB_CNT()}</td>
	    			<td><fmt:formatNumber value="${dto2.getBUY_NOTB_PRICE()}" pattern="#,###"/> 원</td>
	    		</tr>
	    		</c:forEach>
	    </table>
	    <table class="paging" style="width:1000px" align="center">
				<tr>
					<th align="center">
						<!-- 게시글이 있으면 -->
						<c:if test="${cnt1 > 0}">
							<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
							<c:if test="${startPage1 > pageBlock1}">
								<a href="${path}customer/mypage-orderlist">[◀◀]</a>
								<a href="${path}customer/mypage-orderlist?pageNum=${startPage1 - pageBlock1}">[◀]</a>
							</c:if>
							
							<!-- 블록내의 페이지 번호 -->
							<c:forEach var="i" begin="${startPage1}" end="${endPage1}">
								<c:if test="${i == currentPage1}">
								<span><b>[${i}]</b></span>
								</c:if>
								<c:if test="${i != currentPage1}">
									<a href="${path}customer/mypage-orderlist?pageNum=${i}">[${i}]</a>
								</c:if>
							</c:forEach>
							<!-- 다음[▶] / 마지막[▶▶] -->
							<c:if test="${pageCount1 > endPage1}">
								<a href="${path}customer/mypage-orderlist?pageNum=${startPage1 + pageBlock1}">[▶]</a>
								<a href="${path}customer/mypage-orderlist?pageNum=${pageCount1}">[▶▶]</a>
							</c:if>
						</c:if>
					</th>
				</tr>
			</table>
	    <div class="buttoncl1">
		    <div>
		    	<input type="button" id="button5"value="환불" onclick="refund();">
		    </div>
		</div>
    </div>
    </form>
    </div>
    </content>
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