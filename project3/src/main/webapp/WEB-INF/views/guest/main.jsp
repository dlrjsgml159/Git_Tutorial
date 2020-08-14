<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>

<link type="text/css" rel="stylesheet" href="${path}resources/style/main.css">
    <meta charset="utf-8" />
</head>
<body>
<c:choose>
	<c:when test="${selectCnt == -1 }"><!-- 로그인 실패 -->
		<script type="text/javascript">
			alert("비밀번호가 다릅니다. 다시확인하세요.!!")
			window.location='login';
		</script>
	</c:when>
	<c:when test="${selectCnt == 0 }"> <!-- 비가입 -->
		<script type="text/javascript">
			alert("존재하지 않는 아이디 입니다. 다시확인하세요");
			window.location='login';
		</script>	
	</c:when>
	<c:when test="${selectCnt == 2}"> <!-- 회원가입에 성공한경우 -->
		<script type="text/javascript">
			alert("로그인에 성공하였습니다.");
		</script>	
	</c:when>
	<c:when test="${selectCnt == 1}">
		<script type="text/javascript">
			alert("회원가입을 축하합니다. 로그인하세요.");
			window.location='login';
		</script>	
	</c:when>
	<c:when test="${selectCnt == 3 }">
		<script type="text/javascript">
			alert("로그아웃하였습니다 안녕히가십시오.");
		</script>	
	</c:when>
</c:choose>
    <header>
    <!-- 첫화면 , 로그인 실패 -->
    <c:if test="${sessionScope.memId == null}">
        <div class="gnb">
            <ul>
                <li><a href="login" >로그인</a></li>
                <li><a href="order" >주문</a></li>
                <li style="float:left"><a href="main"><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas" >회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board"  onclick="return loginChk();">자유게시판</a></td>
                <td><a href="${path}customer/consulting" onclick="return loginChk();">문의사항</a></td>
            </tr>
        </table>    
        </div>
    </c:if>    
    <!-- 로그인 성공 -->
    <c:if test="${sessionScope.memId != null}">
        <div class="gnb">
            <ul>
            	<li style="font-size:15px; color:white;">ID : ${sessionScope.memId}</li>
                <li><a href="${path}logout" >로그아웃</a></li>
                <li><a href="${path}customer/mypage" >내정보</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="main" ><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas" >회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board" >자유게시판</a></td>
                <td><a href="${path}customer/consulting" >문의사항</a></td>
            </tr>
        </table>    
        </div>
    </c:if>    
    </header>
    <div id="content">
        <div class="section1">
            <div class="slide_banner"><img src="${path}resources/images/note2.png" width="800" height="1000"></div>
            <div class="textsi"><p>ByBook Pro<br>Refresh<br>우리 모두 누군가의 프로</p></div>
        </div>
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