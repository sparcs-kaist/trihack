var WhatLink = {
	initialize:function()
	{
		this.bluearrow = $("#bluearrow");
		this.whatisthetrihack = $("#whatthehack");
		this.registerHandles();
	},
	registerHandles:function()
	{
		this.bluearrow.bind('mouseenter', function() {
			//$("#bluearrow").css('background-color', '#FBD250');
			$("#whatthehack").css('background-color', '#FBD250');
		});
		this.bluearrow.bind('mouseleave', function() {
			//$("#bluearrow").css('background-color', '#FFFFFF');
			$("#whatthehack").css('background-color', '#FFFFFF');
		});
		this.whatisthetrihack.bind('mouseenter', function() {
			//$("#bluearrow").css('background-color', '#FBD250');
			$("#whatthehack").css('background-color', '#FBD250');
		});
		this.whatisthetrihack.bind('mouseleave', function() {
			//$("#bluearrow").css('background-color', '#FFFFFF');
			$("#whatthehack").css('background-color', '#FFFFFF');
		});
	}	
}

var LoadAnim = {
	initialize:function()
	{
		var main_logo = $("#main_logo");
		var main_content = $("#main_content");
		var bluearrow = $("#bluearrow");
		var whatisthetrihack = $("#whatthehack");
		var slogan_change = $("#slogan_change");
		var slogan_influence = $("#slogan_influence");
		var slogan_build = $("#slogan_build");

		main_logo.css('display', 'none');
		main_content.css('display', 'none');
		bluearrow.css('display', 'none');
		whatisthetrihack.css('display', 'none');
		slogan_change.css('display', 'none');
		slogan_influence.css('display', 'none');
		slogan_build.css('display', 'none');

		main_logo.fadeIn("slow", function() {
			main_content.fadeIn("slow", function() {
				bluearrow.fadeIn(300);
				whatisthetrihack.fadeIn(300, function() {
					slogan_change.fadeIn("fast", function() {
						slogan_influence.fadeIn("fast", function() {
							slogan_build.fadeIn("fast");
						});
					});
				});
			});
		});
		
	}
}
