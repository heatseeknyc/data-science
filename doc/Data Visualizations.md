## Data Visualizations

## Applications and Libraries

- [Overview](#overview) 
- [Prototyping](#prototyping) 
    - [Applications](#applications) 
        - [Tableau](#tableau) 
        - [Spotfire](#spotfire) 
- [Publication](#publication)
    - [Libraries](#libraries)
        - [ggplot2](#ggplot)
        - [D3.js](#d3js)
- [Post-processing](#postprocessing)
    - [Design applications](#designapps) 
        - [Adobe Illustrator](#illustrator) 
        - [Inkscape](#inkscape) 
        - [Adobe Photoshop](#photoshop)
     
<a name="overview"/>   
##Overview

<a name="prototyping"/>
##Prototyping

A final, polished visualization typically undergoes multiple iterations and diverse drafts. The process of building a graphic that clearly answers a question or communicates an idea entails experimenting with different techniques in order to more clearly see which best suits the data and your message. Prototyping assists with the visual side of data exploration, and charting libraries that take care of basic chart formatting and data transformation are tremendously useful at this stage. 

Effective prototyping rests on efficiency. Rather than focus on the detailed cosmetic attributes of a graphic, such as axis width, bar spacing, point radius, and font size, now is the time to try out different visualization methods to see which one(s) might be a good fit.

<a name="applications"/>
###Applications

Though not always ideal, since they often come with a price tag and require some setup to install, desktop applications can come in handy if you do not want to write any code. 

<a name="tableau"/>
####Tableau

Tableau provides a relatively straightforward interface for data exploration and visualization drafts, and in this capacity has contributed to early vector versions of the polished charts that appear on the Heat Seek site. While the more robust Desktop version is not free, Tableau Public does facilitate the exploration and sharing of out-of-the-box visualizations, and can in turn serve as a resource for quickly experimenting with (and hackily exporting the structure of) a basic selection of charts without writing any code. 

<a name="spotfire"/>
####Spotfire

<a name="publication"/>
##Publication

Creating a publishable visualization requires tools that provide deeper customizability than a proprietary charting library. Whether this stage is the final step of your process, or merely the precursor to additional visual customization, the following tools give you control over data transformation, variable definition, method, style, and format. 

<a name="libraries"/>
###Libraries

<a name="ggplot2"/>
####ggplot2

[ggplot2](http://ggplot2.org/) is a powerful, streamlined system for plotting nice-looking graphics in R. 

It also supports export to a variety of different graphics formats. 

<a name="d3js"/>
####D3.js

[D3.js](http://d3js.org/), Data-Driven Documents, is a robust JavaScript library best used for creating web-based interactive visualizations. D3 supports your basic charting needs ([bar charts](http://bost.ocks.org/mike/bar/), [line charts](http://bl.ocks.org/mbostock/3883245), [pie charts](http://bl.ocks.org/mbostock/3887235) -- though never to be used, of course), a huge range of more inventive visualization approaches ([maps](http://bost.ocks.org/mike/map/), [network diagrams](http://bl.ocks.org/jose187/4733747), [treemaps](http://bl.ocks.org/mbostock/4063582)), and an unliited range of whatever graphical methods you can come up with using the vector-based buildings blocks of the SVG format, the raster-based pixels of a canvas element, and/or the basic elements of HTML. Graphics can be generated using an external data file, an API call, or a locally-defined data source. 

D3 does have a bit of a learning curve, but nothing that a facility with JavaScript and a bunch of iterations cannot help you master. Vector-based graphics can be [crowbarred](http://nytimes.github.io/svg-crowbar/) to your desktop from the browser, if necessary, though this workflow is only recommended for super complex graphics that you cannot feasibly build using a different tool. 

<a name="postprocessing"/>
##Post-processing

Most Heat Seek visualizations undergo a final round of visual editing before going live. Incorporating a title and subtle branding into a static visualization presents your prospective audience with a level of cohesion along with a succinct description of what they are looking at. In addition, adding a data source provides a guide to those who may want to double-check, confirm, or recreate your work. 

After exporting a graphic from the previous phase, the following tools will help you add polish.

<a name="designapps"/>
###Design applications

<a name="illustrator"/>
####Adobe Illustrator

Adobe Illustrator is an excellent resource for customizing vector graphics. In particular, Illustrator makes it simple to keep style, palette, and overall branding consistent from chart to chart. 

When working with Illustrator, it helps to create a "template" file to assist with the creation of every new graphic. This file should include the following:

*1. Guides, to lay out the basic elements and dimensions of the graphic as a standalone image (margins, padding, title position, subtitle position, data source position).

*2. Repeatable layout elements (logo, title font, subtitle font) -- use placeholder text as needed.

*3. Brand palette (try drawing a row of colored squares to sit outside of the artboard, for easy reference -- alternately, create a set of custom swatches).

The template file can be customized as needed. For final export, Photoshop tends to be the best route for saving high-res, web-ready graphics, but Illustrator itself supports a range of different formats. 

<a name="inkscape"/>
####Inkscape

For those not under the reign of Adobe, Inkscape is a free and open-source vector graphics editor. 

<a name="photoshop"/>
####Adobe Photoshop

Adobe Photoshop enables you to easily publish a high-res, web-ready graphic, especially if Adobe Illustrator is a part of your workflow. Import your vector-based visualization as a Smart Object, adjust the dimensions and resolution, and export a JPEG at 3000px width for sharpest results. 