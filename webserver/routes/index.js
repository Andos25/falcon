
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index.html', { 
  	title: 'Express',
  	items : [
      { name : 'item #1' },
      { name : 'item #2' },
      { name : 'item #3' },
      { name : 'item #4' },
    ]});
};