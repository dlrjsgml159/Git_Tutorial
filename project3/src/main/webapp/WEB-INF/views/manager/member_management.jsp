<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>        
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/member_management.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
	<script type ="text/javascript">
		function CUDelete(){
			if(confirm("회원님을 강제 탈퇴 하시겠습니까?")){
				var chkArray = new Array();
				$("input[name=checkbox]:checked").each(function(){
					chkArray.push($(this).val());
				});
				window.location="deleteMember?chkArray="+chkArray;
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
</head>
<body>
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
    	<table class="text1" align="center">
    		<tr>
    			<th style="width:5%"><input type='checkbox' name="checkAll" id="allCheck"></th>
    			<th style="width:5%">회원아이디</th>
    			<th style="width:5%">비밀번호</th>
    			<th style="width:5%">이름</th>
    			<th style="width:10%">전화번호</th>
    			<th style="width:15%">이메일</th>
    			<th style="width:20%">주소</th>
    			<th style="width:15%">가입일</th>
    		</tr>
    		<c:forEach var="dto" items="${dtos}">
	    		<tr>
	    			<td><input type='checkbox' name="checkbox" value="${dto.getId()}"></td>
	    			<td>${dto.getId()}</td>
	    			<td>${dto.getPwd()}</td>
	    			<td>${dto.getName()}</td>
	    			<td>${dto.getHp()}</td>
	    			<td>${dto.getEmail()}</td>
	    			<td>${dto.getAddress()}</td>
	    			<td>${dto.getReg_date()}</td>
	    		</tr>
	    		</c:forEach>
    		<tr>
    			<td><input type="submit" id="button"value="회원탈퇴" onclick="CUDelete();"></td>
    		</tr>
    	</table>
    	<table class="paging" style="width:1000px" align="center">
				<tr>
					<th align="center">
						<!-- 게시글이 있으면 -->
						<c:if test="${cnt > 0}">
							<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
							<c:if test="${startPage > pageBlock}">
								<a href="${path}manager/member_management">[◀◀]</a>
								<a href="${path}manager/member_management?pageNum=${startPage - pageBlock}">[◀]</a>
							</c:if>
							
							<!-- 블록내의 페이지 번호 -->
							<c:forEach var="i" begin="${startPage}" end="${endPage}">
								<c:if test="${i == currentPage}">
								<span><b>[${i}]</b></span>
								</c:if>
								<c:if test="${i != currentPage}">
									<a href="${path}manager/member_management?pageNum=${i}">[${i}]</a>
								</c:if>
							</c:forEach>
							<!-- 다음[▶] / 마지막[▶▶] -->
							<c:if test="${pageCount > endPage}">
								<a href="${path}manager/member_management?pageNum=${startPage + pageBlock}">[▶]</a>
								<a href="${path}manager/member_management?pageNum=${pageCount}">[▶▶]</a>
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