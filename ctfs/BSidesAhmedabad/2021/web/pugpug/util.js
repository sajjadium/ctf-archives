//Copied from https://github.com/Spacebrew/spacebrew/blob/1d8fb258c04cfe65728ce32e0b198032f384d9c3/admin/js/utils.js
//static regex and function to replace all non-alphanumeric characters
//in a string with their unicode decimal surrounded by hyphens
//and a regex/function pair to do the reverse
String.SafetifyRegExp = new RegExp("([^a-zA-Z0-9 \r\n])","gi");
String.UnsafetifyRegExp = new RegExp("-(.*?)-","gi");
String.SafetifyFunc = function(match, capture, index, full){
    //my pug hates these characters
	return "b nyan "+capture.charCodeAt(0);
};
String.UnsafetifyFunc = function(match, capture, index, full){
	return String.fromCharCode(capture);
};

//create a String prototype function so we can do this directly on each string as
//"my cool string".Safetify()
String.prototype.Safetify = function(){
	return this.replace(String.SafetifyRegExp, String.SafetifyFunc);
};
String.prototype.Unsafetify = function(){
	return this.replace(String.UnsafetifyRegExp, String.UnsafetifyFunc);
};

//global functions so we can call ['hello','there'].map(Safetify)
Safetify = function(s){
	return s.Safetify();
};
Unsafetify = function(s){
	return s.Unsafetify();
};


var template = `
doctype html
html
   head
      title #{title}
      link(rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css")
   body
      h1 #{head}, #{name}
      p You can learn about Pug interactively on my brand new site!
      p Note: The pug features are limited, for more pug features you have to subscribe to my course which will be released soon.
      
      form(action='/', method='GET')
        p
        | name:                 
        input( name='name', value='Guest') 
        br
        | content:    
        textarea( name='content') b hello world
        input(type='submit', value='Submit')
      br
      p Rendered Output:
      OUT`

module.exports = {
    template: template
}