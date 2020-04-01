


image_selection = d3.selectAll("#b2")
place_img_here = d3.select("#img2")
submit_pic_butt = d3.select('#b3')


var restart_but = d3.select('#resets')
restart_but.on("click", function()
  {
  console.log("restart button pressed")
  });


function uploaded_file(image_name)
{
    urlz = `/show/${image_name}`
    urls = `/uploads/${image_name}`/// API ADDRESS USE COUNTRY NAME AS QUERY 
    console.log('the image name is' , image_name)
}


submit_pic_butt.on("click", function()///THIS RUNS OUR PROGRESS BAR ONCE PHOTO HAS BEEN UPLOADED
  {
    d3.select("#progressBarB").style("opacity", "1") 
  });


///=========================================================================================
////      THIS IS THE API CALL -  INITITATED BY THE SUBMIT BUTTON UNDER - CONFIRM INGREDIENTS 
///==========================================================================================
//////////////////////// AF: Search for recipes ///////////////////////
function populateRecipes(item_list) {

  console.log('The Java API function is being run with this list!!', item_list);

  var url = `/recipes/${item_list}`/// API ADDRESS USE COUNTRY NAME AS QUERY 
                
  var recipeContainer = d3.select("#recipes");
  recipeContainer.html(" ")

  if (item_list !=[])
  {
      d3.json(url).then(function(response) {

        var info = response ;
        console.log("The Json Data Response is :", response);
    
        for (var i = 0; i < info.length; i++) {
          // var recipeContainer = d3.select("#recipes");
          var recipe = info[i]["recipe"];
          var calories = info[i]["calories"];
          var url = info[i]["url"];
          var imageUrl = info[i]["image_url"];

          console.log(recipe);
          console.log(calories);
          console.log(url);
          console.log(imageUrl);

          // d3.select("recipeContainer").html(" ")
        
          recipeContainer.append("div").attr("class","col-md-4").html(
            `<br><br><div class="card text-center" style="width: 18rem; height: 32rem;">
                <img class="card-img-top" src="${imageUrl}" alt="${recipe}">
                <div class="card-body">
                  <h5 class="card-title">${recipe}</h5>
                  <p class="card-text">Calories: ${Math.round(calories)}</p>
                  <a href="${url}" target="_blank" class="btn btn-primary">Let's Make It!</a>
                </div>
              </div>`)

        }
        d3.select("#progressBarA").style("opacity", "0")
        window.scrollTo(0, 2100) 
      });
    }   
};



///=========================================================================================
////      THIS GRABS THE BOXES THAT WERE CHECKED, PUTS INTO LIST AND PUSHES TO API FUNC
///===========================================================================================

var ingres_for_api = []
//==============VER. 3===========================
function assess_checkboxes()
{
  var ingres_for_api = []
  var final_ing_api = []
    d3.selectAll("input[type=checkbox]").each(function(_, i) {
  
      // console.log("check boxes are" + (i + 1) + " is: " + d3.select(this).property("checked") + "__",  d3.select(this).property("name") )
    var t = (d3.select(this).property("checked") ) 
    // ingres_for_api.push( t )
    // console.log("check boxes are", d3.select(this).property("name") )
    var u =( d3.select(this).property("name") )
    // ingres_for_api.push( u )
    combo = ([t,u]) 
    ingres_for_api.push(combo)
    // console.log('print this is the ingres_for_api list' , ingres_for_api);

    });

 for (var j = 0; j < ingres_for_api.length; j+=1) 
    {
      // console.log ( 'j for loop print' ,ingres_for_api[j][1] ) ;
        if ( (ingres_for_api[j][0]) == true )
            {
              // console.log('this is type of data we are putting into list for api', 
              item_ = ingres_for_api[j][1];
              text_item = ""
              text_item =item_
              final_ing_api.push(text_item );
              // final_ing_api.push(  ingres_for_api[j][1]  );
            }  
    }

  // console.log('print this is the ingres_for_api list after for loop' , ingres_for_api);
  console.log('print this is the final_ing_api list after for loop ' ,  final_ing_api);
  
  return populateRecipes(final_ing_api); 

}



///=========================================================================================
////    WHEN USER CLICKS BUTTON UNDER CONFIRM INGREDIENTS --- IT RUNS FUNC ABOVE TO BUILD LIST 
///===========================================================================================  

var fake_submit_button = d3.select('#submit1')
fake_submit_button.on("click", function()
  {
  console.log("the fake submit button has been pressed")
  console.log('print this is the ingres_for_api list from fake submit' , ingres_for_api);
  d3.select("#progressBarA").style("opacity", "1") 
  
  return assess_checkboxes()
  });



///=========================================================================================
////      THIS BUILDS THE CHECK BOX CONFIRM INGREDIENT HTML 
///===========================================================================================
  function confirmed_ingres(ingres_list)
    {
      // var confirm_ingred = ['bogus ingred', 'hotdog', 'bun', 'pickles'];
      console.log('ingres_list is', ingres_list);
      console.log('lenth of ingres_list is', ingres_list.length);
      console.log('lenth of ingres_list is', ingres_list[2]);
    //   console.log('confirmed_ingred is', confirmed_ingres);

     ingres_list.map(( x ) => {
    // return ingres_list.map( function ( x )  {
                var inputz = d3.select('#form1')
                inputz.append('br') // PUTS A SPACE BETWEEN EACH CHECK BOX
                
                inputz.append("input")
                .attr("type", "checkbox")
                .attr("id", x)
                .attr("value", x )
                .attr("name",  x )

                inputz.append('label') // INSERTS A LABEL ON SAME LINE AS CHECK BOX
                .html(`...${x}`) // THIS IS THE TEXT OF OUR LABEL
                .style('font-weight', 'bold') // THIS MAKES TEXT BOLD 
              }
            );

        d3.select('#form1')  // GIVE US ONE LINE BREAL
          .append('br')
      } 
 


///=========================================================================================
////      THIS FINDS THE LIST OF ITEMS FROM THE MODEL - THAT WAS PUSHED FROM FLASK INTO HIDDEN HTML IN INDEX.HTML
///===========================================================================================
api_trig_val = d3.select("#f2").select("value")
api_trig_val = d3.select("#f2")
  .attr("value")
  console.log(" the api trigger value is : ", api_trig_val);

  var ingrez_list= d3.select("#f4")
  .attr("value")
  
  console.log ("the ingrez_list is :", ingrez_list);

  if ( ingrez_list.length >=1 )
      {
      console.log("the hidden list is : ", ingrez_list);
      list_of_ingres =ingrez_list.split(',')

       // function scrollWin() 
      // {
      //   window.scrollTo(0, 2000);
      // }
      // scrollWin() ;
      window.scrollTo(0, 900);
 


      confirmed_ingres(list_of_ingres) ;
      }






///=========================================================================================
///=========================================================================================
///=========================================================================================
/// BONE YARD 
///=========================================================================================

      // image_selection.on("change", function()
      // // image_selection.on("click", function()
      // {
      // //    var image_name = image_selection.attr("DOMString")
      // //    var image_name = image_selection.attr(".html")
      //    var image = image_selection.selectAll()
      //    console.log("the image name is", image._parents[0].files[0].name );
      
      //    image_name = image._parents[0].files[0].name 
      //   //  url = 'http://127.0.0.1:5000/show/'+image_name
      //     //  url = '{{url_for(/show/'+image_name+')}}'
      //      url = 'url_for(/show/'+image_name
      
      //     //  url = '..images/'+image_name
      //   //  url = 'http://www.cnn.com'
      
      //    console.log('the url is:', url);
      
      //    d3.select("#b3")
      //    //  .append('href=')
      //      //  b.select("href")
      //      .attr('href', url)
      //      .attr('action', url)
      
      //   // get_image( image_name);
      // });
      






      // function list_builder2()
      // {
      //     var ingreds = ['bogus ingred', 'hotdog', 'bun', 'pickles'];
      //     ingreds.map(( x ) =>
      //           {
      //           var t= d3.select('.article')
      //             t.append('li').html(x)
      //             // .html(x)
      //           }
      //       );
      // }

// list_builder2();


// ================================
// TIMER  
// ================================
// timer = 0;
// var timer = d3.timer(function(duration) {
//   // console.log(duration);
//   if (duration > 10000) timer.stop();
//    } , 1);



//==============VER. 2===========================
// function assess_checkboxes()
// {
//   var ingres_for_api = []
// d3.selectAll("input[type=checkbox]").on("change", function() {
//         d3.selectAll("input[type=checkbox]").each(function(_, i) {
  
//       // console.log("check boxes are" + (i + 1) + " is: " + d3.select(this).property("checked") + "__",  d3.select(this).property("name") )
//     var t = (d3.select(this).property("checked") ) 
//     // ingres_for_api.push( t )
//     console.log("check boxes are", d3.select(this).property("name") )
//     var u =( d3.select(this).property("name") )
//     // ingres_for_api.push( u )
//     combo = ([t,u]) 
//     ingres_for_api.push(combo)
//     console.log('print this is the ingres_for_api list' , ingres_for_api);

//     });

//   });
//   console.log('print this is the ingres_for_api list' , ingres_for_api);
// }

//==============VER. 1===========================
//   function assess_checkboxes()
// {
//   var ingres_for_api = []

// d3.selectAll("input[type=checkbox]").on("click", function() {
    
//     d3.selectAll("input[type=checkbox]").each(function(_, i) {
//       console.log("check boxes are" + (i + 1) + " is: " + d3.select(this).property("checked") + "__",
//       d3.select(this).property("name") )
//     });
    
//   });

//   console.log('print this is the ingres_for_api list' , ingres_for_api);
// }






  // all_check_boxes = d3.selectAll('#form1').selectAll("input").selectAll("id")
  // all_check_boxes=d3.selectAll("input[type=checkbox]").property("checked", true);
//  var all_check_ = d3.selectAll('#form1').selectAll("input").selectAll("id").property("checked", true)

//  var all_check_s = d3.selectAll('#form1').selectAll("input").selectAll("id")  
//  var cow = d3.selectAll('#cow')
//  console.log( "this is cow" , cow._parents);
// //  all_check_s = d3.select('#form1').selectAll("input").property("id")

//  for (var j = 0; j < 4; j+=1) 
//  {  
//   //  console.log("all check box names are", all_check_._parents[j].input);   
//  console.log("all check box names are", d3.selectAll('#form1').selectAll("input").attr("value"));
//  console.log("all check box names are", d3.selectAll('#form1').selectAll("input").selectAll("id").property("checked", true) );

//  }
//  console.log("one all check box name is", all_check_s._parents[0], all_check_s._parents[1], all_check_s._parents[2]); 
//  console.log("one all check box name is", all_check_s._parents[0]); 
//  console.log("the image name is", image._parents[0].files[0].name );
  // all_check_s = d3.select('#form1').selectAll("input").attr("value")


  // all_check_s.map((x)=>
  // {
  //   d3.selectAll("input")
  //   .attr("id")
  // }  );
  // .attr("checked") 
        // {
        //  console.log('One check box is checked')

        // }


    // .attr(value)
    // console.log("all checked boxes are", all_check_boxes)
  //    console.log("check true or false", all_check_)
  //    console.log("all check box id", all_check_s)
  // console.log('this is the listen button function')
  // var submit_button2_ =d3.select('#submit1')
  // // confirmed_ingres() ;
  // submit_button2_.on("click", function(){
  //   console.log('this is the listen button function---The submit button was pressed')
  //   console.log('the 2nd submit button is', submit_button2_)
  // });
  // 
