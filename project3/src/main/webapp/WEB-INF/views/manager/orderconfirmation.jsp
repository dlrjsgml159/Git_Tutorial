<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>         
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/orderconfirmation.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
	<script type ="text/javascript">
	
	function load(){
		var state = 0;
		$("#delebary").change(function(){
			if( $(this).val() == "전체목록"){
				$(".text5").hide();
				$(".text1").show();
			}else{
				$(".text1").hide();
				state = $(this).val();
				console.log(state);
				$.ajax({
					url : '/project3/manager/buystate', //new > file > basic4_json.js
					type : 'GET',
					data : 'state='+state,
					success : function(result){ //콜백 함수
						$('#display').html(result);
					},
					error : function(){
						alert("에러 ");
					}
				});
			}
		});
	}
		function checkAll(){
		      if( $("#allCheck").is(':checked') ){
		        $("input[name=checkAll]").prop("checked", true);
		      }else{
		        $("input[name=checkAll]").prop("checked", false);
		      }
		}
	</script>
</head>
<body onload="load();">
    <header>
        <div class="gnb">
           <ul>
           		<li style="font-size:15px; color:white;">ID : manager</li>
                <li><a href="${path}logout" >로그아웃</a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}manager/inventory_management" >재고관리</a></td>
                <td><a href="${path}manager/orderconfirmation" >주문관리</a></td>
                <td><a href="${path}manager/refund_request" >환불관리</a></td>
                <td><a href="${path}manager/member_management" >회원관리</a></td>
                <td><a href="${path}manager/settlement" >결산</a></td>
            </tr>
        </table>
        </div>
    </header>
    <contents>
    <div align="center">
   		<select id="delebary" onchange="load();">
    		<option value="전체목록">전체목록</option>
    		<option value="1">승인 대기중</option>
    		<option value="2">승인완료 배송준비중</option>
    		<option value="3">배송중</option>
    		<option value="4">배송 완료</option>
    	</select>
    	<table class="text1">
	    		<tr>
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
					<th style="width:10%">
						구매자
					</th>
				</tr>
	    		<c:forEach var="dto2" items="${dtos2}">
	    		<tr>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 1}">
	    			<td>승인대기중<br><input type="button" value="구매승인" onclick="window.location='${path}manager/orderconfirmation_pro?state=${dto2.getBUY_NOTB_STATE()}&id=${dto2.getId()}&notbid=${dto2.getBUY_NOTB_ID()}&notbnum=${dto2.getBUY_NOTB_NUM()}'"></td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 2}">
	    			<td>승인완료 배송준비중<br><input type="button" value="배송시작"onclick="window.location='${path}manager/orderconfirmation_pro?state=${dto2.getBUY_NOTB_STATE()}&id=${dto2.getId()}&notbid=${dto2.getBUY_NOTB_ID()}&notbnum=${dto2.getBUY_NOTB_NUM()}'"></td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 3}">
	    			<td>배송중<br><input type="button" value="배송완료"onclick="window.location='${path}manager/orderconfirmation_pro?state=${dto2.getBUY_NOTB_STATE()}&id=${dto2.getId()}&notbid=${dto2.getBUY_NOTB_ID()}&notbnum=${dto2.getBUY_NOTB_NUM()}'"></td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 4}">
	    			<td>배송완료</td>
	    			</c:if>
	    			<td><img src="${path}resources/images/${dto2.getBUY_NOTB_IMG()}" width="100" height="100"></td>
	    			<td>${dto2.getBUY_NOTB_NAME()}</td>
	    			<td>${dto2.getBUY_NOTB_BRAND()}</td>
	    			<td>${dto2.getBUY_NOTB_CNT()}</td>
	    			<td><fmt:formatNumber value="${dto2.getBUY_NOTB_PRICE()}" pattern="#,###"/> 원</td>
	    			<td>${dto2.getId()}</td>
	    		</tr>
	    		</c:forEach>
	    </table>
	    <div id="display"></div>
	    <table class="paging" style="width:1000px" align="center">
				<tr>
					<th align="center">
						<!-- 게시글이 있으면 -->
						<c:if test="${cnt > 0}">
							<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
							<c:if test="${startPage > pageBlock}">
								<a href="${path}manager/orderconfirmation">[◀◀]</a>
								<a href="${path}manager/orderconfirmation?pageNum=${startPage - pageBlock}">[◀]</a>
							</c:if>
							<!-- 블록내의 페이지 번호 -->
							<c:forEach var="i" begin="${startPage}" end="${endPage}">
								<c:if test="${i == currentPage}">
								<span><b>[${i}]</b></span>
								</c:if>
								<c:if test="${i != currentPage}">
									<a href="${path}manager/orderconfirmation?pageNum=${i}">[${i}]</a>
								</c:if>
							</c:forEach>
							<!-- 다음[▶] / 마지막[▶▶] -->
							<c:if test="${pageCount > endPage}">
								<a href="${path}manager/orderconfirmation?pageNum=${startPage + pageBlock}">[▶]</a>
								<a href="${path}manager/orderconfirmation?pageNum=${pageCount}">[▶▶]</a>
							</c:if>
						</c:if>
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