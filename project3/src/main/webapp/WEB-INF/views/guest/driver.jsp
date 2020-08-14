<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>      
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/driver.css">
    <meta charset="utf-8" />
	<script type ="text/javascript">
	</script>
</head>
<body>
    <header>
        <c:if test="${sessionScope.memId == null}">
        <div class="gnb">
            <ul>
                <li><a href="${path}login" >로그인</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="${path}main" ><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas" >회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board" onclick="return loginChk();">자유게시판</a></td>
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
    <contents>
    <div align="center" class="divtable">
	<table>
	<tr>
		<td ><a href="" alt=""><input type="button" value="driver1 다운"></a></td>
		<td style="width:620px;">Quadro 고급 옵션 (Nview, NVWMI 등)</td>
	</tr>
	<tr>
		<td><a href="" alt=""><input type="button" value="driver2 다운"></a></td>
		<td style="width:620px;">Linux, FreeBSD, and Solaris드라이버</td>
	</tr>
	<tr>	
		<td><a href="" alt=""><input type="button" value="driver3 다운"></a></td>
		<td style="width:620px;">MAC용 NVIDIA CUDA 드라이버</td>
	</tr>
	<tr>
		<td><a href="" alt=""><input type="button" value="driver4 다운"></a></td>
		<td style="width:620px;">엔비디아 위젯</td>
	</tr>
	<tr>	
		<td><a href="" alt=""><input type="button" value="driver5 다운"></a></td>
		<td style="width:620px;">NVIDIA Business Platform드라이버</td>
	</tr>
	<tr>	
		<td><a href="" alt=""><input type="button" value="driver6 다운"></a></td>
		<td style="width:620px;">Zalman Stereoscopic 3D 드라이버</td>
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