var MainNav = {
	initialize:function()
	{
		this.menu_register = $("#menu_register a");
		this.menu_about = $("#menu_about a");
		this.menu_forum = $("#menu_forum a");

		this.setNavImages();
		this.registerHandles();
	},
	registerHandles:function() 
	{
		if (this.loc != "register") {
			this.menu_register.bind('mouseenter', function() {
				$("#menu_register a").css('background', 'url(/media/image/register_registeruper.png)');
			});
			this.menu_register.bind('mouseleave', function() {
				$("#menu_register a").css('background', 'url(/media/image/register.png)');
			});
		}

		if (this.loc != "about") {
			this.menu_about.bind('mouseenter', function() {
				$("#menu_about a").css('background', 'url(/media/image/about_active.png)');
			});
			this.menu_about.bind('mouseleave', function() {
				$("#menu_about a").css('background', 'url(/media/image/about.png)');
			});
		}

		if (this.loc != "forum") {
			this.menu_forum.bind('mouseenter', function() {
				$("#menu_forum a").css('background', 'url(/media/image/forum_active.png)');
			});
			this.menu_forum.bind('mouseleave', function() {
				$("#menu_forum a").css('background', 'url(/media/image/forum.png)');
			});
		}
	},
	setNavImages:function()
	{
		if(location.href.indexOf("/register/") != -1){
			this.loc = "register";
			this.menu_register.css('background','url(/media/image/register_registeruper.png)');				
		}
		else if(location.href.indexOf("/about/") != -1){
			this.loc = "about";
			this.menu_about.css('background','url(/media/image/about_active.png)');
		}
		else if(location.href.indexOf("/forum/") != -1){
			this.loc = "forum";
			this.menu_forum.css('background','url(/media/image/forum_active.png)');
		}
	}
}
