<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/aboutas.css">
<meta charset="utf-8" />
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
        <style>
      #map {
      	margin-top:50px;
        height: 500px;
        width: 800px;
       }
    </style>
  </head>
  <body>
  	<br><br><br><br>
    <h3>회사위치</h3>
    <div align="center">
    	<div id="map" ></div>
    </div>
    <script>
      function initMap() {
        var uluru = {lat: 37.478792, lng: 126.878710};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 14,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD9xF02SrTzjI9tUs157Xb37hm6EH4ilPI&callback=initMap">
    </script>
    <pre>
    <br><br><br>
<h3>우주 공간에서</h3>
600일간의 우주 임무 동안 무결점을 기록한 ADRON 노트북
우주 항공 임무에 사용할 컴퓨터 및 전자 제품의 주요 공급 업체인 R&K는 미르 우주정거장에서 
우주인이 임무를 수행하는 동안 믿고 사용할 수 있는 컴퓨터를 제공하기 위해 2대의 ADRON 노
트북를 선정하였습니다. 600일간의 기간 내내 2대의 노트북에는 아무 결함도 나타나지 않았
습니다. 「다른 업체에서 만든 일부 제품과는 달리 ADRON 노트북은 절대로 과열되는 일이 없
었습니다」 라고 임무에 참여한 러시아 우주비행사인 세르게이 아브데예프가 전했습니다. 「우
주 공간과 지구에서 열유동은 완전히 다릅니다. 최고의 방열 솔루션을 갖춘 노트북만이 계속되
는 작업에서도 살아남을 수 있습니다. 아침에 노트북을 켜고 하루 종일 놔두었지만 아무 문제도
 발생하지 않았습니다.

<h3>상공에서</h3>
ADRON 노트북은 의료 헬기(NRMA CareFlight) 구급팀이 생명을 구하는 데도 도움을 
주고 있습니다.호주의 뉴사우스웨일스에서 응급 의료 및 구조 헬기를 운영하는 NRMA Care
Flight는 비행, 의료 및 관리 등 다양한 분야의 서비스를 제공하는 데 있어서 ADRON 노트
북을 사용하고 있습니다. ADRON 노트북은 머리에 심각한 외상이 발생한 사고에서 생존율을
 높이기 위한 CareFlight의 프로그램에서 특히 중요한 역할을 수행하고 있습니다 모바일
  컴퓨팅의 도움으로, CareFlight은 해당 지역의 구급차보다 더 빨리 의료팀을 현장에
   파견할 수 있으며, 이 새로운 프로그램은 머리 부상으로 인한 사망자수를 33% 줄일 것
   으로 예상됩니다. "모든 조종사가 ADRON M5 노트북에 깊은 인상을 받았으며 항공기의 
   진동에 잘 견디는 것을 보고 놀라워하고 있습니다"라고 CareFlight의 커뮤티니 홍보실
   장인 Mark Lees가 말했습니다. "현재 모든 항공기에 ADRON M5 노트북을 설치하고 
   온보드 내비게이션 컴퓨터에 연결하기 위해 준비하고 있습니다.」

<h3>도로상에서</h3>
ADRON 노트북은 혹독한 오프 로드 자동차 경주에서도 나무랄데 없는 성능을 발휘합니다.
ADRON 노트북은 뜨거운 사막과 눈 덮인 산에서 컴퓨터를 사용하게 되는 PATAGONIA
2000 경주에서 중요한 작업을 수행하기 위해 선택되었습니다. 주요 임무 중 하나는 
내비게이션 장치로서의 역할을 수행하는 것이었는데, 위성 GPS 기능이 내장되었으며 
동적 지도(dynamic map)를 표시할 수 있게 되어 있어서 역할을 훌륭하게 수행하였
습니다. 또한 이메일 통신과 양방향 화상 회의를 모두 가능하게 하는 통신 센터의 역할을
 수행하였습니다. 「말할 필요도 없이, ADRON 컴퓨터는 단 하나의 오작동 없이 이런 
 격렬한 경주와 같은 극한의 조건에서도 잘 살아남았습니다」 라고 경주 조직위원인 Avi
 v Shweky가 말했습니다.

<h3>세계에서 가장 높은 산의 정상에서</h3>
에베레스트산의 정상에 최초로 오른 ADRON 노트북
세계에서 가장 높은 산의 정상과 같은 혹독한 기후 조건에서 다른 노트북은 어려움을 
겪게 되겠지만 ADRON 제품은 개의치 않습니다. 티베트 현지에서 초모랑마(Qomo
langma Peak)로 알려진 에베레스트산의 정상으로 원정을 떠나는 산악팀은 U5
, S6 (모두 가죽 버전와 대나무 버전임), W7과 U1을 포함한 여러 대의 ADRON 
노트북을 등반에 지참했습니다. 5천미터 고도의 베이스캠프에 이르자 오직 ADRON 
노트북만이 계속 작동했습니다. 타사의 노트북 제품들은 주위 온도가 너무 낮아서 부
팅이 되지 않았습니다. 원정대의 리더인 Wang Yongfong 산악대장이 환경친화
적인 기술에 대한 감사의 의미로 지참한 덕분에 ADRON의 U5는 자그마치 높이가 8,84
8.43m인 초모랑마 정상까지 오를 수 있었는데, 이로써 ADRON 노트북은 최초로 에
베레스트산의 정상에 오른 제품이 되었습니다.

<h3>지구의 끝에서</h3>
ADRON 노트북, 북극과 남극을 정복하다.
ADRON 노트북은 여러 차례에 걸쳐 북극과 남극의 결빙 온도에서도 완벽하게 작동할 
수 있다는 것을 입증하였습니다. 이러한 탐험 중 가장 기억에 남는 순간은 높이가 
해발 1만 6천피트, 온도는 화씨 영하 100도를 훨씬 밑도는 남극 대륙의 최고봉인 
마운틴 빈슨(Mount Vinson) 정상으로 위대한 산악인으로 평가받는 Shi Wa
ng과 Jian Liu가 2003년 12월 16일 원정을 떠났을 때입니다. Wang과 Liu
는 원정 경험을 기록하고 공유하기 위해 ADRON S200N 노트북을 각자 가지고 갔습
니다. S200N은 가볍고 소형이었으며 하드디스크는 용량이 크고 혹독한 등반을 견
딜 수 있어서 자신들의 필요에 완벽하게 부응했습니다. 「노트북은 극한의 조건과 
혹한의 날씨에도 사소한 고장 없이 작동했습니다. 고장이 용납되지 않는 상황에서 
믿을 수 있는 노트북을 가지고 간 것은 행운이었습니다」 라고 Wang은 말했습니다.
    </pre>
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