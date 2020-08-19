@Controller
pubilc class UserController{

  //로그인 페이지로 이동
  @RequestMapping("/user/login.do")
  public String login(){
	logger.info("경로:login");

	return "user/login";
  }

  //회원 추가 페이지로 이동
  @RequestMapping("/user/insert.do")
  public String insert(){
	logger.info("경로:insert");

	return "user/insert";
  }

  //회원 수정 페이지로 이동
  @RequestMapping("/user/update.do")
  public String update(){
	logger.info("경로:update");

	return "user/update";
  } 

<<<<<<< HEAD
  //master 브랜치에 주석추가
  //회원 탈퇴시 세션 삭제
=======
>>>>>>> develop

  //회원 삭제 페이지로 이동
  @RequestMapping(/user/delete.do")
	logger.info("경로:delete");

	return "user/delete";
}