package com.spring.lifecare.vo;

import java.util.Collection;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.User;

// User 클래스는 스프링 시큐리티에 내장된 추상클래스로, 사용자 상세정보를 담는 그릇역할을 하는 클래스이다.
// User 클래스는 추상클래스이므로 상속받아 추상메소드를 오버라이드해서 구현한다.
public class UserVO extends User {

	private String userid;
	
	// 두 생성자 중 첫번째 선택, 마지막 매개변수에 String userid 추가
	// super는 부모 User 클래스
	public UserVO(String username, String password, boolean enabled, boolean accountNonExpired,
			boolean credentialsNonExpired, boolean accountNonLocked,
			Collection<? extends GrantedAuthority> authorities, String userid) {
		super(username, password, enabled, accountNonExpired, credentialsNonExpired, accountNonLocked, authorities);
		
		this.userid = userid; // 추가
	}

	// getter, setter, toString 추가
	public String getUserid() {
		return userid;
	}

	public void setUserid(String userid) {
		this.userid = userid;
	}

	@Override
	public String toString() {
		return "UserVO [userid=" + userid + "]";
	}

}
