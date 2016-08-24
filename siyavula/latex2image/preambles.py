def PsPicture_preamble():
    pstricks_tex = r'''
        \documentclass[preview, border=1bp]{standalone}
        \renewcommand{\familydefault}{\sfdefault}
        \usepackage{fp}
        \usepackage{float} % for figures to appear where you want them
        \usepackage{setspace}
        \usepackage{xcolor}
        \usepackage{graphicx}
        \usepackage{changebar}

        %\usepackage{auto-pst-pdf}
        \usepackage{pst-all}
        \usepackage{pst-eucl}
        \usepackage{pst-poly}
        \usepackage{pst-math}
        \usepackage{pstricks-add}

        \usepackage{pst-spectra}
        \usepackage{pst-slpe}
        \usepackage{pst-3dplot}
        \usepackage{pst-diffraction}
        \usepackage{pst-lens}
        \usepackage{pst-optic}
        \usepackage{pst-solides3d}
        \usepackage{pst-node}
        \usepackage{pst-labo}
        \usepackage{pst-electricfield}
        \usepackage{pst-magneticfield}
        \usepackage{pst-circ}



        %% ************* NB ************
        %% The order in which pstricks packages are loaded
        %% matters - so I copied the order from pst-all.sty
        %% and then added the two additional packages at the end.
        %% ************* End NB ************

        %% ************* Packages ************
        \usepackage{pst-circ}
        \usepackage{pstricks-add}         %Jo
        \usepackage{pst-labo}         %Jo
        \usepackage{subfigure}
        \usepackage{multirow}
        \usepackage{amsmath}
        \usepackage{tabularx}
        \usepackage{lscape}
        \usepackage{fancyhdr}
        \usepackage{wasysym}
        \usepackage{url}
        \usepackage{amsmath, amsthm, amsfonts, amssymb}
        \usepackage{eurosym}
        \usepackage{array}
        \usepackage{enumitem}
        \sffamily

        %\usepackage{mdframed}

        \newcommand{\ohm}{\ensuremath{\Omega}}
        \newcommand{\eohm}{\,\Omega}
        \newcommand{\eN}{\,\rm{N}}                %m in text
        \newcommand{\emm}{\,\rm{m}}                %m in text
        \newcommand{\ep}{\,\ekg \cdot \mbox{\ms}}                %m/s in text
        \newcommand{\es}{\,\text{s}}                %s in equation
        \newcommand{\ekg}{\,\text{kg}}                %kg in equation
        \newcommand{\eJ}{\,\text{J}}                %J in equation
        \newcommand{\eA}{\,\text{A}}                %A in equation
        \newcommand{\eV}{\,\text{V}}                %J in equation
        \newcommand{\eW}{\,\text{W}}                %W in equation
        \newcommand{\ms}{$\text{m}\cdot\text{s}^{-1}$}                %m/s in text
        \newcommand{\mss}{$\text{m}\cdot\text{s}^{-2}$}                %m/s in text
        \newcommand{\ems}{\,\text{m} \cdot \text{s}^{-1}}            %m/s in equation
        \newcommand{\emss}{\,\text{m} \cdot \text{s}^{-2}}            %m/s in equation
        \newcommand{\px}{$x$}                % position x, in text
        \newcommand{\py}{$y$}                % position y, in text
        \newcommand{\edx}{\Delta x}        % displacement dx, in text
        \newcommand{\dx}{$\edx$}            % displacement dx, in text
        \newcommand{\edy}{\Delta y}            % displacement dy, in text
        \newcommand{\dy}{$\edy$}            % displacement dy, in text
        \newcommand{\edt}{\Delta t}            % delta time dt, in text
        \newcommand{\dt}{$\edt$}            % delta time dt, in text
        \newcommand{\vel}{$v$}                % velocity
        \newcommand{\kph}{km$\cdot$hr$^{-1}$}    %km/h in text
        \newcommand{\momen}{\vec{p}}            %momentum
        \newcommand{\kener}{KE}                            %kinetic energy
        \newcommand{\poten}{PE}                            %kinetic energy
        \newcommand{\degree}{^{\circ}}
        \newcommand{\ie}{{\em i.e.~}}
        \newcommand{\eg}{{\em e.g.~}}
        \newcommand{\cf}{{\em c.f.~}}
        \newcommand{\resp}{{\em resp.~}}
        \newcommand{\etc}{{\em etc.~}}
        \newcommand{\nb}{{\em n.b.~}}
        \newcommand{\eJSI}{{\,\text{kg} \cdot \text{m}^{2} \cdot \text{s}^{-2}}}
        \def\deg{$^{\circ}$}
        \newcommand{\ud}{\mathrm{d}}

        % Arrow for objects and images
        %\newpsobject{oi}{psline}{arrowsize=6pt, arrowlength=1.5, arrowinset=0, linewidth=2pt}
        %\psset{lensHeight=3,lensColor=lightgray}
        %\newpsobject{PrincipalAxis}{psline}{linewidth=0.5pt,linecolor=gray}

        %\include{DefinitionsV0-5}

        \makeatletter
        \newcommand*{\getlengthinpt}[1]{\strip@pt#1}
        \makeatother

        \pagestyle{empty}
        \usepackage{fontspec}
        \begin{document}
        \begin{pspicture}__CODE__
        \end{pspicture}
        \end{document}
        '''
    return pstricks_tex


def tikz_preamble():
    tikz_tex = r'''
        \documentclass[preview, border=1bp]{standalone}
        \renewcommand{\familydefault}{\sfdefault}

        \usepackage{tikz, ifthen}
        \usetikzlibrary{arrows,shapes,backgrounds,patterns,decorations.pathreplacing,decorations.pathmorphing,decorations.markings,shadows,shapes.misc,calc,positioning,intersections}

        \usepackage{setspace}
        \usepackage{graphicx}
        \usepackage{changebar}
        \usepackage{xcolor}

        \usepackage{pgfplots}
        \usepackage{pgfplotstable}
        \usepackage{tkz-euclide}
        \usetkzobj{all}

        %set diagram styles
        \tikzset{
        dot/.style={circle,inner sep=1pt,fill,},
        every node/.append style={font={\small}},
        -||-/.style={decoration={
        markings,
        mark=at position #1 with {\draw (-1pt,-3pt) -- (-1pt,3pt); \draw ( 1pt,-3pt) -- ( 1pt,3pt);}},postaction={decorate}},
        }

        \pgfplotsset{
        axis lines =center,
        xlabel = $x$,
        ylabel =$y$,
        clip=false,
        cycle list={black\\},
        ticklabel style={scale=1},
        xlabel style={at=(current axis.right of origin), anchor=west},
        ylabel style={at=(current axis.above origin), anchor=south},
        disabledatascaling,
        }
        %% ************* Packages ************
        \usepackage{amsmath}
        \usepackage{wasysym}
        \usepackage{amsmath, amsthm, amsfonts, amssymb}
        \usepackage{eurosym}
        \sffamily

        \pagestyle{empty}
        \usepackage{fontspec}
        \begin{document}
        \begin{tikzpicture}__CODE__
        \end{tikzpicture}
        \end{document}
        '''
    return tikz_tex


def equation_preamble():
    # Remove all the html define colour references when EdTech has removed all
    # hex codes for colours from their code
    equation_tex = u'''\\documentclass[preview, border=1bp]{standalone}
        \\usepackage{amsmath}
        \\usepackage{amsfonts}
        \\usepackage{amssymb}
        \\usepackage{keystroke}
        \\usepackage{cancel}
        \\usepackage[usenames, dvipsnames, svgnames]{xcolor}
        \\usepackage{eurosym}
        \\newcommand{\dottimes}{\ensuremath{\;.\;}}
        \\usepackage[utf8]{inputenc}
        \\newcommand{\lt}{<}
        \\newcommand{\gt}{>}
        \\begin{document}
        \definecolor{\#800380}{HTML}{800380}
        \definecolor{\#0303ff}{HTML}{0303FF}
        \definecolor{\#ff7f00}{HTML}{FF7F00}
        \definecolor{\#008000}{HTML}{008000}
        \definecolor{\#121dc2}{HTML}{121DC2}
        \definecolor{\#0000FF}{HTML}{0000FF}
        \definecolor{\#990066}{HTML}{990066}
        \definecolor{\#ff0000}{HTML}{FF0000}
        \definecolor{\#ff9900}{HTML}{FF9900}
        \definecolor{\#ffcc00}{HTML}{FFCC00}
        \definecolor{\#009900}{HTML}{009900}
        \definecolor{\#ff00ff}{HTML}{FF00FF}
        \definecolor{darkblue}{HTML}{00008B}
        \definecolor{maroon}{HTML}{800000}
        \definecolor{darkred}{HTML}{8B0000}
        \definecolor{crimson}{HTML}{DC143C}
        \definecolor{purple}{rgb}{0.63 0.13 0.94}
        \definecolor{darkgreen}{rgb}{0 0.39 0}
        \definecolor{orange}{rgb}{1 0.35 0}
        __CODE__
        \\end{document}'''.encode('utf-8')
    return equation_tex
