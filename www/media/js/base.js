var MainNav = {
	initialize:function()
	{
		this.menu_register = $("#menu_register a");
		this.menu_login = $("#menu_login a");
		this.menu_logout = $("#menu_logout a");
		this.menu_about = $("#menu_about a");
		this.menu_forum = $("#menu_forum a");

		this.setNavImages();
		this.registerHandles();
	},
	registerHandles:function() 
	{
		if (this.loc != "register") {
			this.menu_register.bind('mouseenter', function() {
				$("#menu_register a").css('background', 'url(/media/image/register_registeruper.png) no-repeat top left');
			});
			this.menu_register.bind('mouseleave', function() {
				$("#menu_register a").css('background', 'url(/media/image/register.png) no-repeat top left');
			});
		}

		if (this.loc != "about") {
			this.menu_about.bind('mouseenter', function() {
				$("#menu_about a").css('background', 'url(/media/image/about_active.png) no-repeat top left');
			});
			this.menu_about.bind('mouseleave', function() {
				$("#menu_about a").css('background', 'url(/media/image/about.png) no-repeat top left');
			});
		}

		if (this.loc != "forum") {
			this.menu_forum.bind('mouseenter', function() {
				$("#menu_forum a").css('background', 'url(/media/image/forum_active.png) no-repeat top left');
			});
			this.menu_forum.bind('mouseleave', function() {
				$("#menu_forum a").css('background', 'url(/media/image/forum.png) no-repeat top left');
			});
		}

		if (this.loc != "login") {
			this.menu_login.bind('mouseenter', function() {
				$("#menu_login a").css('background', 'url(/media/image/login_active.png) no-repeat top left');
			});
			this.menu_login.bind('mouseleave', function() {
				$("#menu_login a").css('background', 'url(/media/image/login.png) no-repeat top left');
			});			
		}

		this.menu_logout.bind('mouseenter', function() {
			$("#menu_logout a").css('background', 'url(/media/image/logout_active.png) no-repeat top left');
		});
		this.menu_logout.bind('mouseleave', function() {
			$("#menu_logout a").css('background', 'url(/media/image/logout.png) no-repeat top left');
		});			
	},
	setNavImages:function()
	{
		if(location.href.indexOf("/register/") != -1){
			this.loc = "register";
			this.menu_register.css('background','url(/media/image/register_registeruper.png) no-repeat top left');
		}
		else if(location.href.indexOf("/about/") != -1){
			this.loc = "about";
			this.menu_about.css('background','url(/media/image/about_active.png) no-repeat top left');
		}
		else if(location.href.indexOf("/forum/") != -1){
			this.loc = "forum";
			this.menu_forum.css('background','url(/media/image/forum_active.png) no-repeat top left');
		}
		else if(location.href.indexOf("/login/") != -1){
			this.loc = "login";
			this.menu_login.css('background','url(/media/image/login_active.png) no-repeat top left');
		}
	}
}
