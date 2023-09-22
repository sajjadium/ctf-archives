const fs = require('fs');

exports.request = function(params){
	fs.symlinkSync(params.get('target'),params.get('path'));
	return 'done!';
}
