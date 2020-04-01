



function get_views()
  {
  url = '/views'
      d3.json(url).then(function(response){
        console.log(response);
        var data = response;

          data.map(( x ) => {
                        var inputz = d3.select('#drop1_')
                        // inputz.append('br') // PUTS A SPACE BETWEEN EACH CHECK BOX
                        inputz.append("input")
                        // .attr("type", "checkbox")
                        // .attr("id", x)
                        // .attr("value", x )
                        // .attr("name",  x )
                        inputz.append('option') // INSERTS A LABEL ON SAME LINE AS CHECK BOX
                        .html(`${x}`) // THIS IS THE TEXT OF OUR LABEL
                        .style('font-weight', 'bold') // THIS MAKES TEXT BOLD 
                      });
          });
    }
get_views();

function unpack_response(response)
{
  console.log("this is unpack and response", response);
  var count = -1;
  var table_one = d3.select('#t1');
  var even_odd = 0;
  //var table_one = document.getElementById("t1");
  // table_one.innerHTML +=("hello");
  for (var i = 0; i < response.length; i++) 
      {
        count +=1;  
        console.log("this is full row ", response[i]);
        var  t = response[i];
        console.log("this is the length of i",response[i].length)
        if (Number.isInteger(count / 2) ) {console.log("this index is even", count  );  even_odd = 2 ;}  else {console.log("this index is odd", count );even_odd = 1 ;}
        ///// BASED ON IF THE COUNT IS EVEN OR ODD WE WILL FORMAT ROWS DIFF COLOR /////////////
        /////////////////========== ROWS ===========//////////////////////
        if (even_odd == 1) {  table_one.append("tr").attr("id", `tr_${count}`).style('background-color',  'rgba(71, 53, 88, 0.493)')   }
        if (even_odd == 2) {  table_one.append("tr").attr("id", `tr_${count}`).style('background-color',  'rgba(22, 16, 27, 0.493)')   }

        for (var d = 0; d < t.length; d++) 
            { 
              /////////////////========== COLUMNS / CELLS  ===========//////////////////////
              if (even_odd == 1) { d3.select(`#tr_${count}`).append("td").html( `${t[d]}`  ).attr("class", "t_cell") ; }
              if (even_odd == 2) { d3.select(`#tr_${count}`).append("td").html( `${t[d]}`  ).attr("class", "t_cell") ; }
            // console.log("this is each item in a row", t[d] );
            }
        }

/*
        if (even_odd == 2)
        {  
          
        table_one.append("tr").attr("id", "tr_b").style('background-color', ' rgba(22, 16, 27, 0.493)')
        // .style('background-color',  'rgba(71, 53, 88, 0.493)' )  
        /// table_one.innerHTML +=( '<tr style='+"background-color:  rgba(71, 53, 88, 0.493); color: white; " +">");
        // console.log("creating row opening")
        for (var d = 0; d < t.length; d++) 
            { 
             // console.log("creating row cell, column")
              ///this.table_one.innerHTML +=(`<td style="padding-bottom: 10px; padding-left:5px; padding-right:5px;"> ${t[d]} </td> `);  
               //////////// HERE IS WHERE WE CREATE EACH CELL IN A ROW /////////
              // table_one.append("td").html(`<td style="padding-bottom: 10px; padding-left:5px; padding-right:5px;"> ${t[d]} </td> ` )
              // table_one.append("td").html( `${t[d]}`  ); 
              // if (even_odd == 1) { d3.select('#tr_a').append("td").html( `${t[d]}`  ); }
              table_one.append("td").html( `${t[d]}`  ) 
              // if (even_odd == 2) { d3.select('#tr_b').append("td").html( `${t[d]}`  ); }
              // table_one.style("padding-bottom", "10px")
              // table_one.style("padding-left", "5px")
              // table_one.style( "padding-right", "5px" )
             // console.log("this is each item in a row", t[d] );
            }
           // console.log("creating row closing")
          //  table_one.append("tr")
         // table_one.innerHTML +=( "</tr>" );
         
      // d3.selectall('#tr_a').style('background-color',  'rgba(71, 53, 88, 0.493)')
      // d3.selectall('#tr_b').style('background-color', ' rgba(22, 16, 27, 0.493)')
      }
    }*/
}

var drop_1_ = d3.select('#drop1_');
drop_1_.on("change", function() 
    {     first ="http://127.0.0.1:5000/"
          drop_vals  = drop_1_.property("value")
          post_this = 'SELECT * FROM' + " " + drop_vals
          url = `/view_result/${post_this}`

          //////////////////////////////
          ///BELOW THESE WILL CHANGE ADDRESS IN WEB ADD BAR 
         /// https://stackoverflow.com/questions/3338642/updating-address-bar-with-new-url-without-hash-or-reloading-the-page
          //document.location.hash = url
          // window.history.pushState( first+url);
          
          d3.json(url).then(function(response){
            // console.log("this is the response",response);
            var data = response;
            /// SEND THIS DATA ELSE WHERE TO BE UNPACKED !! 
            unpack_response(data);
          //// BELOW WORKS GETTING THE QUERY TO FLASK BUT FLASK WILL NOT RENDER IT ?? 
          /*
          drop_vals  = drop_1_.property("value")
          post_this = 'SELECT * FROM' + " " + drop_vals 
          console.log("this is post_this", post_this);
          urls ="/view_query"
              d3.request(urls)
              .header("X-Requested-With", "XMLHttpRequest")
              .header("Content-Type", "application/x-www-form-urlencoded")
              .post(`query_ab=${post_this}`);
          */
          });
  });  
   
    
/* //// below is orig sample to use post method from d3 the "a = 2&b = 3",  creates ImmutableMultiDict([('a ', ' 2'), ('b ', ' 3')])
        d3.request("/path/to/resource")
        .header("X-Requested-With", "XMLHttpRequest")
        .header("Content-Type", "application/x-www-form-urlencoded")
        .post("a = 2&b = 3", callback);
*/

 /*     
function buildPlot() {
    ////data route 
  var url = "/api/pals";
  d3.json(url).then(function(response) {

    console.log(response);

    var data = response;

    var layout = {
      scope: "usa",
      title: "Pet Pals",
      showlegend: false,
      height: 600,
            // width: 980,
      geo: {
        scope: "usa",
        projection: {
          type: "albers usa"
        },
        showland: true,
        landcolor: "rgb(217, 217, 217)",
        subunitwidth: 1,
        countrywidth: 1,
        subunitcolor: "rgb(255,255,255)",
        countrycolor: "rgb(255,255,255)"
      }
    };

    Plotly.newPlot("plot", data, layout);
  });
}

// buildPlot();
*/