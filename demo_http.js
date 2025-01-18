var http = require('http');
var formidable = require('formidable');
var fs = require('fs');

http.createServer(function(req,res){
    if(req.url == '/fileupload'){
        var form = new formidable.IncomingForm();
        form.parse(req, function(err,fields,files){
            var oldPath = files.filetoupload.filepath;
            var newPath = 'C:/Users/kesha/Projects/YouTubeUploadTrendsApp/' + files.filetoupload.originalFilename;
            fs.rename(oldPath,newPath,function (err){
                if (err){
                    throw err;
                }
                res.write("file successfully moved");
                res.end();
            });
        });
    }else{
        res.writeHead(200,{'content-type' : 'text/html'});
        res.write('<form action="fileupload" method="post" enctype="multipart/form-data">');
        res.write('<input type="file" name="filetoupload"><br>');
        res.write('<input type="submit">');
        res.write('</form>');
        return res.end();
    }

    
}).listen(8080);