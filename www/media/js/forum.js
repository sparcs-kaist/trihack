var CommentList = {
	initialize:function() 
	{
		this.comment_delete = $(".comment_delete");
		this.registerHandles();
	},
	registerHandles:function()
	{
		this.comment_delete.bind('click', $proxyWithArgs());
	},
	deleteComment:function()
	{
	},
	voteComment:function()
	{
	}
}
