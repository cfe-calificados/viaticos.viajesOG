# -*- coding: utf-8 -*-

headers = u"""\\documentclass[10pt,letterpaper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{charter}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\usepackage{longtable}
\\usepackage{color}
\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}
\\usepackage[left=1.50cm, right=1.50cm, top=1.50cm, bottom=1.50cm]{geometry}
\\usepackage{fancyhdr, graphicx}
\\usepackage{multicol}
\\usepackage{tabularx}
\\usepackage{hyperref}
\\usepackage[table]{xcolor}
\\definecolor{califiverde}{RGB}{0,116,69}
\\definecolor{califigris}{RGB}{161, 173, 179}
\\definecolor{califigrisecito}{RGB}{203,203,203}

\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[C]{
  %\\begin{tabular}[b]{l}
    \\textbf{\\large Comprobación de gastos}\\\\
  %\\end{tabular}
}
\\fancyhead[OL]{
  \\begin{tabular}[b]{l}
    \\scriptsize{\\textbf{R.F.C.} SCA1701255W0}\\\\
    \\scriptsize{Del Risco 241, Col. Jardines del Pedregal,} \\\\
    \\scriptsize{Del. Álvaro Obregón, C.P. 01900} \\\\
    \\scriptsize{México, Ciudad de México}
  \\end{tabular}
}
\\fancyhead[ER]{\\thepage}
\\fancyhead[OR]{
\\includegraphics[height=3\\baselineskip]{logo_cfe_califi}
}

\\addtolength{\\headheight}{2\\baselineskip}
\\addtolength{\\headheight}{0.61pt}


\\title{Título}
\\author{Autor}
\\date{Fecha}
"""


footer = u"""
\\begin{multicols}{2}
  \\begin{flushleft}
    \\framebox(230,50){}\\\\
    \\noindent\\fbox{
      \\parbox{218pt}{        
        \\centering{FIRMA DEL COORDINADOR}        
      }
    }
  \\end{flushleft}
  \\vfill\\null
  \\columnbreak
  \\begin{flushright}
    \\framebox(230,50){}\\\\ 
    \\noindent\\fbox{
      \\parbox{218pt}{        
        \\centering{FIRMA DEL EMPLEADO}
      }
    }
  \\end{flushright}
  
\\end{multicols}


\\par\\noindent\\rule{\\textwidth}{0.4pt}
\subsubsection*{PARA USO DE FINANZAS}

\\begin{multicols}{2}

  \\begin{Form}
    \\subsubsection*{Datos para efectuar el pago}
    \\begin{tabbing}
      xxxxxxxxxx: \\= \\kill  % This is needed for the right tab width
      Cuenta No.:           \\> \\TextField[bordercolor=,name=cuenta,width=3cm,charsize=10pt,format={this.getField('cuenta').textFont='SegoeMarker';}]
      {\\mbox{}} \\vspace{1cm}
      Sucursal No.: \\TextField[bordercolor=,name=sucursal,width=3cm,charsize=10pt]
      {\\mbox{}} \\\\
    \\end{tabbing}
    \\begin{tabbing}
      xxxxxx: \\= \\kill  % This is needed for the right tab width
      Banco.:           \\> \\TextField[bordercolor=,name=banco,width=4cm,charsize=10pt]
      {\\mbox{}} \\vspace{1cm}
      Plaza No.: \\TextField[bordercolor=,name=plaza,width=3.2cm,charsize=10pt]
      {\\mbox{}} \\\\
    \\end{tabbing}
    Otros: \\TextField[bordercolor=gray,name=otros,charsize=0pt,multiline=true, width=9.3cm, height=3em]
    {\\mbox{}} \\\\ \\\\
    \\hfill ~\\\\
  \\end{Form}

  
  \\vfill\\null
  \\columnbreak


  %\\hfill espacio horizontal
  \\begin{flushright}
    \\framebox(220,90){}\\\\
  \\end{flushright}
  
\\end{multicols}

\\end{document}
"""
