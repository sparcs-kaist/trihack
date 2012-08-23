var MainLink = {
	initialize: function()
	{
		this.backtomain = $("#backtomain"); 
		this.registerHandles();
	},
	registerHandles: function()
	{
		this.backtomain.bind('mouseenter', function() {
			$("#backtomain").css('background-color', '#FBD250');
		});
		this.backtomain.bind('mouseleave', function() {
			$("#backtomain").css('background-color', '#FFFFFF');
		});
	}
}
