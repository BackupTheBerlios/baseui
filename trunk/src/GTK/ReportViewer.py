#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#===============================================================================
# ReportViewer module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import math
import pygtk
pygtk.require('2.0')
import gtk, pango

from Draw.Primitives import *



class PrintPreview:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Print Example")
        window.connect("destroy", lambda w: gtk.main_quit())

        vbox = gtk.VBox()
        window.add(vbox)
        
        toolbar = gtk.Toolbar()
        vbox.pack_start(toolbar, expand=False, fill=True)
        
        button_print = gtk.Button('Druck')
        button_print.connect("clicked", self.on_button_print_clicked)
        toolbar.add(button_print)
        
        button_backward = gtk.Button('<-')
        toolbar.add(button_backward)
        button_forward = gtk.Button('->')
        toolbar.add(button_forward)
        
        button_cancel = gtk.Button('Abbruch')
        button_cancel.connect("clicked", lambda w: gtk.main_quit())
        toolbar.add(button_cancel)
        
        self.area = gtk.DrawingArea()
        self.area.set_size_request(400, 300)
        self.area.connect("expose-event", self.on_drawingarea_expose)
        vbox.add(self.area)
        
        window.show_all()
        self.draw_page()
        

    # This both methods are doing the initial ---------------------------------
    def on_drawingarea_expose(self, area=None, event=None):
        self.draw_page()
        return True


    def on_button_print_clicked(self, widget=None, data=None):
        print_operation = gtk.PrintOperation()
        print_operation.set_n_pages(2)
        print_operation.set_use_full_page(True)
        #print_operation.set_unit(10)
        
        print_operation.connect("draw_page", self.print_page)        
        response = print_operation.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)
        print response
        
        
    # This draws the text on the window ---------------------------------------
    def draw_page(self):
        context = self.area
        sheet = Sheet(context)
        self.page_layout(sheet)
        return
        

    # This draws the text on the virtual print window -------------------------
    def print_page(self, operation=None, context=None, page_nr=None):
        print context, page_nr
        
        sheet = Sheet(context)
        
        if page_nr == 0:
            self.page_layout(sheet)
        else:
            self.page_layout2(sheet)
        return

    
    # Here is the whole print magic! ------------------------------------------
    def page_layout(self, sheet):
        text = Text(sheet)       
        line = Line(sheet)
        circle = Circle(sheet)
        
        text.set_font('Courier New 14')
        text.draw('123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789', 33, 133)
        
        line.draw([[100, 100], [200, 200], [100, 200], [200, 100], [100, 100], [100, 200], [150, 250], [200, 200], [200, 100]])
        line.draw([[120, 120], [510, 120]])
        line.draw([[0,0], [210, (210 * int(round(math.sqrt(2))))]])
        
        line.draw([[0, 0], [240, 240]])
        circle.draw(200, 200, 20)
        
        text.set_font('Arial 20')
        text.draw('''\
123456789-123456789
123456789-Häggismen chila
123456789-123456789
123456789-123456789''', x_pos=10, y_pos=20, width=600000, height=2000)

    def page_layout2(self, sheet):
        text = Text(sheet)       
        
        text.set_font('Arial 11')
        text.draw('''\
Lorem ipsum ad quo novum pericula, eos ut mutat mucius urbanitas. In ius saepe causae tritani, debet solet dolore ius no. Stet brute movet est an, no eam quot unum. Ne nec iudico latine. Diam sale mutat cum id, ei minim novum vituperata mea, te atqui augue mediocritatem per. Pri in saperet nominati ocurreret, delectus reprimique cum ne.

Te nostro admodum nam, nec wisi dolor docendi ea. Delenit labores adolescens ei sea, ea liber voluptua interesset sea. No eum docendi propriae sapientem, ex prima conclusionemque ius. Ut tale dicam consul vim, sit in essent gloriatur definitiones, novum quodsi animal pri no. Latine integre oportere vis ne, postea delectus abhorreant at est.

Et qui saepe appareat iudicabit, vel no verear accumsan disputationi. Aeterno debitis accommodare ad ius, ut pro hinc impedit. Pri posse graece no. Movet quando sit an, vix no aeque impetus insolens, pri minimum intellegat ea. His mollis aliquando cu, eripuit accumsan conclusionemque cum ut. Sit te takimata nominati hendrerit. Vel agam putant nostrud ad, unum vivendum periculis ne his.

Eu his integre civibus maiestatis, per no postulant maiestatis voluptatibus, vide adolescens has te. No has nihil altera audiam, ipsum facer utinam vim cu, dico accumsan mei at. At sit dicat facer constituto, in habeo autem voluptaria cum. Ex nec labitur noluisse sapientem, movet tantas scriptorem ad has. Putant neglegentur has id, lorem verear mediocrem pro ut. Eu docendi facilisi percipitur est, ex quot appareat maiestatis nec, cum ut nonumy fastidii argumentum. Reprimique efficiendi referrentur nam ut, ne nibh semper scripserit sit, cu paulo facilisi usu.

Quod cibo interesset te sit, omittam aliquando instructior te duo, ne est velit nostrud. Vel veritus honestatis theophrastus ut, tempor quaestio ocurreret ut quo, ne vero quando everti mei. Fugit audiam ancillae sit ex, ea omnis legere persequeris mei, cu qui unum inani epicuri. Eos nihil verear partiendo an, quo puto copiosae singulis ex, sale putant ex mei. Nulla nonummy eloquentiam ut vis, in cum ferri prima facilisis.

At usu vidit novum iudico. Assum dolore deseruisse eum cu, duo vidisse expetenda neglegentur cu. Facete cetero veritus id duo, sed eius graeco viderer at, debet animal oblique has ne. Pri cu atqui dicant, dolorum utroque mea et.

Ne laudem semper patrioque pro. In nam volumus antiopam intellegat, putent inermis menandri mei ne. Ea bonorum facilis legendos nam, tale saepe propriae vix ea, in per rebum labores. Vim veritus consequat ut, sea ei mentitum platonem, malis exerci gloriatur an eos. Pro ex audiam propriae contentiones.

Agam affert iudicabit te his, no has persius recusabo definiebas, te vix wisi atqui civibus. At est elitr blandit vivendum, tota brute ridens pri in. Sadipscing concludaturque vim ut. Quo ad accusam assueverit ullamcorper, ut elit zzril oblique vim. Te iudico iisque eos, no has quaeque maiorum partiendo, natum dicit nec te. Cum enim oratio convenire id, in omnes legere molestiae eos, et velit docendi honestatis vim. Vis ut insolens appellantur ullamcorper, id simul admodum adipiscing has, kasd gloriatur constituto ea mei.

Duo error saperet electram ea, decore semper aliquid eum an. Facer persius torquatos vis id, id omnis feugiat indoctum vix, aeterno laoreet omnesque quo in. Primis apeirian similique eum an, eu iudico corpora delectus est, an tota omnium nostrum sed. Exerci ridens pericula in est, assentior contentiones disputationi mei et. Duo ex dicunt luptatum senserit, nibh quas argumentum duo te, et nam minim voluptatum. Pro mutat etiam nobis te, ad ius reque augue vulputate, id qui populo graeci voluptatibus.

Illum eripuit sed ei, id eos iuvaret habemus suscipiantur, mei facete audiam cu. Id vide dolor malorum qui, vix id impetus prompta inimicus, te vis debet numquam. Te eam euismod urbanitas reprimique. An aeque ludus tamquam usu. Est persius deserunt periculis in, mea ei decore inermis inimicus. Meis eleifend nec et, nec ea sale numquam phaedrum.''', x_pos=10, y_pos=20, width=600000, height=2000) #, justify=True)



# Start the GTK mainloop ------------------------------------------------------
def main():
    gtk.main()
    return 0

    
if __name__ == "__main__":
    PrintPreview()
    main()
