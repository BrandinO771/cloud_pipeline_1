///////////////////////////////////////////////////////////////////////////////////////////////////
/// COPYRIGHT BRANDON STEINKE , PATRICK HENNESSY 2020
///////////////////////////////////////////////////////////////////////////////////////////////////
////-----VARIABLES  ---------------////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
var geojson;
var lat = 20;
var long = 10;
var mymap = L.map('map').setView([lat, long], 2);
var database_info = "";
var display_this = 0;//temp var to determine map color
var map_color_data ="";
var db_data =[]; 
// var u = 0;

 L.tileLayer(`https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=${API_KEY}`, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 8,
    minZoom: 2,
    id: "mapbox.light",
}).addTo(mymap);

/////////////////////////////////////////////////////////////
///--- PREVENTS USER FROM SCROLLING OFF MAP ----------
///////////////////////////////////////////////////////////
var southWest = L.latLng(-89.98155760646617, -180),
northEast = L.latLng(89.99346179538875, 180);
var bounds = L.latLngBounds(southWest, northEast);

mymap.setMaxBounds(bounds);
mymap.on('drag', function() {
mymap.panInsideBounds(bounds, { animate: false });
});
/////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////////////////////////
////---- BUILD MAP WITH GEOJASON ---------------///////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
function draw_map(db_data)  /// THIS FUNCTION WRAPS MOST OF THIS CODE 
        {

          // console.log("this is db data", db_data);
          if ( display_this < 11)
              {
              geojson = L.geoJson(worldData, {
                                              style: style,
                                              onEachFeature: onEachFeature,
                                              clickable: true
                                              }).addTo(mymap);
              } 

/////////////////////////////////////////////////////////////////////////////////////////////////
////------- LEGEND ------------------////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////
  ///--LEGEND POSITION:
  var legend = L.control({
                          position: 'bottomleft'
               
                        });

  ///--LEGEND CREATION:
  legend.onAdd = function (map) 
      {
        var colorz =[];
        if (  display_this  == 0 )      { colorz  = [ 15000000, 10000000, 5000000,  2000000,   1000000,  500000,  200000,  150000] ;}
        if (  display_this  == 1 )      { colorz  = [1000,300,250,200,150,100,75,50,25,10,0.1] ;}
        if (  display_this  == 2 )      { colorz  = [160,140,120,100,80,60,40,20,10,1] ;}
        if (  display_this  == 3 || display_this == 4|| display_this == 5)  {  colorz = [90,80,70,60,50,40,20,10,0] ;}
        if (  display_this  == 7 )      { colorz  = [200,180,160,140,120,100,80,60,40,20,10,1] ;}
        if (  display_this  == 6  || display_this== 8 || display_this == 9 )  {  colorz =  [55,50,45,40,35,30,25,10,5,1] ;}
        if (  display_this  == 10 )     { colorz  = [25,20,15,10,5,2,0.1] ;}
 
          var div = L.DomUtil.create('div', 'info legend'),
              colors = colorz,
              labels = [];
     
          if ( display_this == 0 ) { div.innerHTML += '<font id="f1">  GDP in Millions USD  </font><br>';}
          if ( display_this == 1 ) { div.innerHTML += '<font id="f1">  Population in the Millions           </font><br>';}
          if ( display_this == 2 ) { div.innerHTML += '<font id="f1">  World Rank                           </font>'+ '<br><font id="f2">   (Lower is Better)   </font><br>';}
          if ( display_this == 3 ) { div.innerHTML += '<font id="f1">  Government Integrity                 </font>'+ '<br><font id="f2">   (Higher is Better)  </font><br>';}
          if ( display_this == 4 ) { div.innerHTML += '<font id="f1">  Judicial Effectiveness               </font>'+ '<br><font id="f2">   (Higher is Better)  </font><br>';}
          if ( display_this == 5 ) { div.innerHTML += '<font id="f1">  Fiscal Health                        </font>'+ '<br><font id="f2">   (Higher is Better)   </font><br>';}
          if ( display_this == 6 ) { div.innerHTML += '<font id="f1">  Inflation                            </font><br>';}
          if ( display_this == 7 ) { div.innerHTML += '<font id="f1">  Public Debt of GDP                   </font><br>';}
          if ( display_this == 8 ) { div.innerHTML += '<font id="f1">  Avg Income Tax Rate                  </font><br>';}
          if ( display_this == 9 ) { div.innerHTML += '<font id="f1">  Avg Corporate Tax Rate               </font><br>';}
          if ( display_this == 10 ){ div.innerHTML += '<font id="f1">  Unemployement                        </font><br>';}

          // /FOR LOOP CREATE LEGEND -- Loops through GDP data and grabs colors for each range and puts them in the legend’s key
          for (var i = 0; i < colors.length; i++) 
                  {
                      if ( i >= 1)
                        {
                          div.innerHTML +=
                              '<i  style="background:' + getColor(colors[i] + 1) + '"></i>' +
                              '<font id="leg_nums">'+ colors[i] +    (colors[i - 1] ? '&ndash;' + colors[i - 1] +'</font>' + '<br>' : '-');
                        }
                      if ( i <  1 )
                        {
                          div.innerHTML +=
                              '<i  style="background:' + getColor(colors[i] + 1) + '"></i>' +
                              '<font id="leg_nums">'+ colors[i] +    (colors[i - 1] ? '&ndash;' + colors[i ] +'</font>' + '<br>' : '+' +'<br>');
                        }        
                  }
          return div;
      };
      legend.addTo(mymap);

///////////////////////////////////////////////////////////////////////////////////////////////////
////--- INFORMATION BOX --------///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
  ///--ON HOVER-----DISPLAY COUNTRY INFO IN INFORMATION BOX
  var displayInfo = L.control();

  displayInfo.onAdd = function (map) /// create a div with a class "info"
      {
          this._div = L.DomUtil.create('div', 'info');
          this._div.style =('visibility:hidden ;');
          // this.update();
          return this._div;
      };


  displayInfo.clear= function clear_displayInfo_box()///CLEAR CONTENT
      {
        this._div.innerHTML =("");    
      };

  ///--POPULATE THE INFO BOX WITH HTML:
  displayInfo.update = function (props) /// Passes properties of hovered upon country and displays 
      { 
        this._div.style =('visibility:visible ;');
        this._div.innerHTML =  (props ?  `<img id="imgr" src='static/js/Flags/${props.iso_a2}.png'`  + '>'+ '<br>' +   '<br>' +   
        '<font id="f1"> Country: ' + props.name + '</font>' + '<br>'+'<b>' + 'GDP in Trillions of USD: ' + '</b>' + props.gdp_md_est / 1000000 + '<br />' +
        '<b>' + ' GDP in Billions of USD: ' + '</b>' + props.gdp_md_est / 1000 + '<br />' +
        '<b>' + 'Economic Status: ' + '</b>' + props.economy + '<br />' +
        '<b>' + 'Population: ' + '</b>' + props.pop_est / 1000000 + ' million people' :'' );
      }
        displayInfo.addTo(mymap);

/////////////////////////////////////////////////////////////////////////
///   MY INFO BOX  INFO FROM FLASK 
/////////////////////////////////////////////////////////////////////////
      var info_box =  L.control();
      info_box.onAdd = function (map) /// create a div with a class "info"
          {
              this._divi = L.DomUtil.create('table', 'info2');
              this._divi.style =('visibility:hidden ;');
              // this.update();
              return this._divi;
          };

      info_box.clear= function clear_info_box()///CLEAR CONTENT
          {
            this._divi.innerHTML =("");    
          };

    var t = 0;
    var b = 0;

      info_box.update = function (key,value) //UNPACK JSON
              {
                var category ="";
                var step = 0;
                if ( key == "A. Country" )                                  {  step = 1; }
                if ( display_this == 1 && key == "D. Population Millions")  {  step = 1; }
                if ( display_this == 2 && key == "B. World Rank")           {  step = 1; }
                if ( display_this == 3 && key == "K. Govt Integrity")       {  step = 1; }
                if ( display_this == 4 && key == "L. Judical Efficieny")    {  step = 1; }
                if ( display_this == 5 && key == "E. Fiscal Health")        {  step = 1; }
                if ( display_this == 6 && key == "G. Inflation")            {  step = 1; }
                if ( display_this == 7 && key == "H. Public Debt of GDP")   {  step = 1; }
                if ( display_this == 8 && key == "R. Income Tax Rate")      {  step = 1; }
                if ( display_this == 9 && key == "S. Corporate Tax Rate")   {  step = 1; }
                if ( display_this == 10 && key == "F. Unemployment")        {  step = 1; }

                  this._divi.style =('visibility:visible ;');
                ////  BELOW WE ASSIGN A ID TO SO CSS WILL MAKE FONT YELLOW FOR COUNTRY NAME AND LIST ITEM THAT MATCHES CURRENT CATEGORY  
                if ( step == 1 ) {this._divi.innerHTML += ('<tr id="row2"><td>' + key.slice(3,100) + '</td><td>'+  value + '</td></tr>');}
                if ( step == 0 && key != undefined )   {  this._divi.innerHTML +=   ('<tr id="row1"><td>' + key.slice(3)+ '</td><td>'+  value + '</td></tr>');  }
                };  
             
              info_box.addTo(mymap);
/////////////////////////////////////////////////////////////////////////
///  END MY INFO BOX 
////////////////////////////////////////////////////////////////////////  


/////////////////////////////////////////////////////////////////////////
///   INFO BOX 2
////////////////////////////////////////////////////////////////////////   
///////// THIS IS HOW WE FIND THE OLD BOX TO DESTROY ON NEW MAP BUILD /////////////
var all_boxes_3_ =  d3.selectAll(".info3")

/// HERE WE DELETE THE OLD CONTAINER FULL OF MANY ROWS SO WE MAY CREATE A NEW BLANK ONE TO BE FILLED LATER 
if ( all_boxes_3_ != undefined &&  (all_boxes_3_._groups[0]).length > 1 )
      {
      d3.select(".info3").remove()
      }

var info_box_two     = L.control({
                            position: 'topleft'
                            });

info_box_two.onAdd = function (map) /// create a div with a class "info"
    {
      
          this._divi_ = L.DomUtil.create('table', 'info3' );
          this._divi_.style =('visibility:hidden ;');//WE CREATE IT BUT IT REMAINS HIDDEN UNTIL WE UPDATED IT LATER WITH CONTENT
        // this.update();
         return this._divi_;
    };


info_box_two.clear= function clear_info_box()///CLEAR CONTENT
    {
      this._divi_.innerHTML =("clear function called");    
    };

info_box_two.update = function(dics) //UNPACK JSON
        {
          iter = 0;
          var title = "";
          if ( display_this == 0 ) { title =  "GDP Millions"    ;}
          if ( display_this == 1 ) { title =  "Population"      ;}        
          if ( display_this == 2 ) { title =  "World Rank"      ;}                          
          if ( display_this == 3 ) { title =  "Gov Integrity"   ;}              
          if ( display_this == 4 ) { title =  "Judicial Effect" ;}          
          if ( display_this == 5 ) { title =  "Fiscal Health"   ;}                     
          if ( display_this == 6 ) { title =  "Inflation"       ;}                            
          if ( display_this == 7 ) { title =  "Public Debt GDP" ;}                   
          if ( display_this == 8 ) { title =  "Avg Income Tax"  ;}               
          if ( display_this == 9 ) { title =  "Avg Corp Tax"    ;}             
          if ( display_this == 10 ){ title =  "Unemploy"        ;}                      

          this._divi_.style =('visibility:visible ;');/// NOW WE UPDATE THIS DIV AND MAKE IT VISIBLE 
          this._divi_.innerHTML =('<tr><td>'  +'<font id="f1">' +'Top 10: ' + ' ' + ' '  + `${title}` + '<tr><td>');   
          this._divi_.innerHTML +=('<tr><td>'  +'<font id="f2">' + 'Country'  + '</td><td>'+   '<font id="f2">'+ 'Value' +'<tr><td>');//+
         if (dics != undefined && this._divi_ != undefined )
              { 
                while(iter < 10 )//HERE WE BUILD OUR TABLE FOR POPUP
                  {
                  this._divi_.innerHTML += ('<tr><td>' + `${dics[iter].name}`  + '</td><td>'+   `${dics[iter].value}` + '</td></tr>'); 
                  iter+=1;
                  }
              }
        }

      info_box_two.addTo(mymap); 

        function top_tens(query)
        {
           urls = `/top_ten/${query}`/// API ADDRESS USE COUNTRY NAME AS QUERY 
          d3.json(urls).then(function(response) {//JSON RESPONSE
                      var infos = response ;
                      //////////////////////////////////////////////////////
                      //// DO WE NEED TO SORT THIS DIFFERENTLY ? UNLOCK BELOW IF SO
                     // infos.sort(function(a,b){
                        //return a.value - b.value; // if this is a - b then is asc
                      //  return a.value + b.value; // if this is a +  b then is desc
                       // });
                     ///////////////////////////////////////////////////////   
                  if(infos != undefined){ info_box_two.update(infos); }//PASS JASON TO INFO_BOX.UPDATE FUNC    
                 }); 
        }
/////////////////////////////////////////////////////////////////////////
///  END MY INFO BOX 2
////////////////////////////////////////////////////////////////////////  

///////////////////////////////////////////////////////////////////////////////////////////////////
////--- MAP STYLING ------------///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

function highlight(e) /// HOVER ON MAP ITEMS - UPDATES INFO BOXES AND OUTLINES COUNTRY
      {
          var layer = e.target;

          layer.setStyle({
                          weight: 3,
                          color: '#ffd32a'
                          });

          if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {  layer.bringToFront(); }
          displayInfo.update(layer.feature.properties);  // Updates custom legend on hover
      }


function reset(e) /// RESET LEGEND ON MOUSE OUT
    {
        geojson.resetStyle(e.target);
        displayInfo.update();   // Resets custom legend when user unhovers
    }


function getColor(d) /// COLOR GRADIENT THRESHOLDS FOR MAP AND LEGEND
    {
        if ( display_this == 0 ) // GDP COLOR
              {        
              return  d > 15000000 ? '#49006a' :
                      d > 10000000 ? '#7a0177' :
                      d > 5000000 ? '#ae017e' :
                      d > 2000000 ? '#dd3497' :
                      d > 1000000 ? '#f768a1' :
                      d > 500000 ? '#fa9fb5' :
                      d > 200000 ? '#fcc5c0' :
                      d > 150000 ? '#fde0dd' :
                      '#fff7f3'
               }
            
          if ( display_this== 1 )
                {
                return  d > 1000  ?   '#ff0040' :
                        d > 300   ? '#2a003d' :
                        d > 250   ? '#420060' :
                        d > 200   ? '#680188' :
                        d > 150   ? '#7a0177' :
                        d > 100   ? '#ae017e' :
                        d > 75    ? '#c4058d' :
                        d > 50    ? '#dd3497' :
                        d > 25    ? '#f768a1' :
                        d > 10    ? '#ff92be':
                        d > .1   ? '#ffb6d3' :
                        '#fff7f3'
                }

          if ( display_this == 3 || display_this == 4|| display_this == 5)
                {
                  return  d > 90 ? '#260038' :
                          d > 80 ? '#34004d' :
                          d > 70 ? '#49006a' :
                          d > 70 ? '#680188' :
                          d > 60 ? '#7a0177' :
                          d > 50 ? '#ae017e' :
                          d > 40 ? '#c4058d':
                          d > 20 ? '#dd3497':
                          d > 10 ? '#f768a1':
                          d > 0  ? '#ffaccd':
                          '#fff7f3'
                  }
        
          if ( display_this == 2 ) 
                  {
                  return  d > 160 ? '#260038' :
                          d > 140 ? '#49006a' :
                          d > 120 ? '#680188' :
                          d > 100 ? '#7a0177' :
                          d > 80 ? '#ae017e ' :
                          d > 60 ? '#c4058d' :
                          d > 40 ? '#dd3497' :
                          d > 20 ? '#ff80b3' :
                          d > 10 ? '#f768a1' :
                          d > 1? '#ff92be' :
                              '#fff7f3'
                  }

            if ( display_this== 7 ) 
                {
                return  d > 200  ?  '#df0505'  :
                        d > 180   ? '#e45b00'  :
                        d > 160   ? '#2a003d' :
                        d > 140   ? '#34004d' :
                        d > 120   ? '#680188' :
                        d > 100   ? '#7a0177' :
                        d > 80    ? '#ae017e' :
                        d > 60    ? '#c4058d' :
                        d > 40    ? '#dd3497' :
                        d > 20    ? '#f768a1' :
                        d > 10    ? '#ff92be':
                        d > 1   ? '#ffb6d3' :
                        '#fff7f3'
                }

          if (display_this== 6 || display_this== 8 || display_this == 9 ) // ECO TEST
                {
                return  d > 55?  '#260038' :
                        d > 50 ? '#34004d' :
                        d > 45 ? '#49006a' :
                        d > 40 ? '#680188' :
                        d > 35 ? '#7a0177' :
                        d > 30 ? '#ae017e' :
                        d > 25 ? '#c4058d':
                        d > 10 ? '#dd3497':
                        d > 5  ? '#f768a1':
                        d > 1  ? '#ffb6d3':
                          '#fff7f3'
                  }

          if ( display_this == 10  )
                  {
                  return      d > 25 ?  '#260038' :
                              d > 20 ? '#34004d' :
                              d > 15 ? '#49006a' :
                              d > 10 ? '#680188' :
                              d > 5 ? '#7a0177' :
                              d > 2 ? '#c4058d':
                              d > .1 ? '#f768a1':
                          '#fff7f3'
                  }

        mymap.update();
    }


function style(feature)  /// COLOR OF COUNTRYS BASED ON THIS VARIABLE FROM GEOJSON
    {   
            if ( display_this == 0 ) { map_color_data = feature.properties.gdp_md_est}; 
            if ( display_this == 1 ) { map_color_data = feature.properties.Population_Millions};
            if ( display_this == 2 ) { map_color_data = feature.properties.World_Rank};
            if ( display_this == 3 ) { map_color_data = feature.properties.Government_Integrity };
            if ( display_this == 4 ) { map_color_data = feature.properties.Judical_Effectiveness };
            if ( display_this == 5 ) { map_color_data = feature.properties.Fiscal_Health };
            if ( display_this == 6 ) { map_color_data = feature.properties.Inflation };
            if ( display_this == 7 ) { map_color_data = feature.properties.Public_Debtof_GDP };
            if ( display_this == 8 ) { map_color_data = feature.properties.Income_Tax_Rate };
            if ( display_this == 9 ) { map_color_data = feature.properties.Corporate_Tax_Rate };
            if ( display_this == 10) { map_color_data = feature.properties.Unemployment };
    
          return {
               
                  fillColor: getColor(map_color_data),
                  weight: 1,
                  opacity: 1,
                  fillOpacity: .72,
                  className: feature.properties.geounit,
                  };
    }  


function zoomToCountry(e) // zoom into country clicked on
    {
        mymap.fitBounds(e.target.getBounds());
    }


function highlight(e) // OUTLINING COUNTRY POLYGONS /// API CALL ON HOVER COUNTRY
    {
        info_box.clear();
        var layer = e.target;

        layer.setStyle({
                        weight: 3,
                        color: '#ffd32a',
                        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge)   {   layer.bringToFront();    }

        ////// JSON API REQUEST //////////////////////////////////////////////
        name_country =layer.feature.properties.name ; // OR // props.name;

        urlz = `/metadata/${name_country}`/// API ADDRESS USE COUNTRY NAME AS QUERY 
                    
              d3.json(urlz).then(function(response) //JSON RESPONSE
                    {
                        var info = response ;
                        // console.log("this is the data", response);
                        // info_box.update(info);
                        Object.entries(info).forEach(([key, value]) =>
                            {
                              // console.log("the Country>>>>>> info list, JSON key and value breakout  ", key, value);
                              info_box.update(key,value);//PASS JASON TO INFO_BOX.UPDATE FUNC
                            });   
                    });

        displayInfo.update(layer.feature.properties);

    }


function reset(e) /// CLEARING INFO BOX 
    {
        geojson.resetStyle(e.target);  
        // IF WE WANT INFO BOXES TO CLEAR OUT ON MOUSE OUT UNCOMMENT 2 LINES BELOW - 
        // IF LEAVE LINES COMMENTED OUT BELOW - INFO BOXES ONLY UPDATE ON NEW HOVER TARGET
        ///////////////////////////////////////////////////////////////////////////////////
        // displayInfo.update();
        //  info_box.clear();
    }


function onEachFeature(feature, layer) 
    {
        layer.on({
                    // dblclick: zoomToCountry,
                    mousedown: highlight, //highlight is a func when mouse click or touch screen touch
                    mouseover: highlight, //highlight is a func when hover with mouse
                    mouseout: reset,      // reset is a func
                    // click: zoomToCountry  // zoom is a funct 
                });
    }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 //           END  -    MAP    FUNCTIONS 
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////////
//   D3 AND Button AND HTML  control                      /////////////////
///////////////////////////////////////////////////////////////////////////

  var world_drop = d3.select(".world_scroll");
  
  world_drop.on("change", function() 
          { 
          query = '';
          if ( world_drop.property("value") == "GDP"  )               {query = 'GDP_Billions_PPP';        display_this =0 ;}
          if ( world_drop.property("value") == "Population"  )        {query = 'Population_Millions' ;    display_this =1 ;}
          if ( world_drop.property("value") == "World Rank"   )       {query = 'World_Rank'  ;            display_this =2 ;}
          if ( world_drop.property("value") == "Government Integrity" ){query= 'Government_Integrity' ;   display_this =3 ;}
          if ( world_drop.property("value") == "Judical Effectiveness"){query= 'Judical_Effectiveness';   display_this =4 ;}
          if ( world_drop.property("value") == "Fiscal Health" )      {query = 'Fiscal_Health' ;          display_this =5 ;}
          if ( world_drop.property("value") == "Inflation"  )         {query = 'Inflation';               display_this =6 ;}
          if ( world_drop.property("value") == "Public Debt of GDP" ) {query = 'Public_Debtof_GDP' ;      display_this =7 ;}
          if ( world_drop.property("value") == "Income Tax Rate"   )  {query = 'Income_Tax_Rate' ;        display_this =8 ;}
          if ( world_drop.property("value") == "Corporate Tax Rate")  {query =  'Corporate_Tax_Rate';     display_this =9 ;}
          if ( world_drop.property("value") == "Unemployment"   )     {query = 'Unemployment' ;           display_this =10 ;}
          legend.remove();
          displayInfo.remove();
          d3.selectAll(".info2").remove()
          geojson.remove();
          draw_map();  // draws new map 
          top_tens(query); // original location
          clickActions();
        });
    
////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////END OF DRAWMAP FUNCTION WRAP////////////////////////////////////////////////////////// 
}                                                                                     ////////////
/////////////END OF DRAWMAP FUNCTION WRAP////////////////////////////////////////////////////////

    //////////////////////////////////////////////////////////////////////////
    // OPTIONAL WAY OF EXTRACTING COUNTRY NAME
    //// IDENTIFYING MAP ELEMENT THAT HAS BEEN CLICKED 
    ///// EXTRACT COUNTRY NAME FROM CLASS NAME OF PATH ELEMENT

 function clickActions ()
    {
      var map_element = d3.selectAll("path");
      // console.log("this is button", map_element);
      // This function is triggered when the button is clicked
      function handleClick() 
            {
              // console.log("this item was clicked");
              // We can use d3 to see the object that dispatched the event
              // console.log("this is event target", d3.event.target);
            }
      
      // We can use the `on` function in d3 to attach an event to the handler function
      map_element.on("click", handleClick);
      
      // You can also define the click handler inline
      map_element.on("click", function() 
                {
                  element_clicked = d3.event.target;
                  class_element =  element_clicked.className;
                  var class_names = class_element.baseVal;
                  var class_names_text = class_names.toString();
                  var class_split = class_names_text.split(" ");
                  var grab_all_before_this = class_split.length;
                  var country_list = class_split.slice(0,(grab_all_before_this -1 ));
                  var country_name = country_list.join(" ");
                  // console.log("this should be country name " , country_name );
                });
    }


///////////////////////////////
//CALL CLICK FUNCTIONS 
 clickActions();

 ///////////////////////////////////////////////////////////////////////////////
 // INITIALIZER //////////////////////////////////////////////////////////////// 
///////////////////////////////////////////////////////////////////////////////



function alteruser() {
alert("Welcome !   ( This Page will Load Once you Click [OK]. )  _____________ <> TIPS FOR INTERACTING WITH THIS PAGE:  (1.) Select an Economic Category from  'Select Category' Button at top center of screen.\ \
  Once category button selected you can use arrow keys to quickly toggle through each category and render the map.    (2.) Hover or Click on a Country to receive more information. (3.) To 'Zoom In', Double Click anywhere in map or use the + and - signs in the upper left corner. (4.) Click and Hold and  Drag to Pan.\
 (5.) Enjoy Your Trip Around the Globe :-) Best Viewed on Laptop or Computer!");
}

 


function init() {
  draw_map();
  alteruser();
  }


 init(); 






///////////////////////////////////////////////////////////////////////////////////////////////////
////--- END OF ACTIVE CODE------------////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////



/////////////////////////////////////////////////////////////////////////////////////////////////
/// COPYRIGHT BRANDON STEINKE , PATRICK HENNESSY 2020
/////////////////////////////////////////////////////////////////////////////////////////////////



