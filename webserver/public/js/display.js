//
// halfviz.js
//
// instantiates all the helper classes, sets up the particle system + renderer
// and maintains the canvas/editor splitview
//
(function(){
  
  trace = arbor.etc.trace
  objmerge = arbor.etc.objmerge
  objcopy = arbor.etc.objcopy

  //parse the input
  var parse = Parseur().parse

  //input the element pass in
  var DependGraph = function(elt){
    //get the object of element
    var dom = $(elt)
    var _btn = dom.find('#btn')

    sys = arbor.ParticleSystem(2600,512,0.5)
    sys.renderer = Renderer("#view")
    sys.screenPadding(20)


    var that = {

      init:function(){

        //$(window).resize(that.resize)
        //that.resize() 
        _btn.bind('click',that.btnclick)

        return that
      },//end of init

      btnclick:function(){
       that.getData()
      },

      //resize the 
      resize:function(){
        system.renderer.redraw()
      },

      getData:function(){
        $.getJSON('gettopo/',
        function(doc){
         //set the system parameters is there is
         if (doc.sys){
            sys.parameters(doc.sys)
         }

         //parse the input network
         var network = parse(doc.src)

         //set the network information
         $.each(network.nodes, function(nname, ndata){
            if (ndata.label===undefined) ndata.label = nname
         })

         //merge the network
         sys.merge(network)
         that.resize()

        })//end of get json

      }//end of get data

    }//end of that

    
    return that.init()
  }

$(document).ready(function(){
    //alert("come here")
    var mcp = DependGraph("#halfviz")    
})

})()