# ui.R

#for top 50 degrees:
### >>> NAMES = []
### >>> d=g.degree()
### >>> for t in unique(sort(d)[::-1][:50]):  NAMES.extend(g.vs.select(_degree=t)['name'])
### >>> for n in NAMES[::-1]: print '\"%s (degree=%d)\" = \"%s\",'%(n,g.vs.find(name=n).degree(),n)
choices=list("comers@dnc.org (degree=476)" = "comers@dnc.org",
             "mirandal@dnc.org (degree=471)" = "mirandal@dnc.org",
             "kaplanj@dnc.org (degree=274)" = "kaplanj@dnc.org",
             "allenz@dnc.org (degree=144)" = "allenz@dnc.org",
             "parrishd@dnc.org (degree=125)" = "parrishd@dnc.org",
             "paustenbachm@dnc.org (degree=115)" = "paustenbachm@dnc.org",
             "palermor@dnc.org (degree=99)" = "palermor@dnc.org",
             "walkere@dnc.org (degree=97)" = "walkere@dnc.org",
             "manriquezp@dnc.org (degree=89)" = "manriquezp@dnc.org",
             "wrighta@dnc.org (degree=85)" = "wrighta@dnc.org",
             "stowee@dnc.org (degree=85)" = "stowee@dnc.org",
             "bonoskyg@dnc.org (degree=83)" = "bonoskyg@dnc.org",
             "garciaw@dnc.org (degree=83)" = "garciaw@dnc.org",
             "sorbies@dnc.org (degree=81)" = "sorbies@dnc.org",
             "pricej@dnc.org (degree=70)" = "pricej@dnc.org",
             "dillonl@dnc.org (degree=59)" = "dillonl@dnc.org",
             "daceya@dnc.org (degree=58)" = "daceya@dnc.org",
             "freundlichc@dnc.org (degree=57)" = "freundlichc@dnc.org",
             "weis@dnc.org (degree=55)" = "weis@dnc.org",
             "comm_d@dnc.org (degree=53)" = "comm_d@dnc.org",
             "coxc@dnc.org (degree=53)" = "coxc@dnc.org",
             "houghtonk@dnc.org (degree=52)" = "houghtonk@dnc.org",
             "alvillarr@dnc.org (degree=48)" = "alvillarr@dnc.org",
             "reynoldsl@dnc.org (degree=48)" = "reynoldsl@dnc.org",
             "helmstettert@dnc.org (degree=47)" = "helmstettert@dnc.org",
             "hoffmana@dnc.org (degree=46)" = "hoffmana@dnc.org",
             "taylorp@dnc.org (degree=46)" = "taylorp@dnc.org",
             "banfillr@dnc.org (degree=43)" = "banfillr@dnc.org",
             "bhatnagara@dnc.org (degree=42)" = "bhatnagara@dnc.org",
             "walsht@dnc.org (degree=42)" = "walsht@dnc.org",
             "olszewskic@dnc.org (degree=41)" = "olszewskic@dnc.org",
             "lykinst@dnc.org (degree=40)" = "lykinst@dnc.org",
             "comptonm@dnc.org (degree=40)" = "comptonm@dnc.org",
             "shapiroa@dnc.org (degree=39)" = "shapiroa@dnc.org",
             "zallen@tipahconsulting.com (degree=39)" = "zallen@tipahconsulting.com",
             "pought@dnc.org (degree=39)" = "pought@dnc.org",
             "moorec@dnc.org (degree=39)" = "moorec@dnc.org",
             "wilsone@dnc.org (degree=38)" = "wilsone@dnc.org",
             "rauscherr@dnc.org (degree=38)" = "rauscherr@dnc.org",
             "jeffersond@dnc.org (degree=38)" = "jeffersond@dnc.org",
             "crystala@dnc.org (degree=37)" = "crystala@dnc.org",
             "atobias123@gmail.com (degree=36)" = "atobias123@gmail.com",
             "davism@dnc.org (degree=34)" = "davism@dnc.org",
             "marshall@dnc.org (degree=34)" = "marshall@dnc.org",
             "patrick.w.hallahan@gmail.com (degree=34)" = "patrick.w.hallahan@gmail.com",
             "gottschalk-marconie@dnc.org (degree=33)" = "gottschalk-marconie@dnc.org",
             "brinsterj@dnc.org (degree=33)" = "brinsterj@dnc.org",
             "sargem@dnc.org (degree=32)" = "sargem@dnc.org",
             "wileyp@dnc.org (degree=32)" = "wileyp@dnc.org",
             "hrtsleeve@gmail.com (degree=32)" = "hrtsleeve@gmail.com",
             "robertske@dnc.org (degree=32)" = "robertske@dnc.org")

shinyUI(fluidPage(
  titlePanel("Interactive Graph Analysis of the Leaked DNC Emails"),
  
  sidebarLayout(

    sidebarPanel(
    tags$head( tags$script(src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML-full", type = 'text/javascript'),
    tags$script( "MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$']]}});", type='text/x-mathjax-config')),
    helpText("Customize the graphs by adjusting the parameters for Graphs A, B, and C. Black edges indicate one-way communication; red edges mean two-way communication."),

    #selectInput("leDegree", label = h3( sprintf("Graph A: Vertices with degree %s value",HTML("$\\leq$")) ),  
    selectInput("leDegree", label = h3( "Graph A: Vertices with degree <= value"),  
       choices = list("1" = 1,"2" = 2,"3" = 3,"4" = 4,"5" = 5,"6" = 6,"7" = 7,"8" = 8,"9" = 9,"10" = 10,"11" = 11,"12" = 12,"13" = 13,"14" = 14,"15" = 15,"16" = 16,"17" = 17,"18" = 18,"19" = 19,"20" = 20,"21" = 21,"22" = 22,"23" = 23,"24" = 24,"25" = 25,"26" = 26,"27" = 27,"28" = 28,"29" = 29,"30" = 30,"31" = 31,"32" = 32,"33" = 33,"34" = 34,"36" = 36,"37" = 37,"38" = 38,"39" = 39,"40" = 40,"41" = 41,"42" = 42,"43" = 43,"46" = 46,"47" = 47,"48" = 48,"52" = 52,"53" = 53,"55" = 55,"57" = 57,"58" = 58,"59" = 59,"70" = 70,"81" = 81,"83" = 83,"85" = 85,"89" = 89,"97" = 97,"99" = 99,"115" = 115,"125" = 125,"144" = 144,"274" = 274,"471" = 471,"476" = 476),
       selected = 1),
  
    #selectInput("geDegree", label = h3( sprintf("Graph B: Vertices with degree %s value", HTML("$\\geq$")) ),  
    selectInput("geDegree", label = h3( "Graph B: Vertices with degree >= value"),  
       choices = list("476" = 476,"471" = 471,"274" = 274,"144" = 144,"125" = 125,"115" = 115,"99" = 99,"97" = 97,"89" = 89,"85" = 85,"83" = 83,"81" = 81,"70" = 70,"59" = 59,"58" = 58,"57" = 57,"55" = 55,"53" = 53,"52" = 52,"48" = 48,"47" = 47,"46" = 46,"43" = 43,"42" = 42,"41" = 41,"40" = 40,"39" = 39,"38" = 38,"37" = 37,"36" = 36,"34" = 34,"33" = 33,"32" = 32,"31" = 31,"30" = 30,"29" = 29,"28" = 28,"27" = 27,"26" = 26,"25" = 25,"24" = 24,"23" = 23,"22" = 22,"21" = 21,"20" = 20,"19" = 19,"18" = 18,"17" = 17,"16" = 16,"15" = 15,"14" = 14,"13" = 13,"12" = 12,"11" = 11,"10" = 10,"9" = 9,"8" = 8,"7" = 7,"6" = 6,"5" = 5,"4" = 4,"3" = 3,"2" = 2,"1" = 1),
       selected = 471),

  checkboxGroupInput("nameGroup", label = h3("Graph C: Email network for the 50 vertices of highest degree"), 
     choices = choices, selected = "comers@dnc.org")
    ),
    
    mainPanel(plotOutput('lePlot'), plotOutput('gePlot'), plotOutput('namePlot'))
  )
))
